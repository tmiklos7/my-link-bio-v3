from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# In-memory links store for the current app process.
links = [
    {"name": "OpenAI", "url": "https://openai.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Python", "url": "https://www.python.org"},
]


@app.route('/')
def home():
    return render_template('index.html', title='My Links', links=links)


@app.route('/add', methods=['POST'])
def add_link():
    site_name = request.form.get('name', '').strip()
    site_url = request.form.get('url', '').strip()

    if site_name and site_url:
        links.append({"name": site_name, "url": site_url})

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
        links[link_index] = {"name": site_name, "url": site_url}

    return redirect(url_for('home'))


@app.route('/delete/<int:link_index>', methods=['POST'])
def delete_link(link_index):
    if 0 <= link_index < len(links):
        links.pop(link_index)

    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
