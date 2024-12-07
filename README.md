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

## Note

Make sure to replace the Google Maps API key in `my-fleet/page.tsx` with your own key for the map functionality to work.
