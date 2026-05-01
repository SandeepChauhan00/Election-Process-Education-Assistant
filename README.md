# 🗳️ Election Process Education Assistant

> An interactive AI-powered assistant that educates users about India's election process — built with **Google Gemini 1.5 Flash** and deployed on **Google Cloud Run**.

[![Built with Gemini](https://img.shields.io/badge/Built%20with-Google%20Gemini-blue?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Deploy on Cloud Run](https://img.shields.io/badge/Deploy-Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/run)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

---

## 📌 Chosen Vertical

**Election Process Education** — A smart, dynamic AI assistant that helps citizens understand India's democratic election process through interactive conversations, guided topic exploration, and knowledge quizzes.

---

## 🎯 Approach & Logic

### Problem Statement
India has 97 crore+ registered voters, yet many citizens lack clear understanding of the election process — from voter registration to vote counting. This assistant bridges that knowledge gap using AI.

### Solution Architecture
```
User ──► Flask Frontend ──► Gemini 1.5 Flash API ──► Contextual Response
              │                                            │
              ├── Topic-based Learning Paths               │
              ├── Multi-turn Conversation Memory           │
              ├── Interactive Quiz Generation              │
              └── Markdown-rendered Rich Responses ◄───────┘
```

### Key Design Decisions
1. **Google Gemini 1.5 Flash** — Chosen for fast response times and high-quality educational content generation
2. **System Instruction Engineering** — Detailed prompt with 10 knowledge domains, formatting rules, and neutrality constraints
3. **Session-based Chat History** — Maintains conversation context (last 20 messages) for coherent multi-turn interactions
4. **Topic-specific Prompts** — Pre-crafted detailed prompts for each election topic ensure comprehensive, structured responses
5. **Non-partisan Design** — System instruction explicitly enforces political neutrality

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| 🗳️ **10 Election Topics** | Voter registration, timeline, EVM/VVPAT, counting, and more |
| 💬 **Multi-turn Conversations** | Context-aware follow-up questions |
| 🎯 **Interactive Quizzes** | Test election knowledge with AI-generated MCQs |
| 🌙 **Dark Mode** | Toggle between light and dark themes |
| 📱 **Fully Responsive** | Works on desktop, tablet, and mobile |
| ⚡ **Quick Questions** | One-click access to common questions |
| 📝 **Markdown Rendering** | Rich formatted responses with tables, lists, and highlights |
| ⚖️ **Non-Partisan** | 100% politically neutral and fact-based |
| 🔒 **Secure** | Input sanitization, non-root Docker user, env-based secrets |
| 🏥 **Health Check** | `/health` endpoint for monitoring |

---

## 🏗️ Built With

| Technology | Purpose |
|-----------|---------|
| **Google Gemini 1.5 Flash** | AI Engine for generating educational content |
| **Google Antigravity** | Development environment |
| **Google Cloud Run** | Serverless container deployment |
| **Flask 3.0** | Backend web framework |
| **Gunicorn** | Production WSGI server |
| **Marked.js** | Client-side markdown rendering |
| **Docker** | Containerization |

---

## 📁 Project Structure

```
election-education-assistant/
├── app.py                  # Main Flask application with Gemini integration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Production Docker configuration
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── templates/
│   └── index.html          # Main chat interface (Jinja2 template)
└── static/
    ├── css/
    │   └── style.css       # Premium styles with dark mode
    └── js/
        └── app.js          # Chat logic, theme, particles
```

---

## 🚀 How It Works

### 1. User Interaction Flow
```
1. User opens the app → Welcome message with quick-start options
2. User selects a topic OR types a question
3. Frontend sends request to Flask backend
4. Backend builds conversation history + sends to Gemini API
5. Gemini generates educational response with system instruction context
6. Response rendered as rich markdown in chat UI
7. Conversation history maintained for follow-up questions
```

### 2. AI System Design
- **System Instruction**: 10 knowledge domains, formatting rules, neutrality enforcement
- **Context Window**: Last 20 messages maintained for multi-turn coherence
- **Topic Prompts**: Pre-crafted detailed prompts ensure comprehensive topic coverage
- **Safety**: Input sanitization (2000 char limit), error handling, graceful degradation

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.11+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/apikey))

### 1. Clone & Install
```bash
git clone https://github.com/SandeepChauhan00/Twitter-Clone.git
cd Twitter-Clone
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run Locally
```bash
python app.py
# Open http://localhost:8080
```

---

## ☁️ Deploy to Google Cloud Run

### Quick Deploy
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Build & push image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/election-bot

# Deploy
gcloud run deploy election-education-bot \
  --image gcr.io/YOUR_PROJECT_ID/election-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=your_key,SECRET_KEY=your-secret" \
  --memory 512Mi \
  --timeout 120 \
  --port 8080 \
  --min-instances 0 \
  --max-instances 5
```

---

## 📱 Topics Covered

| # | Topic | Description |
|---|-------|-------------|
| 1 | 📝 Voter Registration | Online/offline registration, Form 6, NVSP |
| 2 | 📅 Election Timeline | Announcement to results — complete timeline |
| 3 | 🗳️ Voting Process | Step-by-step EVM voting guide |
| 4 | ⚖️ Election Commission | Role, powers, Article 324 |
| 5 | 👤 Candidate Filing | Nomination, eligibility, security deposit |
| 6 | 📊 Vote Counting | EVM counting, VVPAT verification, results |
| 7 | 📋 Model Code of Conduct | Rules, enforcement, penalties |
| 8 | 🖥️ EVM & VVPAT | Technology, security, concerns addressed |
| 9 | 🏛️ Types of Elections | Lok Sabha, Rajya Sabha, State, Local |
| 10 | 🎯 Election Quiz | Interactive MCQ knowledge test |

---

## 🔒 Security Measures

- **Non-root Docker user** — Container runs as unprivileged `appuser`
- **Environment variables** — Secrets never hardcoded
- **Input sanitization** — User input stripped and length-limited
- **Session management** — Server-side chat history with size limits
- **CORS/XSS** — Flask default protections active

---

## ⚡ Assumptions

1. Users have basic internet connectivity
2. Gemini API key is valid and has sufficient quota
3. Content focuses on Indian elections (ECI framework)
4. All information is educational — not legal advice
5. Election dates/data may change; users are advised to verify with official sources

---

## 👨‍💻 Developer

**Sandeep Kumar** | PromptWars: Virtual Challenge 2

Built with ❤️ using Google Antigravity & Google Gemini AI
