from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    links = [
        {"name": "OpenAI", "url": "https://openai.com"},
        {"name": "GitHub", "url": "https://github.com"},
        {"name": "Python", "url": "https://www.python.org"},
    ]
    return render_template('index.html', title='My Links', links=links)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
