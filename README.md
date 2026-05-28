# my-link-bio-v3

## Project Overview

A personal link in bio page built with Python and Flask. Users can add favorite links, view link preview metadata, learn about the page, and find contact details.

## Features

- Add links from the home page at `/`.
- Edit or delete existing links.
- View Open Graph metadata when it is available for a link.
- See a warning and distinct card style when a saved link has no retrievable preview metadata.
- Visit `/about` for a short about page.
- Visit `/contact` to see a short message and contact email address.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## Dependencies

- Flask: serves the web application and routes.
- requests: fetches link pages for metadata.
- beautifulsoup4: parses Open Graph metadata from fetched pages.
