# scripts/build_knowledge_base.py
import json
import os

CAREERS = [
    # 1. Engineering & Technology
    {
        "career_id": "software_engineer",
        "career_name": "Software Engineer",
        "domain": "Engineering & Technology",
        "description": "Designs, develops, tests, and maintains scalable software applications, systems, and digital platforms.",
        "typical_work": "Writes clean code, architectures microservices, reviews pull requests, debugs distributed systems, and collaborates with product teams.",
        "education_paths": ["B.Tech / B.E. in Computer Science or Information Technology", "BCA / MCA", "B.Sc in Computer Science"],
        "eligibility": "12th / PUC with Physics, Mathematics, and Chemistry/CS with minimum 55-60%.",
        "required_skills": [
            {"skill": "Data Structures & Algorithms", "level": 4, "importance": "High"},
            {"skill": "Programming (Python, Java, or C++)", "level": 4, "importance": "Critical"},
            {"skill": "System Design", "level": 3, "importance": "High"},
            {"skill": "Database Management (SQL/NoSQL)", "level": 3, "importance": "Medium"},
            {"skill": "Git & CI/CD", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Problem Solving", "Analytical Thinking", "Team Collaboration", "Continuous Learning"],
        "related_careers": ["cloud_architect", "devops_engineer", "embedded_engineer"],
        "alternative_careers": ["product_manager", "technical_writer", "data_analyst", "ux_designer"],
        "adjacent_careers": ["qa_automation_engineer", "systems_analyst"],
        "entry_level_roles": ["Junior Software Developer", "Associate Software Engineer", "Graduate Software Trainee"],
        "higher_study_options": ["M.Tech in Software Engineering / Distributed Systems", "MS in Computer Science", "MBA in Technology Management"],
        "certifications": ["AWS Certified Developer Associate", "Oracle Certified Professional Java"],
        "projects": ["Build a Full-Stack Task & Collaboration App", "Implement a High-Throughput REST/GraphQL API with Caching"],
        "portfolio_requirements": ["Active GitHub repository with clean commits", "Deployed web or mobile application demo"],
        "internship_options": ["Summer Software Engineering Internships at tech startups or product enterprises"],
        "future_skills": ["AI-assisted pair programming", "Cloud-native microservices", "Security by design", "LLM integration"],
        "technology_changes": "Transitioning from manual boilerplate writing to AI-augmented coding, automated unit testing, and serverless microservices.",
        "AI_impact": {
            "automated_tasks": ["Boilerplate syntax generation", "Basic unit test writing", "Routine bug triage"],
            "augmented_tasks": ["System architecture design", "Code refactoring", "Performance profiling"],
            "human_skills": ["Architectural trade-off decisions", "High-stakes security judgment", "Cross-functional stakeholder alignment"]
        },
        "pathway": "12th Science (PCM) -> B.Tech in CS/IT (4 Yrs) -> Software Engineering Intern -> Associate Software Engineer -> Senior Software Engineer -> Engineering Lead / Architect",
        "sources": ["Bureau of Labor Statistics (BLS)", "IEEE Computer Society Career Guidance", "NASSCOM Tech Sector Insights"]
    },
    {
        "career_id": "cloud_architect",
        "career_name": "Cloud Solutions Architect",
        "domain": "Engineering & Technology",
        "description": "Designs and oversees enterprise cloud computing strategies, infrastructure security, migration, and resilient architectures.",
        "typical_work": "Architects multi-cloud solutions, designs disaster recovery plans, optimizes cloud cost, and defines deployment governance.",
        "education_paths": ["B.Tech in Computer Science / IT / Electronics", "B.Sc Computer Science + Cloud Certifications"],
        "eligibility": "12th / PUC with Mathematics and Physics.",
        "required_skills": [
            {"skill": "Cloud Platforms (AWS, Azure, GCP)", "level": 4, "importance": "Critical"},
            {"skill": "Networking & Security", "level": 4, "importance": "High"},
            {"skill": "Infrastructure as Code (Terraform)", "level": 3, "importance": "High"},
            {"skill": "Containerization (Docker & Kubernetes)", "level": 3, "importance": "High"},
            {"skill": "Distributed Systems", "level": 4, "importance": "High"}
        ],
        "soft_skills": ["Strategic Planning", "Client Communication", "Risk Management"],
        "related_careers": ["software_engineer", "devops_engineer", "cloud_security_architect"],
        "alternative_careers": ["technical_consultant", "devops_engineer", "data_engineer"],
        "adjacent_careers": ["Site Reliability Engineer (SRE)", "Infrastructure Engineer"],
        "entry_level_roles": ["Cloud Support Associate", "Junior DevOps Specialist", "Infrastructure Trainee"],
        "higher_study_options": ["M.Tech in Cloud Computing", "MS in Network Architecture"],
        "certifications": ["AWS Certified Solutions Architect", "Google Professional Cloud Architect"],
        "projects": ["Multi-tier resilient application deployment on AWS with auto-scaling and CDN", "Zero-downtime database migration architecture"],
        "portfolio_requirements": ["Infrastructure-as-Code Terraform repositories", "Architecture diagrams & SLA whitepapers"],
        "internship_options": ["Cloud operations and infrastructure internships at MSPs or enterprise tech firms"],
        "future_skills": ["Multi-cloud AI workload orchestration", "FinOps cost optimization", "Zero-trust network architecture"],
        "technology_changes": "Shift from on-premise data centers to serverless containers, edge computing, and AI-optimized cloud fabrics.",
        "AI_impact": {
            "automated_tasks": ["Routine server provisioning", "Basic log alerting", "Static resource rightsizing"],
            "augmented_tasks": ["Autonomous incident resolution", "Predictive traffic scaling", "Cloud cost anomaly detection"],
            "human_skills": ["Disaster recovery strategy", "Regulatory compliance design", "Vendor negotiation"]
        },
        "pathway": "12th Science (PCM) -> B.Tech in CS/ECE (4 Yrs) -> Cloud Systems Engineer (2-3 Yrs) -> Cloud Solutions Architect",
        "sources": ["IEEE Cloud Computing Magazine", "AWS Architecture Center", "Gartner Cloud Infrastructure Reports"]
    },
    {
        "career_id": "devops_engineer",
        "career_name": "DevOps & Platform Engineer",
        "domain": "Engineering & Technology",
        "description": "Bridges software development and IT operations by building continuous delivery pipelines and resilient deployment platforms.",
        "typical_work": "Maintains CI/CD pipelines, monitors server health, manages container clusters, and implements automated configuration management.",
        "education_paths": ["B.Tech / B.E. in CS/IT/ECE", "BCA + DevOps Diploma"],
        "eligibility": "12th / PUC with Mathematics and Science stream.",
        "required_skills": [
            {"skill": "Linux & Shell Scripting", "level": 4, "importance": "Critical"},
            {"skill": "CI/CD (GitHub Actions, Jenkins)", "level": 4, "importance": "Critical"},
            {"skill": "Docker & Kubernetes", "level": 4, "importance": "High"},
            {"skill": "Monitoring (Prometheus, Grafana)", "level": 3, "importance": "Medium"},
            {"skill": "Cloud Infrastructure", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Incident Communication", "Fast Troubleshooting", "Collaboration"],
        "related_careers": ["software_engineer", "cloud_architect", "cloud_security_architect"],
        "alternative_careers": ["software_engineer", "technical_consultant", "database_administrator"],
        "adjacent_careers": ["Site Reliability Engineer", "Platform Engineer", "Build & Release Engineer"],
        "entry_level_roles": ["Junior DevOps Engineer", "Build Engineer Trainee", "Linux System Administrator"],
        "higher_study_options": ["MS in Information Technology", "Executive M.Tech in Platform Engineering"],
        "certifications": ["Certified Kubernetes Administrator (CKA)", "HashiCorp Certified Terraform Associate"],
        "projects": ["Automated CI/CD pipeline building, testing, and deploying Docker containers to Kubernetes", "Centralized logging stack with ELK/Loki"],
        "portfolio_requirements": ["Public Git workflows showcasing automated CI/CD and deployment scripts"],
        "internship_options": ["Platform engineering and systems operations internships"],
        "future_skills": ["GitOps", "AIOps autonomous anomaly remediation", "Software supply chain security (SLSA)"],
        "technology_changes": "Evolution toward internal developer platforms (IDPs), automated platform engineering, and AI-driven telemetry diagnostics.",
        "AI_impact": {
            "automated_tasks": ["Routine pipeline linting", "Log pattern clustering", "Metric threshold alerting"],
            "augmented_tasks": ["Root cause diagnosis", "Canary deployment validation", "Capacity planning"],
            "human_skills": ["High-severity outage coordination", "Infrastructure security posture", "Developer experience strategy"]
        },
        "pathway": "12th Science -> B.Tech (4 Yrs) -> Junior Systems Engineer -> DevOps Engineer -> Platform Engineering Lead",
        "sources": ["State of DevOps Report (DORA)", "Linux Foundation Education", "CNCF Landscape"]
    },
    {
        "career_id": "embedded_engineer",
        "career_name": "Embedded Systems Engineer",
        "domain": "Engineering & Technology",
        "description": "Designs low-level firmware and hardware-integrated software for microcontrollers, automotive systems, IoT devices, and medical hardware.",
        "typical_work": "Programs microcontrollers in C/Embedded C, interfaces sensors and actuators, writes device drivers, and debugs with oscilloscopes.",
        "education_paths": ["B.Tech in Electronics & Communication (ECE)", "B.Tech in Electrical / Mechatronics", "B.Tech in Computer Science"],
        "eligibility": "12th / PUC with Physics and Mathematics.",
        "required_skills": [
            {"skill": "Embedded C / C++", "level": 4, "importance": "Critical"},
            {"skill": "Microcontrollers (ARM, ESP32, STM32)", "level": 4, "importance": "Critical"},
            {"skill": "Hardware Communication Protocols (I2C, SPI, UART, CAN)", "level": 3, "importance": "High"},
            {"skill": "RTOS (FreeRTOS / Zephyr)", "level": 3, "importance": "High"},
            {"skill": "Circuit Debugging & Hardware Basics", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Rigorous Attention to Detail", "Hands-on Debugging", "Patience"],
        "related_careers": ["robotics_engineer", "iot_solutions_architect", "aerospace_engineer"],
        "alternative_careers": ["software_engineer", "electrical_engineer", "qa_automation_engineer"],
        "adjacent_careers": ["Firmware Engineer", "Hardware Test Engineer", "SoC Validation Engineer"],
        "entry_level_roles": ["Graduate Trainee Engineer - Firmware", "Junior Embedded Developer"],
        "higher_study_options": ["M.Tech in Embedded Systems / VLSI Design", "MS in Microelectronics"],
        "certifications": ["ARM Accredited Engineer", "Embedded Linux Development (Linux Foundation)"],
        "projects": ["Build an RTOS-based environmental monitoring node with ESP32 and MQTT", "Implement a CAN bus vehicle telemetry simulator"],
        "portfolio_requirements": ["Hardware project demonstration videos", "GitHub repositories of driver code and schematics"],
        "internship_options": ["Hardware/firmware R&D internships at automotive or consumer electronics companies"],
        "future_skills": ["Edge TinyML execution", "Rust for embedded systems", "Hardware cybersecurity & secure boot"],
        "technology_changes": "Integration of low-power on-device machine learning (TinyML) and memory-safe languages like Rust on microcontrollers.",
        "AI_impact": {
            "automated_tasks": ["Register mapping boilerplate", "Basic pinout configuration code"],
            "augmented_tasks": ["Firmware static analysis", "Timing closure analysis", "Power consumption optimization"],
            "human_skills": ["Physical board debugging with logic analyzers", "Strict safety-critical certification (ISO 26262)"]
        },
        "pathway": "12th Science (PCM) -> B.Tech ECE/EEE (4 Yrs) -> Firmware Trainee -> Embedded Systems Engineer -> Lead Systems Architect",
        "sources": ["IEEE Transactions on Embedded Computing", "Embedded.com Industry Survey", "ARM Developer Community"]
    },
    {
        "career_id": "robotics_engineer",
        "career_name": "Robotics Systems Engineer",
        "domain": "Engineering & Technology",
        "description": "Integrates mechanical design, electronic sensing, and intelligent control software to construct autonomous robotic systems.",
        "typical_work": "Develops robot kinematics and dynamics algorithms, integrates LiDAR/cameras using ROS, programs manipulators, and tests robot autonomy.",
        "education_paths": ["B.Tech in Robotics & Automation", "B.Tech in Mechatronics", "B.Tech in Mechanical / ECE / CS"],
        "eligibility": "12th / PUC with Mathematics and Physics (min 60%).",
        "required_skills": [
            {"skill": "ROS / ROS2 (Robot Operating System)", "level": 4, "importance": "Critical"},
            {"skill": "C++ & Python", "level": 4, "importance": "Critical"},
            {"skill": "Robot Kinematics & Control Theory", "level": 4, "importance": "High"},
            {"skill": "Computer Vision for Robotics", "level": 3, "importance": "High"},
            {"skill": "Sensor Fusion (LiDAR, IMU, SLAM)", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Interdisciplinary Collaboration", "Creative Problem Solving", "Safety Orientation"],
        "related_careers": ["embedded_engineer", "ai_engineer", "aerospace_engineer"],
        "alternative_careers": ["autonomous_vehicle_architect", "mechanical_engineer", "simulation_engineer"],
        "adjacent_careers": ["Automation Engineer", "Mechatronics Specialist", "Field Robotics Engineer"],
        "entry_level_roles": ["Associate Robotics Engineer", "Robotics Software Trainee", "Automation Specialist"],
        "higher_study_options": ["M.Tech / MS in Robotics", "Ph.D. in Autonomous Systems"],
        "certifications": ["ROS Developer Certification", "Industrial Robot Programming (KUKA / Fanuc)"],
        "projects": ["Build an autonomous indoor mobile robot navigating using ROS2 SLAM and LiDAR", "Simulate a 6-DOF robotic arm pick-and-place task in Gazebo"],
        "portfolio_requirements": ["Video demonstration of real or simulated autonomous robot tasks", "Clean C++/ROS code repository"],
        "internship_options": ["Robotics research labs, warehouse automation firms, and drone technology startups"],
        "future_skills": ["Reinforcement learning for manipulation", "Human-Robot Collaboration (Cobots)", "Swarm robotics"],
        "technology_changes": "Transitioning from rigid industrial programmed arms to perception-rich, learning-based autonomous mobile robots (AMRs).",
        "AI_impact": {
            "automated_tasks": ["Basic path interpolation", "Standard sensor calibration routines"],
            "augmented_tasks": ["Trajectory optimization", "Obstacle avoidance in dynamic environments", "Inverse kinematics solving"],
            "human_skills": ["Physical safety validation in shared human workspaces", "Multi-disciplinary mechanical-electrical integration"]
        },
        "pathway": "12th PCM -> B.Tech Mechatronics/Robotics/CS (4 Yrs) -> Robotics R&D Intern -> Robotics Engineer -> Principal Autonomy Engineer",
        "sources": ["IEEE Robotics and Automation Society (RAS)", "Robotics Business Review", "International Federation of Robotics (IFR)"]
    },
    {
        "career_id": "aerospace_engineer",
        "career_name": "Aerospace & Avionics Engineer",
        "domain": "Engineering & Technology",
        "description": "Designs, analyzes, and tests aircraft, spacecraft, satellites, and airborne defense systems.",
        "typical_work": "Conducts CFD aerodynamic simulations, designs avionics flight controllers, performs structural stress analysis, and participates in wind tunnel tests.",
        "education_paths": ["B.Tech in Aerospace Engineering", "B.Tech in Aeronautical Engineering", "B.Tech in Mechanical Engineering"],
        "eligibility": "12th / PUC with Physics, Mathematics, and Chemistry with high marks.",
        "required_skills": [
            {"skill": "Aerodynamics & Propulsion Basics", "level": 4, "importance": "Critical"},
            {"skill": "CAD & CFD Tools (ANSYS, SolidWorks)", "level": 4, "importance": "Critical"},
            {"skill": "Flight Dynamics & Control", "level": 3, "importance": "High"},
            {"skill": "Materials & Structural Mechanics", "level": 3, "importance": "High"},
            {"skill": "MATLAB / Simulink", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Extreme Precision", "High Safety Standards", "Teamwork"],
        "related_careers": ["robotics_engineer", "embedded_engineer", "space_systems_specialist"],
        "alternative_careers": ["mechanical_engineer", "automotive_engineer", "renewable_energy_engineer"],
        "adjacent_careers": ["Flight Test Engineer", "Avionics Specialist", "Payload Integration Engineer"],
        "entry_level_roles": ["Graduate Engineer Trainee - Aerodynamics", "Junior Avionics Engineer", "Structural Analyst"],
        "higher_study_options": ["M.Tech in Aerospace Engineering", "MS in Space Technology / Astrodynamics"],
        "certifications": ["CATIA Mechanical Designer", "ANSYS Mechanical Certificate"],
        "projects": ["Design and aerodynamic CFD analysis of a high-lift UAV airfoil", "Simulate spacecraft orbital insertion trajectory using MATLAB"],
        "portfolio_requirements": ["Engineering calculation notebooks, CAD renderings, and simulation validation reports"],
        "internship_options": ["ISRO / DRDO student internships, civil aviation MRO facilities, and private space startups"],
        "future_skills": ["Sustainable aviation (electric & hydrogen propulsion)", "Hypersonic flight simulation", "Autonomous drone traffic management"],
        "technology_changes": "Adoption of generative design for lightweight composites, electric vertical takeoff (eVTOL), and commercial private space systems.",
        "AI_impact": {
            "automated_tasks": ["Standard mesh generation in CFD", "Preliminary parameter checks"],
            "augmented_tasks": ["Aerodynamic shape optimization via generative models", "Predictive structural health monitoring"],
            "human_skills": ["High-stakes flight safety certification (FAA/DGCA)", "Mission-critical go/no-go decisions"]
        },
        "pathway": "12th Science (PCM) -> B.Tech Aerospace/Mechanical (4 Yrs) -> Aerospace Systems Trainee -> Flight/Systems Engineer -> Aerospace Specialist",
        "sources": ["AIAA (American Institute of Aeronautics and Astronautics)", "ISRO Technical Bulletins", "Royal Aeronautical Society"]
    },

    # 2. AI & Data
    {
        "career_id": "ai_engineer",
        "career_name": "AI & Machine Learning Engineer",
        "domain": "AI & Data",
        "description": "Designs, trains, and operationalizes machine learning and deep learning models to solve complex predictive and generative tasks.",
        "typical_work": "Builds neural network architectures, fine-tunes large foundation models, optimizes model latency for production, and validates metrics.",
        "education_paths": ["B.Tech in Artificial Intelligence / Data Science", "B.Tech in Computer Science", "MS / M.Tech in AI"],
        "eligibility": "12th / PUC with Mathematics and Computer Science/Physics.",
        "required_skills": [
            {"skill": "Mathematics (Linear Algebra, Calculus, Probability)", "level": 4, "importance": "Critical"},
            {"skill": "Python & PyTorch / TensorFlow", "level": 4, "importance": "Critical"},
            {"skill": "Deep Learning & Transformer Architectures", "level": 4, "importance": "High"},
            {"skill": "Model Deployment & ONNX / TensorRT", "level": 3, "importance": "High"},
            {"skill": "Data Preprocessing & Feature Engineering", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Curiosity", "Scientific Rigor", "Ethics in AI", "Communication"],
        "related_careers": ["data_scientist", "data_analyst", "computer_vision_engineer"],
        "alternative_careers": ["software_engineer", "data_analyst", "quantitative_analyst", "product_manager"],
        "adjacent_careers": ["MLOps Engineer", "Applied AI Researcher", "NLP Engineer"],
        "entry_level_roles": ["Associate Machine Learning Engineer", "AI Developer Trainee", "Data Science Associate"],
        "higher_study_options": ["M.Tech / MS in Machine Learning", "Ph.D. in Computer Science (Artificial Intelligence)"],
        "certifications": ["TensorFlow Developer Certificate", "AWS Certified Machine Learning - Specialty"],
        "projects": ["Fine-tune an open-source LLM on custom domain data with LoRA and deploy via vLLM", "Train a multi-modal image-text retrieval system with PyTorch"],
        "portfolio_requirements": ["Clean PyTorch model code on GitHub", "HuggingFace model demo or benchmark paper replication"],
        "internship_options": ["AI R&D labs, consumer tech companies, and enterprise AI consulting groups"],
        "future_skills": ["Agentic AI workflows (LangGraph)", "Efficient model distillation & quantization", "Responsible AI & alignment"],
        "technology_changes": "Rapid shift from training small custom models from scratch to foundation model adaptation, retrieval augmentation (RAG), and agent systems.",
        "AI_impact": {
            "automated_tasks": ["Hyperparameter grid sweeps", "Basic data cleansing scripts", "Standard code formatting"],
            "augmented_tasks": ["Model architecture search", "Error analysis and synthetic data generation", "Inference benchmarking"],
            "human_skills": ["Data ethics and bias mitigation", "Formulating real-world business problems into tractable ML formulations", "AI safety governance"]
        },
        "pathway": "12th Science (PCM) -> B.Tech CS/AI (4 Yrs) -> ML Research Intern -> ML Engineer -> Staff AI Engineer / Research Lead",
        "sources": ["IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)", "NeurIPS Proceedings", "AI Now Institute"]
    },
    {
        "career_id": "data_scientist",
        "career_name": "Data Scientist",
        "domain": "AI & Data",
        "description": "Extracts actionable insights and builds predictive statistical models from massive, unstructured, and multi-modal datasets.",
        "typical_work": "Formulates statistical hypotheses, cleans complex data, builds regression/classification models, and communicates findings to executive leaders.",
        "education_paths": ["B.Sc / M.Sc in Statistics or Mathematics", "B.Tech in Data Science / Computer Science", "BS in Data Science"],
        "eligibility": "12th / PUC with high proficiency in Mathematics / Statistics.",
        "required_skills": [
            {"skill": "Applied Statistics & Hypothesis Testing", "level": 4, "importance": "Critical"},
            {"skill": "Python & Data Science Libraries (Pandas, NumPy, Scikit-Learn)", "level": 4, "importance": "Critical"},
            {"skill": "SQL & Relational Databases", "level": 4, "importance": "High"},
            {"skill": "Exploratory Data Analysis (EDA)", "level": 4, "importance": "High"},
            {"skill": "Machine Learning Algorithms", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Data Storytelling", "Business Acumen", "Critical Thinking"],
        "related_careers": ["ai_engineer", "data_analyst", "bi_developer"],
        "alternative_careers": ["data_analyst", "quantitative_analyst", "economist", "product_manager"],
        "adjacent_careers": ["Statistician", "Decision Scientist", "Market Research Analyst"],
        "entry_level_roles": ["Junior Data Scientist", "Associate Quantitative Analyst", "Graduate Data Analyst"],
        "higher_study_options": ["M.Sc in Data Science & Analytics", "Ph.D. in Computational Statistics"],
        "certifications": ["IBM Certified Data Scientist", "Google Professional Data Engineer"],
        "projects": ["Customer churn predictive model with full interpretability analysis (SHAP/LIME)", "End-to-end time series demand forecasting engine"],
        "portfolio_requirements": ["Kaggle notebook contributions with detailed documentation", "GitHub repository showcasing clear data narratives"],
        "internship_options": ["Data science internships in e-commerce, banking, healthcare analytics, and marketing agencies"],
        "future_skills": ["Causal inference in business experimentation", "Graph neural networks for relationship analysis", "AI governance"],
        "technology_changes": "Moving beyond descriptive charts toward automated feature discovery, causal inference, and generative data synthesis.",
        "AI_impact": {
            "automated_tasks": ["Missing value imputation", "Routine exploratory charts", "Standard metric calculations"],
            "augmented_tasks": ["Automated feature selection", "Hypothesis candidate generation", "Natural language report drafts"],
            "human_skills": ["Domain-specific business contextualization", "Discerning correlation from causation", "Translating mathematical findings into policy"]
        },
        "pathway": "12th Science/Commerce with Math -> B.Sc Stats/B.Tech (3-4 Yrs) -> Data Analyst -> Data Scientist -> Lead Data Scientist",
        "sources": ["Journal of the American Statistical Association", "Harvard Business Review Data Analytics", "Kaggle Annual Data Science Survey"]
    },
    {
        "career_id": "data_analyst",
        "career_name": "Data Analyst",
        "domain": "AI & Data",
        "description": "Inspects, cleans, transforms, and models data to discover patterns, inform conclusions, and support business decision-making.",
        "typical_work": "Writes complex SQL queries, builds interactive dashboards in Power BI/Tableau, tracks KPIs, and delivers weekly business reviews.",
        "education_paths": ["B.Sc / BCA / B.Com / B.Tech / BBA with Analytics focus"],
        "eligibility": "12th / PUC in any stream with Mathematics or Business Mathematics.",
        "required_skills": [
            {"skill": "SQL (Joins, Window Functions, Aggregations)", "level": 4, "importance": "Critical"},
            {"skill": "Data Visualization (Tableau, PowerBI)", "level": 4, "importance": "Critical"},
            {"skill": "Excel & Advanced Spreadsheet Modeling", "level": 4, "importance": "High"},
            {"skill": "Descriptive Statistics", "level": 3, "importance": "High"},
            {"skill": "Basic Python or R for Analysis", "level": 2, "importance": "Medium"}
        ],
        "soft_skills": ["Clear Communication", "Business Curiosity", "Attention to Detail", "Reporting"],
        "related_careers": ["data_scientist", "bi_developer", "financial_analyst"],
        "alternative_careers": ["business_analyst", "digital_marketer", "product_manager", "financial_analyst"],
        "adjacent_careers": ["Operations Analyst", "Reporting Specialist", "Marketing Analyst"],
        "entry_level_roles": ["Junior Data Analyst", "Business Intelligence Trainee", "MIS Executive"],
        "higher_study_options": ["M.Sc in Business Analytics", "MBA in Business Analytics"],
        "certifications": ["Google Data Analytics Professional Certificate", "Microsoft Certified: Power BI Data Analyst Associate"],
        "projects": ["Sales performance & regional profitability interactive dashboard in Power BI", "E-commerce customer retention SQL analysis with cohort cohorting"],
        "portfolio_requirements": ["Public Tableau Public profile link", "SQL scripts portfolio with real-world schema queries"],
        "internship_options": ["Analytics internships across FMCG, retail, tech startups, and financial institutions"],
        "future_skills": ["Conversational business intelligence", "Data storytelling with generative summaries", "Metric layer semantic modeling (dbt)"],
        "technology_changes": "Shift from static spreadsheets to semantic layer metrics, automated anomaly alerts, and natural language dashboard querying.",
        "AI_impact": {
            "automated_tasks": ["Basic chart rendering", "Routine daily KPI email reports", "SQL query syntax error correction"],
            "augmented_tasks": ["Variance driver analysis", "Cohort trend summarization", "Natural language query-to-SQL generation"],
            "human_skills": ["Engaging business stakeholders", "Uncovering underlying operational friction", "Data governance and truth enforcement"]
        },
        "pathway": "12th (Any Stream with Math) -> Degree in Science/Commerce/Tech (3-4 Yrs) -> Trainee Analyst -> Data Analyst -> Senior Analytics Manager",
        "sources": ["DAMA International (Data Management)", "Tableau Community Whitepapers", "Coursera Career Insights"]
    },
    {
        "career_id": "bi_developer",
        "career_name": "Business Intelligence (BI) Developer",
        "domain": "AI & Data",
        "description": "Engineers data warehouses, dimensional data models, and enterprise-grade reporting systems to empower organizational decisions.",
        "typical_work": "Designs star schemas, writes ETL/ELT pipelines, optimizes analytical database queries, and manages enterprise BI semantic layers.",
        "education_paths": ["B.Tech in CS/IT", "BCA / MCA", "B.Sc Information Technology"],
        "eligibility": "12th / PUC with Mathematics.",
        "required_skills": [
            {"skill": "Data Modeling (Star / Snowflake Schema)", "level": 4, "importance": "Critical"},
            {"skill": "SQL & Data Warehouses (Snowflake, BigQuery)", "level": 4, "importance": "Critical"},
            {"skill": "ETL/ELT Tools (dbt, Airflow, SSIS)", "level": 3, "importance": "High"},
            {"skill": "Enterprise BI (PowerBI, Looker)", "level": 4, "importance": "High"},
            {"skill": "Performance Tuning & Indexing", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Systematic Thinking", "Stakeholder Management", "Data Integrity Dedication"],
        "related_careers": ["data_analyst", "data_scientist", "cloud_architect"],
        "alternative_careers": ["data_analyst", "software_engineer", "technical_consultant"],
        "adjacent_careers": ["Data Warehouse Architect", "Analytics Engineer", "ETL Developer"],
        "entry_level_roles": ["Associate BI Developer", "ETL Trainee", "Data Warehouse Analyst"],
        "higher_study_options": ["MS in Information Systems", "Post Graduate Diploma in Big Data Analytics"],
        "certifications": ["Snowflake SnowPro Core", "Microsoft Fabric Analytics Engineer Associate"],
        "projects": ["Build an end-to-end data pipeline with dbt, Snowflake, and Power BI on an open retail dataset", "Dimensional model for hospital patient admissions"],
        "portfolio_requirements": ["Architecture diagrams of data pipelines", "dbt transformation models repository"],
        "internship_options": ["BI consulting firms, enterprise IT services, and data warehousing teams"],
        "future_skills": ["dbt semantic layer orchestration", "Reverse ETL", "AI-assisted data pipeline optimization"],
        "technology_changes": "Transition from legacy on-prem data marts to modern cloud data stacks, Git-integrated transformations, and unified analytics fabrics.",
        "AI_impact": {
            "automated_tasks": ["Column mapping validation", "Routine schema DDL script generation"],
            "augmented_tasks": ["ETL pipeline failure triage", "Query optimization suggestions", "Automated data documentation"],
            "human_skills": ["Designing scalable corporate data standards", "Reconciling conflicting business definitions across departments"]
        },
        "pathway": "12th Science/Commerce -> B.Tech / BCA (3-4 Yrs) -> Junior Data Engineer/BI Trainee -> BI Developer -> BI Architect",
        "sources": ["TDWI (Transforming Data With Intelligence)", "dbt Labs State of Analytics Engineering", "Snowflake Engineering Docs"]
    },

    # 3. Cybersecurity
    {
        "career_id": "cybersecurity_analyst",
        "career_name": "Cybersecurity Operations Analyst",
        "domain": "Cybersecurity",
        "description": "Protects digital networks, systems, and sensitive data from cyber threats, unauthorized intrusions, and security breaches.",
        "typical_work": "Monitors SIEM telemetry, analyzes intrusion alerts, performs vulnerability scans, handles malware containment, and reports security events.",
        "education_paths": ["B.Tech in Cybersecurity / CS / IT", "B.Sc Cybersecurity", "BCA with Cybersecurity Diploma"],
        "eligibility": "12th / PUC with Mathematics or Science.",
        "required_skills": [
            {"skill": "Network Protocols (TCP/IP, DNS, VPN)", "level": 4, "importance": "Critical"},
            {"skill": "SIEM Tools (Splunk, Sentinel, QRadar)", "level": 4, "importance": "Critical"},
            {"skill": "Threat Analysis & Incident Response", "level": 3, "importance": "High"},
            {"skill": "Vulnerability Assessment (Nessus, Nmap)", "level": 3, "importance": "High"},
            {"skill": "Security Fundamentals (Firewalls, IDS/IPS)", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["High Vigilance", "Calm Under Pressure", "Ethical Integrity", "Investigation"],
        "related_careers": ["ethical_hacker", "cloud_security_architect", "digital_forensics_analyst"],
        "alternative_careers": ["cloud_security_architect", "devops_engineer", "network_engineer", "technical_consultant"],
        "adjacent_careers": ["SOC Analyst", "Threat Hunter", "Information Security Specialist"],
        "entry_level_roles": ["SOC Tier 1 Analyst", "Junior Security Associate", "Vulnerability Assessment Trainee"],
        "higher_study_options": ["M.Tech in Cybersecurity", "MS in Information Assurance"],
        "certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)", "Cisco Certified CyberOps Associate"],
        "projects": ["Home lab SIEM setup with Splunk analyzing simulated brute-force and malware attacks", "Vulnerability audit report of a sample network with Nessus"],
        "portfolio_requirements": ["Detailed incident response write-ups", "Home lab network topology and security documentation"],
        "internship_options": ["Managed Security Service Providers (MSSP) SOC teams, bank security departments"],
        "future_skills": ["AI-driven automated threat hunting", "Zero Trust Architecture implementation", "Cloud workload protection"],
        "technology_changes": "Escalation from rule-based perimeter alerts to AI-powered behavioral telemetry, zero-trust frameworks, and SOAR automation.",
        "AI_impact": {
            "automated_tasks": ["Low-fidelity alert triage", "Repetitive IP reputation queries", "Automated firewall rule updates"],
            "augmented_tasks": ["Correlating multi-vector attack chains", "Anomaly hunting across petabytes of network logs"],
            "human_skills": ["Adversarial human intent analysis", "Crisis containment leadership during live ransomware events", "Compliance sign-offs"]
        },
        "pathway": "12th Science/Commerce -> B.Tech / B.Sc Cyber (3-4 Yrs) -> Tier 1 SOC Analyst (1-2 Yrs) -> Senior Security Analyst -> Security Architect",
        "sources": ["NIST National Initiative for Cybersecurity Education (NICE)", "SANS Institute", "ISACA State of Cybersecurity"]
    },
    {
        "career_id": "ethical_hacker",
        "career_name": "Penetration Tester & Ethical Hacker",
        "domain": "Cybersecurity",
        "description": "Simulates adversary attacks against web applications, internal networks, and cloud assets to identify vulnerabilities before adversaries exploit them.",
        "typical_work": "Conducts authorized security assessments, exploits vulnerabilities using Burp Suite and Metasploit, drafts exploit proofs-of-concept, and advises mitigation.",
        "education_paths": ["B.Tech in CS / IT / Cybersecurity", "BCA + Offensive Security Certifications"],
        "eligibility": "12th / PUC with Mathematics or Science.",
        "required_skills": [
            {"skill": "Web Application Security (OWASP Top 10)", "level": 4, "importance": "Critical"},
            {"skill": "Penetration Testing Tools (Burp Suite, Metasploit, Nmap)", "level": 4, "importance": "Critical"},
            {"skill": "Network & Active Directory Exploitation", "level": 3, "importance": "High"},
            {"skill": "Scripting for Exploitation (Python, Bash)", "level": 3, "importance": "High"},
            {"skill": "Vulnerability Remediation Advisory", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Lateral Thinking", "Uncompromising Ethics", "Clear Technical Documentation"],
        "related_careers": ["cybersecurity_analyst", "cloud_security_architect", "digital_forensics_analyst"],
        "alternative_careers": ["software_engineer", "cybersecurity_analyst", "qa_automation_engineer"],
        "adjacent_careers": ["Red Teamer", "Vulnerability Researcher", "AppSec Specialist"],
        "entry_level_roles": ["Junior Penetration Tester", "AppSec Analyst Trainee", "Security Consultant Intern"],
        "higher_study_options": ["M.Tech in Offensive Cybersecurity", "MS in Information Security"],
        "certifications": ["Offensive Security Certified Professional (OSCP)", "eJPT (eLearnSecurity Junior Penetration Tester)"],
        "projects": ["Active Directory lab compromise demonstration", "Comprehensive web app vulnerability report on OWASP Juice Shop"],
        "portfolio_requirements": ["HackTheBox / TryHackMe top percentile rankings and published write-ups", "Responsible disclosure bug bounty acknowledgments"],
        "internship_options": ["Boutique penetration testing consultancies, Big 4 security advisory teams"],
        "future_skills": ["LLM & generative AI model red-teaming", "Cloud identity privilege escalation testing", "API security automation"],
        "technology_changes": "Expansion from classic network port scanning to complex web API logic flaw hunting, cloud infrastructure privilege chains, and AI safety testing.",
        "AI_impact": {
            "automated_tasks": ["Static code scanning (SAST)", "Automated baseline fuzzing"],
            "augmented_tasks": ["Payload variation generation", "Exploit chaining suggestion", "Remediation report draft generation"],
            "human_skills": ["Novel business logic bypass detection", "Social engineering evaluations", "Ethical risk judgment"]
        },
        "pathway": "12th Science -> B.Tech CS/Cyber (4 Yrs) -> Junior Pentester -> Senior Penetration Tester -> Red Team Lead",
        "sources": ["OWASP Foundation", "Offensive Security (OffSec)", "MITRE ATT&CK Framework"]
    },
    {
        "career_id": "digital_forensics_analyst",
        "career_name": "Digital Forensics & Incident Responder",
        "domain": "Cybersecurity",
        "description": "Recovers, inspects, and analyzes digital evidence from compromised hard drives, memory dumps, mobile devices, and cloud logs for legal proceedings.",
        "typical_work": "Preserves forensic chain of custody, extracts deleted artifacts using EnCase/Autopsy, analyzes volatile RAM dumps with Volatility, and writes court-admissible reports.",
        "education_paths": ["B.Sc in Forensic Science / Cybersecurity", "B.Tech in Computer Science / IT", "Diploma in Cyber Forensics"],
        "eligibility": "12th / PUC with Science or Mathematics.",
        "required_skills": [
            {"skill": "Disk & File System Forensics (NTFS, EXT4)", "level": 4, "importance": "Critical"},
            {"skill": "Memory Analysis (Volatility, Rekall)", "level": 3, "importance": "High"},
            {"skill": "Chain of Custody & Evidence Law", "level": 4, "importance": "Critical"},
            {"skill": "Forensics Software (Autopsy, FTK, EnCase)", "level": 3, "importance": "High"},
            {"skill": "Log Analysis & Event Reconstruction", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Methodical Patience", "Investigative Curiosity", "Legal Precision"],
        "related_careers": ["cybersecurity_analyst", "ethical_hacker", "cyber_lawyer"],
        "alternative_careers": ["cybersecurity_analyst", "data_analyst", "lawyer"],
        "adjacent_careers": ["Malware Analyst", "Cyber Crime Investigator", "DFIR Consultant"],
        "entry_level_roles": ["Forensics Examiner Trainee", "Junior DFIR Specialist", "Evidence Technician"],
        "higher_study_options": ["M.Sc in Digital Forensics & Information Security", "Master in Cyber Law & Information Security"],
        "certifications": ["Certified Forensic Computer Examiner (CFCE)", "GIAC Certified Incident Handler (GCIH)"],
        "projects": ["Memory dump triage of a simulated ransomware attack reconstructing execution timeline", "Forensic extraction of deleted artifacts from an encrypted image"],
        "portfolio_requirements": ["Detailed forensic case study reports following standard forensic templates"],
        "internship_options": ["State cyber crime police cells, forensic consulting labs, and corporate DFIR teams"],
        "future_skills": ["Ephemeral cloud forensics (Kubernetes/AWS Lambdas)", "Anti-forensic technique counteraction", "Automated timeline stitching"],
        "technology_changes": "Moving from physical dead-box hard drives to live memory forensics, volatile container evidence, and distributed cloud trail forensics.",
        "AI_impact": {
            "automated_tasks": ["Known-hash matching against threat intelligence", "Log timestamp normalization"],
            "augmented_tasks": ["Large-scale artifact clustering", "Timeline anomaly detection across thousands of machines"],
            "human_skills": ["Sworn testimony and cross-examination in court", "Strict adherence to evidentiary chain of custody"]
        },
        "pathway": "12th Science -> B.Sc Forensics/B.Tech (3-4 Yrs) -> Forensics Assistant -> Forensic Analyst -> Chief Digital Investigator",
        "sources": ["Interpol Cybercrime Directorate", "NIST Computer Forensic Tool Testing (CFTT)", "SANS DFIR Summit"]
    },

    # 4. Design
    {
        "career_id": "ux_designer",
        "career_name": "UX Designer (User Experience)",
        "domain": "Design",
        "description": "Crafts intuitive, accessible, and delightful digital user journeys through research, wireframing, prototyping, and usability testing.",
        "typical_work": "Conducts user interviews, maps user journeys, builds interactive wireframes in Figma, runs usability tests, and collaborates with developers.",
        "education_paths": ["B.Des in Interaction Design / Product Design", "B.Tech in Computer Science / IT with Design portfolio", "B.Sc in Visual Communication"],
        "eligibility": "12th / PUC in any stream (Science/Commerce/Arts) with creative aptitude.",
        "required_skills": [
            {"skill": "User Research & Usability Testing", "level": 4, "importance": "Critical"},
            {"skill": "Wireframing & Prototyping (Figma)", "level": 4, "importance": "Critical"},
            {"skill": "Information Architecture & User Flows", "level": 4, "importance": "High"},
            {"skill": "Interaction Design & Micro-interactions", "level": 3, "importance": "High"},
            {"skill": "Design Systems & Component Libraries", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Empathy", "Storytelling", "Facilitation", "Active Listening", "Collaboration"],
        "related_careers": ["ui_designer", "product_designer", "ux_researcher"],
        "alternative_careers": ["product_manager", "technical_writer", "digital_marketer", "instructional_designer"],
        "adjacent_careers": ["Information Architect", "Design Strategist", "Service Designer"],
        "entry_level_roles": ["Junior UX Designer", "Associate Product Designer", "UX/UI Trainee"],
        "higher_study_options": ["M.Des in Interaction Design (NID, IIT IDC)", "MS in Human-Computer Interaction (HCI)"],
        "certifications": ["Google UX Design Professional Certificate", "Nielsen Norman Group UX Master Certified"],
        "projects": ["End-to-end mobile app design solving student public transportation ticketing with user test validations", "E-commerce checkout UX redesign reducing drop-off"],
        "portfolio_requirements": ["2-3 detailed case studies highlighting problem statement, research, iterations, and metrics", "Figma prototype links"],
        "internship_options": ["Design agencies, tech startups, SaaS product companies"],
        "future_skills": ["Voice & conversational UI design", "AI-assisted design iteration", "Spatial computing & AR interface heuristics"],
        "technology_changes": "Evolution from static screens to multi-modal interfaces, automated layout generation, and dynamic adaptive design systems.",
        "AI_impact": {
            "automated_tasks": ["Basic wireframe auto-generation from prompts", "Color palette and typography pairing", "Icon resizing"],
            "augmented_tasks": ["Synthetic persona testing", "Automated usability heatmap synthesis", "Component state generation"],
            "human_skills": ["Deep stakeholder empathy", "Navigating ambiguous human emotions and ethics", "Strategic product-market alignment"]
        },
        "pathway": "12th (Any Stream) -> B.Des / B.Tech / B.A. Design (4 Yrs) -> Junior UX Designer -> Lead UX Designer -> VP of Design",
        "sources": ["Nielsen Norman Group (NN/g)", "Interaction Design Association (IxDA)", "Design Council UK"]
    },
    {
        "career_id": "ui_designer",
        "career_name": "UI Designer (User Interface)",
        "domain": "Design",
        "description": "Specializes in the visual, aesthetic, and interactive presentation of digital products including typography, colors, and motion.",
        "typical_work": "Creates pixel-perfect UI layouts, designs iconography and illustrations, develops responsive design token systems, and animates transitions.",
        "education_paths": ["B.Des in Communication Design / Visual Design", "BFA in Applied Arts", "Diploma in Graphic & Web Design"],
        "eligibility": "12th / PUC in any stream with portfolio/entrance exam.",
        "required_skills": [
            {"skill": "Visual Design & Layout Theory", "level": 4, "importance": "Critical"},
            {"skill": "Advanced Figma & Design Systems", "level": 4, "importance": "Critical"},
            {"skill": "Typography & Color Theory", "level": 4, "importance": "High"},
            {"skill": "Micro-Animations & Motion Design", "level": 3, "importance": "High"},
            {"skill": "Basic HTML/CSS Understanding", "level": 2, "importance": "Medium"}
        ],
        "soft_skills": ["Visual Elegance", "Attention to Micro-Details", "Design Consistency"],
        "related_careers": ["ux_designer", "product_designer", "graphic_designer"],
        "alternative_careers": ["graphic_designer", "motion_graphics_animator", "frontend_developer", "ux_designer"],
        "adjacent_careers": ["Visual Designer", "Brand Interface Specialist", "Design Systems Engineer"],
        "entry_level_roles": ["Junior UI Designer", "Visual Design Associate", "Web Designer"],
        "higher_study_options": ["M.Des in Visual Communication", "Master of Fine Arts (Applied Arts)"],
        "certifications": ["Figma Certified Creator", "Interaction Design Foundation Visual Design Specialist"],
        "projects": ["Complete design system library with 50+ auto-layout components and dark mode tokens", "Fintech mobile application high-fidelity prototype"],
        "portfolio_requirements": ["Dribbble/Behance profile", "Interactive Figma prototype showcasing responsive layouts"],
        "internship_options": ["Digital design studios, branding consultancies, e-commerce tech companies"],
        "future_skills": ["3D web UI design (Spline/Three.js)", "Generative UI tokens", "Dynamic responsive accessibility adaptation"],
        "technology_changes": "Integration of code-generating visual tools, design tokens automated to CSS, and spatial 3D interactive canvases.",
        "AI_impact": {
            "automated_tasks": ["Exporting asset assets across resolutions", "Converting sketches to SVG icons"],
            "augmented_tasks": ["Automated dark-mode theme generation", "Dynamic accessibility contrast corrections"],
            "human_skills": ["Nuanced brand identity expression", "Artistic taste and emotional aesthetic resonance"]
        },
        "pathway": "12th Any Stream -> B.Des / BFA (4 Yrs) -> Visual/UI Designer -> Senior UI Designer -> Head of Visual Experience",
        "sources": ["AIGA Design Archives", "Figma Design Insights", "Design Systems Community"]
    },
    {
        "career_id": "product_designer",
        "career_name": "Product Designer (Digital Products)",
        "domain": "Design",
        "description": "Owns the end-to-end user experience and visual design while aligning directly with business goals, metrics, and engineering constraints.",
        "typical_work": "Bridges user research and visual design, evaluates conversion metrics, collaborates with product managers on product roadmap, and iterates MVPs.",
        "education_paths": ["B.Des in Product Design / Interaction Design", "B.Tech with Design Minor", "B.Sc + Design Portfolio"],
        "eligibility": "12th / PUC in any stream.",
        "required_skills": [
            {"skill": "End-to-End Product Thinking & UX", "level": 4, "importance": "Critical"},
            {"skill": "Visual & Interaction Design (Figma)", "level": 4, "importance": "Critical"},
            {"skill": "Product Metrics & Growth Experiments", "level": 3, "importance": "High"},
            {"skill": "Rapid Prototyping", "level": 4, "importance": "High"},
            {"skill": "Stakeholder Alignment & Strategy", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Holistic Vision", "Business Acumen", "Resilience Under Feedback", "Communication"],
        "related_careers": ["ux_designer", "product_manager", "ui_designer"],
        "alternative_careers": ["product_manager", "ux_researcher", "technical_writer", "data_analyst"],
        "adjacent_careers": ["UX Strategist", "Growth Designer", "Head of Product Experience"],
        "entry_level_roles": ["Associate Product Designer", "Junior UX/UI Designer"],
        "higher_study_options": ["M.Des in Strategic Product Design", "MBA with Product Focus"],
        "certifications": ["Reforge Product Design", "IDEO Human-Centered Design"],
        "projects": ["B2B SaaS dashboard overhaul improving weekly active user task completion by 35%", "Onboarding funnel redesign with A/B experiment blueprints"],
        "portfolio_requirements": ["Comprehensive product case studies linking design decisions to tangible business metrics"],
        "internship_options": ["High-growth tech startups, SaaS companies, global product centers"],
        "future_skills": ["AI product design patterns", "Data-informed generative personalization", "Multi-modal UX"],
        "technology_changes": "Moving from visual hand-offs to autonomous rapid experiment generation, continuous telemetry integration, and AI design orchestration.",
        "AI_impact": {
            "automated_tasks": ["Drafting wireframe variants", "Standard usability test transcription"],
            "augmented_tasks": ["A/B test variation creation", "User feedback sentiment clustering"],
            "human_skills": ["Product vision synthesis", "Cross-functional negotiation between engineers and executives"]
        },
        "pathway": "12th Any Stream -> B.Des / B.Tech (4 Yrs) -> Junior Product Designer -> Senior Product Designer -> VP of Product Design",
        "sources": ["Reforge Product Strategy Reports", "InVision Design Maturity Benchmark", "First Round Review Design"]
    },
    {
        "career_id": "ux_researcher",
        "career_name": "UX Researcher (User Experience Researcher)",
        "domain": "Design",
        "description": "Discovers deep user motivations, behavioral pain points, and cognitive barriers using qualitative and quantitative research methodologies.",
        "typical_work": "Conducts semi-structured interviews, runs diary studies, designs surveys, analyzes behavioral metrics, and synthesizes strategic user insights.",
        "education_paths": ["B.Sc / M.Sc in Psychology or Cognitive Science", "B.Des in Interaction Design", "B.A. in Sociology / Anthropology / HCI"],
        "eligibility": "12th / PUC in any stream (Psychology/Sociology/Science beneficial).",
        "required_skills": [
            {"skill": "Qualitative Interviewing & Observational Research", "level": 4, "importance": "Critical"},
            {"skill": "Usability Testing Methodologies", "level": 4, "importance": "Critical"},
            {"skill": "Survey Design & Quantitative Analysis", "level": 3, "importance": "High"},
            {"skill": "Synthesis & Insight Frameworks (Personas, Journey Maps)", "level": 4, "importance": "Critical"},
            {"skill": "Cognitive Psychology Principles", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Deep Active Listening", "Curiosity", "Unbiased Observation", "Persuasive Storytelling"],
        "related_careers": ["ux_designer", "product_manager", "clinical_psychologist"],
        "alternative_careers": ["data_analyst", "product_manager", "technical_writer", "psychologist"],
        "adjacent_careers": ["Design Researcher", "Customer Insights Lead", "Cognitive Ergonomist"],
        "entry_level_roles": ["Junior UX Researcher", "User Research Assistant", "Insights Associate"],
        "higher_study_options": ["MS in Human-Computer Interaction", "M.Sc in Applied Cognitive Psychology", "Ph.D. in Information Science"],
        "certifications": ["Nielsen Norman UX Research Specialty", "Coursera Quantitative UX Research"],
        "projects": ["Comprehensive exploratory study on elderly smartphone banking adoption barriers with 20 interviews", "Card sorting and tree testing for a university portal"],
        "portfolio_requirements": ["Research repository showcasing study plans, discussion guides, synthesis artifacts, and impact stories"],
        "internship_options": ["Tech enterprise research labs, market research agencies, non-profit digital accessibility initiatives"],
        "future_skills": ["AI-driven qualitative synthesis analysis", "Algorithmic bias user impact testing", "Remote asynchronous testing tools"],
        "technology_changes": "Adoption of automated interview transcript summarization, multi-lingual sentiment tagging, and continuous user telemetry research.",
        "AI_impact": {
            "automated_tasks": ["Audio transcription", "Initial thematic tag generation in interview transcripts"],
            "augmented_tasks": ["Cross-study knowledge base synthesis", "Automated survey response cleaning"],
            "human_skills": ["Building authentic human trust during interviews", "Interpreting cultural body language and tacit unmet needs"]
        },
        "pathway": "12th Any Stream -> B.A. Psychology/B.Des (3-4 Yrs) -> UX Research Assistant -> UX Researcher -> Director of User Insights",
        "sources": ["EPIC (Ethnographic Praxis in Industry Conference)", "UXPA International", "ACM SIGCHI"]
    },

    # 5. Fashion
    {
        "career_id": "fashion_designer",
        "career_name": "Fashion Designer",
        "domain": "Fashion",
        "description": "Creates original clothing, footwear, and accessory collections by blending artistic creativity, trend forecasting, and garment construction.",
        "typical_work": "Sketches design concepts, selects textiles, creates technical pattern packs (tech packs), oversees sample tailoring, and directs runway presentations.",
        "education_paths": ["B.Des in Fashion Design (NIFT, Pearl Academy)", "Diploma in Apparel Design", "B.Sc in Fashion & Apparel Design"],
        "eligibility": "12th / PUC in any stream with creative aptitude test (e.g. NIFT Entrance).",
        "required_skills": [
            {"skill": "Fashion Illustration & CAD (CLO3D, Illustrator)", "level": 4, "importance": "Critical"},
            {"skill": "Pattern Making & Garment Construction", "level": 4, "importance": "Critical"},
            {"skill": "Textile Science & Fabric Knowledge", "level": 3, "importance": "High"},
            {"skill": "Trend Forecasting & Moodboarding", "level": 3, "importance": "High"},
            {"skill": "Production Tech Pack Creation", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Creative Vision", "Cultural Sensitivity", "Commercial Awareness", "Tenacity"],
        "related_careers": ["textile_designer", "costume_designer", "graphic_designer"],
        "alternative_careers": ["graphic_designer", "product_designer", "event_director", "digital_marketer"],
        "adjacent_careers": ["Apparel Stylist", "Fashion Trend Forecaster", "Costume Coordinator"],
        "entry_level_roles": ["Assistant Fashion Designer", "Fashion Design Intern", "Apparel Merchandiser Trainee"],
        "higher_study_options": ["M.Des in Fashion Design", "Master in Luxury Brand Management"],
        "certifications": ["CLO 3D Virtual Fashion Specialist", "Sustainable Fashion Design Certificate"],
        "projects": ["Complete 6-ensemble capsule collection designed, patterned, and 3D rendered in CLO3D with full tech packs", "Upcycled sustainable streetwear line"],
        "portfolio_requirements": ["Fashion lookbook containing mood boards, fabric swatches, technical flats, and photographed samples"],
        "internship_options": ["Apparel export houses, haute couture designer ateliers, retail fashion brands (Zara, Fabindia)"],
        "future_skills": ["Digital 3D fashion modeling (Metaverse/CLO3D)", "Zero-waste circular pattern drafting", "Bio-materials & smart textiles"],
        "technology_changes": "Transition from physical sampling to 3D virtual fitting (saving fabric waste), automated laser cutting, and on-demand digital printing.",
        "AI_impact": {
            "automated_tasks": ["Moodboard image scraping", "Standard color swatch variations"],
            "augmented_tasks": ["Generative print motif creation", "Trend forecast pattern recognition across social feeds"],
            "human_skills": ["Tactile fabric drape assessment", "Original artistic philosophy", "Fitting human body diversity with nuance"]
        },
        "pathway": "12th Any Stream -> B.Des Fashion (4 Yrs) -> Design Assistant -> Associate Designer -> Creative Director / Fashion Label Founder",
        "sources": ["NIFT (National Institute of Fashion Technology)", "WGSN Trend Forecasting", "CFDA (Council of Fashion Designers of America)"]
    },

    # 6. Media & Film
    {
        "career_id": "film_editor",
        "career_name": "Film & Video Editor",
        "domain": "Media & Film",
        "description": "Assembles raw camera footage, audio, and visual effects into compelling, coherent cinematic narratives for films, streaming, and commercials.",
        "typical_work": "Reviews raw takes, cuts scenes for emotional pacing, syncs audio and Foley, color grades footage, and exports masters in Premiere/DaVinci.",
        "education_paths": ["B.Sc / B.A. in Film & Television Production (FTII, SRFTI)", "Diploma in Video Editing & Post-Production", "B.Des in Animation & VFX"],
        "eligibility": "12th / PUC in any stream with visual storytelling passion.",
        "required_skills": [
            {"skill": "Non-Linear Editing (DaVinci Resolve, Premiere Pro)", "level": 4, "importance": "Critical"},
            {"skill": "Cinematic Storytelling & Narrative Pacing", "level": 4, "importance": "Critical"},
            {"skill": "Color Grading & Color Correction", "level": 3, "importance": "High"},
            {"skill": "Audio Mixing & Sound Design Basics", "level": 3, "importance": "High"},
            {"skill": "Motion Graphics Basics (After Effects)", "level": 2, "importance": "Medium"}
        ],
        "soft_skills": ["Patience", "Narrative Empathy", "Attention to Micro-rhythms", "Constructive Collaboration"],
        "related_careers": ["motion_graphics_animator", "sound_designer", "creative_director"],
        "alternative_careers": ["motion_graphics_animator", "technical_writer", "digital_marketer", "ui_designer"],
        "adjacent_careers": ["Colorist", "Post-Production Supervisor", "DIT (Digital Imaging Technician)"],
        "entry_level_roles": ["Assistant Video Editor", "Junior Post-Production Artist", "Roto/Ingest Trainee"],
        "higher_study_options": ["M.A. in Film Editing", "Advanced Masterclasses in DaVinci Color Science"],
        "certifications": ["Blackmagic Certified DaVinci Resolve Professional", "Adobe Certified Professional Video Editor"],
        "projects": ["Edit a 15-minute narrative short film showcasing pacing and sound design", "Commercial spec ad edited and color graded to industry standards"],
        "portfolio_requirements": ["High-energy editing showreel (under 2 minutes)", "Complete edited short films with director credits"],
        "internship_options": ["Film production houses, digital advertising agencies, streaming platform content studios"],
        "future_skills": ["AI-assisted rough cutting and transcript matching", "Virtual production real-time editing", "High dynamic range (HDR) workflows"],
        "technology_changes": "Adoption of text-based video editing, AI scene categorization, neural-engine object tracking, and cloud-collaborative remote timelines.",
        "AI_impact": {
            "automated_tasks": ["Speech-to-text transcript syncing", "Auto-silence/jumpcut removal", "Baseline color balance normalization"],
            "augmented_tasks": ["Semantic footage search ('find sunset shots with car')", "Automated background noise removal"],
            "human_skills": ["Dramatic tension curation", "Emotional rhythm and comedic timing", "Director-editor psychological alignment"]
        },
        "pathway": "12th Any Stream -> Degree in Film Production (3 Yrs) -> Assistant Editor -> Lead Film Editor -> Post-Production Director",
        "sources": ["American Cinema Editors (ACE)", "FTII Academic Curriculum", "Motion Picture Editors Guild"]
    },
    {
        "career_id": "technical_writer",
        "career_name": "Technical Writer & Documentation Strategist",
        "domain": "Media & Film",
        "description": "Translates sophisticated engineering systems, software code, and scientific processes into clear, accessible documentation and user guides.",
        "typical_work": "Interviews software engineers, documents REST APIs in OpenAPI/Swagger, creates interactive developer portals, and writes release notes.",
        "education_paths": ["B.A. / B.Sc in English, Journalism, or Mass Communication", "B.Tech in CS/IT with strong writing skills", "BCA / MCA"],
        "eligibility": "12th / PUC with strong command of English and logical reasoning.",
        "required_skills": [
            {"skill": "Technical Clarity & Structured Writing", "level": 4, "importance": "Critical"},
            {"skill": "Docs-as-Code (Markdown, Git, Static Site Generators)", "level": 4, "importance": "Critical"},
            {"skill": "API Documentation (Swagger / Postman)", "level": 3, "importance": "High"},
            {"skill": "Information Architecture & Topic-Based Authoring", "level": 3, "importance": "High"},
            {"skill": "Basic Code Literacy (JSON, Python, JavaScript)", "level": 2, "importance": "Medium"}
        ],
        "soft_skills": ["Extreme Clarity", "Intellectual Curiosity", "User Advocacy", "Active Questioning"],
        "related_careers": ["ux_designer", "product_manager", "software_engineer"],
        "alternative_careers": ["technical_consultant", "ux_designer", "digital_marketer", "instructional_designer"],
        "adjacent_careers": ["Developer Advocate", "API Documentation Specialist", "Knowledge Manager"],
        "entry_level_roles": ["Associate Technical Writer", "Junior Documentation Specialist", "Content Developer"],
        "higher_study_options": ["M.A. in Technical Communication", "MS in Science & Technology Communication"],
        "certifications": ["Certified Professional Technical Communicator (CPTC)", "Google Technical Writing Badge"],
        "projects": ["Open-source API documentation project deployed with Docusaurus and Git", "Comprehensive beginner tutorial for a complex software library"],
        "portfolio_requirements": ["Public documentation website or writing portfolio showcasing API guides and procedural tutorials"],
        "internship_options": ["Enterprise software giants, open-source technology foundations, fintech documentation teams"],
        "future_skills": ["AI prompt documentation standards", "Interactive runnable documentation notebooks", "Doc search RAG optimization"],
        "technology_changes": "Shift from monolithic PDF manuals to Git-backed docs-as-code, interactive code sandboxes, and AI-assisted search retrieval.",
        "AI_impact": {
            "automated_tasks": ["Spelling and grammatical consistency checks", "Auto-generating initial API parameter tables"],
            "augmented_tasks": ["Multi-language documentation translation", "Drafting initial code explanation templates"],
            "human_skills": ["Empathetic developer onboarding experience", "Testing procedures for real-world usability", "Synthesizing cross-team conceptual context"]
        },
        "pathway": "12th Any Stream -> Degree in English/CS (3-4 Yrs) -> Junior Technical Writer -> Lead Document Strategist -> Head of Technical Content",
        "sources": ["Society for Technical Communication (STC)", "Write the Docs Community", "IEEE Transactions on Professional Communication"]
    },

    # 7. Psychology
    {
        "career_id": "clinical_psychologist",
        "career_name": "Clinical Psychologist",
        "domain": "Psychology",
        "description": "Diagnoses, treats, and supports individuals experiencing psychological distress, mental health disorders, and emotional challenges.",
        "typical_work": "Conducts clinical interviews and diagnostic psychometric assessments, designs evidence-based therapy interventions (CBT), and supports recovery.",
        "education_paths": ["B.A. / B.Sc in Psychology (3 Yrs) -> M.A. / M.Sc in Clinical Psychology (2 Yrs) -> M.Phil in Clinical Psychology (RCI approved) / Psy.D."],
        "eligibility": "12th / PUC in any stream (Psychology or Science advantageous). Professional license requires RCI certification in India.",
        "required_skills": [
            {"skill": "Psychological Assessment & Psychometric Testing", "level": 4, "importance": "Critical"},
            {"skill": "Psychotherapeutic Modalities (CBT, DBT, Psychodynamic)", "level": 4, "importance": "Critical"},
            {"skill": "Diagnostic Criteria (DSM-5 / ICD-11)", "level": 4, "importance": "Critical"},
            {"skill": "Crisis Intervention & Risk Assessment", "level": 4, "importance": "High"},
            {"skill": "Clinical Case Formulation", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Radical Empathy", "Non-Judgmental Listening", "Emotional Stability", "Ethical Discretion"],
        "related_careers": ["counseling_psychologist", "organizational_psychologist", "social_worker"],
        "alternative_careers": ["counseling_psychologist", "ux_researcher", "social_worker", "instructional_designer"],
        "adjacent_careers": ["Neuropsychologist", "Health Psychologist", "Forensic Psychologist"],
        "entry_level_roles": ["Trainee Psychologist", "Assistant Clinical Psychologist", "Mental Health Associate"],
        "higher_study_options": ["M.Phil in Clinical Psychology (NIMHANS/CIP)", "Ph.D. in Clinical Psychology"],
        "certifications": ["RCI Registration (India)", "Certified CBT Practitioner"],
        "projects": ["Clinical research dissertation on adolescent anxiety coping mechanisms", "Case report series on cognitive rehabilitation following trauma"],
        "portfolio_requirements": ["Supervised clinical case logbook", "Certified psychometric testing assessment records"],
        "internship_options": ["Psychiatric hospitals, de-addiction centers, university counseling centers"],
        "future_skills": ["Digital mental health & teletherapy ethics", "Biofeedback & neurofeedback integration", "AI-supported clinical note compliance"],
        "technology_changes": "Adoption of tele-counseling platforms, digital cognitive assessments, and virtual reality exposure therapy (VRET).",
        "AI_impact": {
            "automated_tasks": ["Routine session scheduling", "Standardized psychometric score tabulation"],
            "augmented_tasks": ["Clinical note speech-to-text formatting", "Symptom tracking trend visualization"],
            "human_skills": ["Authentic human therapeutic alliance", "Nuanced crisis containment and suicide intervention", "Unconditional positive regard"]
        },
        "pathway": "12th -> B.A. Psychology (3 Yrs) -> M.A. Clinical Psychology (2 Yrs) -> M.Phil (2 Yrs) -> Licensed Clinical Psychologist -> Chief Clinical Psychologist",
        "sources": ["Rehabilitation Council of India (RCI)", "American Psychological Association (APA)", "NIMHANS Clinical Guidelines"]
    },
    {
        "career_id": "organizational_psychologist",
        "career_name": "Organizational & Industrial Psychologist",
        "domain": "Psychology",
        "description": "Applies psychological principles and behavioral science to workplace dynamics, leadership development, employee well-being, and organizational culture.",
        "typical_work": "Designs psychometric hiring tests, assesses employee engagement metrics, develops leadership coaching programs, and facilitates organizational change.",
        "education_paths": ["B.A. / B.Sc in Psychology -> M.A. / M.Sc in Organizational Psychology / Human Resource Development"],
        "eligibility": "12th / PUC in any stream with interest in human behavior and organizational systems.",
        "required_skills": [
            {"skill": "Workplace Psychometric Testing & Assessment Centers", "level": 4, "importance": "Critical"},
            {"skill": "Organizational Behavioral Science", "level": 4, "importance": "Critical"},
            {"skill": "People Analytics & Survey Analysis", "level": 3, "importance": "High"},
            {"skill": "Leadership Coaching Frameworks", "level": 3, "importance": "High"},
            {"skill": "Change Management Strategies", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Diplomacy", "Strategic Thinking", "Objective Evaluation", "Persuasive Presentation"],
        "related_careers": ["clinical_psychologist", "management_consultant", "ux_researcher"],
        "alternative_careers": ["management_consultant", "ux_researcher", "product_manager", "instructional_designer"],
        "adjacent_careers": ["People Scientist", "Talent Management Strategist", "Culture Consultant"],
        "entry_level_roles": ["Talent Assessment Specialist", "People Analytics Trainee", "HR Transformation Consultant"],
        "higher_study_options": ["Ph.D. in Industrial/Organizational Psychology", "Executive MBA in Leadership"],
        "certifications": ["SHRM-CP", "Hogan Assessment Certification", "Korn Ferry Leadership Architect"],
        "projects": ["Comprehensive culture assessment and remote worker burnout mitigation program for 500+ employees", "Validation study of a customized hiring aptitude tool"],
        "portfolio_requirements": ["Case study reports on workplace interventions and organizational diagnostic metrics"],
        "internship_options": ["Global HR consultancies (Mercer, Korn Ferry), corporate people-analytics teams"],
        "future_skills": ["Hybrid workplace behavioral dynamics", "AI recruiting tool algorithmic bias auditing", "Neuroleadership methodologies"],
        "technology_changes": "Transitioning from annual paper surveys to continuous pulse telemetry, AI-driven sentiment analysis, and talent graph predictive analytics.",
        "AI_impact": {
            "automated_tasks": ["Aggregating survey score distributions", "Scheduling employee check-ins"],
            "augmented_tasks": ["Predicting attrition patterns from engagement signals", "Tailoring personalized training modules"],
            "human_skills": ["Executive leadership conflict resolution", "Navigating high-stakes restructuring with empathy", "Cultivating organizational trust"]
        },
        "pathway": "12th Any Stream -> B.A. Psychology (3 Yrs) -> M.Sc Organizational Psychology (2 Yrs) -> People Scientist -> Head of Organizational Development",
        "sources": ["Society for Industrial and Organizational Psychology (SIOP)", "Chartered Institute of Personnel and Development (CIPD)"]
    },

    # 8. Fine Arts
    {
        "career_id": "concept_artist",
        "career_name": "Concept Artist & Visual Illustrator",
        "domain": "Fine Arts",
        "description": "Visualizes characters, environments, vehicles, and imaginary worlds for video games, animation films, and commercial media.",
        "typical_work": "Translates script briefs into visual thumbnail sketches, paints digital environments, designs character costumes, and delivers production art bibles.",
        "education_paths": ["BFA in Painting / Applied Arts / Animation", "B.Des in Game Art / Visual Communication", "Intensive Atelier Diploma"],
        "eligibility": "12th / PUC in any stream with high drawing aptitude and creative imagination.",
        "required_skills": [
            {"skill": "Anatomy & Figure Drawing", "level": 4, "importance": "Critical"},
            {"skill": "Digital Painting (Photoshop, Procreate)", "level": 4, "importance": "Critical"},
            {"skill": "Perspective, Lighting & Composition", "level": 4, "importance": "Critical"},
            {"skill": "3D Blockout Basics (Blender, ZBrush)", "level": 3, "importance": "High"},
            {"skill": "Visual Storytelling & Worldbuilding", "level": 4, "importance": "High"}
        ],
        "soft_skills": ["Receptive to Art Direction", "Deep Creative Imagination", "Perseverance"],
        "related_careers": ["motion_graphics_animator", "game_designer", "graphic_designer"],
        "alternative_careers": ["graphic_designer", "ui_designer", "fashion_designer", "motion_graphics_animator"],
        "adjacent_careers": ["Matte Painter", "Character Designer", "Storyboard Artist"],
        "entry_level_roles": ["Junior Concept Artist", "Production Art Trainee", "Digital Painter"],
        "higher_study_options": ["MFA in Visual Arts", "Master in Entertainment Design"],
        "certifications": ["ZBrush Certified Sculptor", "ArtStation Verified Pro"],
        "projects": ["Complete visual art bible for an original sci-fi universe including 5 characters, 3 environments, and vehicle callouts", "Environment concept painting series"],
        "portfolio_requirements": ["Polished ArtStation portfolio with sketches, iterative ideation thumbnails, and finished paintings"],
        "internship_options": ["Gaming studios, animation studios, film visual effects houses"],
        "future_skills": ["Generative AI controlnet integration", "Real-time Unreal Engine 5 virtual lighting setup", "3D virtual reality sculpting"],
        "technology_changes": "Evolution from purely 2D painting to hybrid 3D blockouts in Blender, photobashing, and rapid AI-assisted ideation pipelines.",
        "AI_impact": {
            "automated_tasks": ["Extracting texture maps", "Generating baseline perspective grids"],
            "augmented_tasks": ["Rapid thumbnail idea exploration with diffusion models", "Lighting style transfer variations"],
            "human_skills": ["Original auteur artistic voice", "Nuanced visual subtext and worldbuilding narrative depth", "Art direction fidelity"]
        },
        "pathway": "12th Any Stream -> BFA / B.Des (4 Yrs) -> Junior Concept Artist -> Lead Concept Artist -> Art Director",
        "sources": ["Concept Art Association", "GDC (Game Developers Conference) Vault", "ArtStation Annual Industry Survey"]
    },

    # 9. Healthcare
    {
        "career_id": "medical_doctor",
        "career_name": "General Physician / Medical Doctor",
        "domain": "Healthcare",
        "description": "Assesses, diagnoses, treats, and prevents physical illnesses and injuries to preserve human health and well-being.",
        "typical_work": "Conducts patient examinations, orders and interprets diagnostic lab tests, prescribes medications, and coordinates multidisciplinary clinical care.",
        "education_paths": ["MBBS (Bachelor of Medicine, Bachelor of Surgery - 5.5 Yrs including internship) -> MD / MS (Doctor of Medicine / Master of Surgery - 3 Yrs)"],
        "eligibility": "12th / PUC with Physics, Chemistry, and Biology (min 50-60%) with national qualification exam (NEET in India).",
        "required_skills": [
            {"skill": "Clinical Diagnosis & Pathology", "level": 4, "importance": "Critical"},
            {"skill": "Pharmacology & Treatment Protocols", "level": 4, "importance": "Critical"},
            {"skill": "Patient Physical Examination", "level": 4, "importance": "Critical"},
            {"skill": "Emergency Life Support (BLS/ACLS)", "level": 4, "importance": "High"},
            {"skill": "Medical Ethics & Patient Communication", "level": 4, "importance": "Critical"}
        ],
        "soft_skills": ["Compassion", "Emotional Resilience", "Decisiveness in Crisis", "Stamina"],
        "related_careers": ["pharmacist", "clinical_research_associate", "biomedical_engineer"],
        "alternative_careers": ["clinical_research_associate", "biotechnologist", "public_health_specialist", "genetic_counselor"],
        "adjacent_careers": ["Cardiologist", "Pediatrician", "Surgeon", "Medical Administrator"],
        "entry_level_roles": ["Medical Officer", "Junior Resident Doctor", "Emergency Room Resident"],
        "higher_study_options": ["MD / MS Post Graduate Specialization", "DNB (Diplomate of National Board)"],
        "certifications": ["Medical Council Registration (NMC/State Medical Council)", "ACLS Certification"],
        "projects": ["Hospital clinical audit of antimicrobial resistance trends", "Community health epidemiological screening program"],
        "portfolio_requirements": ["Verified MBBS degree, logbook of clinical procedures, medical registration certificate"],
        "internship_options": ["1-year compulsory rotating medical internship across medicine, surgery, obstetrics, and pediatrics"],
        "future_skills": ["AI-assisted medical image interpretation", "Genomic medicine & personalized therapeutics", "Robotic surgical assistance"],
        "technology_changes": "Integration of diagnostic AI algorithms, digital health electronic medical records (EMR), point-of-care ultrasound, and tele-triage.",
        "AI_impact": {
            "automated_tasks": ["Transcribing clinical visit notes", "Drug interaction standard checking"],
            "augmented_tasks": ["Radiology triage of abnormal chest X-rays", "Early sepsis warning algorithms"],
            "human_skills": ["Breaking difficult medical news with compassion", "Complex multi-morbidity bedside clinical decision-making", "Physical palpation and examination"]
        },
        "pathway": "12th PCB -> NEET -> MBBS (5.5 Yrs) -> Junior Resident -> MD/MS (3 Yrs) -> Senior Specialist -> Medical Director / Professor",
        "sources": ["National Medical Commission (NMC)", "World Health Organization (WHO)", "The Lancet Medical Career Studies"]
    },
    {
        "career_id": "clinical_research_associate",
        "career_name": "Clinical Research Associate (CRA)",
        "domain": "Healthcare",
        "description": "Monitors and coordinates clinical drug trials to ensure safety, scientific validity, and strict regulatory compliance.",
        "typical_work": "Conducts clinical site initiation visits, audits patient informed consent forms, verifies adverse event reporting, and ensures GCP protocol adherence.",
        "education_paths": ["B.Pharm / M.Pharm", "B.Sc / M.Sc in Biotechnology / Life Sciences", "MBBS / BDS"],
        "eligibility": "12th / PUC with Biology, Chemistry, and Physics.",
        "required_skills": [
            {"skill": "Good Clinical Practice (ICH-GCP) Guidelines", "level": 4, "importance": "Critical"},
            {"skill": "Clinical Trial Protocols & Regulatory Compliance (FDA/CDSCO)", "level": 4, "importance": "Critical"},
            {"skill": "Source Data Verification & Audit Monitoring", "level": 4, "importance": "High"},
            {"skill": "Pharmacovigilance & Adverse Event Reporting", "level": 3, "importance": "High"},
            {"skill": "Medical Terminology & Life Sciences", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Meticulous Attention to Detail", "High Integrity", "Cross-functional Coordination", "Audit Rigor"],
        "related_careers": ["medical_doctor", "pharmacist", "biotechnologist"],
        "alternative_careers": ["pharmacist", "biotechnologist", "data_analyst", "environmental_scientist"],
        "adjacent_careers": ["Clinical Data Manager", "Regulatory Affairs Specialist", "Clinical Project Manager"],
        "entry_level_roles": ["Clinical Trial Assistant (CTA)", "Trainee CRA", "In-House CRA"],
        "higher_study_options": ["M.Sc in Clinical Research", "Post Graduate Diploma in Regulatory Affairs"],
        "certifications": ["CCRA (Certified Clinical Research Associate - ACRP)", "ICH-GCP TransCelerate Certification"],
        "projects": ["Drafting a comprehensive Phase III clinical trial monitoring plan", "Clinical source document verification audit report following mock trial data"],
        "portfolio_requirements": ["GCP certification records, verified audit trail project reports"],
        "internship_options": ["Global Contract Research Organizations (CROs like IQVIA, Parexel), pharmaceutical clinical trial teams"],
        "future_skills": ["Decentralized and virtual clinical trial monitoring", "Real-world evidence (RWE) analytics", "AI-driven protocol compliance alerts"],
        "technology_changes": "Transitioning from paper case report forms to electronic data capture (EDC), remote decentralized trials, and wearables continuous data collection.",
        "AI_impact": {
            "automated_tasks": ["Routine EDC discrepancy logging", "Form completeness checking"],
            "augmented_tasks": ["Patient recruitment eligibility screening via EHR matching", "Trial risk-based monitoring prioritization"],
            "human_skills": ["Site investigator relationship management", "Ethical patient safety advocacy", "Regulatory audit defense"]
        },
        "pathway": "12th Science -> B.Pharm / B.Sc Life Sciences (3-4 Yrs) -> Clinical Trial Assistant -> CRA I -> Senior CRA -> Clinical Project Director",
        "sources": ["Association of Clinical Research Professionals (ACRP)", "FDA Clinical Trial Guidance", "CDSCO India Standards"]
    },

    # 10. Business & Finance
    {
        "career_id": "financial_analyst",
        "career_name": "Financial Analyst & Equity Researcher",
        "domain": "Business & Finance",
        "description": "Evaluates investment opportunities, builds financial valuation models, assesses company performance, and guides strategic capital allocation.",
        "typical_work": "Builds discounted cash flow (DCF) models in Excel, analyzes quarterly balance sheets, tracks industry macroeconomic trends, and writes investment memos.",
        "education_paths": ["B.Com (Honours) / BBA Finance", "B.Tech + MBA in Finance", "B.Sc in Economics / Mathematics"],
        "eligibility": "12th / PUC with Mathematics or Accountancy/Commerce.",
        "required_skills": [
            {"skill": "Financial Modeling & Valuation (DCF, Multiples)", "level": 4, "importance": "Critical"},
            {"skill": "Financial Statement Analysis (Balance Sheet, P&L, Cash Flow)", "level": 4, "importance": "Critical"},
            {"skill": "Advanced Excel (VBA, Macros, Sensitivity Tables)", "level": 4, "importance": "Critical"},
            {"skill": "Corporate Finance Principles", "level": 3, "importance": "High"},
            {"skill": "Financial Data Platforms (Bloomberg / Capital IQ)", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Analytical Rigor", "Commercial Skepticism", "Concise Executive Communication"],
        "related_careers": ["chartered_accountant", "management_consultant", "data_analyst"],
        "alternative_careers": ["data_analyst", "business_analyst", "product_manager", "economist"],
        "adjacent_careers": ["Equity Research Associate", "Investment Banking Analyst", "Portfolio Analyst"],
        "entry_level_roles": ["Junior Financial Analyst", "Equity Research Trainee", "Corporate FP&A Associate"],
        "higher_study_options": ["MBA in Finance (IIMs, ISB)", "Master in Finance / Financial Engineering"],
        "certifications": ["CFA (Chartered Financial Analyst) Level 1/2/3", "Financial Modeling & Valuation Analyst (FMVA)"],
        "projects": ["Complete 3-statement financial model and DCF equity valuation of an NSE/NYSE public company", "M&A accretion/dilution model for a tech acquisition"],
        "portfolio_requirements": ["Fully formatted Excel financial models with dynamic scenario switches", "Published equity research report memos"],
        "internship_options": ["Investment banks, mutual funds, boutique research firms, corporate FP&A teams"],
        "future_skills": ["Python for quantitative backtesting", "Alternative data analytics (satellite/credit card metrics)", "ESG investing frameworks"],
        "technology_changes": "Integration of automated earnings call transcription, instant 10-K data extraction, and algorithmic scenario simulation.",
        "AI_impact": {
            "automated_tasks": ["Historical financial data pulling into spreadsheets", "Standard financial ratio calculations"],
            "augmented_tasks": ["Earnings call transcript tone analysis", "Automated sensitivity table variations"],
            "human_skills": ["Assessing management integrity during meetings", "Understanding macroeconomic and geopolitical tailwinds", "High-conviction capital judgment"]
        },
        "pathway": "12th Commerce/Science -> B.Com/BBA/B.Tech (3-4 Yrs) -> Junior Analyst -> Senior Financial Analyst -> Portfolio Manager / CFO",
        "sources": ["CFA Institute Global Research", "Corporate Finance Institute (CFI)", "Wall Street Prep Industry Standards"]
    },
    {
        "career_id": "product_manager",
        "career_name": "Product Manager (Tech Products)",
        "domain": "Business & Finance",
        "description": "Guides the success of a product and leads the cross-functional team that is responsible for improving it. Sits at the intersection of business, tech, and UX.",
        "typical_work": "Defines product vision and roadmaps, writes product requirement documents (PRDs), prioritizes feature backlogs, and analyzes user funnel metrics.",
        "education_paths": ["B.Tech / B.E. in any branch + MBA", "B.Tech + Product Experience", "BBA / B.Sc + Product Management Certifications"],
        "eligibility": "12th / PUC in any stream with analytical aptitude.",
        "required_skills": [
            {"skill": "Product Strategy & Roadmapping", "level": 4, "importance": "Critical"},
            {"skill": "PRD Writing & Feature Prioritization (RICE/MoSCoW)", "level": 4, "importance": "Critical"},
            {"skill": "User Experience Intuition & Wireframing", "level": 3, "importance": "High"},
            {"skill": "Product Analytics & Funnel Optimization (Mixpanel, Amplitude)", "level": 3, "importance": "High"},
            {"skill": "Technical Literacy & Engineering Alignment", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Influence Without Authority", "Strategic Prioritization", "Executive Communication", "Empathy"],
        "related_careers": ["ux_designer", "software_engineer", "management_consultant"],
        "alternative_careers": ["ux_designer", "technical_consultant", "business_analyst", "data_analyst"],
        "adjacent_careers": ["Technical Product Manager", "Growth PM", "Product Operations Lead"],
        "entry_level_roles": ["Associate Product Manager (APM)", "Product Analyst", "Product Operations Trainee"],
        "higher_study_options": ["MBA in Tech Management / Strategy", "MS in Engineering Management"],
        "certifications": ["Product School Certified Product Manager", "Reforge Product Leadership"],
        "projects": ["End-to-end PRD for an innovative feature on a popular consumer app with user stories and metric tracking", "Teardown of an onboarding flow with growth experiments"],
        "portfolio_requirements": ["Published product teardowns and comprehensive PRDs hosted on Notion/Medium"],
        "internship_options": ["APM rotational programs at high-growth startups and tech enterprises"],
        "future_skills": ["AI product management (managing non-deterministic systems)", "Data flywheel architecture", "Outcome-driven roadmap roadmaps"],
        "technology_changes": "Moving from feature factory delivery to hypothesis-driven experimentation, AI-native workflows, and automated product telemetry.",
        "AI_impact": {
            "automated_tasks": ["Drafting Jira user stories from notes", "Routine backlog deduplication"],
            "augmented_tasks": ["Customer feedback semantic clustering", "Competitive feature matrix generation"],
            "human_skills": ["High-conviction product intuition", "Saying 'no' to executive pet projects", "Inspiring cross-functional engineering and design teams"]
        },
        "pathway": "12th Any Stream -> B.Tech / Degree (4 Yrs) -> Associate Product Manager -> Product Manager -> VP of Product / Chief Product Officer",
        "sources": ["Product School Annual State of Product Management", "Reforge Product Strategy Series", "Mind the Product"]
    },
    {
        "career_id": "chartered_accountant",
        "career_name": "Chartered Accountant (CA)",
        "domain": "Business & Finance",
        "description": "Provides authoritative expertise in financial auditing, taxation, corporate finance, accounting systems, and statutory statutory compliance.",
        "typical_work": "Audits corporate financial statements, plans corporate tax strategies, assesses internal financial controls, and guides corporate restructuring.",
        "education_paths": ["ICAI Professional Program: CA Foundation -> CA Intermediate + 2-3 Yrs Articleship -> CA Final"],
        "eligibility": "12th / PUC in any stream (Commerce with Mathematics/Accountancy highly recommended).",
        "required_skills": [
            {"skill": "Auditing Standards & Assurance", "level": 4, "importance": "Critical"},
            {"skill": "Direct & Indirect Taxation (Income Tax, GST)", "level": 4, "importance": "Critical"},
            {"skill": "Corporate Financial Reporting (Ind AS / IFRS)", "level": 4, "importance": "Critical"},
            {"skill": "Corporate Law & Business Governance", "level": 3, "importance": "High"},
            {"skill": "Forensic Accounting Basics", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Impeccable Professional Ethics", "Scrupulous Accuracy", "Commercial Judgment"],
        "related_careers": ["financial_analyst", "corporate_lawyer", "management_consultant"],
        "alternative_careers": ["financial_analyst", "corporate_lawyer", "business_analyst", "data_analyst"],
        "adjacent_careers": ["Statutory Auditor", "Tax Consultant", "Chief Financial Officer (CFO)"],
        "entry_level_roles": ["Articled Assistant (mandatory training)", "Audit Executive", "Management Trainee - Accounts"],
        "higher_study_options": ["Certified Public Accountant (CPA USA)", "Chartered Financial Analyst (CFA)"],
        "certifications": ["ICAI Membership (ACA / FCA)", "DISA (Diploma in Information Systems Audit)"],
        "projects": ["Comprehensive statutory audit report of an enterprise client during articleship", "GST impact analysis and input credit optimization framework"],
        "portfolio_requirements": ["Articleship completion certificate from recognized CA firm, ICAI membership credential"],
        "internship_options": ["Mandatory 2-year practical articleship training at practicing CA firms or Big 4 accounting firms"],
        "future_skills": ["Continuous automated audit analytics", "ESG disclosure reporting assurance", "AI tax calculation verification"],
        "technology_changes": "Shift from paper sampling to 100% digital data ledger audits, automated GST matching algorithms, and automated reconciliation software.",
        "AI_impact": {
            "automated_tasks": ["Bank reconciliation matching", "Routine voucher data entry", "Basic depreciation schedule calculations"],
            "augmented_tasks": ["Audit risk anomaly detection across millions of journal entries", "Tax dispute case law semantic search"],
            "human_skills": ["Statutory signing authority and legal liability", "Advising board members on complex financial restructuring", "Ethical whistleblower judgment"]
        },
        "pathway": "12th -> CA Foundation -> CA Intermediate -> 2-3 Yrs Articleship -> CA Final -> Chartered Accountant -> Partner / CFO",
        "sources": ["Institute of Chartered Accountants of India (ICAI)", "International Federation of Accountants (IFAC)"]
    },

    # 11. Law
    {
        "career_id": "corporate_lawyer",
        "career_name": "Corporate & Commercial Lawyer",
        "domain": "Law",
        "description": "Advises businesses on their legal rights, responsibilities, commercial contracts, corporate governance, and complex M&A transactions.",
        "typical_work": "Drafts and negotiates multi-million dollar vendor contracts, conducts legal due diligence for M&A, advises boards on corporate compliance.",
        "education_paths": ["5-Year Integrated Law (B.A. LL.B. / B.B.A. LL.B. from NLUs)", "3-Year LL.B. following graduation in any discipline"],
        "eligibility": "12th / PUC in any stream with national law entrance test (CLAT / AILET in India).",
        "required_skills": [
            {"skill": "Contract Drafting & Negotiation", "level": 4, "importance": "Critical"},
            {"skill": "Corporate & Companies Law (Companies Act, SEBI)", "level": 4, "importance": "Critical"},
            {"skill": "Legal Due Diligence & M&A Protocols", "level": 3, "importance": "High"},
            {"skill": "Legal Research & Statutory Interpretation", "level": 4, "importance": "Critical"},
            {"skill": "Commercial Dispute Resolution Basics", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Persuasive Argumentation", "Rigorous Attention to Clause Detail", "Negotiation", "Discretion"],
        "related_careers": ["cyber_lawyer", "chartered_accountant", "management_consultant"],
        "alternative_careers": ["chartered_accountant", "management_consultant", "technical_writer", "product_manager"],
        "adjacent_careers": ["In-House Legal Counsel", "M&A Legal Associate", "Compliance Officer"],
        "entry_level_roles": ["Junior Legal Associate", "Legal Trainee", "In-House Counsel Intern"],
        "higher_study_options": ["LL.M. in Corporate & Commercial Law", "Master in Corporate Governance"],
        "certifications": ["Bar Council of India Enrollment (AIBE)", "Certified Corporate Governance Professional"],
        "projects": ["Drafting an end-to-end cross-border Share Purchase Agreement (SPA) with indemnification clauses", "Comprehensive legal due diligence report for a startup funding round"],
        "portfolio_requirements": ["Published legal articles in recognized law journals", "Moot court competition awards and memorials"],
        "internship_options": ["Tier-1 corporate law firms (Cyril Amarchand Mangaldas, AZB & Partners), corporate legal departments"],
        "future_skills": ["AI contract analysis auditing", "Cross-border data sovereignty compliance", "Smart legal contracts & automation"],
        "technology_changes": "Adoption of legal tech tools for instant contract clause comparison, automated discovery, and legal research vector databases.",
        "AI_impact": {
            "automated_tasks": ["Routine NDA contract review", "Citation format verification", "Standard corporate filing form population"],
            "augmented_tasks": ["Precedent case law search across decades of Supreme Court rulings", "Risk flagging in 100-page lease agreements"],
            "human_skills": ["High-stakes commercial negotiation tactics", "Fiduciary risk counseling for CEOs", "Advocacy in courtroom and arbitration"]
        },
        "pathway": "12th Any Stream -> CLAT -> 5-Yr B.A. LL.B. -> Bar Enrollment -> Associate at Law Firm -> Senior Associate -> Partner / General Counsel",
        "sources": ["Bar Council of India (BCI)", "American Bar Association (ABA)", "Legally India Corporate Rankings"]
    },
    {
        "career_id": "cyber_lawyer",
        "career_name": "Cyber Law & Digital Privacy Attorney",
        "domain": "Law",
        "description": "Specializes in legal regulations surrounding data privacy (DPDP / GDPR), cybersecurity breaches, intellectual property in code, and cybercrime.",
        "typical_work": "Drafts enterprise privacy policies, advises on breach disclosure requirements, litigates digital intellectual property disputes, and audits compliance.",
        "education_paths": ["5-Year B.A. LL.B. / B.Sc LL.B. with Cyber Law specialization", "LL.B. + Post Graduate Diploma in Cyber Law"],
        "eligibility": "12th / PUC in any stream with interest in technology and law.",
        "required_skills": [
            {"skill": "Data Protection Laws (GDPR, India DPDP Act)", "level": 4, "importance": "Critical"},
            {"skill": "Cyber Crime Legislation & IT Act", "level": 4, "importance": "Critical"},
            {"skill": "Tech Contracts & Cloud Service Agreements", "level": 3, "importance": "High"},
            {"skill": "Digital Evidence & Electronic Discovery", "level": 3, "importance": "High"},
            {"skill": "Basic Understanding of Cyber Attacks & Networks", "level": 2, "importance": "Medium"}
        ],
        "soft_skills": ["Analytical Precision", "Cross-disciplinary Communication", "Fast Technical Learning"],
        "related_careers": ["corporate_lawyer", "digital_forensics_analyst", "cybersecurity_analyst"],
        "alternative_careers": ["corporate_lawyer", "cybersecurity_analyst", "technical_writer", "digital_forensics_analyst"],
        "adjacent_careers": ["Data Protection Officer (DPO)", "Privacy Counsel", "Tech Policy Strategist"],
        "entry_level_roles": ["Junior Privacy Associate", "Cyber Law Researcher", "Legal Tech Associate"],
        "higher_study_options": ["LL.M. in Technology, Media & Telecommunications (TMT) Law", "Master in Cyber Law"],
        "certifications": ["CIPP/E (Certified Information Privacy Professional/Europe)", "CIPM (Certified Information Privacy Manager)"],
        "projects": ["Comprehensive DPDP Act 2023 compliance audit checklist and privacy impact assessment for an e-commerce platform", "Drafting a Data Processing Agreement (DPA)"],
        "portfolio_requirements": ["Published research papers on data privacy or AI regulation", "Sample privacy policies and cross-border transfer agreements"],
        "internship_options": ["TMT practice groups at law firms, tech conglomerate legal teams (Google, Microsoft), privacy consultancies"],
        "future_skills": ["Generative AI copyright liability assessment", "Biometric data regulation compliance", "Autonomous system liability law"],
        "technology_changes": "Rapid emergence of global data sovereignty mandates, generative AI copyright litigation, and mandatory rapid breach disclosure laws.",
        "AI_impact": {
            "automated_tasks": ["Checking standard website privacy notice checkboxes", "Cataloging standard cookie consent scripts"],
            "augmented_tasks": ["Mapping data flows across cross-border cloud providers", "Summarizing new regulatory bills across multiple jurisdictions"],
            "human_skills": ["Navigating complex international jurisdictional conflicts", "Balancing business innovation with strict regulatory liability"]
        },
        "pathway": "12th Any Stream -> 5-Yr Integrated Law (5 Yrs) -> Bar Enrollment -> Cyber/TMT Legal Associate -> Senior Privacy Counsel -> Global DPO",
        "sources": ["International Association of Privacy Professionals (IAPP)", "Cyber Law Association of India", "Electronic Frontier Foundation"]
    },

    # 12. Agriculture
    {
        "career_id": "precision_agriculture_specialist",
        "career_name": "Precision Agriculture & AgriTech Specialist",
        "domain": "Agriculture",
        "description": "Applies IoT sensors, GPS mapping, drone multispectral imagery, and data modeling to optimize crop yields and sustainable farming.",
        "typical_work": "Analyzes soil nutrient maps, programs drone flight plans for crop health assessment, optimizes automated drip irrigation, and advises farmers.",
        "education_paths": ["B.Sc in Agriculture / Agricultural Engineering", "B.Tech in Agricultural Information Technology", "B.Sc in Agronomy"],
        "eligibility": "12th / PUC with Physics, Chemistry, and Biology/Mathematics (min 50-55%).",
        "required_skills": [
            {"skill": "Agronomy Principles & Soil Health", "level": 4, "importance": "Critical"},
            {"skill": "GIS & Remote Sensing for Agriculture", "level": 4, "importance": "Critical"},
            {"skill": "Agri-IoT & Sensor Integration", "level": 3, "importance": "High"},
            {"skill": "Drone Multispectral Image Analysis", "level": 3, "importance": "High"},
            {"skill": "Precision Irrigation & Nutrient Management", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Field Resilience", "Farmer Empathy", "Analytical Practicality"],
        "related_careers": ["environmental_scientist", "food_technologist", "biotechnologist"],
        "alternative_careers": ["environmental_scientist", "data_analyst", "biotechnologist", "renewable_energy_engineer"],
        "adjacent_careers": ["Crop Yield Modeler", "Agri-Drone Pilot", "Smart Farming Consultant"],
        "entry_level_roles": ["Junior AgriTech Executive", "Field Agronomist Trainee", "Precision Farming Associate"],
        "higher_study_options": ["M.Sc in Precision Agriculture", "M.Tech in Farm Machinery & Smart Agriculture"],
        "certifications": ["DGCA Drone Pilot License (for agricultural spraying/mapping)", "Precision Agriculture Professional Certificate"],
        "projects": ["Field NDVI crop stress analysis using open satellite imagery (Sentinel-2) and QGIS", "IoT smart irrigation controller setup based on soil moisture data"],
        "portfolio_requirements": ["Field research reports, spatial mapping portfolios displaying vegetation indices"],
        "internship_options": ["AgTech startups (DeHaat, Cropin), fertilizer & seed R&D companies, government agricultural universities"],
        "future_skills": ["AI-driven automated crop disease classification", "Autonomous electric robotic weeding", "Carbon credit soil sequestration verification"],
        "technology_changes": "Transitioning from traditional calendar-based spraying to micro-variable rate application (VRA) guided by real-time satellite telemetry.",
        "AI_impact": {
            "automated_tasks": ["Satellite cloud cover filtering", "Routine soil moisture logging"],
            "augmented_tasks": ["Pest outbreak prediction models", "Optimal harvest window forecasting"],
            "human_skills": ["Translating complex sensor dashboards into actionable advice for rural farmers", "Ground-truth field verification"]
        },
        "pathway": "12th PCB/PCM -> B.Sc Agriculture (4 Yrs) -> AgriTech Field Trainee -> Precision Farming Specialist -> Chief Agronomist",
        "sources": ["ICAR (Indian Council of Agricultural Research)", "International Society of Precision Agriculture (ISPA)", "FAO Smart Agriculture"]
    },

    # 13. Environment
    {
        "career_id": "environmental_scientist",
        "career_name": "Environmental Scientist & Impact Assessor",
        "domain": "Environment",
        "description": "Monitors ecological systems, analyzes pollution samples, and conducts Environmental Impact Assessments (EIA) to safeguard natural ecosystems.",
        "typical_work": "Conducts air and water quality sampling in the field, models pollutant dispersion, prepares statutory EIA reports, and advises industries on green remediation.",
        "education_paths": ["B.Sc in Environmental Science / Ecology", "B.Tech in Environmental Engineering", "M.Sc in Environmental Science & Management"],
        "eligibility": "12th / PUC with Science (Physics, Chemistry, Biology/Mathematics).",
        "required_skills": [
            {"skill": "Environmental Impact Assessment (EIA) Procedures", "level": 4, "importance": "Critical"},
            {"skill": "Water, Soil & Air Quality Laboratory Analysis", "level": 4, "importance": "Critical"},
            {"skill": "Environmental Regulations & Statutory Standards", "level": 4, "importance": "High"},
            {"skill": "GIS for Environmental Modeling (QGIS / ArcGIS)", "level": 3, "importance": "High"},
            {"skill": "Ecological Remediation Techniques", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Scientific Objectivity", "Environmental Ethics", "Clear Report Writing"],
        "related_careers": ["renewable_energy_engineer", "precision_agriculture_specialist", "biotechnologist"],
        "alternative_careers": ["renewable_energy_engineer", "data_analyst", "precision_agriculture_specialist", "research_scientist"],
        "adjacent_careers": ["Sustainability Specialist", "Pollution Control Officer", "Conservation Ecologist"],
        "entry_level_roles": ["Junior Environmental Scientist", "EIA Assistant", "Field Sampling Officer"],
        "higher_study_options": ["M.Sc in Environmental Engineering", "Ph.D. in Climate Science & Mitigation"],
        "certifications": ["NABET Certified EIA Functional Area Expert", "ISO 14001 Environmental Lead Auditor"],
        "projects": ["Comprehensive watershed water quality assessment across 10 sample stations with statistical remediation report", "Air pollution dispersion simulation"],
        "portfolio_requirements": ["Field research documentation, statutory EIA project write-ups, GIS environmental hazard maps"],
        "internship_options": ["State Pollution Control Boards, environmental consulting engineering firms, ecological conservation NGOs"],
        "future_skills": ["Carbon accounting & Scope 1/2/3 greenhouse gas auditing", "Biodiversity credit monitoring", "Climate risk scenario modeling"],
        "technology_changes": "Transitioning from manual point sampling to continuous IoT environmental sensor arrays, drone multispectral environmental audits, and AI modeling.",
        "AI_impact": {
            "automated_tasks": ["Continuous sensor baseline alerting", "Standard compliance report checklist formatting"],
            "augmented_tasks": ["Predictive air quality dispersion forecasting", "Satellite deforestation pattern detection"],
            "human_skills": ["Public stakeholder hearing facilitation", "Balancing economic development with conservation ethics", "Court testimony on environmental harm"]
        },
        "pathway": "12th Science -> B.Sc / B.Tech Environmental Science (3-4 Yrs) -> Environmental Trainee -> Environmental Specialist -> Senior EIA Director",
        "sources": ["Ministry of Environment, Forest and Climate Change (MoEFCC)", "United Nations Environment Programme (UNEP)", "EPA Guidelines"]
    },
    {
        "career_id": "renewable_energy_engineer",
        "career_name": "Renewable Energy & Solar Systems Engineer",
        "domain": "Environment",
        "description": "Designs, models, installs, and optimizes clean energy generation infrastructure including solar photovoltaic parks, wind farms, and battery storage.",
        "typical_work": "Simulates solar irradiance yields in PVsyst, designs electrical balance of plant (BOP), inspects solar inverter performance, and models grid integration.",
        "education_paths": ["B.Tech in Electrical Engineering / Mechanical Engineering / Energy Engineering", "B.Tech in Renewable Energy"],
        "eligibility": "12th / PUC with Mathematics and Physics.",
        "required_skills": [
            {"skill": "Solar PV System Design & Simulation (PVsyst, Helioscope)", "level": 4, "importance": "Critical"},
            {"skill": "Electrical Single Line Diagrams & Balance of Plant", "level": 4, "importance": "Critical"},
            {"skill": "Grid Integration & Power Electronics Basics", "level": 3, "importance": "High"},
            {"skill": "Battery Energy Storage Systems (BESS)", "level": 3, "importance": "High"},
            {"skill": "Renewable Project Financial Modeling (LCOE)", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Practical Engineering Logic", "Project Management", "Safety Consciousness"],
        "related_careers": ["environmental_scientist", "embedded_engineer", "cloud_architect"],
        "alternative_careers": ["environmental_scientist", "software_engineer", "precision_agriculture_specialist", "technical_consultant"],
        "adjacent_careers": ["Wind Power Engineer", "Energy Auditor", "Microgrid Design Specialist"],
        "entry_level_roles": ["Graduate Engineer Trainee - Solar", "Junior Design Engineer", "Site Commissioning Trainee"],
        "higher_study_options": ["M.Tech in Renewable Energy Technologies", "MS in Sustainable Energy Systems"],
        "certifications": ["NABCEP Certified PV Installation Professional", "Certified Energy Manager (BEE India)"],
        "projects": ["Design of a 1 MW rooftop solar PV system with string inverter layout and shading analysis in PVsyst", "BESS capacity sizing calculation for solar smoothing"],
        "portfolio_requirements": ["PVsyst simulation reports, AutoCAD electrical single-line diagrams, engineering calculation sheets"],
        "internship_options": ["Solar EPC developers (Tata Power Solar, Adani Green), clean energy consultancies, battery technology startups"],
        "future_skills": ["Green hydrogen electrolyzer integration", "AI-driven solar forecasting and grid dispatch", "Smart bidirectional EV charging infrastructure"],
        "technology_changes": "Adoption of bifacial solar modules, utility-scale battery storage, digital twin predictive maintenance, and virtual power plants (VPPs).",
        "AI_impact": {
            "automated_tasks": ["Inverter error code logging", "Standard string calculation sizing tables"],
            "augmented_tasks": ["Solar irradiance forecasting from cloud satellite feeds", "Drone thermal image fault detection on solar panels"],
            "human_skills": ["On-site high-voltage safety commissioning", "Overcoming local grid interconnect engineering hurdles", "Project financing defense"]
        },
        "pathway": "12th PCM -> B.Tech Electrical/Energy (4 Yrs) -> Solar Design Trainee -> Renewable Energy Engineer -> Lead Energy Architect",
        "sources": ["International Renewable Energy Agency (IRENA)", "Ministry of New and Renewable Energy (MNRE)", "IEEE Power and Energy Society"]
    },

    # 14. Hospitality & Tourism
    {
        "career_id": "hotel_manager",
        "career_name": "Luxury Hotel General Manager",
        "domain": "Hospitality & Tourism",
        "description": "Leads all operational and commercial facets of a luxury resort or hotel, orchestrating guest experience, revenue management, and team excellence.",
        "typical_work": "Inspects operational standards across rooms and F&B, oversees dynamic room pricing yield strategies, handles high-profile VIP guests, and manages P&L.",
        "education_paths": ["B.Sc in Hospitality & Hotel Administration (NCHMCT)", "BHM (Bachelor of Hotel Management)", "BBA in Hospitality"],
        "eligibility": "12th / PUC in any stream with strong communication and hospitality aptitude.",
        "required_skills": [
            {"skill": "Hotel Operations Management (Front Office, Housekeeping, F&B)", "level": 4, "importance": "Critical"},
            {"skill": "Hospitality Revenue Management & RevPAR Optimization", "level": 4, "importance": "Critical"},
            {"skill": "Hotel PMS Systems (Opera, Fidelio)", "level": 3, "importance": "High"},
            {"skill": "Luxury Service Standards & Guest Experience Design", "level": 4, "importance": "Critical"},
            {"skill": "Hospitality P&L & Cost Control", "level": 3, "importance": "Medium"}
        ],
        "soft_skills": ["Exceptional Warmth", "Crisis Composure", "Impeccable Grooming & Etiquette", "Inspiring Leadership"],
        "related_careers": ["event_director", "chef", "tourism_consultant"],
        "alternative_careers": ["event_director", "digital_marketer", "product_manager", "corporate_lawyer"],
        "adjacent_careers": ["Director of Rooms", "Food & Beverage Director", "Resort Operations Lead"],
        "entry_level_roles": ["Management Trainee (MT)", "Guest Service Associate", "Front Desk Officer"],
        "higher_study_options": ["MBA in International Hospitality Management (EHL Switzerland)", "Master in Tourism Management"],
        "certifications": ["CHA (Certified Hotel Administrator - AHLA)", "WSET Level 2/3 Certification"],
        "projects": ["Complete hotel opening operational checklist and guest journey map for a 150-room boutique hotel", "Revenue yield strategy case study maximizing RevPAR"],
        "portfolio_requirements": ["Hospitality management training completion certificates, operational audit records"],
        "internship_options": ["6-month industrial exposure training in 5-star hotel properties (Taj, Marriott, Oberoi)"],
        "future_skills": ["Hyper-personalized guest AI concierge integration", "Sustainable eco-resort zero-waste management", "Contactless luxury service balance"],
        "technology_changes": "Adoption of dynamic algorithmic room pricing, automated mobile check-ins, guest preference AI profiling, and energy management IoT.",
        "AI_impact": {
            "automated_tasks": ["Routine booking confirmation messages", "Standard room billing folio generation"],
            "augmented_tasks": ["Dynamic yield pricing based on city-wide event demand", "Guest preference pattern tracking across stays"],
            "human_skills": ["Genuine personal human hospitality", "De-escalating delicate VIP guest grievances", "In-person staff morale and team culture"]
        },
        "pathway": "12th Any Stream -> B.Sc Hospitality (3 Yrs) -> Management Trainee -> Department Manager -> Resident Manager -> General Manager",
        "sources": ["National Council for Hotel Management and Catering Technology (NCHMCT)", "American Hotel & Lodging Educational Institute (AHLEI)"]
    },

    # 15. Education
    {
        "career_id": "edtech_instructional_designer",
        "career_name": "Instructional Designer & Learning Experience Architect",
        "domain": "Education",
        "description": "Designs evidence-based, interactive online courses, learning simulations, and corporate upskilling programs grounded in cognitive learning science.",
        "typical_work": "Conducts learning needs analysis, architects curriculum blueprints, develops interactive course modules in Articulate Storyline, and evaluates efficacy.",
        "education_paths": ["B.A. / B.Sc in Education or Psychology", "M.A. in Instructional Design / Educational Technology", "B.Tech + EdTech Diploma"],
        "eligibility": "12th / PUC in any stream with strong pedagogical interest and structured communication.",
        "required_skills": [
            {"skill": "Instructional Design Models (ADDIE, Bloom's Taxonomy, SAM)", "level": 4, "importance": "Critical"},
            {"skill": "Authoring Tools (Articulate 360, Storyline, Rise)", "level": 4, "importance": "Critical"},
            {"skill": "Learning Management Systems (Canvas, Moodle)", "level": 3, "importance": "High"},
            {"skill": "Micro-learning & Gamification Design", "level": 3, "importance": "High"},
            {"skill": "Assessment & Rubric Construction", "level": 4, "importance": "Critical"}
        ],
        "soft_skills": ["Pedagogical Empathy", "Conceptual Clarity", "Storyboarding", "Creativity"],
        "related_careers": ["teacher", "ux_designer", "technical_writer"],
        "alternative_careers": ["technical_writer", "ux_designer", "organizational_psychologist", "product_manager"],
        "adjacent_careers": ["Learning Experience Designer (LXD)", "Curriculum Architect", "E-Learning Developer"],
        "entry_level_roles": ["Junior Instructional Designer", "E-Learning Content Developer", "Course Development Associate"],
        "higher_study_options": ["M.Ed in Educational Technology", "MS in Instructional Systems Technology"],
        "certifications": ["ATD Master Instructional Designer", "Association for Educational Communications and Technology (AECT)"],
        "projects": ["Interactive, gamified 4-module digital course with knowledge checks built in Articulate Storyline", "Comprehensive curriculum map following Bloom's taxonomy"],
        "portfolio_requirements": ["Live portfolio with interactive course samples, storyboards, and learner evaluation reports"],
        "internship_options": ["EdTech companies (Coursera, Khan Academy), university e-learning centers, corporate training academies"],
        "future_skills": ["AI-driven adaptive personalized learning paths", "Immersive VR educational simulation design", "Competency-based automated grading validation"],
        "technology_changes": "Evolution from static video lectures and PDF quizzes to adaptive interactive problem sandboxes, AI tutoring companions, and competency graphs.",
        "AI_impact": {
            "automated_tasks": ["Drafting multiple-choice quiz distractors", "Course transcript formatting"],
            "augmented_tasks": ["Adapting reading levels to individual student grade standards", "Translating course content across languages"],
            "human_skills": ["Crafting emotionally engaging narrative learning journeys", "Sensing cognitive student frustration", "Fostering authentic inquiry"]
        },
        "pathway": "12th Any Stream -> Degree in Education/Arts/Tech (3-4 Yrs) -> E-Learning Developer -> Instructional Designer -> Chief Learning Officer",
        "sources": ["Association for Talent Development (ATD)", "International Society for Technology in Education (ISTE)", "EDUCAUSE Review"]
    },

    # 16. Skilled & Vocational
    {
        "career_id": "precision_machinist",
        "career_name": "CNC Precision Machining Specialist",
        "domain": "Skilled/Vocational",
        "description": "Programs, sets up, and operates high-precision Computer Numerical Control (CNC) multi-axis milling and turning machines to fabricate aerospace and medical components.",
        "typical_work": "Reads engineering blueprints with GD&T tolerances, writes G-code/CAM programs in Mastercam, measures parts with coordinate measuring machines (CMM).",
        "education_paths": ["Diploma in Mechanical Engineering / Tool & Die Making (3 Yrs)", "ITI Machinist / CNC Certification (2 Yrs)", "B.Voc in Precision Manufacturing"],
        "eligibility": "10th / 12th with Mathematics and Science aptitude.",
        "required_skills": [
            {"skill": "CNC Programming (G-Code & M-Code, CAM)", "level": 4, "importance": "Critical"},
            {"skill": "Geometric Dimensioning & Tolerancing (GD&T)", "level": 4, "importance": "Critical"},
            {"skill": "Multi-Axis Milling & Turning Setup", "level": 4, "importance": "Critical"},
            {"skill": "Precision Metrology (Micrometers, Calipers, CMM)", "level": 3, "importance": "High"},
            {"skill": "Cutting Tool Selection & Feeds/Speeds", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Extreme Mechanical Precision", "Safety Rigor", "Patience", "Spatial Reasoning"],
        "related_careers": ["mechanical_engineer", "industrial_automation_technician", "biomedical_equipment_specialist"],
        "alternative_careers": ["industrial_automation_technician", "robotics_engineer", "qa_automation_engineer"],
        "adjacent_careers": ["CAM Programmer", "Tool & Die Maker", "Quality Inspection Technician"],
        "entry_level_roles": ["Junior CNC Operator", "Machinist Trainee", "CAM Apprentice"],
        "higher_study_options": ["Advanced Diploma in Die & Mould Technology (NTTF/CIPET)", "B.Tech in Manufacturing Engineering (Lateral Entry)"],
        "certifications": ["NIMS Machinist Certification", "Mastercam Certified Associate"],
        "projects": ["Program and machine a complex 5-axis aerospace titanium turbine bracket following micron tolerances", "CMM dimensional inspection report"],
        "portfolio_requirements": ["Photographs and video logs of precision-machined physical parts, verified CAM toolpath simulations"],
        "internship_options": ["Aerospace component machining suppliers, medical implant manufacturers, automotive toolrooms"],
        "future_skills": ["Hybrid additive-subtractive manufacturing", "Digital twin in-situ tool wear monitoring", "Autonomous robotics CNC tending"],
        "technology_changes": "Transitioning from manual 3-axis mills to 5-axis simultaneous machining, automated pallet changers, and sensorized live tool vibration monitoring.",
        "AI_impact": {
            "automated_tasks": ["Basic toolpath generation for standard pockets", "Standard feed rate lookup table matching"],
            "augmented_tasks": ["Vibration acoustic anomaly detection for tool breakage prediction", "Thermal expansion compensation"],
            "human_skills": ["Hands-on physical machine setup and fixture clamping feel", "Interpreting subtle material stress warpage in exotic alloys"]
        },
        "pathway": "10th/12th -> ITI / Diploma Tool & Die (3 Yrs) -> CNC Operator -> CNC Specialist / CAM Programmer -> Plant Toolroom Head",
        "sources": ["National Institute for Metalworking Skills (NIMS)", "NTTF (Nettur Technical Training Foundation)", "Modern Machine Shop Magazine"]
    },

    # 17. Emerging Careers
    {
        "career_id": "prompt_workflow_engineer",
        "career_name": "AI Workflow & Agentic Systems Engineer",
        "domain": "Emerging Careers",
        "description": "Architects multi-agent autonomous LLM workflows, structured evaluation pipelines, and context-augmented retrieval systems for enterprise deployment.",
        "typical_work": "Builds stateful agent graphs in LangGraph, evaluates prompt reliability with automated benchmarks, optimizes vector RAG, and governs hallucination safeguards.",
        "education_paths": ["B.Tech / B.E. in Computer Science or Software Engineering", "BCA + Modern AI Engineering Specializations", "Self-Taught Portfolio with Open Source"],
        "eligibility": "12th / PUC with Mathematics and Computer Science.",
        "required_skills": [
            {"skill": "Agentic Frameworks (LangGraph, CrewAI, AutoGen)", "level": 4, "importance": "Critical"},
            {"skill": "Advanced Prompt Engineering & Guardrails (NeMo, Guidance)", "level": 4, "importance": "Critical"},
            {"skill": "RAG Architectures & Vector Databases (pgvector, Pinecone)", "level": 4, "importance": "Critical"},
            {"skill": "Python & Async API Development (FastAPI)", "level": 3, "importance": "High"},
            {"skill": "LLM Evaluation Benchmarks (Ragas, TruLens)", "level": 3, "importance": "High"}
        ],
        "soft_skills": ["Systems Architecture Thinking", "Empirical Experimentation", "Clear Communication", "Fast Adaptability"],
        "related_careers": ["ai_engineer", "software_engineer", "data_scientist"],
        "alternative_careers": ["software_engineer", "ai_engineer", "technical_consultant", "product_manager"],
        "adjacent_careers": ["LLM Application Developer", "Cognitive Systems Architect", "AI Integration Specialist"],
        "entry_level_roles": ["Junior AI Engineer", "Agent Systems Trainee", "LLM Integration Associate"],
        "higher_study_options": ["MS in Artificial Intelligence Systems", "Executive Master in Applied Generative AI"],
        "certifications": ["DeepLearning.AI LangChain / LangGraph Specialist", "AWS Certified Machine Learning Engineer"],
        "projects": ["Build a production multi-agent research analyst graph with verification loops and pgvector RAG", "Automated LLM hallucination benchmark suite with Ragas"],
        "portfolio_requirements": ["Public GitHub repository showcasing functional LangGraph agent architectures and evaluation metrics"],
        "internship_options": ["AI native startups, enterprise innovation incubators, developer tooling companies"],
        "future_skills": ["Multi-modal agentic computer vision control", "Autonomous code synthesis verification", "Local quantized edge model fine-tuning"],
        "technology_changes": "Rapid shift from single prompt-response interactions to stateful, cyclic multi-agent graphs equipped with tools, memory, and reflection.",
        "AI_impact": {
            "automated_tasks": ["Basic prompt formatting templates", "Simple schema extraction parsers"],
            "augmented_tasks": ["Systematic automated red-teaming", "Synthetic test query generation for RAG benchmarking"],
            "human_skills": ["Architecting deterministic governance over non-deterministic models", "Systemic safety and ethical alignment boundaries"]
        },
        "pathway": "12th Science -> B.Tech CS (4 Yrs) -> Software/AI Engineer -> AI Workflow Engineer -> Chief AI Architect",
        "sources": ["LangChain / LangGraph Architectural Guides", "Hugging Face Generative AI Reports", "Stanford AI Index Report"]
    }
]

def main():
    os.makedirs("data/careers", exist_ok=True)
    out_path = "data/careers/careers.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(CAREERS, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(CAREERS)} core careers in {out_path}")

if __name__ == "__main__":
    main()
