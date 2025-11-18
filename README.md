🏨 Hotel Booking System

A complete hotel room booking and management platform built with Django, Django REST Framework, Celery, and Docker.
This system provides REST APIs for reservations, room availability, user authentication, and automated tasks such as email notifications.

✨ Features
🛏️ Booking & Reservations
- Create, update, and cancel room reservations
- Check room availability
- Overlapping booking prevention
- Reservation history per user

🔐 Authentication & Authorization
- JWT authentication
- Protected endpoints for customers and administrators
- User registration and login

🌐 REST API
- Endpoints built with Django REST Framework
- Pagination, filtering, and serialization
- Validation of room capacity and dates

📧 Background Tasks
- Automated confirmation emails using Celery
- Celery workers + Redis as message broker
- Asynchronous reservation processing

🐳 Docker Support
- Fully containerized application
- Docker Compose for local development
- Containers: Django API, Redis, Celery Worker, Celery Beat

🚀 Quick Start

# Clone the repository
git clone https://github.com/PatrickMenegassi/Sistema-Reserva-Hoteis.git

# Run with Docker
docker-compose up --build

📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| GET | `/api/rooms/` | List available rooms |
| POST | `/api/reservations/` | Create reservation |
