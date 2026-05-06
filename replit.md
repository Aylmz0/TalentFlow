# TalentFlow

A Django-based talent management and job matching platform.

## Architecture

- **Framework**: Django 5.2 (Python 3.10)
- **Database**: PostgreSQL (Replit managed, via `DATABASE_URL` environment variable)
- **Static Files**: WhiteNoise for serving static assets
- **Production Server**: Gunicorn

## Project Structure

```
talentflow/
├── apps/
│   ├── accounts/       # Custom user model (AbstractUser + target_role, cv_file)
│   ├── jobs/           # Job listings (Kaggle + SerpAPI sources)
│   ├── talent_models/  # Skills, Applications, UserProjects
│   ├── dashboard/      # Dashboard app (templates only)
│   └── interviews/     # Interviews app (templates only)
├── config/             # Django project config (settings, urls, wsgi, asgi)
├── core/
│   ├── interfaces/     # Abstract interfaces
│   └── services/       # Business logic (ai_coach, resume_parser, ingestion, matchmaking)
├── infrastructure/
│   ├── ai_client/      # AI provider integration
│   ├── repositories/   # Data access layer
│   └── serp_api/       # SerpAPI integration for live job data
├── templates/          # HTML templates (dashboard/, interviews/, partials/)
├── static/             # Static files
└── media/              # User-uploaded files (CVs, etc.)
```

## Key Models

- `accounts.User` — Extended Django user with `target_role` and `cv_file`
- `jobs.Job` — Job listings from Kaggle dataset or live SerpAPI
- `talent_models.Skill` — Skills catalog
- `talent_models.JobSkill` — Skills required per job
- `talent_models.UserSkill` — Skills a user has (with level 1-5)
- `talent_models.Application` — User job applications with status tracking
- `talent_models.UserProject` — AI-recommended project ideas for users

## Running the App

```
python3 manage.py runserver 0.0.0.0:5000
```

## Environment Variables

- `DATABASE_URL` — PostgreSQL connection string (set by Replit)
- `SECRET_KEY` — Django secret key (optional, has default for dev)

## Deployment

Configured as `autoscale` using Gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 config.wsgi:application
```
