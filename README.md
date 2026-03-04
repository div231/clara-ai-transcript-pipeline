Clara AI Transcript Configuration Pipeline
Overview
This project implements a pipeline that converts customer call transcripts into structured configuration artifacts used to deploy AI voice agents.

The system processes two types of transcripts:

Demo Call Transcripts → Generate initial configuration

Onboarding Call Transcripts → Update and refine configuration

The pipeline extracts relevant information such as services, business hours, integrations, contact details, and emergency routing logic, and converts it into structured JSON outputs.

It also generates versioned configurations and tracks changes between versions.

System Architecture
Demo Transcript
      │
      ▼
Demo Extractor
      │
      ▼
Account Memo v1
      │
      ▼
Agent Configuration v1
      │
      ▼
Onboarding Transcript
      │
      ▼
Onboarding Extractor
      │
      ▼
Account Memo v2
      │
      ▼
Agent Configuration v2
      │
      ▼
Diff Generator
      │
      ▼
Change Log
Project Structure
clara-ai-transcript-pipeline
│
├── dataset
│   ├── demo_calls
│   │   ├── account1.txt
│   │   ├── account2.txt
│   │   └── ...
│   │
│   └── onboarding_calls
│       ├── account1.txt
│       ├── account2.txt
│       └── ...
│
├── outputs
│   └── accounts
│       ├── account1
│       │   ├── v1
│       │   │   ├── memo.json
│       │   │   └── agent.json
│       │   │
│       │   ├── v2
│       │   │   ├── memo.json
│       │   │   └── agent.json
│       │   │
│       │   └── changes.json
│       │
│       └── ...
│
├── scripts
│   ├── extract_demo.py
│   ├── extract_onboarding.py
│   ├── diff_generator.py
│   ├── agent_generator.py
│   ├── batch_runner.py
│   └── logger.py
│
├── templates
│   └── agent_prompt.txt
│
├── dashboard.py
├── run_pipeline.py
└── README.md
Features
Transcript Processing
Extracts structured data from unstructured call transcripts.

Extracted fields include:

Company name

Services offered

Business hours

Phone numbers

Email addresses

Pricing mentions

Software integrations

Emergency definitions

Call routing rules

Configuration Generation
Produces structured configuration artifacts:

Account Memo

memo.json
Contains operational details extracted from transcripts.

Agent Configuration

agent.json
Defines how the AI voice agent should behave.

Versioning
Each account configuration is versioned:

v1 → generated from demo transcript
v2 → updated with onboarding transcript
This simulates how real systems evolve as more customer information becomes available.

Change Tracking
A diff generator compares configuration versions and produces:

changes.json
This shows what changed between v1 and v2.

Example:

business_hours: null → 8am - 5pm
emergency_definition added
call_transfer_rules added
Dashboard Viewer
A simple Streamlit dashboard allows exploration of generated configurations.

Users can:

Select account

Select version

View memo

View agent configuration

Inspect configuration changes

Running the Pipeline
1 Install Dependencies
pip install streamlit
2 Run the Pipeline
python run_pipeline.py
This processes all transcripts and generates outputs.

3 Launch Dashboard
streamlit run dashboard.py
Then open:

http://localhost:8501
Example Output
Example generated memo:

{
  "company_name": "Apex Electrical Services",
  "services_supported": [
    "electrical",
    "generator",
    "panel",
    "lighting"
  ],
  "business_hours": "8am - 5pm",
  "integration_constraints": [
    "jobber",
    "quickbooks"
  ],
  "phone_numbers": [
    "214-555-9812"
  ],
  "emails": [
    "mike@apexelectrical.com"
  ]
}
Design Principles
The pipeline follows several principles:

Deterministic Extraction
Only extract information explicitly present in transcripts.

No Hallucination
Missing data remains null and is flagged as unknown.

Incremental Configuration
Onboarding transcripts update existing configuration rather than replacing it.

Traceable Changes
All configuration updates are recorded via diffs.

Technologies Used
Python

Regex-based text extraction

JSON configuration generation

Streamlit dashboard

Git version control

Future Improvements
Possible enhancements include:

NLP-based entity extraction

LLM-assisted transcript parsing

automatic routing rule generation

integration validation

richer dashboard analytics

Author
Divyansh Rao

License
This project is for demonstration and educational purposes.
