# Task Management System

A full-stack task management application that allows users to authenticate with Google, create and assign tasks, track task status, and receive email notifications for task assignments, task completion, and upcoming due dates.

The application is built with Next.js and TypeScript on the frontend, Flask on the backend, and Supabase for authentication and database management.

## 🚀 Live Demo

**Frontend:**  
https://task-management-system-five-bice.vercel.app/

**Backend API:**  
https://task-management-backend-65sz.onrender.com/

---

## 📌 Features

### Authentication
- Google OAuth authentication using Supabase
- Secure session-based authentication
- Protected dashboard
- Backend token verification
- User synchronization between Supabase Authentication and the application database

### Task Management
- Create tasks
- Add task descriptions
- Assign tasks to other registered users
- Set task due dates
- View assigned and created tasks
- Mark assigned tasks as completed
- Track task status

### Email Notifications
- Email notification when a task is assigned
- Email notification when a task is completed
- Due-date reminder emails
- Gmail API integration for sending emails

### Due-Date Reminder System
- Tasks can have a due date
- Background scheduler checks pending tasks
- Tasks due within the next 24 hours are identified
- Reminder email is sent to the assigned user
- `reminder_sent` prevents duplicate reminder emails

### Deployment
- Frontend deployed on Vercel
- Backend deployed on Render
- Supabase used as the production database and authentication provider
- Environment variables used for sensitive configuration

---

## 🛠️ Tech Stack

### Frontend

- Next.js
- TypeScript
- React
- CSS
- Supabase SSR

### Backend

- Python
- Flask
- Flask-CORS
- REST API
- APScheduler

### Database & Authentication

- Supabase
- PostgreSQL
- Supabase Authentication
- Google OAuth

### Email

- Gmail API
- Google OAuth 2.0

### Deployment

- Vercel
- Render

### Development Tools

- Git
- GitHub
- VS Code
- Thunder Client

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Next.js Frontend  │
                    │      (Vercel)       │
                    └──────────┬──────────┘
                               │
                    REST API + Auth Token
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    │      (Render)       │
                    └──────┬──────┬───────┘
                           │      │
                 ┌─────────┘      └──────────┐
                 ▼                            ▼
        ┌─────────────────┐          ┌─────────────────┐
        │    Supabase     │          │    Gmail API    │
        │ PostgreSQL/Auth │          │ Email Service   │
        └─────────────────┘          └─────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │   APScheduler    │
                  │ Due Date Checker │
                  └──────────────────┘