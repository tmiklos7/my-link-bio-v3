from flask import Flask, redirect, render_template, request, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

NOT_AVAILABLE = "Not Available"


# In-memory links store for the current app process.
links = [
    {"name": "OpenAI", "url": "https://openai.com", "og_title": NOT_AVAILABLE, "og_description": NOT_AVAILABLE, "og_image": NOT_AVAILABLE},
    {"name": "GitHub", "url": "https://github.com", "og_title": NOT_AVAILABLE, "og_description": NOT_AVAILABLE, "og_image": NOT_AVAILABLE},
    {"name": "Python", "url": "https://www.python.org", "og_title": NOT_AVAILABLE, "og_description": NOT_AVAILABLE, "og_image": NOT_AVAILABLE},
]


def extract_og_metadata(site_url):
    """Fetch a page and parse Open Graph metadata used by social cards."""
    metadata = {
        "og_title": NOT_AVAILABLE,
        "og_description": NOT_AVAILABLE,
        "og_image": NOT_AVAILABLE,
    }

    try:
        response = requests.get(site_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return metadata

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('meta', attrs={'property': 'og:title'})
    description_tag = soup.find('meta', attrs={'property': 'og:description'})
    image_tag = soup.find('meta', attrs={'property': 'og:image'})

    if title_tag and title_tag.get('content'):
        metadata['og_title'] = title_tag['content']
    if description_tag and description_tag.get('content'):
        metadata['og_description'] = description_tag['content']
    if image_tag and image_tag.get('content'):
        metadata['og_image'] = image_tag['content']

    return metadata


@app.route('/')
def home():
    return render_template('index.html', title='My Links', links=links)


@app.route('/add', methods=['POST'])
def add_link():
    site_name = request.form.get('name', '').strip()
    site_url = request.form.get('url', '').strip()

    if site_name and site_url:
        metadata = extract_og_metadata(site_url)
        links.append({"name": site_name, "url": site_url, **metadata})

    return redirect(url_for('home'))


@app.route('/edit/<int:link_index>')
def edit_link(link_index):
    if not 0 <= link_index < len(links):
        return redirect(url_for('home'))

    link = links[link_index]
    return render_template('edit.html', title='Edit Link', link=link, link_index=link_index)


@app.route('/update/<int:link_index>', methods=['POST'])
def update_link(link_index):
    if not 0 <= link_index < len(links):
        return redirect(url_for('home'))

    site_name = request.form.get('name', '').strip()
    site_url = request.form.get('url', '').strip()

    if site_name and site_url:
        metadata = extract_og_metadata(site_url)
        links[link_index] = {"name": site_name, "url": site_url, **metadata}

    return redirect(url_for('home'))


@app.route('/delete/<int:link_index>', methods=['POST'])
def delete_link(link_index):
    if 0 <= link_index < len(links):
        links.pop(link_index)

    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='Page Not Found'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', title='Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True)
