
```md
#  Travel Assistant API

An AI-powered Travel Assistant built with **FastAPI**, **LangGraph**, and **tool-based reasoning**.  
The system intelligently decides when to use tools such as weather lookup, dictionary definitions, and web search (DuckDuckGo) to answer user queries.

---

##  Features

-  Tool-aware AI agent (LangGraph)
-  Weather lookup tool (simulated)
-  Dictionary lookup tool
-  Web search via DuckDuckGo (`ddgs`)
-  FastAPI backend
-  Automated system performance testing
-  Web-based user interface

---

##  Architecture Overview

```

User Request
↓
FastAPI (/api/assist)
↓
LangGraph Agent
↓
LLM Decision
├── get_weather
├── define_word
└── web_search
↓
Tool Execution
↓
Final Answer

```

### Key Design Decisions
- **LangGraph** manages agent flow and tool execution loops
- **ToolMessage with tool_call_id** ensures correct tool-call resolution
- **No RAG** (lightweight, fast inference)
- **DuckDuckGo search** avoids API key dependency

---

##  Available Tools

| Tool Name     | Description                                   |
|--------------|-----------------------------------------------|
| get_weather  | Returns simulated weather for a city          |
| define_word  | Dictionary definition lookup                  |
| web_search   | Web search using DuckDuckGo                   |

---

## 📡 API Endpoints

### Health Check
```

GET /

```

### Travel Assistant
```

POST /api/assist

````

**Request Body**
```json
{
  "question": "What is the weather in Abuja?",
  "city": "Abuja"
}
````

**Response**

```json
{
  "answer": "...",
  "tool_used": "get_weather",
  "city": "Paris",
  "success": true
}
```

### List Tools

```
GET /api/tools
```

---

## Testing

A full system-level test suite is available.

### Test File

```
test.py
```

### What It Measures

* Tool selection accuracy
* Latency per request
* Tool usage distribution
* Failure and mismatch counts

### Run Tests

```bash
python test.py
```

---

## User Interface

A simple web-based UI is available in the `ui/` folder.

```
ui/
├── index.html
├── styles.css
└── script.js
```

### UI Features

* Ask travel-related questions
* See real-time responses
* Demonstrates tool-backed reasoning

> The UI communicates directly with the FastAPI backend.

---

## 🛠 Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Run the API:

```bash
uvicorn main:app --reload
```

---

## 📌 Notes

* This system is **agent-based**, not a chatbot wrapper
* Built for extensibility (more tools can be added easily)
* Designed to be testable, observable, and production-safe

---

## ✅ Status

✔ Tool-calling stable
✔ LangGraph compliant
✔ Test-covered
✔ UI-enabled

---
