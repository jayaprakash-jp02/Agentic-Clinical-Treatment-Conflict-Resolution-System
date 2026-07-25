# Agentic Clinical Treatment Conflict Resolution System

## Overview

The **Agentic Clinical Treatment Conflict Resolution System** is an AI-powered clinical decision support system that assists in resolving treatment conflicts for patients with multiple co-existing diseases.

Unlike traditional systems that generate a single recommendation, this project uses multiple specialist AI agents to independently analyze the patient's condition, retrieve evidence from clinical guidelines using Retrieval-Augmented Generation (RAG), identify conflicting treatment recommendations, negotiate conflicts, and generate a consensus-based clinical recommendation.

---

## Problem Statement

Patients suffering from multiple chronic diseases often receive conflicting treatment recommendations from different clinical specialties. These conflicts may lead to medication interactions, contraindications, and inconsistent treatment plans.

This project aims to automate the process of:

- Understanding patient information
- Consulting multiple virtual specialist agents
- Retrieving evidence from medical guidelines
- Detecting treatment conflicts
- Resolving conflicts through a planner-driven negotiation process
- Producing a unified clinical recommendation

---

## Supported Diseases

Currently the system supports:

- Diabetes Mellitus
- Chronic Kidney Disease (CKD)
- Hypertension
- Heart Failure

---

## Key Features

- Multi-Agent Clinical Reasoning
- Retrieval-Augmented Generation (RAG)
- Specialist-specific guideline retrieval
- Conflict detection between specialist recommendations
- Planner-based negotiation workflow
- Consensus generation
- Structured final clinical report
- Local LLM inference using Ollama
- Offline execution without cloud APIs

---

## System Architecture

```
Patient JSON
      │
      ▼
Patient Understanding Agent
      │
      ▼
Patient Context
      │
      ▼
Consultation Engine
      │
      ▼
Specialist Agents
(Cardiology, Nephrology,
Endocrinology, General Medicine)
      │
      ▼
Guideline Retrieval (RAG)
      │
      ▼
Specialist Recommendations
      │
      ▼
Conflict Detection
      │
      ▼
Negotiation Loop
      │
      ▼
Consensus Builder
      │
      ▼
Decision Support Agent
      │
      ▼
Final Clinical Recommendation
```

---

## Project Structure

```
Agentic-Clinical-Treatment-Conflict-Resolution-System/

├── agents/
├── knowledge/
├── llm/
├── models/
├── planner/
├── prompts/
├── state/
├── tests/
├── utils/
├── data/
├── main.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| Local LLM | Ollama (Qwen 2.5) |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| PDF Processing | PyMuPDF |
| Data Validation | Pydantic |
| Architecture | Multi-Agent System |
| Knowledge Retrieval | Retrieval-Augmented Generation (RAG) |

---

## Workflow

1. Load patient information.
2. Generate structured patient context.
3. Identify required specialists.
4. Retrieve relevant clinical guidelines.
5. Generate specialist recommendations.
6. Detect treatment conflicts.
7. Resolve conflicts using planner-driven negotiation.
8. Build consensus recommendations.
9. Generate the final clinical decision support report.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/roshk10/Agentic-Clinical-Treatment-Conflict-Resolution-System.git
```

Move into the project folder:

```bash
cd Agentic-Clinical-Treatment-Conflict-Resolution-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run:

```bash
python main.py
```

The system will:

- Load patient data
- Retrieve guideline evidence
- Consult specialist agents
- Detect conflicts
- Build consensus
- Generate the final recommendation

---

## Sample Input

Patient information is provided in JSON format inside:

```
data/patients/
```

Example fields include:

- Diagnoses
- Medications
- Laboratory results
- Vital signs
- Symptoms

---

## Sample Output

The system generates:

- Patient summary
- Specialist recommendations
- Evidence sources
- Conflict analysis
- Consensus treatment recommendations
- Final clinical report

---

## Future Enhancements

- Support additional diseases
- Web-based user interface
- Explainable AI visualizations
- Real-time Electronic Health Record (EHR) integration
- FHIR interoperability
- Larger clinical guideline repository

---

## Disclaimer

This project is developed for educational and research purposes during an internship. It is **not intended for direct clinical use** or as a substitute for professional medical advice.

---

## Author

**Roshan Raguraman**

B.E. Computer Science and Engineering

St. Joseph's Institute of Technology



