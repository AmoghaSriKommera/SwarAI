# SwarAI - Voice-Enabled AI Assistant

SwarAI is a lightweight, browser-accessible voice-enabled Progressive Web App (PWA) that allows users to speak naturally, get intelligent responses, and store their voice conversations.

<p align="center">
  <img src="https://i.imgur.com/placeholder.png" alt="SwarAI Logo" width="200"/>
</p>

## 🌟 Features

- **Voice-First Interface**: Record and transcribe speech directly in your browser
- **Hybrid LLM System**:
  - Primary: Local LLaMA 3.2 model via Ollama
  - Fallback: External LLMs (Gemini) when local model is unavailable
- **Progressive Web App**: Works offline and is installable on mobile devices
- **Chat History**: Stores conversations using IndexedDB for offline access
- **Cross-Platform**: Works on mobile, tablet, and desktop browsers
- **No Installation Required**: Runs directly in modern browsers

## 🏗️ Architecture

SwarAI is built with a hybrid architecture:

- **Frontend**: React + TypeScript + TailwindCSS
- **Backend**: FastAPI (Python)
- **Local LLM**: Ollama running LLaMA 3.2
- **Fallback LLM**: Google's Gemini API
- **Speech Recognition**: OpenAI Whisper API
- **Database**: PostgreSQL for server-side logging

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL
- [Ollama](https://ollama.ai) with LLaMA 3.2 model

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/swarai.git
cd swarai
```

2. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Run the setup script**

```bash
python main.py
```

This script will:
- Check for required dependencies
- Set up a Python virtual environment
- Install all Python dependencies
- Install all npm dependencies
- Start both backend and frontend servers

### Manual Setup

If you prefer to set up manually:

#### Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m backend.main
```

#### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## 🔧 Troubleshooting

### NPM Dependency Conflicts

If you encounter dependency conflicts during `npm install` (especially with TypeScript versions), try the following:

```bash
# Option 1: Use legacy peer dependencies flag
npm install --legacy-peer-deps

# Option 2: Force installation
npm install --force
```

Common issues:
- **TypeScript version conflict**: React-scripts 5.0.1 requires TypeScript 3.x or 4.x, but newer versions may cause conflicts. SwarAI uses TypeScript 4.9.5 which is compatible with all dependencies.
- **Workbox dependencies**: Make sure all workbox packages use the same version (6.5.4) to avoid conflicts.

### Backend Connection Issues

If the frontend can't connect to the backend:

1. Verify the backend is running (`python -m backend.main`)
2. Check that the backend is listening on the correct port (default: 8000)
3. Make sure CORS is properly configured in the backend
4. Check for any firewall or network issues blocking the connection

### Microphone Access

If the app can't access your microphone:

1. Make sure your browser has permission to access the microphone
2. Try using Chrome or Edge if other browsers are having issues
3. Check if your microphone is properly connected and working
4. Try reloading the page after granting microphone permissions

## 📱 Usage

1. Open the application in your browser (http://localhost:3000)
2. Click the microphone button and allow microphone access
3. Speak your query clearly
4. Wait for the transcription and AI response
5. Continue the conversation as needed

The app will show:
- Your spoken queries
- AI responses
- Response source (Ollama or Gemini)
- Response latency

## 🔧 Technical Details

### Backend API Endpoints

- `POST /ask`: Send a text query and receive an AI response
- `POST /transcribe`: Upload audio and receive transcribed text

### LLM Fallback System

The system first attempts to use the local Ollama model for responses. If Ollama:
- Is not available
- Times out
- Returns an error

The system automatically falls back to the Gemini API.

### Database Schema

The application logs all queries and responses to PostgreSQL with:
- Query ID (UUID)
- Timestamp (UTC)
- User query
- AI response
- Response source
- Response latency

### PWA Capabilities

- Works offline using service workers
- Installable on mobile devices
- Stores conversations in browser storage

## 🛠️ Development

### Project Structure

```
swarai/
├── backend/
│   ├── main.py            # FastAPI application
│   ├── ollama_helper.py   # Ollama integration
│   ├── gemini_fallback.py # Gemini API fallback
│   ├── models.py          # SQLAlchemy models
│   └── database.py        # Database connection
├── frontend/
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── App.tsx        # Main application component
│   │   ├── index.tsx      # Application entry point
│   │   ├── components/    # React components
│   │   │   ├── Recorder.tsx    # Voice recording component
│   │   │   └── ChatBubble.tsx  # Message display component
│   └── package.json       # Frontend dependencies
├── main.py                # Application launcher
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

### Adding New Features

To extend the application:
1. Frontend changes go in the `frontend/src` directory
2. Backend API changes go in `backend/main.py`
3. New LLM providers can be added similar to `gemini_fallback.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for the local LLM implementation
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend library
- [TailwindCSS](https://tailwindcss.com/) for styling