from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# HTML template with a form and links to get and clear cookies.
template = """
<!doctype html>
<title>Cookie Demo</title>
<h2>Cookie Example</h2>
<!-- Simple form to accept user's name -->
<form method="POST" action="/setcookie">
Enter your name: <input type="text" name="username">
<input type="submit" value="Set Cookie">
</form>
<br>
Experiment 1: Implement a simple demonstration of creating,
retrieving, and deleting: 1) Cookies 2) Sessions

<!-- Links to check and clear cookies -->
<a href="/getcookie">Check Cookie</a> <br>
<a href="/clearcookie">Clear Cookie</a>
"""

@app.route('/')
def home():
    # render_template_string is used to render inline HTML content
    return render_template_string(template)

@app.route('/setcookie', methods=['POST'])
def setcookie():
    username = request.form.get('username')
    # make_response allows us to attach cookies to a response object
    resp = make_response(f"Cookie has been set for user: {username}<br><a href='/'>Go back</a>")
    if username:
        # set_cookie sets a cookie key-value pair in the response
        resp.set_cookie('username', username)
    return resp

@app.route('/getcookie')
def getcookie():
    # request.cookies is used to access cookies sent by the browser
    username = request.cookies.get('username')
    if username:
        return f"Hello {username}, welcome back!"
    else:
        return "No cookie found. Please enter your name first."

@app.route('/clearcookie')
def clearcookie():
    # make_response allows modification of the response before returning
    resp = make_response("Cookie has been cleared!<br><a href='/'>Go back</a>")
    # Setting cookie value to empty and expiry to 0 deletes the cookie
    resp.set_cookie('username', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)