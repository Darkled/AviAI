# AviAI — AI-Powered Airline Fleet Analyst

AviAI is a full-stack application developed as a final project for an **AI-Assisted Programming** university course. The objective was to build a comprehensive, functional prototype from scratch using an AI-first development methodology. 

I chose to design this application for **airline fleet management**, enabling operations managers and analysts to converse with their fleet database using natural language. The system leverages an autonomous AI agent to explore schemas, generate safe SQL queries, and provide deep insights into aircraft utilization, maintenance status, and fleet capabilities.

## 📺 Demo

<div align="center">
  <video src="assets/demo.mp4" width="100%" autoplay loop muted playsinline></video>
</div>

---

## 🚀 Features

- **Natural Language Fleet Analysis:** Ask questions like *"How many Airbus A320s are currently in 'Active' status?"* or *"Which aircraft have a range greater than 5000km?"* and get instant data.
- **Schema-Aware Intelligence:** The AI agent automatically discovers tables (like `fleet` and `aircraft_models`) to understand the relationship between specific aircraft and their technical specifications.
- **Safe Data Exploration:** Implements strict read-only (`SELECT`) validation, ensuring the AI can only query data without modifying critical fleet records.
- **Persistent Operations Hub:** Save your analysis sessions. Whether you are tracking maintenance cycles or planning fleet expansion, your chat history is preserved locally via SQLite.
- **Modern Executive Dashboard:** A professional chat interface built with React 19 and optimized for desktop fleet management.

---

## 🛠️ Tech Stack

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **AI Engine:** [pydantic-ai](https://ai.pydantic.dev/) for structured, tool-calling agents.
- **Database (Internal):** SQLite for conversation persistence.
- **Database (Fleet Data):** PostgreSQL (Target for analytical queries).
- **ORM:** SQLAlchemy 2.x / SQLModel.

### Frontend
- **Framework:** React 19 + Vite.
- **Components:** [shadcn/ui](https://ui.shadcn.com/) with Tailwind CSS v4.
- **Routing:** React Router 7.

---

## 🧠 Methodology: The AI-First Approach

This project serves as a case study in **AI-First Software Engineering**. Rather than manually writing every line of code, I developed a "Portable AI Layer" (`.agents/`) that lives within the repository.

- **Plan → Implement → Validate (PIV):** Every feature, from the fleet database connection to the chat streaming, was researched and designed by AI sub-agents before implementation.
- **Living Context:** The repository contains its own development rules and architectural patterns, allowing the AI to maintain consistency across the entire stack.

---

## 🏗️ Architecture

```text
AviAI/
├── frontend/       # React Fleet Management Dashboard
├── backend/        # FastAPI Analytics Server
├── assets/         # Project demo and media
└── .agents/        # AI Layer (Context, Commands, History)
```

---

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (Pre-loaded with fleet data)

### Installation

1. **Clone & Install:**
   ```bash
   git clone <repo-url>
   cd AviAI
   ```

2. **Server Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env  # Add your database URL and LLM API Key
   uvicorn app.main:app --reload
   ```

3. **Client Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
