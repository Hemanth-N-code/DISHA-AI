# backend/app/services/llm_service.py
import os
import logging
from typing import Optional, List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """
    Provider-agnostic LLM interface supporting OpenAI, Gemini, Anthropic,
    and a reliable offline deterministic synthesis fallback.
    """
    def __init__(self):
        self._cached_gemini_url = None
        self._sync_keys()

    def _sync_keys(self):
        self.provider = (os.getenv("LLM_PROVIDER") or settings.LLM_PROVIDER or "gemini").lower()
        self.openai_key = (os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY or "").strip()
        self.gemini_key = (os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY or "").strip()
        self.anthropic_key = (os.getenv("ANTHROPIC_API_KEY") or settings.ANTHROPIC_API_KEY or "").strip()
        
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
        max_tokens: int = 500,
        query_only: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generates grounded response using active provider, with fallback.
        """
        self._sync_keys()

        # 1. Try Gemini if key is set or provider is gemini
        gemini_key = self.gemini_key
        if gemini_key:
            try:
                import httpx
                
                # Multi-turn contents structure
                contents = []
                if conversation_history:
                    for turn in conversation_history[-6:]:
                        if not isinstance(turn, dict):
                            continue
                        role = turn.get("role") or turn.get("sender") or "user"
                        gemini_role = "model" if role == "assistant" else "user"
                        text = turn.get("content") or turn.get("text") or ""
                        if text and text.strip():
                            if contents and contents[-1]["role"] == gemini_role:
                                contents[-1]["parts"][0]["text"] += f"\n\n{text.strip()}"
                            else:
                                contents.append({"role": gemini_role, "parts": [{"text": text.strip()}]})

                # Append current user prompt
                current_text = prompt
                if contents and contents[-1]["role"] == "user":
                    contents[-1]["parts"][0]["text"] += f"\n\n{current_text}"
                else:
                    contents.append({"role": "user", "parts": [{"text": current_text}]})

                # Gemini API strictly requires that contents must start with a 'user' turn
                while contents and contents[0]["role"] != "user":
                    contents.pop(0)

                # Ensure at least one valid user message exists
                if not contents:
                    contents.append({"role": "user", "parts": [{"text": current_text}]})

                payload: Dict[str, Any] = {
                    "contents": contents,
                    "generationConfig": {
                        "maxOutputTokens": max_tokens,
                        "temperature": 0.4
                    }
                }

                full_system = system_prompt or "You are DISHA AI Career Counselor."
                if context:
                    full_system += f"\n\nAuthoritative Career Taxonomy & Grounding Knowledge:\n{context[:2000]}"

                payload["system_instruction"] = {
                    "parts": [{"text": full_system}]
                }

                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": gemini_key
                }

                # Primary verified working model: gemini-flash-lite-latest (fastest & highest availability)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={gemini_key}"
                try:
                    resp = httpx.post(url, headers=headers, json=payload, timeout=10.0)
                    if resp.status_code == 200:
                        data = resp.json()
                        candidates = data.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            parts = candidates[0]["content"].get("parts", [])
                            full_text = "".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()
                            if full_text:
                                logger.info("Successfully received live completion from Google gemini-flash-lite-latest.")
                                return full_text
                    else:
                        logger.warning(f"Gemini API returned HTTP {resp.status_code}: {resp.text[:120]}. Falling back to internal engine.")
                except httpx.TimeoutException:
                    logger.warning("Gemini API request timed out after 10s. Using instant grounded fallback.")
                except Exception as model_err:
                    logger.warning(f"Gemini API invocation error: {model_err}. Using instant grounded fallback.")
            except Exception as e:
                logger.warning(f"Gemini API top-level error: {e}. Using instant grounded fallback.")

        # 2. Try OpenAI if key is set
        if (self.provider == "openai" or self.openai_key) and self.openai_key:
            try:
                import httpx
                headers = {
                    "Authorization": f"Bearer {self.openai_key}",
                    "Content-Type": "application/json"
                }
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                if conversation_history:
                    for turn in conversation_history[-6:]:
                        role = turn.get("role") or turn.get("sender") or "user"
                        msg_role = "assistant" if role == "assistant" else "user"
                        text = turn.get("content") or turn.get("text") or ""
                        if text:
                            messages.append({"role": msg_role, "content": text})

                full_user_content = f"Context:\n{context}\n\nPrompt:\n{prompt}" if context else prompt
                messages.append({"role": "user", "content": full_user_content})
                
                resp = httpx.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "gpt-4o-mini",
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": 0.4
                    },
                    timeout=15.0
                )
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logger.warning(f"OpenAI completion failed: {e}. Falling back to internal engine.")

        # 3. Deterministic Grounded Offline Fallback Synthesizer
        return self._generate_offline_grounded_response(
            prompt=prompt,
            system_prompt=system_prompt,
            context=context,
            query_only=query_only,
            conversation_history=conversation_history
        )

    def _generate_offline_grounded_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
        query_only: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Deterministic, professional, evidence-grounded response generator.
        Evaluates the student's actual current query to avoid false positives
        from long-term student background context.
        """
        eval_text = (query_only or prompt).lower()

        # 1. Conversational questions: "what was my previous question", "what did I ask"
        if any(w in eval_text for w in [
            "previous question", "last question", "what did i ask", 
            "what did i just ask", "previous message", "my last question", 
            "what was my previous query", "what was my last question"
        ]):
            if conversation_history:
                past_user_msgs = [
                    (m.get("content") or m.get("text") or "")
                    for m in conversation_history
                    if isinstance(m, dict) and (m.get("role") == "user" or m.get("sender") == "user") and (m.get("content") or m.get("text"))
                ]
                if past_user_msgs and past_user_msgs[-1].strip().lower() == eval_text.strip():
                    past_user_msgs.pop()
                if past_user_msgs:
                    last_q = past_user_msgs[-1]
                    return (
                        f"Your previous question was:\n\n"
                        f"> \"**{last_q}**\"\n\n"
                        f"Would you like to delve deeper into that topic, examine related career paths, or test alternative scenarios in the What-If Explorer?"
                    )
            return (
                "You haven't asked any previous questions in this session yet. What career path, branch, or college question would you like to explore?"
            )

        # 2. KCET / CET entrance exam & college rank guidance
        if any(w in eval_text for w in ["kcet", "cet", "rank", "counselling", "cutoff", "allotment", "rvce", "bmsce", "msrit", "pes"]):
            return (
                "For Karnataka KCET / KEA Option Entry, DISHA provides an active **CET-Support Module** covering 58 premier and regional colleges across Karnataka:\n\n"
                "1. **Option Strategy Rule**: In KEA counselling, there is zero penalty for entering ambitious colleges first. If your rank doesn't qualify for option #1, KEA automatically checks #2, then #3, etc. Therefore, always order options: **Tier 1 Dream Colleges** (e.g. RVCE, BMSCE, MSRIT) → **Tier 2 Realistic Matches** (e.g. BIT, DSCE, RNSIT, CMRIT, NIE, SJCE) → **Tier 3 Safety Cushions** (e.g. Global Academy, Acharya, Cambridge, Oxford).\n\n"
                "2. **Check Your Rank**: Go to **CET-Support → Explorer** (`/cet/explore`) and enter your exact rank and category (GM, 2A, 3B, SC, ST). You will see instant classifications (Strong Match, Possible Match, Safer Cushion) with verified multi-year cutoffs (2023–2025) and median placement packages.\n\n"
                "3. **Build Your List**: Use the **Option Entry Builder** (`/cet/option-list`) to arrange your choices with Move Up/Down controls, then print or copy your final preference sheet."
            )

        # 3. Class 12 / PUC confused student guidance
        if any(w in eval_text for w in ["confused", "don't know what to do", "12th", "puc", "after 12th", "guide me", "how do i decide"]):
            return (
                "It is completely natural to feel overwhelmed after 12th/PUC—most students are pressured to follow the crowd without knowing what daily work actually looks like.\n\n"
                "Here is the recommended 4-step exploration path in DISHA:\n"
                "1. **Start with Discovery** (`/discover`): Browse 118 real careers across Tech, Design, Science, Business, and Sustainability to see what daily work and real skills look like.\n"
                "2. **Simulate Scenarios** (`/what-if`): Test 'What if I want less programming?' or 'What if I want high people interaction?' and watch how compatible pathways re-align dynamically.\n"
                "3. **Compare Options** (`/compare`): Put 2 or 3 careers side-by-side to contrast work style, future AI automation impact, and compensation.\n"
                "4. **CET Option Entry** (`/cet`): If you wrote KCET, calibrate your rank with our 58 Karnataka colleges to find realistic, high-quality college options."
            )

        # 4. Branch choice vs career fit
        if any(w in eval_text for w in ["which branch", "branch selection", "branch vs career", "cse or ece", "aiml or cse", "between branches", "best branch"]):
            return (
                "When choosing an engineering branch, connect it to your target future career direction rather than just cutoff peer pressure:\n\n"
                "• **Software & Web/Cloud Architecture**: Computer Science (CS) or Information Science (IS).\n"
                "• **Data Science & Machine Learning**: CS, IS, or specialized Artificial Intelligence & ML (AI).\n"
                "• **Semiconductors, VLSI & Embedded Systems**: Electronics & Communication (EC) or Electrical & Electronics (EE).\n"
                "• **Robotics & Autonomous Systems**: EC, CS, or Mechanical (ME) with programming electives.\n\n"
                "Tip: You can use DISHA's **Path Graph** (`/graph`) or **CET-Support Bridge** to inspect which 118 modern career profiles map to each undergraduate branch."
            )

        # 5. AI impact / automation / daily tasks
        if any(w in eval_text for w in ["ai affect", "ai change", "automation", "future of jobs", "ai impact", "daily tasks of this job", "daily tasks"]):
            return (
                "According to the World Economic Forum (WEF) Future of Jobs Report and O*NET 2024 analysis, AI transforms daily work tasks rather than eliminating entire professions outright:\n\n"
                "1. **Task Automation**: Routine syntactic coding, basic unit tests, and templated documentation are heavily accelerated by AI assistants.\n"
                "2. **Human Resilience**: High-judgment responsibilities—such as user research, ethical trade-off analysis, system architecture, and stakeholder communication—remain distinctly human-driven.\n"
                "3. **Comparative Impact**: While Software Developers shift towards higher-level system orchestration, UX Designers and Product Strategists increasingly focus on AI governance and empathic user journeys.\n\n"
                "In DISHA's **Compare Careers** tab (`/compare`), you can see the empirical 'AI Automation Exposure Index' side-by-side for any two paths."
            )

        # 6. Skill gap query
        if any(w in eval_text for w in ["skill gap", "skills required", "deterministic skill gap"]):
            return (
                "DISHA calculates your **Deterministic Skill Gap** by comparing your verified profile competencies against O*NET & ESCO industry standards:\n\n"
                "• **Foundational Prerequisites**: Core quantitative and technical concepts required before entry.\n"
                "• **Specialized Competencies**: Domain-specific tools (e.g. PyTorch for Data Science, Figma for UX).\n"
                "• **Estimated Runway**: Time and project milestones required to bridge the gap.\n\n"
                "Check the **Roadmap** section on your Dashboard (`/dashboard`) or any career card to view your exact missing skills breakdown."
            )

        # 7. Programming aversion / learning
        if any(w in eval_text for w in ["coding", "programming"]):
            if any(w in eval_text for w in ["don't like", "do not like", "less", "not for me", "avoid", "hate", "without", "no coding", "non-coding"]):
                return (
                    "Based on your profile and decision preferences, avoiding heavy programming is a completely viable and flourishing path. "
                    "In modern technology and digital ecosystems, several high-impact careers emphasize human factors, visual systems, "
                    "and business strategy over low-level coding. High-potential areas to explore include UX Design, UX Research, Product Management, "
                    "Digital Marketing Strategy, and Technical Writing. You can use DISHA's 'What-If Explorer' to simulate reduced programming intensity across all career matches."
                )
            elif "learn" in eval_text or "start" in eval_text:
                return (
                    "If you are eager to build programming competencies, starting with Python or JavaScript provides the highest immediate leverage. "
                    "The recommended progression is: 1) Syntax and algorithmic thinking, 2) Data handling and APIs, and 3) Building tangible full-stack "
                    "or analytical portfolio projects. Review the personalized Roadmap section for structured milestone checklists."
                )

        # 8. Specific Math interest (strictly evaluated on the user query itself)
        if any(w in eval_text for w in ["math", "mathematics", "quantitative"]):
            return (
                "Willingness to invest in quantitative mathematics unlocks specialized, future-resilient career tracks such as "
                "Data Science, Quantitative Research, Actuarial Risk Analysis, and Artificial Intelligence Engineering. "
                "DISHA allows you to test this via the What-If Explorer by toggling 'Mathematics Willingness = High' to see newly unlocked pathways."
            )

        # 9. Career context present
        if context:
            return (
                f"Based on authoritative knowledge regarding this pathway:\n\n"
                f"{context[:450]}...\n\n"
                f"Key Takeaway: Rather than viewing this career in isolation, DISHA recommends examining adjacent alternatives "
                f"and reviewing the required skill gap before making a final commitment."
            )

        return (
            "DISHA Career Counselor: Your career journey is an exploratory decision process rather than a one-time assignment. "
            "Consider exploring adjacent careers on the Career Graph, adjusting constraints in What-If analysis, or inspecting your personalized skill gap."
        )

llm_service = LLMService()

llm_service = LLMService()
