# 🧠 SwarAI – Full Feature Prompt Specification

## 🔥 Objective

This prompt defines the full feature-set and expected conversational behaviors of **SwarAI**, a desktop-capable, browser-accessible AI assistant. It should act like a natural voice-based assistant that can interact with the local OS, apps, messaging platforms, and perform intelligent tasks via conversation.

---

## 🗣️ Conversational Capabilities

SwarAI should behave like a real human assistant and support:

### ✅ Core Interactions:

* Friendly, natural tone
* Memory of past interactions (stored in local DB)
* Can explain, clarify, joke, or guide the user step-by-step

### 🎭 Example Dialogues:

* **User**: "Open my resume."

  * **SwarAI**: "Sure! Opening your Word file titled 'Resume.docx'."
* **User**: "Send a birthday message to Arjun on WhatsApp."

  * **SwarAI**: "Got it! Launching WhatsApp Web and preparing your message for Arjun."
* **User**: "Write an apology email to my teacher."

  * **SwarAI**: "Done. Here's a draft email: \[insert]. Would you like me to send it?"

---

## 💻 Desktop Integration Tasks

### 🧰 Local OS Features (via Python + OS modules):

* `open_file(path)`: Open a document, image, video, etc.
* `write_to_word(content)`: Open MS Word and insert content
* `launch_app(app_name)`: Start installed apps like Chrome, Spotify, Word
* `read_clipboard()`: Return current clipboard content
* `screenshot()`: Take and save screenshot to disk
* `speak(text)`: Read out a message using TTS

### 📝 Word Automation (via `python-docx` or `pywin32`):

* Open Word template
* Insert text or generate new content
* Save as PDF or `.docx`

---

## 📲 Communication Features

### 🟢 WhatsApp Messaging

* Open WhatsApp Web
* Search for contact (via UI automation)
* Insert message & send (if permissions available)

### 📧 Email

* Authenticate with Gmail (via OAuth or SMTP)
* Compose and send emails
* Attach files if requested

---

## 🤹 Smart Features (AI-Powered)

* **Joke generator**: Pull jokes from local DB or OpenAI/Gemini
* **Summarizer**: Summarize pasted or spoken text
* **Speech-to-text**: Whisper for transcriptions
* **Contextual memory**: Store and recall session-level context
* **Sentiment checker**: Detect tone of user (angry, happy, etc.)

---

## 🧠 Prompt Guide (for Coding Assistants like Cursor or Copilot)

Use the following prompt to instruct the assistant to build SwarAI:

```
Build a hybrid voice assistant in Python + React that can:
- Transcribe voice via Whisper
- Respond using LLM (local via Ollama, fallback to Gemini API)
- Send WhatsApp Web messages using pyautogui or Selenium
- Send Gmail messages via SMTP or Gmail API
- Open files or launch apps (Word, Chrome, etc.) using Python's os or subprocess
- Create, write, and save a Word document via python-docx or pywin32
- Store chat history in PostgreSQL
- Deliver responses via browser-based chat UI (React + Tailwind)
- Work offline partially via service workers (PWA)
Ensure that everything runs via a local FastAPI backend, with async endpoints.
```

---

## 🏗️ Future Add-ons

* Calendar events integration
* Alarm or reminders
* Spotify music control
* File search and summarization
* Offline TTS (using Coqui or eSpeak)

---

## ✅ Evaluation Criteria

| Feature            | Complete When...                                     |
| ------------------ | ---------------------------------------------------- |
| WhatsApp Messaging | Message sent and confirmed in chat                   |
| Word Typing        | MS Word opens and saves new content file             |
| Email              | Message is delivered to recipient's inbox            |
| Voice Interaction  | App responds to spoken prompts fully                 |
| Fallback AI        | Switches from local LLM to Gemini if needed          |
| UI                 | Fully responsive chat interface with visual feedback |

---

## 🔒 Security & Permissions

* Files and apps should only be opened with user confirmation.
* WhatsApp and Gmail access should be opt-in and securely authenticated.
* All user data must be locally stored unless explicitly uploaded.

---

## 🎯 Summary

SwarAI should function like an **OS-level intelligent assistant**, combining:

* The power of local and cloud AI
* System-level access
* Conversational awareness
* A simple UI-first browser delivery model

This is not a chatbot. It's an **AI co-pilot for your device**.

---
