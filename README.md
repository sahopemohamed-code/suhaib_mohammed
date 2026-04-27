# BusNet 🚌

A Django web app for booking bus routes — built as a CS50 Web Lab extension of the airport example.

## Features

### Core Requirements
- **Station & Route models** — ForeignKey relationships (origin/destination → Station), ManyToMany to Django's built-in User
- **Authentication** — Register, Login, Logout using Django's built-in auth system
- **Index page** — Lists all routes with passenger counts and search
- **Route detail page** — Shows passengers, Book/Unbook buttons (login required)
- **Booking restricted** — Anonymous users cannot book; redirected to login

### Bonus Features (+15%)
- ✅ **"My Routes" page** — Shows all routes the logged-in user has booked
- ✅ **Station detail page** — Lists all departing and arriving routes for a station
- ✅ **Search/filter** — Filter routes by origin or destination city/station name
- ✅ **Passenger count** — Shown on every route card on the index page
- ✅ **Bootstrap 5 styling** — Polished, responsive UI with custom orange theme

## Setup (Local)

```bash
git clone <repo-url>
cd busnet

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set a real SECRET_KEY

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Seed Data
```bash
python manage.py shell
>>> from routes.models import Station
>>> for s in [('Central','Ramadi'), ('University','Ramadi'), ('Downtown','Baghdad'), ('Airport','Baghdad')]:
...     Station.objects.create(name=s[0], city=s[1])
```
Then add routes via `/admin/`.

## Deploy to Render

1. Push to GitHub (make sure `.env` is in `.gitignore`)
2. Create a **Postgres** database on Render (Free plan)
3. Create a **Web Service** on Render:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
4. Set environment variables:
   - `SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `DEBUG` — `False`
   - `DATABASE_URL` — Internal Database URL from Render Postgres
   - `PYTHON_VERSION` — `3.12.0`

## Known Limitations
- Free Render Postgres expires after 90 days
- Free tier sleeps after 15 min inactivity (first request is slow)
