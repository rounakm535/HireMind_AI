# 🚀 HireMind AI - Deployment Guide

> Production deployment documentation for **HireMind AI**, an AI-Powered Applicant Tracking System & Resume Screening Platform.

---

## 📋 Table of Contents

1. [Quick Local Setup (1-Command Launcher)](#1-quick-local-setup-1-command-launcher)
2. [Docker Compose Deployment (Recommended for Production)](#2-docker-compose-deployment-recommended-for-production)
3. [Cloud Deployment (Render / Railway / Vercel)](#3-cloud-deployment-render--railway--vercel)
4. [Environment Variables Reference](#4-environment-variables-reference)
5. [Architecture & Services Overview](#5-architecture--services-overview)

---

## 1. Quick Local Setup (1-Command Launcher)

For fast local development and testing, run both the FastAPI Backend and React Frontend with a single command:

```bash
# Clone the repository
git clone https://github.com/rounakm535/hiremind-ai.git
cd hiremind-ai

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..

# Run both servers with the python launcher
python run_app.py
```

- **Frontend App**: `http://localhost:5173`
- **Backend Swagger Docs**: `http://localhost:8000/docs`
- **Demo Account**: `rony.test@gmail.com` / `Admin@1234`

---

## 2. Docker Compose Deployment (Recommended for Production)

HireMind AI is fully containerized with **Docker Compose**, including PostgreSQL 16, Redis 7, Qdrant Vector Search, FastAPI (Backend), and Nginx (Frontend SPA Server).

### Steps:

1. **Configure Environment Variables**:
   Copy `.env.example` to `.env` in `backend/`:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Add your Google Gemini API key if available:
   ```env
   GEMINI_API_KEY="your_actual_gemini_api_key_here"
   ```

2. **Build and Start Container Cluster**:
   ```bash
   docker-compose up --build -d
   ```

3. **Verify Active Services**:
   ```bash
   docker-compose ps
   ```

   - **Frontend App**: `http://localhost` (or `http://localhost:3000`)
   - **Backend API**: `http://localhost:8000/api/v1`
   - **API Health Check**: `http://localhost:8000/health`
   - **Qdrant Vector DB Dashboard**: `http://localhost:6333/dashboard`

4. **Stop Services**:
   ```bash
   docker-compose down
   ```

---

## 3. Cloud Deployment (Render / Railway / Vercel)

### Option A: Render / Railway (Full Stack Docker)

1. Connect your GitHub repository `hiremind-ai` to **Render** or **Railway**.
2. Create a **Web Service** for the backend using `backend/Dockerfile` or Docker runtime:
   - Build Context: `./backend`
   - Dockerfile Path: `Dockerfile`
   - Port: `8000`
3. Add environment variables in Render/Railway dashboard:
   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `GEMINI_API_KEY`: Google Gemini AI API key.
   - `SECRET_KEY`: Random 32+ character JWT secret string.
4. Create a static web app for `frontend/` on **Render** or **Vercel**:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Environment Variable: `VITE_API_BASE_URL=https://your-backend-service.onrender.com/api/v1`

---

## 4. Environment Variables Reference

| Variable Name | Required | Default | Description |
|---|---|---|---|
| `PROJECT_NAME` | No | `HireMind AI` | Application Name |
| `API_V1_STR` | No | `/api/v1` | API version prefix |
| `DATABASE_URL` | Yes | `sqlite+aiosqlite:///./hiremind_db.sqlite` | SQLAlchemy Async DB Connection URL |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis caching & task queue URL |
| `QDRANT_HOST` | No | `localhost` | Qdrant Vector Search host |
| `QDRANT_PORT` | No | `6333` | Qdrant Vector Search port |
| `GEMINI_API_KEY` | Optional | `""` | Google Gemini API key (Uses heuristic fallback if omitted) |
| `SECRET_KEY` | Yes | `super_secret_jwt_key...` | JWT Access Token signing key |
| `REFRESH_SECRET_KEY` | Yes | `super_secret_refresh_jwt...` | JWT Refresh Token signing key |

---

## 5. Architecture & Services Overview

```
                          ┌───────────────────────────┐
                          │    Browser Client (React) │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   Nginx Reverse Proxy     │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │     FastAPI Backend       │
                          └──────┬──────┬──────┬──────┘
                                 │      │      │
            ┌────────────────────┘      │      └────────────────────┐
            ▼                           ▼                           ▼
  ┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
  │ PostgreSQL / DB   │       │   Redis Cache     │       │ Qdrant Vector DB  │
  └───────────────────┘       └───────────────────┘       └───────────────────┘
```

---

## 💡 Troubleshooting & Verification

- **Backend Health Check**:
  `curl http://localhost:8000/health` -> `{"status":"healthy","service":"HireMind AI"}`
- **Test Database Auto-Seeding**:
  `curl -X POST http://localhost:8000/api/v1/seed`
- **Run Backend Tests**:
  `cd backend && pytest`
- **Check Frontend Build**:
  `cd frontend && npm run build`
