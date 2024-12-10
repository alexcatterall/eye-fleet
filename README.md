![Eye Fleet](Public/eye_fleet_logo.png)
![Entrepreneur First Hack](Public/EF_hack.avif)

# Eye Fleet - Modern Fleet Management System

[![Built with Next.js](https://img.shields.io/badge/Built%20with-Next.js-000000?style=flat-square&logo=Next.js)](https://nextjs.org/)
[![Backend: Django](https://img.shields.io/badge/Backend-Django-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)

We try to build an intelligent fleet management system that leverages AI to provide intelligent vehicle tracking, maintenance scheduling, and fleet optimisation.

## 👥 Team
- **Members**: [Kosi](https://github.com/asuzukosi) and [Alex](https://github.com/alexcatterall)
- **Event**: Entrepreneur First Fall Hack
- **Talent Investor**: Amy Brese
- **Date**: December 7th-8th 2024
- [View Presentation](https://docs.google.com/presentation/d/1WtD_G2vL_SqJvIVu5_JGixV7Ah6BgdQJwzBHdljkFYc/edit?usp=sharing)

## 🚀 Key Features

- **Real-time Fleet Dashboard**: Monitor your entire fleet at a glance
- **Vehicle Management**: Comprehensive vehicle tracking and information
- **Interactive Map**: Live location tracking with route visualization
- **AI-Powered Insights**: Intelligent fleet analysis using Gemma-2b
- **Maintenance Tracking**: Automated maintenance scheduling
- **Dark Mode Support**: Enhanced UI experience
- **Responsive Design**: Optimized for all devices

## 🏗️ Project Structure

```
eye-fleet/
├── frontend/          # Next.js frontend application
│   ├── src/          # Source code
│   │   ├── app/      # Next.js pages and components
│   │   ├── styles/   # Global styles and themes
│   │   └── lib/      # Utility functions and helpers
│   └── package.json  # Frontend dependencies
├── backend/          # Django backend services
   └── eyefleet/
     ├── manage.py
     ├── api/      # REST API endpoints 
        └── eyefleet/ # Core settings

```

## 🛠️ Quick Start Guide

### Backend Setup

```bash
# Navigate to backend directory
cd backend/eyefleet

# Install dependencies
pip3 install django djangorestframework django-cors-headers

# Apply database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Start Django server
python3 manage.py runserver
```
Backend API will be available at `http://localhost:8000/docs/`

### Frontend Setup

```bash
# Navigate to frontend directory
cd eye-fleet

# Install dependencies
npm install

# Start development server
npm run dev
```
Frontend will be available at `http://localhost:3000`


## 🔌 API Reference

| Endpoint | Method | Description | Example Request |
|----------|--------|-------------|-----------------|
| `/api/maintenance/assets/` | POST | Add new vehicle | `{"name": "Truck 1", "type": "Heavy Duty"}` |
| `/api/maintenance/assets/` | GET | List all vehicles | N/A |
| `/api/fleet/status/` | GET | Fleet overview | N/A |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Entrepreneur First for hosting the Fall Hack
- Amy Brese for talent investment and guidance