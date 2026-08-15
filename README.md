# TN Fact Check AI 🛡️

An AI-powered claim verification and fact-checking system designed for the **AI, Information Technology and Digital Services Department, Government of Tamil Nadu**. 

This system employs a multi-agent AI desk powered by **CrewAI** and **Gemini 3.5 Flash** to triage user claims, search live web archives via **Exa Search API**, verify facts against authoritative sources, and stream progress events dynamically to a responsive React chatbot interface.

---

## 🚀 Key Features

* **Multi-Agent Collaboration**: Orchestrates 4 specialized agents sequentially:
  1. **Query Analyzer (Desk Editor)**: Triages user claims, extracts entities, and classifies the era (Historical vs Current).
  2. **Research Investigator (News Researcher)**: Retrieves live evidence and academic references with strict recency-biasing.
  3. **Verification Specialist (Fact-Checker)**: Cross-checks statements and assigns validation statuses (Verified, False, Outdated, etc.).
  4. **Report Writer (Chief Editor)**: Generates structured, citation-mapped Pydantic JSON reports.
* **Server-Sent Events (SSE) Progress Widget**: Streams active agent states (e.g. analyzing, researching, verifying) to the frontend in real time using FastAPI's EventSource.
* **Premium Government Branding**: Features a clean emerald-green and gold theme styled with custom typography, the official state logo, and interactive accordion claim lists.
* **Minimalist Bibliography**: Lists the top 5 most relevant deduplicated sources complete with support alignments and reliability ratings.

---

## 📁 Repository Structure

```text
fact_checker/
├── backend/                  # FastAPI & CrewAI backend service
│   ├── agents/               # CrewAI Agent definitions
│   ├── crew/                 # Crew compilation & kickoff logic
│   ├── Models/               # Pydantic structured output models
│   ├── tasks/                # CrewAI Task definitions
│   ├── tools/                # Exa Search and scraping tool integrations
│   ├── main.py               # FastAPI server & SSE streaming endpoint
│   └── requirements.txt      # Python dependencies
│
└── frontend/                 
    └── tn_fact_check/        # React + Vite application
        ├── src/
        │   ├── App.jsx       # Chatbot interface & SSE EventSource listener
        │   ├── App.css       # Premium TN government brand stylesheet
        │   └── index.css     # Global Outfit/Inter typography tokens
        └── public/assets/    # Branding logos & assets
```

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.11+
* Node.js 18+ & npm
* Gemini API Key & Exa Search API Key

---

### 1. Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY="your-gemini-api-key"
   EXA_API_KEY="your-exa-api-key"
   ```

3. Recreate the virtual environment and install packages (recommended to use `uv` for speed):
   ```bash
   uv pip install -r requirements.txt
   ```

4. Launch the Uvicorn development server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend server will run on `http://127.0.0.1:8000`.

---

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend/tn_fact_check
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite React development server:
   ```bash
   npm run dev
   ```
   Open the displayed local address (typically `http://localhost:5173`) in your web browser.

---

## 👨‍💻 Developer Attribution
* **Developed by**: Harish R
* **Department & Campus**: AI & DS Student, MIT Campus, Anna University
* **Contact**: [harish.ai.engineer@gmail.com](mailto:harish.ai.engineer@gmail.com)
