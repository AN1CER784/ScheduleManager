# ScheduleManager

**ScheduleManager** is a Django-based **corporate task manager** for organizing work inside companies.

Key features:
- Company -> Projects -> Tasks -> People
- Clear task workflow with roles (creator + assignee) and status transitions
- Task deadlines and priority
- Task results with multiple messages
- Change history (audit log) for key fields
- Bonus points system for on-time completion and overdue penalties
- Localization (Russian supported)

---

## Technologies & Dependencies

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

## Docker Setup

1. **Create or edit** the `.env` file in the `docker/` directory with the following variables:

   ```dotenv
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   SECRET_KEY=
   ALLOWED_HOSTS=             # comma-separated hostnames or IPs
   DEBUG=                     # True or False
   ```

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

## Project Structure

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

## Core Functionality

* **Task Workflow**
  NEW -> IN_PROGRESS -> ON_REVIEW -> DONE with strict role-based transitions.
* **Audit & Results**
  Track changes to key fields and attach multiple result messages per task.
* **Bonuses**
  Automatic points for on-time completion and overdue penalties.
* **Scheduling**
  Calendar view for assigned tasks.
* **Localization**
  Interface translation to Russian via `django-modeltranslation`.
