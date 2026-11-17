// frontend/src/pages/AssistantPage.tsx
import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import {
  Bot, Send, Sparkles, BookOpen, Sliders, ArrowRight, User as UserIcon,
  ShieldCheck, RefreshCw, Compass, Lightbulb, MessageSquare
} from 'lucide-react';
import { api } from '../services/api';
import { CareerDetail } from '../types';

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  sources?: string[];
  suggestedActions?: string[];
  whatIfTrigger?: any;
  timestamp: string;
}

export const AssistantPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialCareerContext = searchParams.get('career') || '';

  const [careerList, setCareerList] = useState<CareerDetail[]>([]);
  const [selectedCareerContext, setSelectedCareerContext] = useState<string>(initialCareerContext);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: "Hello! I am DISHA's Grounded Career Decision Counselor. Unlike standard LLMs that generate arbitrary career advice, my responses are strictly grounded in empirical labor market data (O*NET 2024, WEF Future of Jobs, ESCO) and your personalized 5-pillar profile.\n\nHow can I help you explore your direction today?",
      sources: ['O*NET 2024 Content Model', 'WEF Future of Jobs 2023', 'National Education Policy 2020'],
      suggestedActions: [
        "I'm in 12th PCM but confused between branches. How do I decide?",
        "I got ~28,000 rank in KCET, which colleges can I target?",
        "I don't like heavy coding. Which engineering or tech careers fit me?",
        "Which engineering branch is best if I want to become a Data Scientist?",
        "How will AI affect UX Designers versus Software Developers?",
      ],
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.careers.list().then(setCareerList).catch(console.warn);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = textToSend || inputMessage;
    if (!query.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const historyPayload = messages.map((m) => ({
        role: m.sender,
        content: m.text,
        sender: m.sender,
        text: m.text,
      }));

      const res = await api.chat.send(
        query,
        selectedCareerContext || undefined,
        historyPayload
      );

      const assistantMsg: ChatMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        text: res.reply,
        sources: res.grounded_career_sources || [],
        suggestedActions: res.suggested_actions || [],
        whatIfTrigger: res.what_if_trigger,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      console.error('Chat failed:', err);
      const errorMsg: ChatMessage = {
        id: `error-${Date.now()}`,
        sender: 'assistant',
        text: `I encountered an issue retrieving grounded guidance: ${err?.message || 'Please check your connection and try again.'}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-6 px-4 sm:px-6 lg:px-8 flex flex-col">
      <div className="max-w-4xl w-full mx-auto flex-1 flex flex-col bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        {/* Chat Header */}
        <div className="border-b border-slate-200 p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-brand-600 text-white flex items-center justify-center shadow-md shadow-brand-500/20">
              <Bot className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-bold text-slate-900 text-base">DISHA Career Counselor</h1>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> Grounded RAG
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Evidence-backed guidance with verifiable citations and interactive What-If triggers.
              </p>
            </div>
          </div>

          {/* Context Career Filter */}
          <div className="flex items-center gap-2">
            <label className="text-xs text-slate-500 font-medium">Context:</label>
            <select
              value={selectedCareerContext}
              onChange={(e) => setSelectedCareerContext(e.target.value)}
              className="text-xs bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-800 focus:outline-none focus:ring-2 focus:ring-brand-500 font-medium"
            >
              <option value="">General Guidance (All 118 Careers)</option>
              {careerList.map((c) => (
                <option key={c.career_id} value={c.career_id}>
                  {c.career_name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Message Thread */}
        <div className="flex-1 p-4 sm:p-6 overflow-y-auto space-y-6 max-h-[620px]">
          {messages.map((msg) => {
            const isUser = msg.sender === 'user';

            return (
              <div
                key={msg.id}
                className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
              >
                {!isUser && (
                  <div className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div
                  className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-sm leading-relaxed space-y-3 ${
                    isUser
                      ? 'bg-brand-600 text-white rounded-tr-none'
                      : 'bg-slate-100/80 border border-slate-200 text-slate-800 rounded-tl-none'
                  }`}
                >
                  {/* Message Text with Paragraphs */}
                  <div className="whitespace-pre-line space-y-2">
                    {msg.text}
                  </div>

                  {/* Grounded Sources Citations */}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="pt-2 border-t border-slate-200/60 text-xs">
                      <div className="font-semibold text-slate-600 flex items-center gap-1 mb-1">
                        <BookOpen className="w-3 h-3 text-brand-600" /> Grounded Citations & Evidence:
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {msg.sources.map((src, i) => (
                          <span
                            key={i}
                            className="bg-white px-2 py-0.5 rounded border border-slate-200 text-[11px] text-slate-600 font-medium"
                          >
                            {src}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Suggested Next Actions Chips */}
                  {msg.suggestedActions && msg.suggestedActions.length > 0 && (
                    <div className="pt-2 space-y-1.5">
                      <div className="text-[11px] font-semibold text-slate-500 flex items-center gap-1">
                        <Lightbulb className="w-3 h-3 text-amber-500" /> Explore Further:
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.suggestedActions.map((action, i) => (
                          <button
                            key={i}
                            type="button"
                            onClick={() => handleSendMessage(action)}
                            className="text-left text-xs bg-white hover:bg-brand-50 text-brand-700 border border-brand-200 px-2.5 py-1 rounded-lg transition-colors"
                          >
                            {action}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* What-If Trigger Button */}
                  {msg.whatIfTrigger && (
                    <div className="pt-2">
                      <button
                        type="button"
                        onClick={() => navigate('/what-if')}
                        className="inline-flex items-center gap-1.5 bg-brand-600 hover:bg-brand-700 text-white text-xs font-semibold px-3 py-2 rounded-xl transition-colors shadow-sm"
                      >
                        <Sliders className="w-3.5 h-3.5" />
                        Launch Counterfactual Simulator with this scenario
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </div>
                  )}

                  <div
                    className={`text-[10px] text-right ${
                      isUser ? 'text-brand-200' : 'text-slate-400'
                    }`}
                  >
                    {msg.timestamp}
                  </div>
                </div>

                {isUser && (
                  <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center flex-shrink-0 mt-0.5">
                    <UserIcon className="w-4 h-4" />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 animate-spin" />
              </div>
              <div className="bg-slate-100 border border-slate-200 rounded-2xl rounded-tl-none p-4 text-xs text-slate-600 flex items-center gap-2">
                <div className="w-2 h-2 bg-brand-500 rounded-full animate-ping" />
                Retrieving grounded labor market context and synthesizing recommendations...
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="border-t border-slate-200 p-4 bg-white">
          {/* Quick Starters for 12th / CET Students */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2.5 mb-2 no-scrollbar text-xs">
            <span className="text-slate-400 font-medium text-[11px] whitespace-nowrap flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-500" /> Quick Ask:
            </span>
            <button
              type="button"
              onClick={() => handleSendMessage("I'm in 12th/PUC and confused about my future options. How should I start?")}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 border border-slate-200 text-xs transition-colors"
            >
              🎓 12th Confused Guidance
            </button>
            <button
              type="button"
              onClick={() => handleSendMessage("I got ~28,000 rank in KCET. What colleges and branches should I target?")}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 border border-slate-200 text-xs transition-colors"
            >
              🏛️ KCET Rank Strategy
            </button>
            <button
              type="button"
              onClick={() => handleSendMessage("Which branch should I choose: CSE, ECE, or specialized AI/ML?")}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 border border-slate-200 text-xs transition-colors"
            >
              💻 Branch Selection Guide
            </button>
            <button
              type="button"
              onClick={() => handleSendMessage("I don't like heavy coding. What non-coding tech and design careers fit me?")}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 border border-slate-200 text-xs transition-colors"
            >
              🎨 Tech Without Heavy Coding
            </button>
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              placeholder={
                selectedCareerContext
                  ? `Ask anything about ${selectedCareerContext.replace('_', ' ')}...`
                  : 'Ask about career options, skill gaps, educational paths, or AI transformation...'
              }
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              disabled={loading}
              className="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-4 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-brand-500 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || loading}
              className="bg-brand-600 hover:bg-brand-700 disabled:bg-slate-300 text-white p-3 rounded-xl transition-colors shadow-sm disabled:shadow-none"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>

          <div className="flex items-center justify-between text-[11px] text-slate-400 mt-2 px-1">
            <span className="flex items-center gap-1">
              <Compass className="w-3 h-3 text-brand-500" />
              Grounded on O*NET 2024, WEF Future of Jobs, and AISHE 2024
            </span>
            <span>DISHA AI Counselor v1.0</span>
          </div>
        </div>
      </div>
    </div>
  );
};
