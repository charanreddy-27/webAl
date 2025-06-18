from flask import Flask, session, request, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

template = """
<!doctype html>
<title>Session Demo</title>
<h2>Session Example</h2>
<form method="POST" action="/setsession">
Enter your name: <input type="text" name="username">
<input type="submit" value="Set Session">
</form>
<br>
<a href="/getsession">Check Session</a> <br>
<a href="/clearsession">Clear Session</a>
"""

@app.route('/')
def home():
    return render_template_string(template)

@app.route('/setsession', methods=['POST'])
def setsession():
    username = request.form.get('username')
    session['username'] = username
    return f"Session has been set for user: {username}<br><a href='/'>Go back</a>"

@app.route('/getsession')
def getsession():
    username = session.get('username')
    if username:
        return f"Hello {username}, you are logged in via session!"
    else:
        return "No session found. Please enter your name first."

@app.route('/clearsession')
def clearsession():
    session.pop('username', None)
    return "Session has been cleared!<br><a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)