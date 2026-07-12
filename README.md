# 🚀 HireMind AI – AI-Powered Resume Screening & Applicant Tracking System (ATS)

> A production-grade AI-powered Applicant Tracking System (ATS) that automates resume screening, candidate ranking, skill gap analysis, interview preparation, and recruiter workflows using Large Language Models (LLMs).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-purple)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange)

---

# 📖 Overview

HireMind AI is an AI-first SaaS Applicant Tracking System designed to help recruiters and hiring managers automate the hiring process. Instead of manually reviewing hundreds of resumes, recruiters can upload job descriptions and candidate resumes to receive AI-powered insights including candidate rankings, skill gap analysis, resume summaries, interview questions, and semantic candidate search.

The project follows production-grade software engineering practices with a scalable architecture, modular backend, AI orchestration using LangGraph, vector search with Qdrant, cloud storage on AWS S3, and containerized deployment using Docker.

---

# ✨ Key Features

## 🔐 Authentication & Authorization

* JWT Authentication
* Refresh Tokens
* Role-Based Access Control (RBAC)
* Password Reset
* Email Verification
* Secure Session Management

---

## 💼 Job Management

* Create, update, archive, and delete job postings
* Required & preferred skills
* Experience and education requirements
* Salary range
* Employment type
* Job status management

---

## 📄 Resume Management

* Upload PDF and DOCX resumes
* Bulk resume upload
* Resume versioning
* Resume parsing
* Resume storage in AWS S3
* Metadata extraction

---

## 🤖 AI Resume Screening

* Resume vs Job Description matching
* Semantic similarity search
* AI-generated match score
* Candidate ranking
* Skill gap analysis
* Resume summaries
* Strengths and weaknesses
* Hiring recommendations

---

## 🧠 AI Recruiter Assistant

Recruiters can ask natural language questions such as:

* Find Python developers with FastAPI experience
* Show candidates with AWS certifications
* Rank React developers with Docker experience
* Compare the top 5 candidates
* Generate interview questions for Candidate A

---

## 📊 Analytics Dashboard

* Active jobs
* Resume uploads
* Candidate pipeline
* Average AI match score
* Hiring funnel
* Recruiter productivity
* Top skills distribution

---

## 📧 AI Email Generator

Generate personalized:

* Interview invitations
* Shortlist emails
* Rejection emails
* Follow-up emails
* Offer letters (template)

---

# 🏗️ Tech Stack

## Frontend

* React
* TypeScript
* Tailwind CSS
* Redux Toolkit
* React Router
* Axios

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic
* Pydantic

## Database

* PostgreSQL

## Cache

* Redis

## AI

* Google Gemini
* LangGraph

## Vector Database

* Qdrant

## File Storage

* AWS S3

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Nginx

## Deployment

* AWS / GCP

---

# 🏛️ High-Level Architecture

```text
                    React Frontend
                           │
                           ▼
                    FastAPI Backend
                           │
     ┌───────────────┬───────────────┬───────────────┐
     │               │               │               │
 PostgreSQL       Redis          Qdrant          AWS S3
     │               │               │               │
     └───────────────┴───────────────┴───────────────┘
                           │
                     LangGraph Engine
                           │
                     Google Gemini API
```

---

# 🧩 System Workflow

1. Recruiter logs in.
2. Creates a new Job Description.
3. Uploads one or more resumes.
4. Resumes are stored in AWS S3.
5. Background workers parse resume content.
6. Candidate information is stored in PostgreSQL.
7. Embeddings are generated and stored in Qdrant.
8. LangGraph orchestrates AI workflows.
9. Gemini evaluates candidate-job fit.
10. AI generates rankings, summaries, interview questions, and recommendations.
11. Dashboard displays analytics and hiring insights.
12. Recruiters interact with candidates using AI-powered search and chat.

---

# 📂 Project Structure

```text
hiremind-ai/

├── frontend/
│   ├── src/
│   ├── public/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── redux/
│   └── utils/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── ai/
│   │   ├── workers/
│   │   ├── middleware/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── alembic/
│   └── Dockerfile/
│
├── docker/
├── docs/
├── scripts/
├── .github/workflows/
├── docker-compose.yml
└── README.md
```

---

# 🛠️ Core AI Pipeline

```text
Resume Upload
      │
      ▼
Resume Parsing
      │
      ▼
Metadata Extraction
      │
      ▼
Embedding Generation
      │
      ▼
Qdrant Vector Storage
      │
      ▼
LangGraph Workflow
      │
      ▼
Gemini Reasoning
      │
      ▼
Match Score
      │
      ▼
Skill Gap Analysis
      │
      ▼
Interview Questions
      │
      ▼
Recruiter Dashboard
```

---

# 🔒 Security Features

* JWT Authentication
* Refresh Tokens
* RBAC
* Password Hashing (bcrypt)
* Input Validation
* Rate Limiting
* CORS Protection
* Secure Environment Variables
* Signed AWS S3 URLs
* Audit Logging
* Prompt Injection Mitigation
* API Versioning

---

# 🧪 Testing Strategy

* Unit Tests
* Integration Tests
* API Tests
* AI Workflow Tests
* Authentication Tests
* End-to-End Tests
* Load Testing
* Security Testing

---

# 🚀 Deployment

The application is containerized using Docker and can be deployed to AWS or GCP.

Deployment components include:

* Docker Compose
* Nginx Reverse Proxy
* GitHub Actions CI/CD
* PostgreSQL
* Redis
* Qdrant
* AWS S3
* HTTPS

---

# 📈 Future Enhancements

* Multi-Tenant Organizations
* Video Interview Analysis
* AI Voice Interview Agent
* Calendar Integration
* LinkedIn Resume Import
* GitHub Profile Analysis
* Resume OCR
* Candidate Recommendation Engine
* Offer Prediction
* Slack & Microsoft Teams Integration
* Real-Time Notifications
* Advanced Analytics Dashboard

---

# 📚 Engineering Practices

* Clean Architecture
* SOLID Principles
* Repository Pattern
* Dependency Injection
* Background Task Processing
* Async APIs
* Structured Logging
* OpenAPI Documentation
* Environment-Based Configuration
* Containerized Infrastructure
* CI/CD Automation

---

# 🎯 Resume Highlights

This project demonstrates:

* Production-grade SaaS Architecture
* FastAPI Backend Development
* React + TypeScript Frontend
* AI Workflow Orchestration using LangGraph
* LLM Integration with Google Gemini
* Vector Search using Qdrant
* JWT Authentication & RBAC
* PostgreSQL Database Design
* Redis Caching
* Docker & Docker Compose
* AWS S3 Integration
* GitHub Actions CI/CD
* RESTful API Design
* Scalable System Design
* Cloud-Native Deployment

---

# 🤝 Contributing

Contributions, feature requests, and bug reports are welcome. Please open an issue or submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rounak Mishra**

* AI Engineer | Backend Developer | Software Engineer
* Python • FastAPI • React • LangGraph • Google Gemini • PostgreSQL • Docker • AWS
* GitHub: https://github.com/rounakm535

If you found this project useful, consider giving it a ⭐ on GitHub!
#   H i r e M i n d _ A I  
 