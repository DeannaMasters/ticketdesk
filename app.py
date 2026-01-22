from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
import os
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-placeholder")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default="Low")


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.get("/register")
def register(): 
    return render_template("register.html")


@app.post("/register")
def register_post():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    if not email or not password:
        flash("Email and password are required.", "danger")
        return render_template("register.html", error="Email and password are required.")

    if User.query.filter_by(email=email).first():
        flash("That email is already registered.", "danger")
        return render_template("register.html", error="That email is already registered.")

    u = User(email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()

    flash("Account created. Please log in.", "success")
    return redirect(url_for("login"))


@app.get("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def login_post():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""

    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password):
        return render_template("login.html", error="Invalid email or password.")

    remember = request.form.get("remember") == "1"
    login_user(u, remember=remember)
    flash("Welcome back!", "success")
    return redirect(url_for("home"))


@app.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.get("/")
@login_required
def home():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template("home.html", tickets=tickets)


@app.post("/tickets")
@login_required
def create_ticket():
    title = (request.form.get("title") or "").strip()
    severity = (request.form.get("severity") or "Low").strip()

    if title:
        t = Ticket(title=title, severity=severity)
        db.session.add(t)
        db.session.commit()

    return redirect(url_for("home"))


@app.get("/tickets/<int:ticket_id>/edit")
@login_required
def edit_ticket(ticket_id: int):
    t = Ticket.query.get_or_404(ticket_id)
    return render_template("edit.html", ticket=t)


@app.post("/tickets/<int:ticket_id>/edit")
@login_required
def edit_ticket_post(ticket_id: int):
    t = Ticket.query.get_or_404(ticket_id)

    title = (request.form.get("title") or "").strip()
    severity = (request.form.get("severity") or "Low").strip()

    if title:
        t.title = title
        t.severity = severity
        db.session.commit()

    return redirect(url_for("home"))


@app.post("/tickets/<int:ticket_id>/delete")
@login_required
def delete_ticket(ticket_id: int):
    t = Ticket.query.get_or_404(ticket_id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/api/tickets")
@login_required
def api_tickets():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return jsonify([{"id": t.id, "title": t.title, "severity": t.severity} for t in tickets])


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
