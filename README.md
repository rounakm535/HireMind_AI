# 🚀 HireMind AI – AI-Powered Resume Screening & Applicant Tracking System (ATS)

> A production-grade AI-powered Applicant Tracking System (ATS) that leverages Large Language Models (LLMs) to automate resume screening, side-by-side candidate comparison, candidate ranking, skill gap analysis, interview preparation, and recruiter workflows.

![Status](https://img.shields.io/badge/Status-Completed%20%26%20Deployed-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌐 Live Deployments & API Links

- **Live Backend API (Render)**: [https://hiremind-ai-backend-o4ua.onrender.com](https://hiremind-ai-backend-o4ua.onrender.com)
- **Interactive Swagger API Docs**: [https://hiremind-ai-backend-o4ua.onrender.com/docs](https://hiremind-ai-backend-o4ua.onrender.com/docs)
- **Live Health Endpoint**: [https://hiremind-ai-backend-o4ua.onrender.com/health](https://hiremind-ai-backend-o4ua.onrender.com/health)

---

## 📌 Overview

**HireMind AI** is an AI-first Applicant Tracking System inspired by modern recruiting platforms like Greenhouse, Lever, and Ashby.

The platform eliminates manual resume screening by combining semantic vector search, Large Language Models (Google Gemini), and production-grade FastAPI & React engineering to help recruiters identify, evaluate, compare, and contact top candidates in seconds.

---

# ✨ Features

### 🔐 Authentication & Security

- JWT Authentication with Refresh Tokens
- Role-Based Access Control (RBAC: Admin, Recruiter, Hiring Manager)
- Password Hashing (Bcrypt) & Password Show/Hide Toggle
- Input Validation & Prompt Injection Defense

### 💼 Job Management

- Create, Edit, & Delete Jobs
- Job Post Filtering by Status (Open, Draft, Closed) & Type (Full-Time, Remote, Contract)
- Skill Requirements Tagging & Experience Criteria

### 📄 Resume Management & Parsing

- PDF/DOCX Resume Upload & Storage
- Heuristic + LLM Dual Parser Engine (No Prompt Leak Guarantee)
- Automated Candidate Skill & Experience Metadata Extraction
- Interactive Resume Reader & Text Previewer

### 🎯 AI Resume Screening & Matching

- Job Description vs Resume Fit Match Score (0–100%)
- Automated Skill Gap Analysis (Matching Skills vs Missing Skills)
- Recruiter Hiring Recommendations & Fit Explanations

### ⚔️ AI Side-by-Side Candidate Comparison

- Multi-Candidate Checkbox Selection
- AI Comparison Matrix (Top Pick Banner, Key Strengths, Skill Gaps, Recruiter Verdicts)
- Direct Email Outreach to Selected Candidates

### ❓ AI Interview Preparation Questionnaire

- Tailored Technical & Behavioral Question Generator
- Ideal Candidate Answer Rubrics & Difficulty Levels
- 1-Click Clipboard Copy & Export

### 🤖 AI Recruiter Assistant Copilot

- Natural Language RAG Queries over Candidate Database
- Interactive Quick-Prompt Suggestion Chips
- Formatted Markdown Chat Responses

### 📊 Dashboard & Analytics

- Recruitment Funnel Breakdown (Applied -> Screened -> Interviewed -> Hired)
- Time-to-Hire & AI Screening Throughput Analytics
- 1-Click CSV Report Export

### ✉️ AI Email Generator

- Personalized Outreach Templates (Interview Invitation, Shortlist, Rejection, Offer Letter)
- Direct Email Composer Modal

---

# 🏗 Tech Stack

## Frontend

- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS & Modern Glassmorphism Aesthetic
- **State Management**: Redux Toolkit & React-Redux
- **Routing**: React Router v6
- **HTTP Client**: Axios with Interceptors
- **Icons**: Lucide React

## Backend

- **Language**: Python 3.12
- **Framework**: FastAPI (Async)
- **Database ORM**: SQLAlchemy 2.0 (Asyncpg & AIOSqlite)
- **Validation**: Pydantic v2
- **Testing**: PyTest

## Database & Caching

- **Primary Database**: PostgreSQL 16 (SQLite fallback for local dev)
- **Cache**: Redis 7
- **Vector Database**: Qdrant Vector Search

## AI Engine

- **LLM**: Google Gemini API (`google-genai` / `gemini-3.6-flash` / `gemini-3.7-flash`)
- **Orchestration**: LangGraph & Heuristic Fallback Engine

## DevOps & Deployment

- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx High-Performance Reverse Proxy
- **Cloud Hosting**: Render (Backend) & Vercel (Frontend)

---

# 🏛 High-Level Architecture

```
                 React Frontend (Vite + Tailwind)
                               │
                               ▼
                   Nginx / Vercel Edge Proxy
                               │
                               ▼
                   FastAPI Backend (Async)
                               │
       ┌─────────┬─────────────┼──────────────┐
       │         │             │              │
 PostgreSQL   Redis     Qdrant Vector DB   AWS S3 / Uploads
       │         │             │
       └─────────┴─────────────┘
               │
          LangGraph Workflow
               │
        Google Gemini LLM
```

---

# 🔄 System Workflow

```
Recruiter Login
      ↓
Create Job Post
      ↓
Upload Candidate Resume (PDF/DOCX)
      ↓
Resume Parsing & Metadata Extraction
      ↓
Vector Embeddings & Storage
      ↓
AI Resume Match Scoring & Skill Gap Analysis
      ↓
Side-by-Side Candidate Comparison Matrix
      ↓
Generate Interview Prep Questionnaires
      ↓
Recruiter Copilot Chat Querying
      ↓
Generate & Send Candidate Outreach Email
```

---

# 📁 Project Structure

```
hiremind-ai/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/          # Axios API Services (Auth, Candidates, AI, Jobs, Resume)
│   │   ├── components/   # Modular UI Components (Candidates, Chat, Jobs, Common)
│   │   ├── pages/        # Router Pages (Dashboard, Candidates, Analytics, Login)
│   │   ├── redux/        # Redux Toolkit Slices & Store
│   │   ├── routes/       # Protected Router Shell
│   │   └── types/        # TypeScript Definitions
│   ├── Dockerfile        # Multi-stage Nginx Production Dockerfile
│   └── nginx.conf        # Nginx SPA Routing & API Proxy Config
│
├── backend/
│   ├── app/
│   │   ├── ai/           # Gemini Client, Matcher, Parser, Question Gen, Ranker
│   │   ├── api/v1/       # FastAPI Endpoint Routers
│   │   ├── core/         # Config, Security, JWT Setup
│   │   ├── db/           # Async Session, Base Models, Demo Seeder (seed.py)
│   │   ├── models/       # SQLAlchemy Async ORM Models
│   │   ├── schemas/      # Pydantic Schemas
│   │   └── services/     # Business Logic Layer
│   ├── tests/            # PyTest Integration & Unit Test Suite
│   ├── Dockerfile        # Python 3.12 FastAPI Dockerfile
│   └── requirements.txt  # Backend Dependencies
│
├── docker-compose.yml     # Multi-Container Stack (Postgres, Redis, Qdrant, Backend, Frontend)
├── run_app.py             # 1-Command Local Development Launcher
├── DEPLOYMENT.md          # Step-by-Step Production Deployment Documentation
└── README.md
```

---

# 🚀 Development Roadmap

- [x] Project Planning & System Architecture
- [x] Backend Setup with Async FastAPI & SQLAlchemy
- [x] Frontend Setup with React, TypeScript & Tailwind CSS
- [x] JWT Authentication & Role-Based Access Control
- [x] Job Management (Create, Edit, Delete, Filter)
- [x] Resume Upload & Robust Dual Parsing Engine
- [x] AI Resume Matching & Fit Scoring
- [x] AI Side-by-Side Candidate Comparison Matrix
- [x] Candidate Ranking Engine
- [x] AI Tailored Interview Prep Question Generator
- [x] AI Recruiter Assistant Copilot Chat
- [x] Recruiter Dashboard & Analytics with CSV Export
- [x] Candidate Email Generation & Direct Outreach
- [x] Automated Database Seeder (`seed.py`)
- [x] Multi-Container Dockerization (`docker-compose.yml` & `nginx.conf`)
- [x] Production Cloud Deployment (Render + Vercel)

---

# ⚙️ Getting Started

### 1-Command Local Launcher (Recommended)

Run both the FastAPI Backend (port 8000) and React Frontend (port 5173) with a single command:

```bash
# Clone Repository
git clone https://github.com/rounakm535/HireMind_AI.git
cd HireMind_AI

# Install Backend Dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install Frontend Dependencies
cd frontend
npm install
cd ..

# Run both servers concurrently
python run_app.py
```

- **Frontend App**: `http://localhost:5173`
- **Backend Swagger Docs**: `http://localhost:8000/docs`

---

### Docker Compose Deployment

```bash
# Build and launch all 5 services (Postgres, Redis, Qdrant, Backend, Frontend)
docker-compose up --build -d
```

- **Web App**: `http://localhost` (or `http://localhost:3000`)
- **Backend API**: `http://localhost:8000/api/v1`

---

# 🧪 Testing

Run backend test suite:

```bash
cd backend
pytest
```

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rounak Mishra**  
AI Engineer | Backend Developer | Software Engineer

- **GitHub**: [github.com/rounakm535](https://github.com/rounakm535)
- **LinkedIn**: [linkedin.com/in/rounakm535](https://linkedin.com/in/rounakm535)

---

⭐ If you found this project interesting, don't forget to star the repository!
