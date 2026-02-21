# Remarcable Product Catalog

A Django-based product catalog

## Tech Stack

- **Python 3** + **Django 6.0**
- **django-money** — currency-aware price fields (USD / CAD)
- **SQLite** — default dev database

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/soysushi/remarcable.git
cd remarcable
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the development server

**Note:** The database (`db.sqlite3`) is pre-populated with sample data for your convenience.

If the database file is missing or you want to reset it:

```bash
rm db.sqlite3  # Optional: Remove existing database
python manage.py migrate
python manage.py loaddata sample_data
```

Start the server:

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/) to browse the catalog.

### 5. (Optional) Create a superuser for the admin panel

```bash
python manage.py createsuperuser
```

Admin is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Project Structure

```
remarcable/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── remarcable/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── products/            # Main app
    ├── models.py        # Category, Tag, Product (with TimeStampedModel base)
    ├── views.py         # ProductListView with search, filter, pagination
    ├── forms.py         # ProductFilterForm
    ├── admin.py         # Customized admin with annotations & fieldsets
    ├── signals.py       # Auto-generate slugs on save
    ├── urls.py
    ├── fixtures/
    │   └── sample_data.json
    └── templates/
        ├── base.html
        └── products/
            └── product_list.html
```

## Features

- **Search** — case-insensitive search across product name and description
- **Category filter** — dropdown to narrow by category (e.g. Wire & Cable, Panels & Breakers)
- **Tag filter** — multi-select checkboxes (e.g. Commercial, Industrial, Prefab, Data Center)
- **Pagination** — 10 products per page
- **Auto-slug generation** — slugs are created automatically via `pre_save` signals
- **N+1 prevention** — queries use `select_related` / `prefetch_related`
- **Currency support** — prices stored with currency via `django-money` (USD / CAD)

## Sample Data

The database comes pre-populated with:
- **8 categories** (Conduit & Fittings, Wire & Cable, Panels & Breakers, etc.)
- **10 tags** (Commercial, Residential, Industrial, High Voltage, Low Voltage, Data Center, Prefab, Job Site Essential, Outdoor Rated, Heavy Duty)
- **38 products** — realistic electrical contractor supplies

Sample data can be reloaded via: `python manage.py loaddata sample_data`

## Sample Data Categories

| Category | Example Products |
|---|---|
| Conduit & Fittings | EMT conduit, rigid conduit, PVC conduit, compression couplings |
| Wire & Cable | THHN wire, Romex, MC cable, Cat6 plenum |
| Panels & Breakers | Load centers, circuit breakers, 3-phase panelboards, disconnects |
| Boxes & Enclosures | Junction boxes, old work boxes, NEMA 4X enclosures |
| Lighting | High bays, LED troffers, exit signs, temp job site lights |
| Power Tools | Milwaukee drills, DeWalt saws, Greenlee benders, Fluke meters |
| Safety & PPE | Arc flash shields, insulated gloves, FR vests, LOTO kits |
| Switches & Receptacles | GFCI outlets, Decora switches, twist-lock receptacles |

## AI-Generated Code

Minimal AI assistance was used in this project:

- **Slug generation logic** (`apps/products/signals.py`): The `generate_unique_slug()` function
- **Frontend templates** (`base.html`, `product_list.html`): HTML structure and CSS styling
- **Form widgets** (`apps/products/forms.py`): Bootstrap CSS classes and `CheckboxSelectMultiple` widget suggestion

### Human Contributions

All other code was written by the submitter, including:
- Project architecture and structure
- Models, views, forms, admin, and URL configuration
- Signal handlers setup and registration
- Sample data fixtures
- All business logic and database queries

All AI-generated code has been reviewed, understood, and can be fully explained by the submitter.
