# 🤖 AI Voice Bot - Real-Time Conversation Application

An interactive AI voice bot that engages children in a 1-minute conversation about an image using **Google Gemini AI**, **FastAPI**, and **React**. Features real-time voice interaction, visual effects, and tool calling for enhanced engagement.

## ✨ Features

- **🎨 Visual Display**: Shows an engaging image that serves as the conversation topic
- **🎙️ Voice Interaction**: Real-time speech-to-text and text-to-speech using browser APIs (100% free!)
- **🤖 AI Conversation**: Powered by Google Gemini 2.0 Flash with vision capabilities
- **⏱️ Timed Conversation**: Automatically manages a 1-minute conversation session
- **🎯 Tool Calling**: AI can trigger UI actions (highlights, animations, fun facts, emojis)
- **🌈 Child-Friendly UI**: Vibrant colors, smooth animations, and engaging design

## 🏗️ Tech Stack

### Backend
- **FastAPI** - High-performance async web framework
- **Google Gemini 2.0 Flash** - LLM with vision and function calling (free tier)
- **WebSockets** - Real-time bidirectional communication
- **Python 3.8+**

### Frontend
- **React 18** - UI framework
- **Vite** - Fast development server
- **Web Speech API** - Browser speech recognition (free)
- **Speech Synthesis API** - Browser text-to-speech (free)

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Google AI API Key** (free tier) - Get it from [Google AI Studio](https://aistudio.google.com/apikey)
- **Modern Browser** - Chrome, Edge, or Safari (for speech features)

## 🚀 Setup Instructions

### 1. Clone/Download the Project

```bash
cd "d:\ML\Projects\AI_assignment\AI Voice Bot"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

### 4. Add Sample Image

Copy a child-friendly image to `frontend/public/sample_image.png`, or use the generated one provided.

## ▶️ Running the Application

You need to run both backend and frontend servers:

### Terminal 1 - Backend Server

```bash
cd backend
venv\Scripts\activate
python main.py
```

Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Terminal 2 - Frontend Server

```bash
cd frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

## 🎮 How to Use

1. **Open** `http://localhost:5173` in Chrome, Edge, or Safari
2. **Allow** microphone permissions when prompted
3. **Click** "Start Talking" button
4. **Listen** to the AI's greeting
5. **Speak** your responses - the AI will listen and reply
6. **Watch** for visual effects triggered by the AI (highlights, emojis, fun facts)
7. **Enjoy** the 1-minute conversation!

## 🛠️ API Endpoints

### REST Endpoints

- `GET /` - Health check
- `POST /api/analyze-image` - Upload and analyze an image
- `GET /api/image-context/{image_name}` - Get context for predefined image

### WebSocket

- `WS /ws/conversation/{session_id}` - Real-time conversation endpoint

## 🎨 Tool Calls (UI Actions)

The AI can trigger these visual actions during conversation:

- **`highlight_area`** - Highlights specific areas of the image
- **`show_fun_fact`** - Displays interesting facts in a popup
- **`play_animation`** - Triggers animations (sparkles, bounce, pulse, confetti)
- **`show_emoji`** - Shows emojis matching the conversation mood

## 📁 Project Structure

```
AI Voice Bot/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── gemini_client.py           # Gemini API integration
│   ├── conversation_manager.py    # Conversation state management
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example              # Environment template
│   └── .env                      # Your API keys (create this)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Main application component
│   │   ├── components/
│   │   │   ├── ImageDisplay.jsx      # Image display with effects
│   │   │   ├── VoiceInterface.jsx    # Voice input/output
│   │   │   └── ConversationDisplay.jsx # Chat messages
│   │   ├── styles.css            # Application styling
│   │   └── main.jsx              # React entry point
│   ├── public/
│   │   └── sample_image.png      # Sample conversation image
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── README.md
```

## 🔑 Environment Variables

Create `backend/.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
HOST=0.0.0.0
PORT=8000
CONVERSATION_DURATION_SECONDS=60
```

