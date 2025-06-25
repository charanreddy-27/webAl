from flask import Flask, session, redirect, request
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = 'exit-metrics-demo-key'

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            exit_page TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- Helper ----------
def log_exit(session_id, page):
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO sessions (id, exit_page) VALUES (?, ?)", (session_id, page))
    conn.commit()
    conn.close()

# ---------- Routes ----------
@app.route('/')
def home():
    session.clear()
    return '''
    <h1>Welcome to Our Newsletter</h1>
    <p><a href="/signup">Sign Up</a></p>
    <p><a href="/metrics">View Exit Metrics</a></p>
    '''

@app.route('/signup')
def signup():
    session['session_id'] = str(uuid.uuid4())
    return '''
    <h1>Newsletter Signup</h1>
    <form action="/subscribe" method="POST">
        <input type="email" name="email" required placeholder="Your email">
        <button type="submit">Subscribe</button>
    </form>
    <p><a href="/exit/signup">Exit Without Signing Up</a></p>
    '''

@app.route('/subscribe', methods=['POST'])
def subscribe():
    session_id = session.get('session_id')
    if session_id:
        log_exit(session_id, 'subscribe')
        session.clear()
    return '''
    <h1>Thank You!</h1>
    <p>You’ve successfully subscribed.</p>
    <p><a href="/">Return Home</a></p>
    '''

@app.route('/exit/<page>')
def exit_page(page):
    session_id = session.get('session_id')
    if session_id:
        log_exit(session_id, page)
        session.clear()
    return redirect('/')

@app.route('/metrics')
def metrics():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM sessions")
    total = c.fetchone()[0] or 1  # avoid division by zero
    c.execute("SELECT COUNT(*) FROM sessions WHERE exit_page = 'signup'")
    exit_signup = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM sessions WHERE exit_page = 'subscribe'")
    exit_subscribe = c.fetchone()[0]
    conn.close()
    percent_signup = (exit_signup / total) * 100
    percent_subscribe = (exit_subscribe / total) * 100
    return f'''
    <h1>Exit Page Metrics</h1>
    <p>Total Sessions Recorded: {total}</p>
    <h2>Exit Rate Details</h2>
    <ul>
        <li>Signup Page: {exit_signup} exits ({percent_signup:.2f}%)</li>
        <li>Subscribe Page: {exit_subscribe} exits ({percent_subscribe:.2f}%)</li>
    </ul>
    <p><a href="/">Return Home</a></p>
    '''

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)