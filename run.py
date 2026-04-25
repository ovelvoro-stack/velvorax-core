from flask import Flask, render_template_string, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "velvorax-super-secure-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "velvorax.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ================= DATABASE =================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ================= TEMPLATE =================

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Velvorax Corporate</title>
<style>
body {margin:0;font-family:Arial;background:#0f172a;color:white;}
.container {width:400px;margin:80px auto;background:#1e293b;padding:30px;border-radius:10px;}
input {width:100%;padding:10px;margin:10px 0;border:none;border-radius:5px;}
button {width:100%;padding:10px;background:#2563eb;color:white;border:none;border-radius:5px;}
h2 {text-align:center;}
.logo {text-align:center;font-size:22px;font-weight:bold;margin-bottom:20px;color:#38bdf8;}
.link {text-align:center;margin-top:10px;}
a {color:#60a5fa;text-decoration:none;}
.dashboard {text-align:center;margin-top:100px;}
</style>
</head>
<body>

<div class="logo">VELVORAX GLOBAL CRM</div>

{% if page == "register" %}
<div class="container">
<h2>Company Registration</h2>
<form method="POST">
<input type="text" name="company" placeholder="Company Name" required>
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Register</button>
</form>
<div class="link">
<a href="{{ url_for('login') }}">Already Registered? Login</a>
</div>
</div>

{% elif page == "login" %}
<div class="container">
<h2>Company Login</h2>
<form method="POST">
<input type="email" name="email" placeholder="Email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Login</button>
</form>
<div class="link">
<a href="{{ url_for('register') }}">Create Company Account</a>
</div>
</div>

{% elif page == "dashboard" %}
<div class="dashboard">
<h2>Welcome {{ company }}</h2>
<p>Corporate Dashboard Active</p>
<a href="{{ url_for('logout') }}">Logout</a>
</div>
{% endif %}

</body>
</html>
"""

# ================= ROUTES =================

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        user = User(
            company=request.form["company"],
            email=request.form["email"],
            password=hashed
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template_string(TEMPLATE, page="register")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            session["company"] = user.company
            return redirect(url_for("dashboard"))
    return render_template_string(TEMPLATE, page="login")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template_string(TEMPLATE, page="dashboard", company=session["company"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= RUN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)