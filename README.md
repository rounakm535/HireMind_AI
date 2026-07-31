# 🚀 HireMind AI –> AI-Powered Resume Screening & Applicant Tracking System (ATS)

> A production-grade AI-powered Applicant Tracking System (ATS) that leverages Large Language Models (LLMs) to automate resume screening, candidate ranking, skill gap analysis, interview preparation, and recruiter workflows.

![Status](https://img.shields.io/badge/Status-Under%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

HireMind AI is an AI-first Applicant Tracking System inspired by modern recruiting platforms like Greenhouse, Lever, and Ashby.

The goal is to eliminate manual resume screening by combining semantic search, Large Language Models, and production-grade backend engineering to help recruiters identify the best candidates in seconds.

This project is being built with scalability, maintainability, and cloud-native deployment in mind.

---

# ✨ Features

### Authentication

- JWT Authentication
- Refresh Tokens
- Role-Based Access Control (RBAC)
- Password Reset
- Email Verification

### Job Management

- Create/Edit/Delete Jobs
- Publish & Archive Jobs
- Required & Preferred Skills
- Experience Requirements
- Employment Type

### Resume Management

- Upload PDF/DOCX
- Bulk Resume Upload
- Resume Parsing
- Resume Storage
- Resume Metadata Extraction

### AI Resume Screening

- Resume vs Job Description Matching
- AI Match Score
- Candidate Ranking
- Skill Gap Analysis
- Resume Summaries
- Hiring Recommendations

### AI Recruiter Assistant

Recruiters can ask:

- Find Python developers with FastAPI experience
- Show candidates with Docker knowledge
- Compare the top candidates
- Generate interview questions
- Search resumes using natural language

### Dashboard

- Active Jobs
- Candidate Analytics
- Hiring Funnel
- Resume Upload Statistics
- AI Match Insights

### AI Email Generator

- Interview Invitation
- Shortlist Email
- Rejection Email
- Follow-up Email
- Offer Letter Template

---

# 🏗 Tech Stack

## Frontend

- React
- TypeScript
- Tailwind CSS
- Redux Toolkit
- React Router
- Axios

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

## Database

- PostgreSQL

## Cache

- Redis

## AI

- Google Gemini
- LangGraph

## Vector Database

- Qdrant

## Cloud Storage

- AWS S3

## DevOps

- Docker
- Docker Compose
- GitHub Actions
- Nginx

## Deployment

- AWS
- Google Cloud Platform

---

# 🏛 High-Level Architecture

```
                React Frontend
                       │
                       ▼
                FastAPI Backend
                       │
       ┌─────────┬──────────┬───────────┐
       │         │          │           │
 PostgreSQL   Redis     Qdrant      AWS S3
       │         │          │
       └─────────┴──────────┘
               │
          LangGraph
               │
        Google Gemini
```

---

# 🔄 Workflow

```
Recruiter Login

↓

Create Job

↓

Upload Resume

↓

Resume Parsing

↓

Generate Embeddings

↓

Store in Qdrant

↓

AI Resume Matching

↓

Candidate Ranking

↓

Interview Question Generation

↓

Recruiter Dashboard

↓

AI Chat

↓

Email Generation
```

---

# 📁 Project Structure

```
hiremind-ai/

├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── redux/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── routes/
│   │   └── utils/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ai/
│   │   ├── core/
│   │   ├── db/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── workers/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── alembic/
│   └── requirements.txt
│
├── docs/
├── docker/
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# 🤖 AI Pipeline

```
Resume Upload

↓

Resume Parsing

↓

Extract Candidate Information

↓

Generate Embeddings

↓

Store in Qdrant

↓

LangGraph Workflow

↓

Google Gemini

↓

Candidate Analysis

↓

Match Score

↓

Skill Gap Analysis

↓

Interview Questions

↓

Dashboard
```

---

# 🔒 Security

- JWT Authentication
- Refresh Tokens
- Password Hashing
- RBAC
- Input Validation
- API Rate Limiting
- Secure Environment Variables
- Signed S3 URLs
- Audit Logging
- Prompt Injection Protection

---

# 🧪 Testing

- Unit Testing
- Integration Testing
- API Testing
- AI Workflow Testing
- Authentication Testing
- End-to-End Testing

---

# 🚀 Development Roadmap

- [x] Project Planning
- [x] PRD
- [x] System Architecture
- [x] Backend Setup
- [x] Frontend Setup
- [ ] Authentication
- [ ] Job Management
- [ ] Resume Upload
- [ ] Resume Parsing
- [ ] AI Resume Matching
- [ ] Candidate Ranking
- [ ] AI Chat
- [ ] Recruiter Dashboard
- [ ] Email Generation
- [ ] Dockerization
- [ ] Deployment
- [ ] CI/CD Pipeline

---

# ⚙️ Getting Started

## Clone Repository

```bash
git clone https://github.com/rounakm535/hiremind-ai.git
cd hiremind-ai
```

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Docker

```bash
docker-compose up --build
```

---

# 📈 Future Enhancements

- Multi-Tenant Organizations
- Resume OCR
- Voice Interview Agent
- GitHub Profile Analysis
- LinkedIn Import
- Calendar Integration
- Slack Notifications
- AI Hiring Copilot
- Resume Recommendation Engine
- Candidate Recommendation Engine

---

# 💡 Engineering Practices

- Clean Architecture
- SOLID Principles
- Repository Pattern
- Dependency Injection
- Async FastAPI
- Background Workers
- Dockerized Infrastructure
- RESTful APIs
- Environment-Based Configuration
- CI/CD
- Cloud Native Deployment

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rounak Mishra**

AI Engineer | Backend Developer | Software Engineer

**Tech Stack**

- Python
- FastAPI
- React
- PostgreSQL
- Redis
- LangGraph
- Google Gemini
- Docker
- AWS

GitHub: https://github.com/rounakm535

---

⭐ If you found this project interesting, don't forget to star the repository!
