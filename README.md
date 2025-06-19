# SwarAI - Voice-Enabled AI Assistant

SwarAI is a lightweight, browser-accessible Progressive Web App (PWA) that allows users to speak naturally, get intelligent responses, and store their voice conversations.

![SwarAI Logo](https://via.placeholder.com/150x150.png?text=SwarAI)

## Features

- **Voice-First Interface**: Speak naturally and get intelligent responses
- **Hybrid AI System**: Uses locally hosted LLM via Ollama, falls back to cloud LLMs when needed
- **Progressive Web App**: Works across devices with offline capabilities
- **No Installation Required**: Runs in modern browsers on desktop, tablet, and mobile
- **Conversation Storage**: Keeps history of all your interactions locally
- **Latency Metrics**: Shows response times and which AI model was used
- **Privacy-Focused**: Local-first approach with cloud fallback only when needed

## Architecture

SwarAI is built with a hybrid architecture:

### Frontend
- **React**: Modern component-based UI
- **TailwindCSS**: Utility-first CSS framework for styling
- **TypeScript**: Type safety throughout the codebase
- **IndexedDB**: Client-side storage for conversation history
- **Service Workers**: For offline functionality and PWA capabilities

### Backend
- **FastAPI**: High-performance Python web framework
- **Ollama**: Local LLM integration (LLaMA 3.2)
- **Gemini API**: External LLM fallback
- **Whisper API**: For speech-to-text transcription
- **PostgreSQL**: Database for logging queries and responses
- **SQLAlchemy**: ORM for database interactions

## Getting Started

### Prerequisites

- Python 3.8+ with pip
- Node.js 14+ with npm
- PostgreSQL database
- Ollama (optional, for local LLM support)
- API keys for Gemini and OpenAI Whisper (for fallback and transcription)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/swarai.git
cd swarai
```

2. **Setup environment variables**

Copy the example env file and update it with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your database credentials and API keys.

3. **Run the installation script**

The easiest way to get started is to use the provided launcher:

```bash
python main.py
```

This script will:
- Check your system for dependencies
- Create a Python virtual environment
- Install Python dependencies
- Install npm dependencies
- Start both backend and frontend servers
- Open the application in your default browser

### Manual Setup

If you prefer to set up components manually:

#### Backend Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# OR (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
python -m backend.main
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Usage

1. Open the app in your browser (automatically opened when using the launcher)
2. Grant microphone permission when prompted
3. Click the microphone button and start speaking
4. Wait for the AI response
5. Continue the conversation naturally

The app will work in offline mode for previously cached content, and conversations are stored locally in your browser.

## Development

### Project Structure

```
swarai/
├── backend/
│   ├── main.py             # FastAPI server and endpoints
│   ├── ollama_helper.py    # Local LLM integration
│   ├── gemini_fallback.py  # External LLM fallback
│   ├── models.py           # SQLAlchemy models
│   └── database.py         # Database connection logic
├── frontend/
│   ├── public/             # Static files
│   ├── src/
│   │   ├── App.tsx         # Main application component
│   │   ├── index.tsx       # Entry point
│   │   ├── components/     # React components
│   │   │   ├── Recorder.tsx    # Voice recording component
│   │   │   └── ChatBubble.tsx  # Message display component
│   └── tailwind.config.js  # TailwindCSS configuration
├── main.py                 # Launcher script
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration
```

### API Endpoints

- **POST /ask**: Send a text query to the AI
  - Request: `{ "query": "your question here" }`
  - Response: `{ "response": "AI response", "source": "ollama|gemini", "latency_ms": 123 }`

- **POST /transcribe**: Convert speech to text
  - Request: `FormData` with audio file
  - Response: `{ "text": "transcribed text" }`

### Adding New Features

- **New LLM Providers**: Add new service files similar to `gemini_fallback.py`
- **Enhanced UI Components**: Add to the `frontend/src/components` directory
- **Additional Storage Options**: Modify `App.tsx` for client-side or `database.py` for server-side

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- LLaMA 3.2 by Meta
- Ollama for local LLM hosting
- Gemini by Google
- Whisper by OpenAI

---

Built with ❤️ for privacy-first, voice-enabled AI assistance.