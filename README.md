# 🤖 Code Review Agent

> An AI-powered code review agent that learns and remembers your team's coding standards, common mistakes, and review preferences.

## 📌 Overview

Generic code linters can detect syntax and common style issues, but they usually do not understand how a specific development team prefers to write and review code.

**Code Review Agent** combines:

* 🤖 **Groq-powered AI code review**
* 🧠 **Hindsight long-term memory**
* 🔍 **Flake8 static analysis**
* 🔄 **Team feedback and continuous learning**

The system retrieves relevant historical team knowledge before reviewing new code. Team members can then **Accept**, **Reject**, or indicate **"We do it this way"** for a suggestion. This feedback is stored and can be retrieved during future reviews.

---

## 🎯 Problem Statement

Code review in development teams can be:

* Time-consuming
* Inconsistent between reviewers
* Dependent on individual reviewer knowledge
* Repetitive when the same issues are discussed repeatedly

Traditional linters can identify generic coding problems, but they don't remember a team's historical review decisions or project-specific conventions.

### Our Approach

The Code Review Agent combines static analysis with a memory-enabled AI reviewer.

Instead of only asking:

> "Is this code good?"

the system can consider:

> "What coding standards and previous review decisions has this team established?"

---

## ✨ Key Features

### 1. 🔍 Generic Code Analysis

Flake8 is used to detect common Python code-quality issues.

Examples include:

* Syntax/style issues
* Indentation problems
* Unused variables
* Formatting issues

---

### 2. 🧠 Team Memory

Hindsight stores and retrieves team-specific coding knowledge.

Examples of remembered rules:

```text
R1 → Use logger instead of print() for logging

R2 → Parameterize SQL queries

R3 → Functions should follow the team's documentation standard

R4 → Never hard-code passwords or API keys

R5 → Catch specific exceptions instead of bare except

R6 → Use descriptive snake_case names
```

The retrieved memories are provided to the AI reviewer as context.

---

### 3. 🤖 AI-Powered Review

The Groq API is used to analyze the submitted code along with relevant team memories.

The reviewer can generate:

* Code review comments
* Line references
* Severity
* Suggestions
* Reasons
* References to team memory

---

### 4. 🔄 Continuous Team Feedback

After a review, the team can respond to suggestions using:

```text
✅ Accept
❌ Reject
💬 We do it this way
```

The feedback is stored in Hindsight.

This allows future reviews to consider previous team decisions.

---

### 5. 🧠 Memory-Aware Reviews

For example, if the team previously accepted:

```text
Rename parameter 'id' → 'user_id'
```

a future review containing:

```python
def fetchUser(id):
    ...
```

can retrieve that historical feedback and use it when generating the new review.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │   User / Developer│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Streamlit UI     │
                    │    app.py        │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌─────────────┐
       │  Flake8    │ │ Hindsight  │ │ PR Details  │
       │  Linter    │ │  Memory    │ │             │
       └─────┬──────┘ └─────┬──────┘ └──────┬──────┘
             │              │               │
             └──────────────┼───────────────┘
                            ▼
                    ┌──────────────────┐
                    │  Groq AI Agent   │
                    │    reviewer.py   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Review Comments  │
                    │ + Memory Used    │
                    └────────┬─────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
                 Accept             Reject
                    │                 │
                    └────────┬────────┘
                             ▼
                    ┌──────────────────┐
                    │ Hindsight Memory │
                    │  Feedback Store  │
                    └──────────────────┘
                             │
                             ▼
                     Future Reviews
```

---

## 🔄 Review Workflow

```text
1. Developer submits code
          ↓
2. Flake8 performs generic analysis
          ↓
3. Hindsight retrieves relevant team memories
          ↓
4. Groq receives code + team knowledge
          ↓
5. AI generates review comments
          ↓
6. Team accepts/rejects suggestions
          ↓
7. Feedback is stored in Hindsight
          ↓
8. Future reviews can use that knowledge
```

---

## 🧩 Project Structure

```text
code-review-agent/
│
├── app.py
├── memory.py
├── reviewer.py
├── lint.py
├── seed_memory.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│
├── prompts/
│   ├── review_plain.txt
│   └── review_with_memory.txt
│
├── docs/
│
└── tests/
```

### File Responsibilities

| File             | Purpose                                         |
| ---------------- | ----------------------------------------------- |
| `app.py`         | Streamlit frontend and review workflow          |
| `memory.py`      | Hindsight memory retrieval and feedback storage |
| `reviewer.py`    | Groq-powered AI review                          |
| `lint.py`        | Flake8 integration                              |
| `seed_memory.py` | Initial team knowledge                          |
| `config.py`      | Project configuration                           |
| `prompts/`       | AI review prompts                               |
| `tests/`         | Testing files                                   |

---

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core application                |
| Streamlit     | Web interface                   |
| Groq          | AI-powered code review          |
| Hindsight     | Long-term team memory           |
| Flake8        | Static code analysis            |
| python-dotenv | Environment variable management |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd code-review-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_API_KEY=your_hindsight_api_key
```

Never commit `.env` to GitHub.

The project includes `.gitignore` protection for environment variables.

---

## ▶️ Run the Application

Start Streamlit using:

```powershell
python -m streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---

## 🧪 Example

### Input

```python
def getUser(id):
    data = []

    try:
        data = db.find(id)
    except:
        pass

    return data
```

### Team Memory Retrieved

```text
Team rule R5 mandates catching specific exceptions
instead of using a bare except clause.
```

```text
The team established a coding standard requiring
parameters to use descriptive snake_case names.
```

### AI Review

```text
Rename parameter 'id' to a descriptive snake_case
name such as 'user_id'.

Catch a specific exception instead of using a bare
except clause.
```

The UI also displays the relevant team memory used for the review.

---

## 🧠 Learning Through Feedback

The system supports a feedback loop.

### Example

First review:

```text
AI:
Rename parameter 'id' to 'user_id'.
```

Team:

```text
✅ Accept
```

The decision is stored in memory.

Later review:

```python
def fetchUser(id):
    ...
```

The system can retrieve the previous team decision and use it as supporting context for the new review.

This creates a continuous feedback cycle:

```text
Review
  ↓
Team Decision
  ↓
Memory
  ↓
Future Review
  ↓
Better Team Alignment
```

---

## 🆚 Generic Linter vs Code Review Agent

| Capability                    | Generic Linter | Code Review Agent |
| ----------------------------- | -------------: | ----------------: |
| Detect common code issues     |              ✅ |                 ✅ |
| AI-generated explanations     |              ❌ |                 ✅ |
| Remember team standards       |              ❌ |                 ✅ |
| Retrieve previous feedback    |              ❌ |                 ✅ |
| Accept/reject team feedback   |              ❌ |                 ✅ |
| Use historical review context |              ❌ |                 ✅ |
| Adapt to team preferences     |              ❌ |                 ✅ |

---

## 🎯 Why Memory Matters

The main idea is not simply generating another AI code review.

The system attempts to preserve **team-specific knowledge** that would otherwise remain scattered across:

* Previous pull requests
* Code review discussions
* Developer decisions
* Coding standards
* Repeated review comments

This makes historical team feedback available as context during future reviews.

---

## 🔐 Security Considerations

* API keys are stored in environment variables.
* `.env` should never be committed.
* Secrets should not be included in source code.
* Production deployments should use secure secret-management mechanisms.

---

## 🚀 Future Improvements

Potential extensions include:

* GitHub Pull Request integration
* Automatic review of changed files
* Support for multiple programming languages
* Repository-level memory
* Team/user authentication
* Review history dashboard
* Memory confidence and relevance scoring
* Automatic detection of conflicting team rules
* Analytics for recurring code-review issues

---

## 👥 Team

**Hackathon Project — Code Review Agent**

Team responsibilities:

* **Memory & Hindsight:** Memory retrieval and feedback storage
* **AI Reviewer:** Groq integration and review prompts
* **Frontend & Integration:** Streamlit UI and linter integration
* **Data & Documentation:** Demo data, documentation, and project presentation

---

## 📌 Project Summary

**Code Review Agent** combines static analysis, generative AI, and long-term memory to create a review workflow that can incorporate a team's historical coding standards and feedback.

```text
Generic Code Analysis
        +
AI Code Review
        +
Team Memory
        +
Human Feedback
        ↓
Team-Aware Code Review
```

---
