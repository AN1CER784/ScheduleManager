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

## Simplified Local Run

For local development, it is simpler to run Django from a local virtual environment and lift only PostgreSQL + Redis through Docker from the project root.

1. **Create or edit** the `.env` file in the project root with the following variables:

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

2. **Create and activate** a virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate
   # Linux / macOS
   source .venv/bin/activate
   ```

3. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Start infrastructure from the project root**:

   ```bash
   docker compose up -d
   ```

5. **Apply migrations and run Django**:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

This will start:

* PostgreSQL
* Redis

The web app will be available at [http://localhost:8000/].

If needed, start Celery separately in additional terminals:

```bash
celery -A ScheduleManager worker -l info
celery -A ScheduleManager beat -l info
```

---

## Docker Setup

If you need the full containerized environment with Nginx, Django and Celery inside containers:

1. **Create or edit** the `.env` file in the project root.

2. **Run docker compose from the `docker/` directory**:

   ```bash
   cd docker
   docker compose up --build
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
