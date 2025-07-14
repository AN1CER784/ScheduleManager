# ScheduleManager

**ScheduleManager** is a Django-based web application for **task tracking and productivity analysis**.  
It uses a combination of **Cellular Automata** and **LLM (Large Language Model)** logic to visualize user behavior and assess task completion patterns.

Key features:
- Task tracking and scheduling  
- Grouping by projects and weekly planning
- Productivity insights powered by Cellular Automata and LLM  
- Localization (Russian supported)  
- User productivity reports emails via celery

---

## 🛠️ Technologies & Dependencies

- **Python 3.10**, **Django 5.2.1**  
- **Celery 5.5.2** + Redis  
- **PostgreSQL**  
- `django-debug-toolbar`  
- `django-modeltranslation`  
- **Gunicorn**  
- **Bootstrap**, **jQuery**  
- **Docker** & **Docker Compose**  

All Python dependencies are listed in `requirements.txt`.

---

## 🚀 Docker Setup

1. **Create or edit** the `.env` file in the `docker/` directory with the following variables:

   ```dotenv
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   SECRET_KEY=
   ALLOWED_HOSTS=             # comma‑separated hostnames or IPs
   DEBUG =                    # True or False


2. **Build and run** containers:

   ```bash
   cd docker
   docker-compose up --build # for localhost (development)
   ```

This will start:

* Django + Nginx
* PostgreSQL
* Redis
* Celery worker & beat

The web app will be available at [http://localhost:80/].

---

## 📁 Project Structure

```
/
├── docker/                  # Docker & env configuration
│   ├── .env
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.dev.conf
│   ├── nginx.prod.conf
├── locale/ru/LC_MESSAGES    # Translation files
├── ScheduleManager/         # Project settings
├── analysis/                # Productivity analysis module
├── common/                  # Shared utilities & mixins
├── main/                    # Homepage
├── projects/                # Project grouping
├── schedule/                # Scheduling app
├── tasks/                   # Tasks management app
├── templates/               # Base HTML templates
├── users/                   # Users app
├── requirements.txt
```

---

## ✨ Core Functionality

* **Productivity Tracking**
  Tracks tasks and evaluates patterns in productivity.
* **LLM + Cellular Automaton Analysis**
  Visual representation and intelligent analysis of user behavior.
* **Scheduling**
  Organize tasks by projects and visualize them.
* **Background Processing**
  Email notifications, data cleanups, and analysis via Celery.
* **Localization**
  Interface translation to Russian via `django-modeltranslation`.

