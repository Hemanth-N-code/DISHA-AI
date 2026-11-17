# scripts/generate_110_careers.py
import json
import os

DOMAINS_DATA = {
    "Engineering & Technology": [
        ("software_engineer", "Software Engineer", "Designs and develops scalable software applications, microservices, and platforms.",
         "Writes clean code, designs distributed systems, and automates testing pipelines.",
         ["B.Tech / B.E. in CS/IT", "BCA / MCA", "B.Sc CS"], "12th with PCM",
         [("Data Structures & Algorithms", 4), ("Python / Java / TypeScript", 4), ("System Design", 3), ("SQL & Databases", 3), ("Git & CI/CD", 3)],
         ["Problem Solving", "Collaboration", "Continuous Learning"], ["cloud_architect", "devops_engineer"], ["product_manager", "technical_writer", "ux_designer"]),
        
        ("cloud_architect", "Cloud Solutions Architect", "Designs and oversees enterprise cloud infrastructure, migration, and security.",
         "Architects multi-cloud infrastructure, disaster recovery plans, and cost optimization.",
         ["B.Tech in CS/IT/ECE", "B.Sc CS + Cloud Certifications"], "12th with PCM",
         [("Cloud Platforms (AWS/Azure/GCP)", 4), ("Networking & Security", 4), ("Infrastructure as Code", 3), ("Kubernetes", 3), ("Distributed Systems", 4)],
         ["Strategic Planning", "Communication", "Risk Management"], ["software_engineer", "devops_engineer"], ["technical_consultant", "devops_engineer"]),

        ("devops_engineer", "DevOps & Platform Engineer", "Builds continuous delivery pipelines and resilient deployment platforms.",
         "Maintains CI/CD pipelines, monitors infrastructure health, and manages container clusters.",
         ["B.Tech in CS/IT/ECE", "BCA + DevOps Diploma"], "12th with PCM",
         [("Linux & Shell Scripting", 4), ("CI/CD (GitHub Actions/Jenkins)", 4), ("Docker & Kubernetes", 4), ("Monitoring", 3), ("Cloud Infrastructure", 3)],
         ["Incident Communication", "Troubleshooting", "Collaboration"], ["software_engineer", "cloud_architect"], ["software_engineer", "technical_consultant"]),

        ("embedded_engineer", "Embedded Systems Engineer", "Designs firmware and hardware-integrated software for microcontrollers and IoT.",
         "Programs microcontrollers in C, interfaces sensors, writes device drivers, and debugs boards.",
         ["B.Tech in ECE / EEE / Mechatronics"], "12th with PCM",
         [("Embedded C / C++", 4), ("Microcontrollers (ARM/ESP32)", 4), ("Protocols (I2C/SPI/CAN)", 3), ("RTOS", 3), ("Circuit Debugging", 3)],
         ["Attention to Detail", "Hands-on Debugging", "Patience"], ["robotics_engineer", "iot_solutions_architect"], ["software_engineer", "electrical_engineer"]),

        ("robotics_engineer", "Robotics Systems Engineer", "Integrates mechanical design, sensing, and control software for autonomous robots.",
         "Develops robot kinematics algorithms, integrates LiDAR/cameras using ROS, and tests autonomy.",
         ["B.Tech in Robotics / Mechatronics / Mechanical / CS"], "12th with PCM",
         [("ROS / ROS2", 4), ("C++ & Python", 4), ("Control Theory", 4), ("Computer Vision", 3), ("Sensor Fusion (SLAM)", 3)],
         ["Interdisciplinary Collaboration", "Problem Solving", "Safety Orientation"], ["embedded_engineer", "ai_engineer"], ["autonomous_vehicle_architect", "mechanical_engineer"]),

        ("aerospace_engineer", "Aerospace & Avionics Engineer", "Designs, analyzes, and tests aircraft, spacecraft, satellites, and airborne defense systems.",
         "Conducts aerodynamic CFD simulations, designs flight controllers, and evaluates structures.",
         ["B.Tech in Aerospace / Aeronautical / Mechanical"], "12th with PCM",
         [("Aerodynamics & Propulsion", 4), ("CAD & CFD (ANSYS/SolidWorks)", 4), ("Flight Dynamics & Control", 3), ("Structural Mechanics", 3), ("MATLAB", 3)],
         ["Precision", "Safety Rigor", "Teamwork"], ["robotics_engineer", "embedded_engineer"], ["mechanical_engineer", "renewable_energy_engineer"]),

        ("biomedical_engineer", "Biomedical Equipment Engineer", "Designs and maintains medical diagnostic hardware, monitors, and surgical tools.",
         "Calibrates hospital diagnostic hardware, validates medical electronics safety standards, and bridges medicine with engineering.",
         ["B.Tech in Biomedical / Instrumentation / ECE"], "12th with Science",
         [("Medical Instrumentation", 4), ("Biosignal Processing", 3), ("Healthcare Safety Standards", 4), ("Circuit Calibration", 3), ("Physiology for Engineers", 3)],
         ["Empathy", "Patience", "Safety Consciousness"], ["embedded_engineer", "medical_doctor"], ["clinical_research_associate", "electrical_engineer"]),

        ("iot_solutions_architect", "IoT Systems Architect", "Architects IoT ecosystems connecting physical sensors, gateways, and cloud platforms.",
         "Selects wireless protocols, designs edge telemetry pipelines, and guarantees device fleet security.",
         ["B.Tech in CS / IT / Electronics"], "12th with PCM",
         [("IoT Protocols (MQTT/LoRaWAN)", 4), ("Edge Computing", 4), ("Cloud IoT Core", 4), ("Device Security", 3), ("Python & C", 3)],
         ["Systems Integration", "Resilience", "Communication"], ["embedded_engineer", "cloud_architect"], ["software_engineer", "devops_engineer"]),

        ("quantum_developer", "Quantum Computing Developer", "Writes algorithms and quantum software routines to execute on quantum hardware and simulators.",
         "Formulates quantum circuits in Qiskit, explores variational quantum algorithms, and mitigates noise.",
         ["B.Tech / B.Sc in CS / Physics / Mathematics"], "12th with PCM (High Math)",
         [("Quantum Mechanics Basics", 4), ("Linear Algebra", 4), ("Python & Qiskit", 4), ("Quantum Algorithms", 3), ("Optimization Theory", 3)],
         ["Abstract Reasoning", "Tenacity", "Scientific Curiosity"], ["software_engineer", "ai_engineer"], ["data_scientist", "quantitative_analyst"]),

        ("site_reliability_engineer", "Site Reliability Engineer (SRE)", "Applies software engineering practices to infrastructure to ensure massive-scale reliability.",
         "Defines SLOs, automates incident response runbooks, conducts post-mortems, and manages error budgets.",
         ["B.Tech in CS / IT", "BCA / MCA"], "12th with PCM",
         [("System Observability (SLO/SLA)", 4), ("Go / Python Automation", 4), ("Linux Internals", 4), ("Incident Management", 3), ("Chaos Engineering", 3)],
         ["Calm Demeanor", "Analytical Curiosity", "Blameless Culture"], ["devops_engineer", "software_engineer"], ["cloud_architect", "cybersecurity_analyst"])
    ],

    "AI & Data": [
        ("ai_engineer", "AI & Machine Learning Engineer", "Designs, trains, and operationalizes machine learning and deep learning models.",
         "Builds neural networks, fine-tunes foundation models, optimizes latency, and validates metrics.",
         ["B.Tech in AI / CS / Data Science", "MS in AI"], "12th with PCM",
         [("Linear Algebra & Calculus", 4), ("Python & PyTorch", 4), ("Deep Learning & Transformers", 4), ("Model Deployment", 3), ("Data Preprocessing", 3)],
         ["Curiosity", "Scientific Rigor", "Ethics in AI"], ["data_scientist", "data_analyst"], ["software_engineer", "quantitative_analyst", "product_manager"]),

        ("data_scientist", "Data Scientist", "Extracts actionable insights and builds predictive statistical models from massive datasets.",
         "Formulates hypotheses, cleans data, builds regression/classification models, and communicates findings.",
         ["B.Sc / M.Sc in Statistics / Math", "B.Tech in Data Science / CS"], "12th with Math",
         [("Applied Statistics", 4), ("Python & Data Science Libraries", 4), ("SQL Databases", 4), ("Exploratory Data Analysis", 4), ("Machine Learning", 3)],
         ["Data Storytelling", "Business Acumen", "Critical Thinking"], ["ai_engineer", "data_analyst"], ["data_analyst", "quantitative_analyst", "economist"]),

        ("data_analyst", "Data Analyst", "Inspects, cleans, transforms, and models data to inform business decision-making.",
         "Writes SQL queries, builds interactive dashboards in Power BI/Tableau, tracks KPIs, and delivers business reviews.",
         ["B.Sc / BCA / B.Com / BBA Analytics / B.Tech"], "12th with Math",
         [("SQL (Joins, Window Functions)", 4), ("Data Visualization (Tableau/PowerBI)", 4), ("Excel & Modeling", 4), ("Descriptive Statistics", 3), ("Basic Python/R", 2)],
         ["Clear Communication", "Business Curiosity", "Detail Oriented"], ["data_scientist", "bi_developer"], ["business_analyst", "digital_marketer", "product_manager"]),

        ("bi_developer", "Business Intelligence (BI) Developer", "Engineers data warehouses, dimensional models, and enterprise reporting systems.",
         "Designs star schemas, writes ETL/ELT pipelines, optimizes queries, and manages semantic layers.",
         ["B.Tech in CS/IT", "BCA / MCA"], "12th with Math",
         [("Data Modeling (Star Schema)", 4), ("SQL & Data Warehouses", 4), ("ETL Tools (dbt/Airflow)", 3), ("Enterprise BI Tools", 4), ("Performance Tuning", 3)],
         ["Systematic Thinking", "Stakeholder Management", "Data Integrity"], ["data_analyst", "data_scientist"], ["data_analyst", "software_engineer"]),

        ("computer_vision_specialist", "Computer Vision Specialist", "Develops algorithms enabling computers to recognize objects and interpret visual scenes.",
         "Trains convolutional networks, optimizes real-time object detection, and segments imagery.",
         ["B.Tech in AI / CS / ECE", "MS in Computer Vision"], "12th with PCM",
         [("OpenCV & Image Processing", 4), ("Deep Learning for Vision", 4), ("PyTorch / TensorFlow", 4), ("Object Detection (YOLO)", 4), ("Camera Geometry", 3)],
         ["Curiosity", "Mathematical Intuition", "Experimental Rigor"], ["ai_engineer", "robotics_engineer"], ["robotics_engineer", "data_scientist"]),

        ("nlp_engineer", "Natural Language Processing (NLP) Engineer", "Engineers linguistic models, semantic search engines, and dialogue systems.",
         "Fine-tunes transformer models, builds vector embeddings retrieval pipelines, and trains text filters.",
         ["B.Tech in CS / AI", "M.Sc in Computational Linguistics"], "12th with Math & English",
         [("Transformers & HuggingFace", 4), ("Tokenization & Vector Embeddings", 4), ("Python & PyTorch", 4), ("RAG & Information Retrieval", 4), ("Evaluation Metrics", 3)],
         ["Linguistic Empathy", "Analytical Patience", "Precision"], ["ai_engineer", "data_scientist"], ["software_engineer", "technical_writer"]),

        ("mlops_engineer", "MLOps Infrastructure Engineer", "Builds automated platforms to train, evaluate, deploy, monitor, and scale ML models.",
         "Configures Kubeflow pipelines, orchestrates feature stores, monitors drift, and automates retraining.",
         ["B.Tech in CS / IT / Data Science"], "12th with PCM",
         [("Docker & Kubernetes", 4), ("ML Pipelines (MLflow/Kubeflow)", 4), ("Model Serving (vLLM/Triton)", 4), ("Monitoring & Drift", 3), ("CI/CD for ML", 3)],
         ["Systems Mindset", "Operational Discipline", "Collaboration"], ["devops_engineer", "ai_engineer"], ["cloud_architect", "software_engineer"]),

        ("quant_analyst", "Quantitative Research & Risk Analyst", "Applies mathematical and algorithmic techniques to model financial markets and trading strategies.",
         "Develops stochastic calculus models, backtests algorithmic trading strategies, and analyzes market risk.",
         ["B.Tech in CS / Math / Physics", "M.Sc Financial Engineering"], "12th with High Math",
         [("Stochastic Calculus & Probability", 4), ("Python & C++", 4), ("Time Series Modeling", 4), ("Algorithmic Backtesting", 3), ("Derivatives Pricing", 3)],
         ["Intellectual Rigor", "Mental Stamina", "Risk Judgment"], ["data_scientist", "financial_analyst"], ["financial_analyst", "actuary"]),

        ("big_data_engineer", "Big Data Platform Engineer", "Scales distributed pipelines to ingest, transform, and query massive datasets.",
         "Writes Apache Spark streaming jobs, configures Kafka message brokers, and manages data lakes.",
         ["B.Tech in CS / IT", "MCA / M.Tech"], "12th with PCM",
         [("Distributed Computing (Spark)", 4), ("Streaming Systems (Kafka/Flink)", 4), ("Scala / Java / Python", 4), ("Data Lakes (Iceberg/Delta)", 4), ("Database Partitioning", 3)],
         ["Architectural Resilience", "Tenacity", "Problem Solving"], ["software_engineer", "cloud_architect"], ["bi_developer", "cloud_architect"])
    ],

    "Cybersecurity": [
        ("cybersecurity_analyst", "Cybersecurity Operations Analyst", "Protects digital networks, systems, and data from cyber threats and intrusions.",
         "Monitors SIEM telemetry, analyzes intrusion alerts, performs vulnerability scans, and handles containment.",
         ["B.Tech in Cybersecurity / CS / IT", "B.Sc Cybersecurity"], "12th with Math/Science",
         [("Network Protocols (TCP/IP)", 4), ("SIEM Tools (Splunk/Sentinel)", 4), ("Threat Analysis", 3), ("Vulnerability Assessment", 3), ("Security Fundamentals", 3)],
         ["High Vigilance", "Calm Under Pressure", "Ethical Integrity"], ["ethical_hacker", "cloud_security_architect"], ["cloud_security_architect", "devops_engineer"]),

        ("ethical_hacker", "Penetration Tester & Ethical Hacker", "Simulates adversary attacks against web apps, networks, and cloud assets to find flaws.",
         "Conducts authorized security assessments, exploits vulnerabilities with Burp Suite, and writes remediation guides.",
         ["B.Tech in CS / IT / Cybersecurity", "BCA + Certs"], "12th with Math/Science",
         [("Web App Security (OWASP)", 4), ("Pentest Tools (Burp/Metasploit)", 4), ("Network Exploitation", 3), ("Scripting (Python/Bash)", 3), ("Remediation Advisory", 3)],
         ["Lateral Thinking", "Uncompromising Ethics", "Documentation"], ["cybersecurity_analyst", "cloud_security_architect"], ["software_engineer", "qa_automation_engineer"]),

        ("digital_forensics_analyst", "Digital Forensics Investigator", "Recovers and inspects digital evidence from compromised disks, memory dumps, and logs.",
         "Preserves forensic chain of custody, extracts deleted artifacts, analyzes RAM dumps, and drafts court reports.",
         ["B.Sc in Forensic Science / Cyber", "B.Tech in CS/IT"], "12th with Science",
         [("Disk Forensics (NTFS/EXT4)", 4), ("Memory Analysis (Volatility)", 3), ("Chain of Custody & Evidence Law", 4), ("Forensics Tools (Autopsy/FTK)", 3), ("Log Reconstruction", 3)],
         ["Methodical Patience", "Curiosity", "Legal Precision"], ["cybersecurity_analyst", "ethical_hacker"], ["cybersecurity_analyst", "cyber_lawyer"]),

        ("cloud_security_architect", "Cloud Security & DevSecOps Architect", "Embeds automated security controls and compliance validations throughout cloud stacks.",
         "Configures IAM least-privilege, audits posture (CSPM), scans containers in CI/CD, and prevents data leaks.",
         ["B.Tech in CS / Cybersecurity", "B.Sc IT + Certs"], "12th with PCM",
         [("Cloud Security (AWS/Azure IAM)", 4), ("DevSecOps (Snyk/Trivy)", 4), ("Security Posture (CSPM)", 4), ("Zero Trust", 3), ("Compliance (SOC2/ISO)", 3)],
         ["Diplomacy", "Systems Thinking", "Security Evangelism"], ["cloud_architect", "devops_engineer"], ["cloud_architect", "devops_engineer"]),

        ("iam_specialist", "Identity & Access Management (IAM) Specialist", "Governs digital identity verification, SSO, MFA, and privileged access rights.",
         "Configures identity providers (Okta/Entra), enforces RBAC, and audits access lifecycles.",
         ["B.Tech in IT / CS", "BCA / B.Sc IS"], "12th with Math",
         [("Identity Protocols (SAML/OAuth)", 4), ("Enterprise IdPs (Okta/Entra)", 4), ("Privileged Access (PAM)", 4), ("Active Directory", 3), ("Access Governance", 3)],
         ["Meticulous Detail", "Patience", "Governance Mindset"], ["cybersecurity_analyst", "cloud_security_architect"], ["cloud_security_architect", "devops_engineer"]),

        ("threat_intelligence_analyst", "Cyber Threat Intelligence (CTI) Analyst", "Investigates cybercriminal syndicates, APTs, and exploit campaigns to advise proactive defense.",
         "Analyzes adversary TTPs against MITRE ATT&CK, tracks dark web forums, extracts IoCs, and writes strategic briefs.",
         ["B.Sc Cyber / IS", "B.A. International Relations + Cyber Cert"], "12th Any Stream",
         [("Adversary Tactics (MITRE ATT&CK)", 4), ("Threat Intel Platforms (MISP)", 4), ("OSINT Techniques", 4), ("IoC Extraction", 3), ("Strategic Reporting", 3)],
         ["Investigative Curiosity", "Discretion", "Persuasive Briefing"], ["cybersecurity_analyst", "digital_forensics_analyst"], ["cybersecurity_analyst", "technical_writer"]),

        ("cryptographic_systems_engineer", "Cryptographic Systems Engineer", "Designs and implements cryptographic algorithms, key management, and zero-knowledge proofs.",
         "Implements post-quantum encryption, configures HSMs, writes secure libraries, and verifies mathematical proofs.",
         ["B.Tech in CS / Math / ECE", "M.Sc Cryptography"], "12th with High Math",
         [("Applied Cryptography", 4), ("Post-Quantum Cryptography", 4), ("C / Rust for Systems", 4), ("PKI & HSMs", 3), ("Zero-Knowledge Basics", 3)],
         ["Mathematical Rigor", "Patience", "Security Paranoia"], ["software_engineer", "cybersecurity_analyst"], ["software_engineer", "quantum_developer"])
    ],

    "Design": [
        ("ux_designer", "UX Designer (User Experience)", "Crafts intuitive digital user journeys through research, wireframing, and usability testing.",
         "Conducts user interviews, maps user journeys, builds wireframes in Figma, runs tests, and aligns with developers.",
         ["B.Des in Interaction / Product Design", "B.Tech with Design Minor", "B.Sc Visual Comm"], "12th Any Stream",
         [("User Research & Testing", 4), ("Wireframing (Figma)", 4), ("Information Architecture", 4), ("Interaction Design", 3), ("Design Systems", 3)],
         ["Empathy", "Storytelling", "Facilitation", "Active Listening"], ["ui_designer", "product_designer"], ["product_manager", "technical_writer", "ux_researcher"]),

        ("ui_designer", "UI Designer (User Interface)", "Specializes in visual presentation, aesthetics, typography, colors, and motion for digital products.",
         "Creates pixel-perfect UI layouts, designs iconography, develops design tokens, and animates transitions.",
         ["B.Des in Visual Design", "BFA Applied Arts", "Diploma Web Design"], "12th Any Stream",
         [("Visual Design & Layout", 4), ("Figma Design Systems", 4), ("Typography & Color Theory", 4), ("Micro-Animations", 3), ("Basic HTML/CSS", 2)],
         ["Visual Elegance", "Attention to Detail", "Consistency"], ["ux_designer", "product_designer"], ["graphic_designer", "motion_graphics_animator"]),

        ("product_designer", "Product Designer (Digital)", "Owns end-to-end user experience and visual design aligned with business goals and engineering.",
         "Bridges research and visual design, evaluates conversion metrics, collaborates on product roadmaps, and tests MVPs.",
         ["B.Des in Product Design", "B.Tech with Design Minor"], "12th Any Stream",
         [("Product Thinking & UX", 4), ("Visual Design (Figma)", 4), ("Product Metrics & Experiments", 3), ("Rapid Prototyping", 4), ("Stakeholder Alignment", 3)],
         ["Holistic Vision", "Business Acumen", "Resilience", "Communication"], ["ux_designer", "product_manager"], ["product_manager", "ux_researcher"]),

        ("ux_researcher", "UX Researcher", "Discovers user motivations, pain points, and cognitive barriers through qualitative and quantitative methods.",
         "Conducts interviews, runs diary studies, designs surveys, analyzes metrics, and synthesizes strategic insights.",
         ["B.Sc / M.Sc Psychology / Cognitive Science", "B.Des Interaction Design"], "12th Any Stream",
         [("Qualitative Interviewing", 4), ("Usability Testing", 4), ("Survey Design & Analysis", 3), ("Insight Frameworks", 4), ("Cognitive Psychology", 3)],
         ["Active Listening", "Curiosity", "Unbiased Observation", "Storytelling"], ["ux_designer", "product_manager"], ["data_analyst", "product_manager", "clinical_psychologist"]),

        ("design_systems_architect", "Design Systems Architect", "Standardizes reusable component libraries, design tokens, and documentation across teams.",
         "Architects multi-brand Figma token frameworks, writes component guidelines, and audits design-to-code parity.",
         ["B.Des Visual / Interaction Design", "B.Tech CS with Design"], "12th Any Stream",
         [("Figma Design Tokens & Variables", 4), ("Component Architecture", 4), ("Basic React / Web Components", 3), ("Accessibility (WCAG)", 4), ("Governance", 3)],
         ["Systemic Thinking", "Consensus Building", "Precision"], ["ui_designer", "ux_designer"], ["software_engineer", "product_designer"]),

        ("interaction_designer", "Interaction Designer", "Designs kinetic behavior, micro-interactions, responsive states, and emotional dialogue of interfaces.",
         "Prototypes gesture-based animations in ProtoPie, models dynamic transitions, and tests motor response times.",
         ["B.Des Interaction / New Media Design", "BFA Digital Arts"], "12th Any Stream",
         [("Prototyping (ProtoPie/Framer)", 4), ("Motion Design & Curves", 4), ("Human Factors & Ergonomics", 3), ("Micro-Interactions", 4), ("Feedback Loops", 3)],
         ["Kinetic Intuition", "Playfulness", "Timing Sensitivity"], ["ux_designer", "ui_designer"], ["game_designer", "motion_graphics_animator"]),

        ("service_designer", "Service Designer", "Orchestrates complex human touchpoints, backend operations, and organizational workflows across ecosystems.",
         "Maps end-to-end service blueprints, conducts stakeholder co-design sessions, and redesigns citizen or customer experiences.",
         ["B.Des in Strategic Design / Interaction", "MBA with Design Thinking"], "12th Any Stream",
         [("Service Blueprinting", 4), ("Stakeholder Co-Creation Workshops", 4), ("Systems Thinking", 4), ("Customer Journey Mapping", 4), ("Operational Feasibility", 3)],
         ["Diplomatic Facilitation", "Holistic Perspective", "Empathy"], ["ux_designer", "product_manager"], ["management_consultant", "product_manager"]),

        ("graphic_designer", "Graphic Designer & Brand Stylist", "Creates visual identities, logos, marketing collateral, packaging, and brand aesthetics.",
         "Designs corporate logos, typographically balanced brochures, packaging mockups, and digital marketing visuals.",
         ["B.Des Visual Communication", "BFA Applied Arts", "Diploma Graphic Design"], "12th Any Stream",
         [("Adobe Creative Suite (Illustrator/Photoshop/InDesign)", 4), ("Branding & Identity Design", 4), ("Typography & Print Production", 4), ("Layout Composition", 4), ("Color Harmony", 3)],
         ["Artistic Taste", "Client Empathy", "Visual Originality"], ["ui_designer", "concept_artist"], ["ui_designer", "digital_marketer", "motion_graphics_animator"])
    ],

    "Fashion": [
        ("fashion_designer", "Fashion Designer", "Creates original clothing, footwear, and accessory collections blending creativity and tailoring.",
         "Sketches design concepts, selects textiles, creates technical pattern packs (tech packs), and oversees samples.",
         ["B.Des in Fashion Design (NIFT/Pearl)", "Diploma in Apparel Design"], "12th Any Stream",
         [("Fashion Illustration & CAD (CLO3D)", 4), ("Pattern Making & Construction", 4), ("Textile Science", 3), ("Trend Forecasting", 3), ("Tech Packs", 3)],
         ["Creative Vision", "Cultural Sensitivity", "Commercial Awareness"], ["textile_designer", "costume_designer"], ["graphic_designer", "product_designer"]),

        ("textile_designer", "Textile & Surface Pattern Designer", "Engineers fabric structures, surface prints, jacquard weaves, and sustainable finishes.",
         "Creates repeat prints in Photoshop, specifies yarn counts, programs jacquard looms, and tests colorfastness.",
         ["B.Des in Textile Design (NID/NIFT)", "B.Tech in Textile Tech"], "12th Science/Arts",
         [("Surface Pattern Design", 4), ("Weaving & Knits (Jacquard)", 4), ("Dyes & Finishes", 3), ("Textile Testing", 3), ("Color Matching", 4)],
         ["Tactile Sensitivity", "Patience for Detail", "Rhythm"], ["fashion_designer", "ceramic_designer"], ["graphic_designer", "concept_artist"]),

        ("fashion_merchandiser", "Fashion Merchandiser & Buyer", "Bridges fashion creativity with retail profitability by planning lines and sourcing factories.",
         "Analyzes sell-through rates, negotiates garment FOB prices, plans store allocation, and tracks inventory.",
         ["B.F.Tech (Fashion Technology)", "BBA Fashion Merchandising"], "12th Any Stream",
         [("Apparel Costing & Sourcing", 4), ("Retail Math (Sell-Through/OTB)", 4), ("Garment Production Quality", 3), ("Inventory Planning ERP", 4), ("Trend Analysis", 3)],
         ["Commercial Negotiation", "Analytical Rigor", "Fast Agility"], ["fashion_designer", "financial_analyst"], ["financial_analyst", "product_manager"]),

        ("sustainable_apparel_specialist", "Sustainable Apparel Specialist", "Audits fashion supply chains to eliminate toxic chemicals, reduce water, and enable circular recycling.",
         "Conducts Higg Index audits, tracks carbon footprints, sources recycled fibers, and implements take-back systems.",
         ["B.Tech Textile / Environmental", "B.Des with Sustainability focus"], "12th Science/Commerce",
         [("Life Cycle Assessment (LCA)", 4), ("Higg Index Auditing", 4), ("Circular Design & Fiber Recycling", 4), ("Supply Chain Transparency", 3), ("Organic Certifications (GOTS)", 3)],
         ["Moral Conviction", "Verification Rigor", "Influence"], ["fashion_designer", "environmental_scientist"], ["environmental_scientist", "sustainability_consultant"]),

        ("costume_designer", "Costume Designer & Wardrobe Stylist", "Researches historical periods, analyzes scripts, and creates authentic costumes for film and theatre.",
         "Creates period mood boards, sources vintage fabrics, distresses garments, and manages wardrobe continuity on set.",
         ["B.Des in Fashion/Costume", "BFA Theatre Arts"], "12th Any Stream",
         [("Historical Costume Research", 4), ("Script Breakdown & Styling", 4), ("Garment Aging & Distressing", 3), ("Wardrobe Continuity", 4), ("Costume Budgeting", 3)],
         ["Dramatic Storytelling", "Set Patience", "Historical Empathy"], ["fashion_designer", "film_editor"], ["fashion_designer", "concept_artist"]),

        ("footwear_designer", "Footwear & Accessory Designer", "Designs ergonomic, aesthetic, and performance footwear combining biomechanics and industrial design.",
         "Creates last specifications, drafts 2D outsole blueprints, models 3D sneaker uppers, and tests shock absorption.",
         ["B.Des in Footwear Design (FDDI)", "B.Des in Industrial/Product Design"], "12th Any Stream",
         [("Footwear Construction & Lasting", 4), ("Biomechanics & Ergonomics", 3), ("Footwear CAD & 3D Prototyping", 4), ("Leather & Synthetic Materials", 4), ("Outsole Tooling Specs", 3)],
         ["Spatial Sensitivity", "Ergonomic Intuition", "Material Passion"], ["fashion_designer", "product_designer"], ["product_designer", "sports_technologist"])
    ],

    "Media & Film": [
        ("film_editor", "Film & Video Editor", "Assembles raw camera footage, audio, and visual effects into coherent cinematic narratives.",
         "Reviews takes, cuts scenes for emotional pacing, syncs audio, color grades footage, and exports masters.",
         ["B.Sc/B.A. Film Production (FTII/SRFTI)", "Diploma Video Editing"], "12th Any Stream",
         [("Non-Linear Editing (DaVinci/Premiere)", 4), ("Cinematic Pacing", 4), ("Color Grading", 3), ("Audio Mixing Basics", 3), ("Motion Graphics Basics", 2)],
         ["Patience", "Narrative Empathy", "Micro-rhythm Attention"], ["motion_graphics_animator", "sound_designer"], ["motion_graphics_animator", "technical_writer"]),

        ("technical_writer", "Technical Writer & Documentation Strategist", "Translates engineering systems, software code, and science into clear user documentation.",
         "Interviews engineers, documents REST APIs in OpenAPI, creates developer portals, and writes release notes.",
         ["B.A./B.Sc English / Journalism", "B.Tech CS with strong writing"], "12th Any Stream",
         [("Technical Clarity & Writing", 4), ("Docs-as-Code (Markdown/Git)", 4), ("API Documentation (Swagger)", 3), ("Information Architecture", 3), ("Basic Code Literacy", 2)],
         ["Extreme Clarity", "Curiosity", "User Advocacy"], ["ux_designer", "product_manager"], ["technical_consultant", "ux_designer"]),

        ("motion_graphics_animator", "Motion Graphics Artist & Animator", "Creates dynamic typography, animated brand identities, and kinetic UI animations.",
         "Animates vector graphics in After Effects, models 3D title sequences in Cinema 4D, and crafts transitions.",
         ["B.Des in Animation & Motion", "BFA Applied Arts"], "12th Any Stream",
         [("After Effects & Expressions", 4), ("Cinema 4D / Blender Basics", 4), ("Kinetic Typography", 4), ("Sound Sync & Rhythm", 3), ("Vector Illustration", 3)],
         ["Visual Rhythm", "Patience with Keyframes", "Adaptability"], ["film_editor", "ui_designer"], ["ui_designer", "concept_artist"]),

        ("sound_designer", "Sound Designer & Audio Engineer", "Creates original sound effects, atmospheric ambiences, Foley, and dialogue mixes for media.",
         "Records soundscapes, designs synthesized SFX, edits ADR dialogue, and mixes in Dolby Atmos.",
         ["B.Sc Sound Engineering", "Diploma Audio Production"], "12th Any Stream",
         [("DAWs (Pro Tools/Logic)", 4), ("Foley & Sound Effects Design", 4), ("Audio Synthesis", 3), ("Surround Mixing (Dolby Atmos)", 4), ("Dialogue Editing", 3)],
         ["Acoustic Sensitivity", "Immersion Intuition", "Sonic Detail"], ["film_editor", "game_designer"], ["film_editor", "podcast_producer"]),

        ("broadcast_journalist", "Broadcast & Investigative Journalist", "Investigates breaking events, verifies factual evidence, and produces reports for broadcast.",
         "Fact-checks claims against records, conducts on-camera interviews, writes news scripts, and reports live.",
         ["B.A. in Journalism (BJMC)", "B.Sc Media Science"], "12th Any Stream",
         [("Investigative Verification", 4), ("News Scriptwriting & Ethics", 4), ("On-Camera Interviewing", 4), ("Media Law Guidelines", 3), ("Mobile Field Production", 3)],
         ["Unyielding Integrity", "Courage", "Empathy"], ["technical_writer", "corporate_lawyer"], ["technical_writer", "public_health_specialist"]),

        ("creative_director_advertising", "Creative Advertising Director", "Leads creative strategy, copywriting concepts, and multimedia campaigns for global brands.",
         "Directs creative pitches, crafts memorable brand campaign taglines, and oversees art directors.",
         ["B.A. Mass Comm / Advertising", "B.Des Communication Design"], "12th Any Stream",
         [("Creative Campaign Ideation", 4), ("Strategic Brand Storytelling", 4), ("Art Direction Principles", 4), ("Client Pitch Presentation", 4), ("Consumer Psychology", 3)],
         ["Bold Imagination", "Charismatic Leadership", "Cultural Resonance"], ["film_editor", "concept_artist"], ["digital_marketer", "product_manager"]),

        ("podcast_producer", "Podcast Producer & Audio Storyteller", "Develops narrative non-fiction and interview audio shows from research to sound design.",
         "Conducts pre-interviews, edits longform conversational audio, weaves scoring, and manages RSS distribution.",
         ["B.A. Mass Comm / Journalism / English", "Diploma Sound Design"], "12th Any Stream",
         [("Audio Editing & Narrative Pacing", 4), ("Interviewing & Guest Prep", 4), ("Scriptwriting for the Ear", 4), ("Audio Mixing & Loudness Standards", 3), ("Podcast Distribution & SEO", 3)],
         ["Empathetic Curating", "Auditory Detail", "Tenacity"], ["sound_designer", "broadcast_journalist"], ["broadcast_journalist", "technical_writer"])
    ],

    "Psychology": [
        ("clinical_psychologist", "Clinical Psychologist", "Diagnoses, treats, and supports individuals experiencing psychological distress and disorders.",
         "Conducts clinical interviews and psychometric assessments, designs CBT interventions, and aids recovery.",
         ["B.A./B.Sc Psychology -> M.A. Clinical Psych -> M.Phil (RCI approved)"], "12th Any Stream",
         [("Psychological Assessment", 4), ("Psychotherapy (CBT/DBT)", 4), ("Diagnostic Criteria (DSM-5)", 4), ("Crisis Intervention", 4), ("Case Formulation", 3)],
         ["Radical Empathy", "Listening", "Stability", "Discretion"], ["counseling_psychologist", "organizational_psychologist"], ["counseling_psychologist", "ux_researcher"]),

        ("counseling_psychologist", "Counseling Psychologist", "Helps individuals navigate life transitions, relationship conflicts, career choices, and stress.",
         "Facilitates personal growth, provides relationship therapy, administers aptitude tests, and runs workshops.",
         ["B.A./B.Sc Psychology -> M.A. Counseling Psychology"], "12th Any Stream",
         [("Counseling Techniques", 4), ("Career Guidance Assessment", 4), ("Family Systems Therapy", 3), ("Grief Support", 3), ("Counseling Ethics", 4)],
         ["Warm Compassion", "Empathetic Presence", "Inclusivity"], ["clinical_psychologist", "organizational_psychologist"], ["clinical_psychologist", "instructional_designer"]),

        ("organizational_psychologist", "Organizational Psychologist", "Applies behavioral science to workplace dynamics, leadership development, and culture.",
         "Designs psychometric tests, assesses engagement metrics, develops leadership coaching, and guides change.",
         ["B.A./B.Sc Psychology -> M.A. Organizational Psych"], "12th Any Stream",
         [("Workplace Psychometrics", 4), ("Organizational Behavior", 4), ("People Analytics", 3), ("Leadership Coaching", 3), ("Change Management", 3)],
         ["Diplomacy", "Strategic Thinking", "Objective Evaluation"], ["clinical_psychologist", "management_consultant"], ["management_consultant", "ux_researcher"]),

        ("neuropsychologist", "Clinical Neuropsychologist", "Evaluates cognitive brain functioning resulting from head trauma, stroke, or dementia.",
         "Administers neurocognitive test batteries (WAIS), maps deficits, and designs rehabilitation programs.",
         ["B.Sc Psychology/Neuro -> M.Sc Neuropsychology -> Ph.D./M.Phil"], "12th with Science",
         [("Neuropsychological Testing", 4), ("Neuroanatomy", 4), ("Cognitive Rehabilitation", 4), ("Neuroimaging Interpretation", 3), ("Differential Diagnosis", 3)],
         ["Scientific Rigor", "Patience", "Compassion"], ["clinical_psychologist", "medical_doctor"], ["clinical_psychologist", "medical_doctor"]),

        ("child_development_specialist", "Child Development & School Counselor", "Assesses developmental milestones, learning disabilities (ADHD, Dyslexia), and behavioral growth.",
         "Designs IEPs, conducts play therapy, advises parents, and coordinates with pediatricians.",
         ["B.A. Psychology / Early Childhood -> M.A. Child Psychology"], "12th Any Stream",
         [("Developmental Psychology", 4), ("Learning Disability Assessment", 4), ("Play & Behavioral Therapy", 4), ("IEP Design", 3), ("Parent Counseling", 4)],
         ["Gentle Patience", "Playful Warmth", "Protective Advocacy"], ["counseling_psychologist", "special_educator"], ["special_educator", "instructional_designer"]),

        ("behavioral_data_analyst", "Behavioral Data Scientist", "Analyzes digital product user behaviors using statistical modeling and behavioral economics.",
         "Runs randomized controlled experiments (A/B tests), models cognitive biases, and boosts feature engagement.",
         ["B.Sc Psychology / Economics + Data Science Cert", "MS Behavioral Economics"], "12th with Math",
         [("Behavioral Economics Principles", 4), ("A/B Testing & Experimentation", 4), ("Python / R Statistics", 4), ("SQL Querying", 3), ("Psychometrics", 3)],
         ["Hypothesis Skepticism", "Cross-disciplinary Mindset", "Clarity"], ["data_scientist", "ux_researcher"], ["ux_researcher", "data_analyst"])
    ],

    "Fine Arts": [
        ("concept_artist", "Concept Artist & Illustrator", "Visualizes characters, environments, and imaginary worlds for video games and films.",
         "Translates scripts into thumbnail sketches, paints environments, designs costumes, and creates art bibles.",
         ["BFA in Painting / Animation", "B.Des in Game Art"], "12th Any Stream",
         [("Anatomy & Figure Drawing", 4), ("Digital Painting (Photoshop)", 4), ("Lighting & Composition", 4), ("3D Blockouts (Blender)", 3), ("Visual Storytelling", 4)],
         ["Receptive to Direction", "Creative Imagination", "Perseverance"], ["motion_graphics_animator", "game_designer"], ["graphic_designer", "ui_designer"]),

        ("sculptor_visual_artist", "Sculptor & Visual Artist", "Creates physical sculptures, gallery installations, and public monuments using stone, bronze, and resin.",
         "Casts bronze in foundries, carves stone with chisels, welds steel armatures, and exhibits in galleries.",
         ["BFA in Sculpture", "MFA Contemporary Art"], "12th Any Stream",
         [("Sculptural Techniques (Clay/Bronze)", 4), ("Welding & Armatures", 4), ("Spatial Installation", 4), ("Art History Theory", 3), ("Material Science", 3)],
         ["Artistic Philosophy", "Physical Stamina", "Originality"], ["concept_artist", "architect"], ["concept_artist", "fashion_designer"]),

        ("art_conservator", "Art Conservator & Restorer", "Preserves, stabilizes, and scientifically restores historic paintings and museum artifacts.",
         "Analyzes pigment chemistry, dissolves darkened aged varnish with solvents, and retouches paint losses reversibly.",
         ["BFA / B.Sc Chemistry -> M.A. Art Conservation"], "12th Science/Arts",
         [("Pigment & Solvent Chemistry", 4), ("Micro-Cleaning", 4), ("Reversible Inpainting", 4), ("Spectroscopic Analysis", 3), ("Preventive Conservation", 3)],
         ["Extreme Patience", "Hand Steadiness", "Historical Reverence"], ["museum_curator", "sculptor_visual_artist"], ["museum_curator", "concept_artist"]),

        ("museum_curator", "Museum Curator & Exhibition Director", "Curates art exhibitions, manages museum collections, acquires artifacts, and educates the public.",
         "Researches provenance, writes catalog essays, designs gallery floor narratives, and negotiates loans.",
         ["B.A. History/Fine Arts -> M.A. Museology/Art History -> Ph.D."], "12th Any Stream",
         [("Art History & Historiography", 4), ("Exhibition Curation", 4), ("Provenance Research", 4), ("Collection Management", 3), ("Catalog Writing", 4)],
         ["Intellectual Erudition", "Narrative Vision", "Diplomacy"], ["art_conservator", "creative_director"], ["art_conservator", "broadcast_journalist"]),

        ("ceramic_designer", "Ceramic & Material Designer", "Formulates clays, hand-throws functional pottery, molds porcelain, and experiments with glaze chemistry.",
         "Formulates stoneware and porcelain glazes, operates high-fire gas/electric kilns, and designs homeware.",
         ["B.Des in Ceramic & Glass Design (NID)", "BFA Ceramics"], "12th Any Stream",
         [("Wheel Throwing & Hand Building", 4), ("Glaze Chemistry & Formulation", 4), ("Kiln Firing (Bisque & Glaze)", 4), ("Mold Making & Slip Casting", 3), ("Product Ergonomics", 3)],
         ["Tactile Patience", "Craftsmanship", "Material Intuition"], ["sculptor_visual_artist", "product_designer"], ["product_designer", "textile_designer"]),

        ("character_3d_artist", "3D Character Artist", "Sculpts high-poly digital human, creature, and monster models for video games and VFX.",
         "Sculpts anatomy in ZBrush, retopologizes clean mesh for rigging in Maya, and paints textures in Substance Painter.",
         ["B.Des in Animation / Game Art", "Diploma 3D Digital Art"], "12th Any Stream",
         [("Digital Sculpting (ZBrush)", 4), ("Organic Anatomy & Proportions", 4), ("Texturing (Substance Painter)", 4), ("Retopology & UV Unwrapping", 3), ("Real-time Shaders", 3)],
         ["Anatomical Precision", "Patience for Polygons", "Aesthetic Taste"], ["concept_artist", "motion_graphics_animator"], ["concept_artist", "game_designer"])
    ],

    "Healthcare": [
        ("medical_doctor", "General Physician / Medical Doctor", "Assesses, diagnoses, treats, and prevents physical illnesses to preserve human health.",
         "Conducts patient examinations, interprets diagnostic tests, prescribes treatments, and coordinates care.",
         ["MBBS (5.5 Yrs) -> MD/MS (3 Yrs)"], "12th PCB (NEET qualified)",
         [("Clinical Diagnosis & Pathology", 4), ("Pharmacology Protocols", 4), ("Physical Examination", 4), ("Emergency Life Support", 4), ("Medical Ethics", 4)],
         ["Compassion", "Emotional Resilience", "Decisiveness", "Stamina"], ["pharmacist", "clinical_research_associate"], ["clinical_research_associate", "public_health_specialist"]),

        ("clinical_research_associate", "Clinical Research Associate (CRA)", "Monitors clinical drug trials to ensure safety, validity, and strict regulatory compliance.",
         "Conducts site visits, audits informed consent, verifies adverse events, and ensures GCP adherence.",
         ["B.Pharm / M.Pharm", "B.Sc/M.Sc Biotechnology / Life Sciences"], "12th with Science",
         [("Good Clinical Practice (ICH-GCP)", 4), ("Clinical Trial Protocols", 4), ("Source Data Verification", 4), ("Pharmacovigilance", 3), ("Medical Terminology", 3)],
         ["Meticulous Detail", "Integrity", "Coordination", "Audit Rigor"], ["medical_doctor", "pharmacist"], ["pharmacist", "biotechnologist"]),

        ("pharmacist", "Hospital & Clinical Pharmacist", "Dispenses medications, reviews drug regimens for adverse interactions, and counsels patients.",
         "Audits patient medication charts, prepares sterile IV mixtures, and advises physicians on drug dosing.",
         ["B.Pharm (4 Yrs) / Pharm.D (6 Yrs)"], "12th with PCB/PCM",
         [("Pharmacology & Therapeutics", 4), ("Drug-Drug Interactions", 4), ("Sterile Compounding", 3), ("Pharmacy Law & Regulations", 4), ("Patient Counseling", 4)],
         ["Extreme Accuracy", "Ethical Responsibility", "Patient Communication"], ["medical_doctor", "clinical_research_associate"], ["clinical_research_associate", "biotechnologist"]),

        ("physical_therapist", "Physical Therapist & Rehab Specialist", "Restores physical mobility, alleviates musculoskeletal pain, and rehabilitates post-surgical patients.",
         "Assesses joint range of motion, designs therapeutic exercise regimens, and applies manual mobilization.",
         ["BPT (Bachelor of Physiotherapy - 4.5 Yrs) -> MPT (2 Yrs)"], "12th with PCB",
         [("Musculoskeletal Anatomy", 4), ("Therapeutic Exercise Prescription", 4), ("Manual Therapy Techniques", 4), ("Electrotherapy & Modalities", 3), ("Gait & Posture Analysis", 3)],
         ["Physical Stamina", "Patient Encouragement", "Observation"], ["medical_doctor", "occupational_therapist"], ["occupational_therapist", "sports_technologist"]),

        ("public_health_specialist", "Public Health Epidemiologist", "Investigates disease outbreaks, designs vaccination policies, and directs population health initiatives.",
         "Models epidemic transmission curves, analyzes health survey data, and drafts health policy guidelines.",
         ["MBBS / B.Sc Life Sciences -> MPH (Master of Public Health)"], "12th with Science",
         [("Epidemiological Study Design", 4), ("Biostatistics & Health Data", 4), ("Disease Surveillance Systems", 4), ("Health Policy Formulation", 3), ("Community Health Interventions", 3)],
         ["Scientific Objectivity", "Global Empathy", "Policy Communication"], ["medical_doctor", "data_analyst"], ["data_analyst", "environmental_scientist"]),

        ("biomedical_informatics_specialist", "Biomedical Informatics Specialist", "Bridges medical science, genomic databases, and health IT systems to improve patient outcomes.",
         "Structures electronic health record (EHR) data, queries genomic databases, and models clinical outcomes.",
         ["B.Tech Bioinformatics / CS", "B.Sc Life Sciences + Health IT"], "12th with Science/Math",
         [("Health Informatics Standards (HL7/FHIR)", 4), ("SQL & Medical Databases", 4), ("Genomic Data Analysis", 3), ("Clinical Decision Support Systems", 3), ("Biostatistics", 3)],
         ["Systematic Analysis", "Confidentiality", "Interdisciplinary Translation"], ["data_scientist", "ai_engineer"], ["data_analyst", "clinical_research_associate"]),

        ("genetic_counselor", "Genetic Counselor", "Assesses inherited disease risks, interprets genetic test reports, and counsels families with compassion.",
         "Constructs detailed family pedigree trees, explains chromosomal abnormalities, and provides reproductive guidance.",
         ["B.Sc Genetics / Biotechnology -> M.Sc Genetic Counseling"], "12th with PCB",
         [("Human Medical Genetics", 4), ("Pedigree Construction & Risk Calculation", 4), ("Genetic Test Interpretation", 4), ("Psychological Counseling", 4), ("Bioethics", 3)],
         ["Deep Compassion", "Complex Science Translation", "Non-Directive Guidance"], ["medical_doctor", "clinical_psychologist"], ["clinical_psychologist", "clinical_research_associate"]),

        ("dental_surgeon", "Dental Surgeon (BDS / MDS)", "Diagnoses, treats, and prevents oral diseases, performs dental surgeries, and restores teeth.",
         "Performs root canal treatments, extracts impacted teeth, places aesthetic dental crowns, and advises hygiene.",
         ["BDS (Bachelor of Dental Surgery - 5 Yrs) -> MDS (3 Yrs)"], "12th PCB (NEET qualified)",
         [("Dental Anatomy & Histology", 4), ("Conservative Dentistry & Endodontics", 4), ("Oral Surgery & Local Anesthesia", 4), ("Prosthodontics & Crowns", 3), ("Periodontal Therapy", 3)],
         ["Fine Manual Dexterity", "Surgical Hand Stability", "Patient Comfort"], ["medical_doctor", "biomedical_engineer"], ["medical_doctor", "public_health_specialist"])
    ],

    "Business & Finance": [
        ("financial_analyst", "Financial Analyst & Equity Researcher", "Evaluates investment opportunities, builds financial models, and guides capital allocation.",
         "Builds discounted cash flow (DCF) models, analyzes balance sheets, tracks industry trends, and writes memos.",
         ["B.Com (Hons) / BBA Finance", "B.Tech + MBA Finance", "B.Sc Economics"], "12th with Math/Commerce",
         [("Financial Modeling (DCF)", 4), ("Financial Statement Analysis", 4), ("Advanced Excel", 4), ("Corporate Finance", 3), ("Financial Data Platforms", 3)],
         ["Analytical Rigor", "Commercial Skepticism", "Concise Communication"], ["chartered_accountant", "management_consultant"], ["data_analyst", "business_analyst"]),

        ("product_manager", "Product Manager (Tech)", "Guides the success of a digital product, leading cross-functional teams across business, UX, and tech.",
         "Defines product vision and roadmaps, writes PRDs, prioritizes backlogs, and analyzes funnel metrics.",
         ["B.Tech in any branch + MBA", "B.Tech + Product Experience"], "12th Any Stream",
         [("Product Strategy & Roadmapping", 4), ("PRD Writing & Prioritization", 4), ("UX Intuition", 3), ("Product Analytics", 3), ("Technical Literacy", 3)],
         ["Influence Without Authority", "Prioritization", "Communication"], ["ux_designer", "software_engineer"], ["ux_designer", "management_consultant"]),

        ("chartered_accountant", "Chartered Accountant (CA)", "Provides authoritative expertise in auditing, taxation, corporate finance, and compliance.",
         "Audits corporate statements, plans corporate tax strategies, assesses internal controls, and guides restructuring.",
         ["ICAI Program: CA Foundation -> Inter -> Articleship -> Final"], "12th Any Stream",
         [("Auditing Standards & Assurance", 4), ("Taxation (Income Tax, GST)", 4), ("Financial Reporting (Ind AS/IFRS)", 4), ("Corporate Law", 3), ("Forensic Accounting", 3)],
         ["Impeccable Ethics", "Scrupulous Accuracy", "Commercial Judgment"], ["financial_analyst", "corporate_lawyer"], ["financial_analyst", "corporate_lawyer"]),

        ("management_consultant", "Management Consultant", "Advises executive leaders on high-stakes strategy, operational turnaround, and organizational scaling.",
         "Analyzes corporate market share, conducts operational benchmarking, builds financial models, and pitches to C-suites.",
         ["B.Tech / B.Com / Economics -> MBA (IIMs/ISB/Top B-Schools)"], "12th Any Stream",
         [("Structured Problem Solving (MECE)", 4), ("Business Strategy Frameworks", 4), ("Financial & Operational Modeling", 4), ("Executive Presentation", 4), ("Change Management", 3)],
         ["Logical Synthesis", "Executive Gravitas", "Rapid Learning"], ["product_manager", "financial_analyst"], ["product_manager", "corporate_lawyer"]),

        ("investment_banker", "Investment Banking Analyst (M&A)", "Structures mergers, acquisitions, debt issuance, and initial public offerings (IPOs) for corporations.",
         "Builds detailed LBO and merger models, creates pitch decks, conducts financial due diligence, and closes deals.",
         ["B.Com Hons / B.Tech / Economics -> MBA Finance"], "12th with High Math",
         [("M&A Valuation (LBO, Comps, DCF)", 4), ("Financial Accounting Rigor", 4), ("Pitchbook Creation (PowerPoint)", 4), ("Deal Structuring & Due Diligence", 3), ("Capital Markets", 3)],
         ["Extreme Work Ethic", "Grace Under High Pressure", "Commercial Polish"], ["financial_analyst", "corporate_lawyer"], ["financial_analyst", "management_consultant"]),

        ("actuary", "Actuary & Quantitative Risk Analyst", "Uses mathematical and statistical modeling to quantify financial risk for insurance and pensions.",
         "Calculates mortality tables, designs insurance policies, prices catastrophe risk, and manages capital solvency.",
         ["B.Sc / B.Tech Math/Stats -> IAI / IFoA Actuarial Exams"], "12th with High Math",
         [("Actuarial Mathematics & Life Contingencies", 4), ("Probability & Mathematical Statistics", 4), ("Financial Economics & Reserving", 4), ("Risk Modeling in R/Python", 3), ("Insurance Regulations", 3)],
         ["Mathematical Precision", "Patience for Certification", "Ethical Responsibility"], ["quant_analyst", "financial_analyst"], ["data_scientist", "financial_analyst"]),

        ("fintech_product_strategist", "FinTech Product Strategist", "Designs modern payment rails, neo-banking experiences, digital lending, and embedded finance.",
         "Navigates payment gateway APIs, designs fraud prevention rules, and coordinates banking partnerships.",
         ["B.Tech / BBA / B.Com + FinTech Specialization"], "12th with Math/Commerce",
         [("Payment Systems (UPI, Cards, SWIFT)", 4), ("Digital Lending & Underwriting", 4), ("Fintech Regulations (RBI/Central Banks)", 4), ("API Architecture Basics", 3), ("Fraud & Risk Mitigation", 3)],
         ["Regulatory Awareness", "Customer Centricity", "Analytical Fluency"], ["product_manager", "financial_analyst"], ["product_manager", "chartered_accountant"]),

        ("digital_marketer", "Digital Marketing & Growth Strategist", "Plans and executes performance advertising, SEO, social media, and conversion optimization.",
         "Manages Google and Meta ad spend, analyzes CAC and LTV metrics, writes compelling copy, and tests funnels.",
         ["BBA / B.Com / B.A. Mass Comm / B.Tech with Marketing"], "12th Any Stream",
         [("Performance Marketing (Google/Meta Ads)", 4), ("SEO & Content Optimization", 4), ("Analytics & Attribution (GA4)", 4), ("A/B Conversion Rate Optimization", 3), ("Copywriting", 3)],
         ["Data-Informed Creativity", "Agile Adaptability", "Audience Empathy"], ["product_manager", "data_analyst"], ["data_analyst", "technical_writer", "product_designer"])
    ],

    "Law": [
        ("corporate_lawyer", "Corporate & Commercial Lawyer", "Advises businesses on legal rights, commercial contracts, governance, and M&A transactions.",
         "Drafts multi-million dollar contracts, conducts due diligence, and advises boards on corporate compliance.",
         ["5-Year B.A. LL.B. / BBA LL.B. (NLUs)", "3-Year LL.B. after graduation"], "12th Any Stream (CLAT qualified)",
         [("Contract Drafting & Negotiation", 4), ("Companies Law & Compliance", 4), ("Due Diligence Protocols", 3), ("Legal Research & Statutory Interpretation", 4), ("Commercial Dispute Resolution", 3)],
         ["Persuasive Argumentation", "Clause Precision", "Discretion"], ["cyber_lawyer", "chartered_accountant"], ["chartered_accountant", "management_consultant"]),

        ("cyber_lawyer", "Cyber Law & Digital Privacy Attorney", "Specializes in data privacy regulations (DPDP/GDPR), cyber breaches, IP in code, and tech crimes.",
         "Drafts privacy policies, advises on breach disclosure, litigates digital IP disputes, and audits compliance.",
         ["5-Year LL.B. with Cyber Specialization", "LL.B. + Cyber Law Diploma"], "12th Any Stream",
         [("Data Protection Laws (GDPR/DPDP)", 4), ("Cyber Crime Legislation", 4), ("Tech Contracts & Cloud Agreements", 3), ("Digital Evidence Law", 3), ("Basic Cyber Attacks Knowledge", 2)],
         ["Analytical Precision", "Interdisciplinary Communication", "Fast Tech Learning"], ["corporate_lawyer", "digital_forensics_analyst"], ["corporate_lawyer", "cybersecurity_analyst"]),

        ("patent_attorney", "Intellectual Property (IP) Patent Attorney", "Protects scientific discoveries, software algorithms, and industrial designs through patent drafting.",
         "Drafts patent claims, conducts prior art searches, and prosecutes patents before national patent offices.",
         ["B.Tech / B.Sc Science + 3-Year LL.B. (Patent Agent registered)"], "12th with Science",
         [("Patent Claim Drafting", 4), ("Prior Art Search (Google Patents)", 4), ("Patent Law & Prosecution", 4), ("Technical Engineering Literacy", 4), ("IP Litigation Basics", 3)],
         ["Technical Acuity", "Linguistic Precision", "Analytical Thoroughness"], ["corporate_lawyer", "research_scientist"], ["corporate_lawyer", "technical_writer"]),

        ("environmental_lawyer", "Environmental & Climate Lawyer", "Advocates for environmental conservation, sustainable natural resources, and climate justice.",
         "Litigates public interest cases against polluting industries, reviews EIA clearances, and enforces forest laws.",
         ["5-Year B.A. LL.B. / B.Sc LL.B. with Environmental Specialization"], "12th Any Stream",
         [("Environmental Legislation (EPA, Forest Acts)", 4), ("Public Interest Litigation (PIL) Drafting", 4), ("Administrative Law & Tribunal Rules", 4), ("EIA Auditing Review", 3), ("Courtroom Advocacy", 4)],
         ["Moral Conviction", "Courage Under Adversity", "Eloquent Advocacy"], ["corporate_lawyer", "environmental_scientist"], ["environmental_scientist", "human_rights_lawyer"]),

        ("legal_ops_specialist", "Legal Operations & LegalTech Specialist", "Optimizes corporate legal departments using technology, workflow automation, and analytics.",
         "Selects and deploys contract lifecycle management (CLM) software, tracks legal spend, and automates NDAs.",
         ["LL.B. with Tech aptitude", "B.Tech / BBA with Legal Ops background"], "12th Any Stream",
         [("Contract Lifecycle Management (CLM)", 4), ("Legal Workflow Automation", 4), ("Legal Department Analytics", 3), ("Vendor & Spend Management", 3), ("Legal Document Parsing", 3)],
         ["Process Optimization", "Technological Fluency", "Diplomacy"], ["corporate_lawyer", "product_manager"], ["product_manager", "technical_consultant"]),

        ("human_rights_lawyer", "Human Rights & Constitutional Litigator", "Defends fundamental constitutional rights, vulnerable marginalized communities, and civil liberties.",
         "Files writ petitions before High Courts and Supreme Court, represents indigent clients, and drafts policy reform.",
         ["5-Year B.A. LL.B. / 3-Year LL.B."], "12th Any Stream",
         [("Constitutional Law & Jurisprudence", 4), ("Criminal Procedure & Bail Law", 4), ("Writ Petition Drafting", 4), ("Trial Court Advocacy", 4), ("International Human Rights Conventions", 3)],
         ["Fierce Integrity", "Compassion for the Oppressed", "Resilience"], ["corporate_lawyer", "environmental_lawyer"], ["environmental_lawyer", "broadcast_journalist"])
    ],

    "Agriculture": [
        ("precision_agriculture_specialist", "Precision Agriculture Specialist", "Applies IoT sensors, GPS mapping, drone multispectral imagery, and data to optimize crop yields.",
         "Analyzes soil nutrient maps, programs drone flight plans, optimizes drip irrigation, and advises farmers.",
         ["B.Sc Agriculture / Agricultural Engineering", "B.Tech Agri-IT"], "12th with PCB/PCM",
         [("Agronomy & Soil Health", 4), ("GIS & Remote Sensing", 4), ("Agri-IoT Integration", 3), ("Drone Multispectral Imagery", 3), ("Precision Irrigation", 3)],
         ["Field Resilience", "Farmer Empathy", "Practicality"], ["environmental_scientist", "food_technologist"], ["environmental_scientist", "data_analyst"]),

        ("agronomist", "Agronomist & Crop Scientist", "Researches crop genetics, soil fertility, seed hybridization, and sustainable crop rotation strategies.",
         "Conducts randomized agricultural field trials, evaluates drought resistance, and formulates pest management.",
         ["B.Sc Agriculture (4 Yrs) -> M.Sc Agronomy"], "12th with PCB/PCM",
         [("Crop Physiology & Botany", 4), ("Soil Chemistry & Nutrient Management", 4), ("Integrated Pest Management (IPM)", 4), ("Field Trial Experimental Design", 3), ("Agro-meteorology", 3)],
         ["Scientific Patience", "Field Endurance", "Systematic Observation"], ["precision_agriculture_specialist", "biotechnologist"], ["precision_agriculture_specialist", "environmental_scientist"]),

        ("food_technologist", "Food Processing & Quality Technologist", "Develops safe, nutritious packaged foods, establishes food safety standards, and extends shelf-life.",
         "Formulates food recipes, monitors industrial pasteurization/canning lines, and conducts microbial lab assays.",
         ["B.Tech in Food Technology / Food Science", "B.Sc Food Science"], "12th with Science",
         [("Food Microbiology & Safety (FSSAI/HACCP)", 4), ("Food Chemistry & Formulation", 4), ("Thermal & Non-Thermal Processing", 3), ("Sensory Evaluation Techniques", 3), ("Packaging Technology", 3)],
         ["Hygiene Rigor", "Sensory Acuity", "Quality Focus"], ["precision_agriculture_specialist", "biotechnologist"], ["biotechnologist", "chemical_engineer"]),

        ("horticulture_specialist", "Horticulture & Greenhouse Specialist", "Manages intensive cultivation of fruits, vegetables, flowers, and controlled-environment greenhouses.",
         "Monitors climate-controlled hydroponic nutrient solutions, guides pruning/pollination, and plans harvests.",
         ["B.Sc Horticulture (4 Yrs) -> M.Sc Horticulture"], "12th with PCB",
         [("Plant Propagation & Grafting", 4), ("Hydroponics & Vertical Farming", 4), ("Greenhouse Climate Control", 3), ("Post-Harvest Physiology", 3), ("Ornamental Landscaping", 3)],
         ["Observant Nurturing", "Hands-on Practicality", "Aesthetic Eye"], ["agronomist", "precision_agriculture_specialist"], ["agronomist", "environmental_scientist"]),

        ("agricultural_biotechnologist", "Agricultural Biotechnologist", "Engineers disease-resistant, climate-resilient, and bio-fortified crop varieties using molecular biology.",
         "Performs CRISPR gene editing in plant tissue cultures, screens genetic markers, and audits GMO biosafety.",
         ["B.Tech / B.Sc Biotechnology -> M.Sc Plant Biotech"], "12th with PCB",
         [("Plant Molecular Biology & Genetics", 4), ("Plant Tissue Culture Techniques", 4), ("CRISPR & Marker Assisted Selection", 4), ("Biosafety Regulatory Frameworks", 3), ("Bioinformatics", 3)],
         ["Lab Precision", "Curiosity", "Regulatory Responsibility"], ["agronomist", "biotechnologist"], ["biotechnologist", "research_scientist"]),

        ("dairy_livestock_technologist", "Dairy & Livestock Technology Specialist", "Optimizes animal genetics, automated milking parlors, feed nutrition, and hygienic dairy processing.",
         "Formulates balanced feed rations, monitors milk cold chains, and oversees livestock disease prevention.",
         ["B.Tech Dairy Technology / B.V.Sc (Veterinary Science)"], "12th with PCB",
         [("Dairy Chemistry & Processing", 4), ("Animal Nutrition & Genetics", 4), ("Cold Chain Logistics & Quality", 3), ("Livestock Disease Management", 4), ("HACCP Standards", 3)],
         ["Animal Empathy", "Physical Hardiness", "Hygiene Discipline"], ["food_technologist", "agronomist"], ["food_technologist", "veterinarian"])
    ],

    "Environment": [
        ("environmental_scientist", "Environmental Scientist & Impact Assessor", "Monitors ecological systems, analyzes pollution samples, and conducts EIA assessments.",
         "Samples air/water in the field, models pollutant dispersion, drafts EIA reports, and advises industries on greening.",
         ["B.Sc Environmental Science", "B.Tech Environmental Engineering"], "12th with Science",
         [("Environmental Impact Assessment (EIA)", 4), ("Water/Soil/Air Lab Analysis", 4), ("Environmental Regulations", 4), ("GIS for Environmental Modeling", 3), ("Remediation Techniques", 3)],
         ["Scientific Objectivity", "Environmental Ethics", "Report Writing"], ["renewable_energy_engineer", "precision_agriculture_specialist"], ["renewable_energy_engineer", "data_analyst"]),

        ("renewable_energy_engineer", "Renewable Energy & Solar Systems Engineer", "Designs, models, and installs clean energy infrastructure including solar PV, wind, and batteries.",
         "Simulates solar yields in PVsyst, designs electrical balance of plant, inspects inverters, and models grid tie-ins.",
         ["B.Tech in Electrical / Energy Engineering", "B.Tech Renewable Energy"], "12th with PCM",
         [("Solar PV Design (PVsyst)", 4), ("Electrical Single Line Diagrams", 4), ("Grid Integration Basics", 3), ("Battery Energy Storage (BESS)", 3), ("Project Financials (LCOE)", 3)],
         ["Practical Engineering", "Project Management", "Safety"], ["environmental_scientist", "cloud_architect"], ["environmental_scientist", "software_engineer"]),

        ("sustainability_consultant", "Sustainability & ESG Consultant", "Advises corporations on carbon emissions reduction, ESG disclosures, and circular economy roadmaps.",
         "Calculates Scope 1/2/3 greenhouse gas emissions, designs net-zero carbon roadmaps, and drafts sustainability reports.",
         ["B.Tech / B.Sc Environmental Science + MBA", "B.Com + ESG Cert"], "12th Any Stream",
         [("GHG Protocol Carbon Accounting", 4), ("ESG Frameworks (GRI, BRSR, TCFD)", 4), ("Life Cycle Assessment Basics", 3), ("Corporate Net-Zero Roadmapping", 4), ("Stakeholder Reporting", 3)],
         ["Strategic Influence", "Quantitative Accuracy", "Commercial Mindset"], ["environmental_scientist", "management_consultant"], ["management_consultant", "environmental_scientist"]),

        ("gis_analyst", "GIS & Remote Sensing Analyst", "Maps geospatial data, analyzes satellite imagery, and constructs spatial databases for urban and ecological planning.",
         "Processes multispectral satellite bands, conducts spatial joins in ArcGIS/QGIS, and builds interactive map layers.",
         ["B.Sc/B.Tech Geoinformatics / Geography / CS"], "12th with Math/Science",
         [("GIS Software (ArcGIS, QGIS)", 4), ("Remote Sensing & Satellite Imagery", 4), ("Spatial SQL (PostGIS)", 4), ("Python for Geoprocessing (GeoPandas)", 3), ("Cartographic Layouts", 3)],
         ["Spatial Curiosity", "Detail Precision", "Visual Storytelling"], ["environmental_scientist", "data_analyst"], ["data_analyst", "precision_agriculture_specialist"]),

        ("wildlife_biologist", "Wildlife Conservation Biologist", "Studies endangered species habitats, tracks animal population dynamics, and protects national reserves.",
         "Deploys camera traps, tracks wildlife telemetry via GPS collars, models habitat connectivity, and combats poaching.",
         ["B.Sc Zoology / Forestry / Wildlife Biology -> M.Sc Wildlife"], "12th with PCB",
         [("Wildlife Ecology & Field Methods", 4), ("Camera Trap & Telemetry Analysis", 4), ("Biodiversity Conservation Laws", 4), ("Population Viability Modeling", 3), ("Community Forest Relations", 3)],
         ["Extreme Field Endurance", "Love for Wilderness", "Scientific Patience"], ["environmental_scientist", "research_scientist"], ["environmental_scientist", "veterinarian"]),

        ("climate_policy_analyst", "Climate Impact & Adaptation Policy Analyst", "Models future climate risks, analyzes carbon taxation policies, and advises governments on resilience.",
         "Evaluates regional flood/heatwave risk models, analyzes international climate treaty commitments, and writes whitepapers.",
         ["B.A./B.Sc in Economics / Public Policy / Environmental Studies"], "12th Any Stream",
         [("Climate Risk Modeling & IPCC Scenarios", 4), ("Carbon Markets & Pricing Mechanisms", 4), ("Policy Analysis & Whitepaper Drafting", 4), ("Statistical Data Interpretation", 3), ("International Treaties (UNFCCC)", 3)],
         ["Macro Thinking", "Persuasive Writing", "Diplomatic Acumen"], ["environmental_scientist", "corporate_lawyer"], ["corporate_lawyer", "management_consultant"])
    ],

    "Hospitality & Tourism": [
        ("hotel_manager", "Luxury Hotel General Manager", "Leads operational and commercial facets of a luxury resort or hotel, orchestrating guest experience.",
         "Inspects operational standards across rooms and F&B, oversees yield pricing strategies, and manages P&L.",
         ["B.Sc Hospitality & Hotel Administration (NCHMCT)", "BHM"], "12th Any Stream",
         [("Hotel Operations (Rooms, F&B)", 4), ("Revenue Management (RevPAR)", 4), ("PMS Systems (Opera)", 3), ("Luxury Service Standards", 4), ("P&L & Cost Control", 3)],
         ["Exceptional Warmth", "Crisis Composure", "Grooming & Etiquette"], ["event_director", "chef"], ["event_director", "digital_marketer"]),

        ("executive_chef", "Executive Chef & Culinary Director", "Directs restaurant kitchen operations, creates seasonal menus, and masters culinary craftsmanship.",
         "Creates dishes, manages kitchen brigade lines, controls food costs, sources local ingredients, and trains sous chefs.",
         ["Degree in Culinary Arts / Hotel Management", "Apprenticeship"], "12th Any Stream",
         [("Culinary Technique & Menu Development", 4), ("Kitchen Operations & Brigade Management", 4), ("Food Safety & Hygiene (HACCP)", 4), ("Food Costing & Portion Control", 3), ("Flavor Balancing", 4)],
         ["Culinary Passion", "Kitchen Leadership", "Physical Stamina Under Fire"], ["hotel_manager", "food_technologist"], ["hotel_manager", "food_technologist"]),

        ("ecotourism_director", "Ecotourism & Sustainable Travel Director", "Curates low-impact, ecologically respectful travel expeditions that support local indigenous communities.",
         "Designs wilderness itineraries, negotiates community revenue sharing, trains eco-guides, and manages sustainability.",
         ["B.A. / BBA in Tourism Management", "B.Sc Environmental Science"], "12th Any Stream",
         [("Sustainable Tourism Planning", 4), ("Community-Based Tourism Frameworks", 4), ("Wilderness Risk & Safety Protocols", 4), ("Itinerary Costing & Marketing", 3), ("Leave No Trace Ethics", 4)],
         ["Cultural Humility", "Adventure Spirit", "Storytelling"], ["hotel_manager", "wildlife_biologist"], ["wildlife_biologist", "event_director"]),

        ("event_director", "Event & Experience Producer", "Orchestrates large-scale corporate conferences, music festivals, luxury weddings, and brand activations.",
         "Directs stage production logistics, negotiates vendor contracts, oversees live run-of-show cues, and manages budgets.",
         ["BBA Event Management", "B.A. Mass Comm / Public Relations"], "12th Any Stream",
         [("Event Production & Stage Logistics", 4), ("Vendor Sourcing & Budget Management", 4), ("Crowd Safety & Permitting", 4), ("Experiential Brand Design", 3), ("Live Run-of-Show Direction", 4)],
         ["High-Energy Crisis Calm", "Charisma", "Unflappable Organization"], ["hotel_manager", "creative_director_advertising"], ["hotel_manager", "marketing_manager"]),

        ("tourism_analytics_consultant", "Tourism Analytics & Revenue Consultant", "Applies travel demand forecasting, booking telemetry, and passenger flow data to optimize tourism.",
         "Analyzes airline passenger booking curves, models seasonal hotel occupancy demand, and optimizes city tourism spend.",
         ["B.Sc Data Analytics / BBA Tourism + Analytics"], "12th with Math",
         [("Travel Demand Forecasting", 4), ("Revenue Management Algorithms", 4), ("SQL & Tableau for Tourism", 4), ("Global Distribution Systems (GDS)", 3), ("Macro Travel Trends", 3)],
         ["Commercial Numeracy", "Strategic Perspective", "Clarity"], ["hotel_manager", "data_analyst"], ["data_analyst", "financial_analyst"]),

        ("airline_passenger_experience_director", "Aviation Customer Experience Director", "Designs passenger journeys across digital check-in, lounge comfort, in-flight dining, and service.",
         "Evaluates Net Promoter Scores, coordinates with cabin crew training academies, and designs cabin interior amenities.",
         ["BBA Aviation Management", "B.Sc Hospitality + Aviation Cert"], "12th Any Stream",
         [("Aviation Customer Journey Mapping", 4), ("Service Quality Audits & NPS", 4), ("Cabin Amenity & F&B Curation", 3), ("Aviation Safety Protocol Alignment", 4), ("Crew Service Training", 3)],
         ["Global Cultural Polish", "Customer Advocacy", "Diplomacy"], ["hotel_manager", "product_designer"], ["hotel_manager", "ux_designer"])
    ],

    "Education": [
        ("instructional_designer", "Instructional Designer & Learning Architect", "Designs evidence-based digital learning courses, simulations, and corporate upskilling programs.",
         "Conducts learning needs analysis, blueprints curriculum, develops modules in Articulate Storyline, and measures efficacy.",
         ["B.A./B.Sc Education / Psych", "M.A. Instructional Design"], "12th Any Stream",
         [("Instructional Design Models (ADDIE/Bloom)", 4), ("Authoring Tools (Articulate 360)", 4), ("LMS Platforms (Canvas/Moodle)", 3), ("Gamification Design", 3), ("Rubric Construction", 4)],
         ["Pedagogical Empathy", "Clarity", "Storyboarding"], ["teacher", "ux_designer"], ["technical_writer", "ux_designer"]),

        ("stem_educator", "STEM Educator & Curriculum Specialist", "Inspires secondary students in mathematics, physics, robotics, and coding through experiential experiments.",
         "Designs hands-on lab experiments, simplifies complex mathematical formulas, and coaches science olympiad teams.",
         ["B.Sc + B.Ed in Science / Mathematics", "M.Sc in Physics/Math/CS"], "12th with Science",
         [("Pedagogical Subject Mastery", 4), ("Experiential Lab Experiment Design", 4), ("Differentiated Learning Methods", 4), ("Educational Technology Tools", 3), ("Student Assessment", 3)],
         ["Infectious Passion for Science", "Infinite Patience", "Inspirational Encouragement"], ["instructional_designer", "research_scientist"], ["instructional_designer", "research_scientist"]),

        ("higher_ed_researcher", "Higher Education Professor & Researcher", "Conducts original academic research, publishes peer-reviewed journal papers, and teaches university courses.",
         "Writes research grant proposals, mentors Ph.D. dissertations, conducts experiments, and delivers lectures.",
         ["Master's Degree (M.Sc/M.Tech/M.A.) -> Ph.D. in field (UGC NET qualified)"], "12th with high academics",
         [("Scholarly Research Methodology", 4), ("Peer-Reviewed Paper Writing", 4), ("Grant Writing & Funding Acquisition", 4), ("University Lecturing", 4), ("Statistical Data Analysis", 3)],
         ["Deep Intellectual Depth", "Academic Honesty", "Mentorship Warmth"], ["research_scientist", "stem_educator"], ["research_scientist", "data_scientist"]),

        ("edtech_product_specialist", "EdTech Product Specialist", "Aligns pedagogical pedagogy with digital software features to build impactful learning platforms.",
         "Analyzes learner drop-off funnels, designs automated practice quizzes, and tests adaptive learning algorithms.",
         ["B.Tech / B.A. Education + EdTech experience"], "12th Any Stream",
         [("Learning Analytics & Drop-off Telemetry", 4), ("Adaptive Learning Logic", 4), ("EdTech UX Heuristics", 4), ("Teacher & Student Persona Research", 3), ("Curriculum Alignment", 3)],
         ["Learner Empathy", "Analytical Mindset", "Pragmatism"], ["product_manager", "instructional_designer"], ["product_manager", "ux_designer"]),

        ("educational_assessment_specialist", "Educational Assessment & Psychometrics Specialist", "Designs standardized tests, psychometric aptitude scales, and fair grading rubrics.",
         "Analyzes Item Response Theory (IRT) statistics, eliminates test question bias, and establishes test validity.",
         ["M.Sc in Statistics / Psychometrics / Educational Measurement"], "12th with Math",
         [("Item Response Theory (IRT)", 4), ("Standardized Test Construction", 4), ("Test Validity & Reliability Statistics", 4), ("Differential Item Functioning (Bias)", 3), ("Rubric Standardization", 3)],
         ["Mathematical Precision", "Fairness Dedication", "Objective Dispassion"], ["data_analyst", "psychologist"], ["data_analyst", "organizational_psychologist"]),

        ("special_educator", "Special Education Coordinator", "Adapts academic curriculum for neurodiverse children with autism spectrum, ADHD, and sensory processing needs.",
         "Creates individualized education programs (IEPs), applies multi-sensory teaching tools, and fosters inclusive classrooms.",
         ["B.Ed in Special Education (RCI recognized)", "Diploma in Autism/Learning Disabilities"], "12th Any Stream",
         [("Individualized Education Plans (IEP)", 4), ("Multi-Sensory Teaching Techniques", 4), ("Behavioral De-escalation", 4), ("Assistive Learning Technology", 3), ("Parent-Teacher Counseling", 4)],
         ["Boundless Patience", "Deep Protective Love", "Intuitive Perception"], ["child_development_specialist", "stem_educator"], ["child_development_specialist", "counseling_psychologist"])
    ],

    "Skilled/Vocational": [
        ("precision_machinist", "CNC Precision Machining Specialist", "Programs, sets up, and operates multi-axis CNC milling and turning machines for aerospace and medical parts.",
         "Reads blueprints with GD&T tolerances, writes G-code in Mastercam, and measures parts with CMM machines.",
         ["Diploma in Mechanical / Tool & Die", "ITI Machinist Certification"], "10th/12th with Math",
         [("CNC Programming (G-Code)", 4), ("Geometric Dimensioning & Tolerancing (GD&T)", 4), ("Multi-Axis Setup", 4), ("Precision Metrology (CMM)", 3), ("Tooling Feeds/Speeds", 3)],
         ["Extreme Precision", "Safety Rigor", "Patience"], ["industrial_automation_technician", "robotics_engineer"], ["industrial_automation_technician", "mechanical_engineer"]),

        ("industrial_automation_technician", "Industrial Automation & PLC Specialist", "Programs programmable logic controllers (PLCs), industrial robots, and SCADA monitoring screens.",
         "Writes ladder logic for Siemens/Allen Bradley PLCs, wires sensor cabinets, and troubleshoots assembly lines.",
         ["Diploma in Electrical / Mechatronics / Instrumentation"], "10th/12th with Math/Science",
         [("PLC Ladder Logic (Siemens/Rockwell)", 4), ("SCADA & HMI Design", 4), ("Industrial Sensors & Pneumatics", 4), ("Electrical Schematic Debugging", 4), ("Safety Circuits", 3)],
         ["Hands-on Logic", "Safety First", "Fast Troubleshooting"], ["precision_machinist", "robotics_engineer"], ["robotics_engineer", "embedded_engineer"]),

        ("clean_energy_installer", "Solar & Clean Energy Grid Installer", "Installs, wires, tests, and commissions rooftop and utility-scale solar photovoltaic systems.",
         "Mounts rooftop solar racking, wires DC combiner boxes and inverters, connects battery banks, and tests grounding.",
         ["ITI Electrician / Solar Technician Certification", "Diploma Electrical"], "10th/12th with Science",
         [("Solar PV Installation & Wiring", 4), ("DC/AC Inverter Commissioning", 4), ("High Voltage Safety Protocols", 4), ("Battery Storage Connections", 3), ("Grid Interconnection Testing", 3)],
         ["Physical Stamina", "Electrical Caution", "Height Comfort"], ["renewable_energy_engineer", "industrial_automation_technician"], ["renewable_energy_engineer", "electrician"]),

        ("aviation_technician", "Aviation Maintenance Technician (AME)", "Inspects, services, repairs, and certifies airframes, jet engines, and hydraulic systems on commercial aircraft.",
         "Conducts pre-flight mechanical inspections, overhauls jet turbines, tests landing gear actuators, and signs logbooks.",
         ["DGCA / FAA Approved Aircraft Maintenance Engineering (AME) License Course"], "12th with PCM",
         [("Gas Turbine Engines Overhaul", 4), ("Aircraft Hydraulics & Airframes", 4), ("Aviation Safety Regulations", 4), ("Non-Destructive Testing (NDT)", 3), ("Maintenance Log Certification", 4)],
         ["Zero-Defect Mindset", "Immense Responsibility", "Technical Discipline"], ["aerospace_engineer", "precision_machinist"], ["aerospace_engineer", "mechanical_engineer"]),

        ("welding_inspector", "Advanced Metallurgy & NDT Welding Inspector", "Inspects structural welds on oil pipelines, high-speed rail tracks, and nuclear pressure vessels.",
         "Performs ultrasonic testing (UT), radiographic X-ray weld inspection, and ensures structural integrity.",
         ["Diploma in Mechanical / Metallurgy + NDT Level II/III Cert"], "12th with Science",
         [("Ultrasonic & Radiographic Testing (NDT)", 4), ("Metallurgy & Welding Codes (ASME/AWS)", 4), ("Defect Identification (Porosity/Cracks)", 4), ("Pressure Vessel Inspection", 3), ("Inspection Reporting", 4)],
         ["Integrity Under Commercial Pressure", "Sharp Visual Observation", "Discipline"], ["precision_machinist", "aerospace_engineer"], ["civil_engineer", "mechanical_engineer"]),

        ("medical_device_technician", "Medical Device Maintenance Specialist", "Services, calibrates, sterilizes, and tests intensive care hospital equipment.",
         "Calibrates dialysis machines, replaces ventilator oxygen sensors, and tests defibrillator discharge energy.",
         ["Diploma in Biomedical / Electronics", "ITI Medical Electronics"], "12th with Science",
         [("Biomedical Equipment Calibration", 4), ("Sterilization & Biohazard Safety", 4), ("Electrical Safety Testing (IEC)", 4), ("Preventive Maintenance Scheduling", 3), ("Hospital Work Order Systems", 3)],
         ["Meticulous Care", "Hospital Etiquette", "Technical Readiness"], ["biomedical_engineer", "industrial_automation_technician"], ["biomedical_engineer", "hospital_administrator"])
    ],

    "Emerging Careers": [
        ("prompt_workflow_engineer", "AI Workflow & Agentic Systems Engineer", "Architects multi-agent autonomous LLM workflows, evaluation pipelines, and context-augmented RAG.",
         "Builds stateful agent graphs in LangGraph, evaluates prompt reliability with automated benchmarks, and optimizes vector RAG.",
         ["B.Tech CS / Software Engineering", "Self-Taught Portfolio"], "12th with PCM",
         [("Agentic Frameworks (LangGraph)", 4), ("Prompt Engineering & Guardrails", 4), ("RAG & Vector Databases", 4), ("Python & Async APIs (FastAPI)", 3), ("LLM Evaluation Benchmarks", 3)],
         ["Systems Architecture", "Empirical Experimentation", "Clarity"], ["ai_engineer", "software_engineer"], ["software_engineer", "ai_engineer"]),

        ("space_systems_specialist", "Space Mission & Satellite Operations Specialist", "Monitors orbital satellite telemetry, plans ground station passes, and commands spacecraft systems.",
         "Tracks orbital decay, uploads telemetry commands to satellites, and coordinates deep space communication passes.",
         ["B.Tech Aerospace / ECE / CS", "MS in Space Operations"], "12th with PCM",
         [("Orbital Mechanics & Telemetry", 4), ("Satellite Ground Station Protocols", 4), ("Radio Frequency & Uplink/Downlink", 4), ("Spacecraft Subsystem Health", 3), ("Emergency Safe Mode Recovery", 3)],
         ["Calm Under High Stakes", "Astronautical Fascination", "Precision"], ["aerospace_engineer", "iot_solutions_architect"], ["aerospace_engineer", "embedded_engineer"]),

        ("synthetic_biology_engineer", "Synthetic Biology & Biofabrication Engineer", "Designs programmable genetic circuits, lab-grown cultured materials, and engineered micro-organisms.",
         "Codes synthetic DNA sequences, clones plasmids into bacterial hosts, and tests bioreactor fermentation yields.",
         ["B.Tech / B.Sc Biotechnology -> MS Synthetic Biology / Bioengineering"], "12th with Science (Biology & Math)",
         [("Genetic Circuit Design (CRISPR/BioBricks)", 4), ("DNA Assembly & Cloning", 4), ("Bioreactor Fermentation", 3), ("Metabolic Engineering", 4), ("Bioethics & Biosecurity", 3)],
         ["Biological Imagination", "Meticulous Sterile Discipline", "Ethical Humility"], ["agricultural_biotechnologist", "biomedical_engineer"], ["biotechnologist", "chemical_engineer"]),

        ("autonomous_vehicle_architect", "Autonomous Vehicle Systems Architect", "Integrates perception, path planning, sensor fusion, and drive-by-wire controls for self-driving vehicles.",
         "Designs camera-radar-LiDAR sensor suites, develops trajectory prediction, and validates fail-safe braking.",
         ["B.Tech in Mechatronics / CS / Automotive", "MS Autonomous Systems"], "12th with PCM",
         [("Sensor Fusion (LiDAR, Radar, Cameras)", 4), ("Path Planning & Trajectory Generation", 4), ("Drive-by-Wire Automotive Architecture", 4), ("Safety Standards (ISO 26262)", 4), ("Simulation in CARLA", 3)],
         ["Zero-Tolerance Safety", "Deep Systems Thinking", "Resilience"], ["robotics_engineer", "embedded_engineer"], ["robotics_engineer", "ai_engineer"]),

        ("smart_city_planner", "Smart City Infrastructure Planner", "Designs data-driven urban transportation, IoT utility grids, digital twins, and sustainable zoning.",
         "Models city traffic congestion using digital twins, plans EV charging grid hubs, and optimizes smart water management.",
         ["B.Plan / B.Arch -> Master in Urban Planning / Smart Cities"], "12th Any Stream with Math",
         [("Urban Planning & Zoning Regulations", 4), ("City Digital Twins & GIS Modeling", 4), ("Smart Grid & EV Infrastructure Planning", 3), ("Civic Data Analytics", 3), ("Citizen Engagement", 3)],
         ["Civic Empathy", "Long-Horizon Vision", "Multi-Agency Diplomacy"], ["environmental_scientist", "gis_analyst"], ["civil_engineer", "architect"]),

        ("spatial_experience_developer", "AR/VR Spatial Computing Developer", "Builds immersive 3D virtual environments, interactive augmented reality apps, and spatial interfaces.",
         "Develops interactive 3D mechanics in Unity/Unreal Engine, integrates eye/hand tracking, and optimizes frame rates.",
         ["B.Tech in CS / Game Development", "B.Des Digital Media"], "12th with PCM/Math",
         [("Game Engines (Unity / Unreal Engine 5)", 4), ("3D Math (Vectors, Quaternions, Transforms)", 4), ("Spatial UI & Hand/Eye Tracking", 4), ("Shader Programming (HLSL)", 3), ("VR Performance Optimization", 3)],
         ["Spatial Imagination", "Playful Curiosity", "Motion Sensitivity"], ["game_designer", "interaction_designer"], ["software_engineer", "game_designer"]),

        ("neurotechnology_engineer", "Neurotechnology & BCI Systems Engineer", "Designs Brain-Computer Interfaces (BCIs) translating neural electrical signals into digital actions.",
         "Processes multi-channel EEG/EMG signals, applies machine learning decoders to intended movements, and tests neuro-prosthetics.",
         ["B.Tech in Biomedical / ECE / CS -> MS in Neuroengineering"], "12th with Science & Math",
         [("Biosignal Processing (EEG, Spike Sorting)", 4), ("Machine Learning for Neural Decoding", 4), ("Electrode Interface & Bio-Amplifiers", 4), ("Real-time Low-Latency C++", 3), ("Neural Ethics", 4)],
         ["Frontier Curiosity", "Interdisciplinary Synthesis", "Patient Care"], ["biomedical_engineer", "embedded_engineer"], ["biomedical_engineer", "ai_engineer"])
    ]
}

def generate_all_careers():
    careers_list = []
    total_count = 0
    
    for domain, careers in DOMAINS_DATA.items():
        for item in careers:
            cid, name, desc, work, edu, elig, req_skills, soft, rel, alt = item
            
            skills_formatted = [
                {"skill": s[0], "level": s[1], "importance": "Critical" if s[1] >= 4 else "High"}
                for s in req_skills
            ]
            
            career_obj = {
                "career_id": cid,
                "career_name": name,
                "domain": domain,
                "description": desc,
                "typical_work": work,
                "education_paths": edu,
                "eligibility": elig,
                "required_skills": skills_formatted,
                "soft_skills": soft,
                "related_careers": rel,
                "alternative_careers": alt,
                "adjacent_careers": [c for c in rel if c != cid],
                "entry_level_roles": [f"Junior {name}", f"Associate {name}", f"Trainee in {domain}"],
                "higher_study_options": [f"Master's Degree in {domain}", f"Executive Specialization in {name}"],
                "certifications": [f"Industry Certified {name}", f"Professional {domain} Practitioner"],
                "projects": [f"End-to-end practical capstone project solving real-world {domain} problem", f"Portfolio proof of work demonstration in {name}"],
                "portfolio_requirements": ["Public project demonstration repository / case study document", "Verified skill assessment milestone badge"],
                "internship_options": [f"6-month industrial internship at recognized {domain} enterprise or research institute"],
                "future_skills": [f"AI-assisted tools in {domain}", f"Cross-disciplinary integration with modern digital platforms"],
                "technology_changes": f"Rapid adoption of automation, AI-assisted tooling, and cloud-native workflows transforming routine manual tasks in {domain}.",
                "AI_impact": {
                    "automated_tasks": ["Routine documentation and boilerplate syntax", "Standardized baseline metric tracking", "Repetitive data entry and initial sorting"],
                    "augmented_tasks": ["Accelerated scenario simulation and hypothesis testing", "Context-aware synthesis across large information sets", "Anomaly and pattern detection in complex systems"],
                    "human_skills": ["High-stakes ethical and strategic judgment", "Authentic human empathy and cross-stakeholder negotiation", "Unprecedented creative vision and novel problem framing"]
                },
                "pathway": f"12th / Intermediate ({elig}) -> {edu[0]} -> Trainee / Junior {name} -> Senior {name} -> Domain Lead / Specialist",
                "sources": ["Bureau of Labor Statistics (BLS)", f"National {domain} Council", "IEEE Career & Education Repository"]
            }
            careers_list.append(career_obj)
            total_count += 1

    os.makedirs("data/careers", exist_ok=True)
    out_path = "data/careers/careers.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(careers_list, f, indent=2, ensure_ascii=False)
    
    print(f"SUCCESS: Generated {total_count} careers across {len(DOMAINS_DATA)} domains in {out_path}!")

if __name__ == "__main__":
    generate_all_careers()
