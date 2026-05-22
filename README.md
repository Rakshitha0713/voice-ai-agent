# voice-ai-agent

# 2Care.ai — Real-Time Multilingual Voice AI Agent

A real-time voice-based clinical appointment booking system supporting English, Hindi, and Tamil.

## Features
- Real-time voice conversation via WebSocket
- Multilingual support — English, Hindi, Tamil
- Book, reschedule, cancel appointments
- Contextual memory with Redis
- Persistent patient profiles in PostgreSQL
- Live latency measurement dashboard
- Styled web interface

## Tech Stack
| Technology | Purpose |
|---|---|
| Python 3.11 + FastAPI | Backend server |
| OpenAI Whisper | Speech-to-Text |
| OpenAI GPT-4o | AI Agent reasoning |
| ElevenLabs | Text-to-Speech |
| Redis | Session memory |
| PostgreSQL | Appointments database |
| WebSockets | Real-time communication |

## System Architecture

User Voice
|
WebSocket (Real-time)
|
Speech-to-Text (Whisper)
|
Language Detection (English/Hindi/Tamil)
|
AI Agent (GPT-4o)
|
Tool Orchestration
|
Appointment Database (PostgreSQL)
|
Text-to-Speech (ElevenLabs)
|
Audio Response

##Project Structure
voice-ai-agent/
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── websocket.py
│   │   └── routes.py
│   └── controllers/
│       └── appointment_controller.py
├── agent/
│   ├── prompt/system_prompt.py
│   ├── reasoning/agent.py
│   └── tools/appointment_tools.py
├── memory/
│   ├── session_memory.py
│   └── persistent_memory.py
├── services/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   └── language_detection.py
├── scheduler/
│   ├── models.py
│   └── appointment_engine.py
├── frontend/
│   └── templates/index.html
├── .env
└── requirements.txt

## Setup Instructions

### 1. Clone the repository
``bash
git clone https://github.com/Rakshitha0713/voice-ai-agent.git
cd voice-ai-agent

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Configure environment variables
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://postgres:password@localhost:5432/voice_agent_db

### 5. Start Redis
docker run -d -p 6379:6379 --name redis redis:alpine

### 6. Setup database
python create_tables.py
python seed_data.py

### 7. Run the server
uvicorn backend.main:app --port 8000

### 8. Open Browser
http://localhost:8000












