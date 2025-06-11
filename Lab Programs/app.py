from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Home</h1>"

@app.route('/About')
def about():
    return "about method called"

@app.route('/Contact')
def contact():
    return "contact method called"

if __name__ == '__main__':
    app.run(debug=True)
