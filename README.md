# Eye Fleet - Fleet Management System

A comprehensive fleet management system built with Next.js frontend and Django backend.

## Project Structure

```
eye-fleet/
├── frontend/          # Next.js frontend
│   ├── src/
│   │   └── app/      # Next.js pages and components
│   └── package.json
└── backend/          # Django backend
    └── eyefleet/
        ├── manage.py
        └── eyefleet/  # Django settings
```

## Setup Instructions

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```bash
   cd backend/eyefleet
   ```

2. Install Python dependencies:
   ```bash
   pip3 install django djangorestframework django-cors-headers
   ```

3. Apply database migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

4. Start the Django development server:
   ```bash
   python3 manage.py runserver
   ```
   The backend will be available at `http://localhost:8000/docs/`

### Frontend Setup (Next.js)

1. From the project root directory, install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

## Ollama API Setup

The fleet-vision page includes an AI assistant powered by Gemma-2b through Ollama. Follow these steps to set it up:

### 1. Install Ollama

First, install Ollama on your system:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the Gemma-2b Model

After installing Ollama, pull the Gemma-2b model:

```bash
ollama pull gemma2:2b
```

### 3. Start Ollama Server

Start the Ollama server in a terminal:

```bash
ollama serve
```

### 4. Set Up Python Flask Server

The Flask server acts as a bridge between the frontend and Ollama. Set it up as follows:

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the Flask server:
```bash
# From the project root directory
python3 ollama_api/generate.py
```

The Flask server will run on `http://localhost:5328` and provide the following endpoint:
- POST `/ollama_api/generate`: Handles chat messages and communicates with Ollama

### Verification

To verify everything is working:

1. Ensure Ollama server is running (default: http://localhost:11434)
2. Ensure Flask server is running (http://localhost:5328)
3. Navigate to the fleet-vision page in your Next.js app
4. Try sending a message in the chat interface

### Troubleshooting

If you encounter issues:

1. Check if Ollama server is running:
```bash
curl http://localhost:11434/api/tags
```

2. Check if Flask server is running:
```bash
curl http://localhost:5328/ollama_api/generate -X POST -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

3. Common issues:
   - "Network Error": Make sure both Ollama and Flask servers are running
   - "Model not found": Run `ollama pull gemma2:2b` again
   - CORS errors: Ensure Flask server is running with CORS enabled

## Features

- Add new vehicles with detailed information
- View fleet overview with statistics
- Interactive map showing vehicle locations
- Comprehensive vehicle list with status indicators
- Dark mode support
- Responsive design for all screen sizes

## API Endpoints


add an asset:(http://localhost:8000/api/maintenance/assets/) 

## Development

To run both servers for development:

1. Start the Django backend:
   ```bash
   cd backend/eyefleet
   python3 manage.py runserver
   ```

2. In a new terminal, start the Next.js frontend:
   ```bash
   npm run dev
   ```

