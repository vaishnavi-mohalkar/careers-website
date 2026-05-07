# TalentHub Careers Website

A careers website for job seekers built with Python and Flask.

## Architecture

- **Backend**: Python 3.11 + Flask
- **Database**: SQLite via Flask-SQLAlchemy
- **Frontend**: Jinja2 templates + vanilla CSS/JS
- **Entry point**: `app.py`
- **Port**: 5000

## Project Structure

```
app.py              # Flask application, routes, models
templates/          # Jinja2 HTML templates
  base.html         # Shared layout (navbar, footer)
  index.html        # Homepage with featured jobs
  jobs.html         # Jobs listing with filters
  job_detail.html   # Individual job detail page
  apply.html        # Application form
  application_success.html  # Post-apply confirmation
  about.html        # About company page
static/
  css/style.css     # All styles
  js/main.js        # Minimal JS (nav toggle, alerts)
```

## Running

```bash
python app.py
```

The app seeds sample job data on first run automatically.

## User Preferences

- Python + Flask for backend
- SQLite for database (no external DB required)
- Clean, professional design
