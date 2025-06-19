# SwarAI - Voice-Enabled AI Assistant

SwarAI is a lightweight, accessible, voice-first Progressive Web App (PWA) that allows users to speak naturally, get intelligent responses, and store their voice conversations. It works in modern browsers on mobile, tablet, and desktop — no installation required.

## Features

- **Voice-First Interface**: Speak naturally and get intelligent responses
- **Hybrid AI System**: Uses locally hosted LLM via Ollama (LLaMA 3.2) with fallback to external LLM APIs (Gemini)
- **Progressive Web App**: Works offline and can be installed on devices
- **Database Storage**: Stores conversations in PostgreSQL
- **Local-First**: Prioritizes privacy by using local models when available
- **Cross-Platform**: Works on desktop, tablet, and mobile devices

## Architecture

SwarAI uses a hybrid architecture:
- **Frontend**: React + TailwindCSS Progressive Web App
- **Backend**: FastAPI (Python) with SQLAlchemy
- **Primary AI**: Local Ollama running LLaMA 3.2
- **Fallback AI**: Google's Gemini Pro API
- **Database**: PostgreSQL
- **Storage**: IndexedDB for local storage in browser

## Prerequisites

- Node.js and npm (for frontend)
- Python 3.8+ (for backend)
- PostgreSQL database
- [Ollama](https://ollama.ai/) with LLaMA 3.2 model installed
- Google Gemini API key(s) (for fallback)

## Setup

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/swarai

# Gemini API Keys (comma-separated for multiple keys)
GEMINI_API_KEYS=your-gemini-api-key-1,your-gemini-api-key-2

# Whisper API Key for speech-to-text
WHISPER_API_KEY=your-whisper-api-key

# Server Configuration
PORT=8000
HOST=0.0.0.0
```

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure Ollama is running with LLaMA 3.2:
   ```bash
   ollama run llama3.2
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser to `http://localhost:3000`
2. Allow microphone access when prompted
3. Click the microphone button and start speaking
4. Your speech will be transcribed and sent to the AI
5. The AI response will be displayed in the chat

## Project Structure

```
swarai/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ollama_helper.py     # Ollama LLM integration
│   ├── gemini_fallback.py   # Gemini API fallback
│   ├── models.py            # Database models
│   └── database.py          # Database connection
├── frontend/
│   ├── public/              # Static assets
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── index.tsx        # React entry point
│   │   ├── components/
│   │   │   ├── Recorder.tsx # Voice recording component
│   │   │   └── ChatBubble.tsx # Message display component
│   └── tailwind.config.js   # TailwindCSS configuration
├── README.md
├── .env                     # Environment variables (gitignored)
```

## Development

- The backend server runs on port 8000 by default
- The frontend development server runs on port 3000 by default
- API communication happens via POST requests to `/ask`

## License

MIT