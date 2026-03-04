Here’s a **clean, professional README you can paste directly into GitHub’s README editor**. No commands, no extra formatting headaches — just copy everything below.

---

# Clara AI Transcript Configuration Pipeline

## Overview

This project implements a pipeline that converts **customer call transcripts into structured configuration artifacts** used to deploy AI voice agents.

The system processes two types of transcripts:

* **Demo Call Transcripts** → Generate an initial configuration
* **Onboarding Call Transcripts** → Update and refine the configuration

The pipeline extracts operational information such as services offered, business hours, contact details, integrations, pricing, and routing rules, then converts this information into structured JSON outputs.

It also maintains **versioned configurations** and tracks changes between versions.

---

## System Workflow

Demo Transcript
↓
Demo Extraction
↓
Account Memo (v1)
↓
Agent Configuration (v1)
↓
Onboarding Transcript
↓
Onboarding Extraction
↓
Account Memo (v2)
↓
Agent Configuration (v2)
↓
Configuration Diff
↓
Change Log

---

## Project Structure

```
clara-ai-transcript-pipeline

dataset/
    demo_calls/
    onboarding_calls/

scripts/
    extract_demo.py
    extract_onboarding.py
    diff_generator.py
    agent_generator.py
    batch_runner.py
    logger.py

templates/
    agent_prompt.txt

outputs/
    accounts/
        account1/
            v1/
            v2/
            changes.json

dashboard.py
run_pipeline.py
README.md
```

---

## Features

### Transcript Processing

Extracts structured information from unstructured call transcripts.

Information extracted includes:

* Company name
* Services offered
* Business hours
* Email addresses
* Phone numbers
* Pricing mentions
* Software integrations
* Emergency definitions
* Call routing rules

---

### Configuration Generation

The pipeline generates two primary artifacts:

**Account Memo (`memo.json`)**
A structured representation of operational details extracted from transcripts.

**Agent Configuration (`agent.json`)**
Defines the AI voice agent’s behavior for handling incoming customer calls.

---

### Versioning

Each account configuration is versioned.

* **v1** → Generated from the demo transcript
* **v2** → Updated using onboarding transcript data

This mirrors how real systems evolve as more client information becomes available.

---

### Change Tracking

A diff generator compares configuration versions and produces a change log.

Example changes:

* Business hours updated
* Emergency routing rules added
* New integrations confirmed
* Contact information updated

All changes are stored in `changes.json`.

---

### Dashboard Viewer

A simple **Streamlit dashboard** allows users to inspect generated configurations.

The dashboard allows users to:

* Select an account
* Select configuration version
* View account memo
* View agent configuration
* Inspect configuration changes

---

## Running the Project

1. Install dependencies

```
pip install streamlit
```

2. Run the pipeline

```
python run_pipeline.py
```

3. Launch the dashboard

```
streamlit run dashboard.py
```

Open the dashboard at:

```
http://localhost:8501
```

---

## Example Output

Example generated memo:

```
{
  "company_name": "Apex Electrical Services",
  "services_supported": [
    "electrical",
    "generator",
    "lighting",
    "panel"
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
```

---

## Design Principles

**Deterministic Extraction**
The system extracts only information explicitly present in transcripts.

**No Hallucination**
Missing information remains empty and is flagged as unknown.

**Incremental Configuration**
Onboarding transcripts refine and extend existing configuration rather than replacing it.

**Traceable Changes**
All updates between configuration versions are tracked.

---

## Technologies Used

* Python
* Regex-based text extraction
* JSON configuration generation
* Streamlit dashboard
* Git version control

---

## Author

Divyansh Rao

---

If you want, I can also help you add **one small section that makes the README look like a real startup project (with architecture + pipeline diagram)** which makes the repo look **way more impressive to recruiters.**
