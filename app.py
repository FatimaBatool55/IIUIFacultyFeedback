from flask import Flask, render_template, request, redirect, session
import re

from database import create_database, save_feedback
from email_service import (
    send_thank_you,
    send_admin_notification,
    generate_otp,
    send_otp
)

app = Flask(__name__)
app.secret_key = "iiui_feedback_secret_key"

create_database()


# -----------------------------
# Login Page
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------
# Send OTP
# -----------------------------
@app.route("/send-otp", methods=["POST"])
def send_otp_route():

    student_email = request.form["student_email"].strip().lower()

    allowed_domains = (
        "@student.iiu.edu.pk",
        "@iiu.edu.pk"
    )

    if not student_email.endswith(allowed_domains):
        return render_template(
            "login.html",
            error="Please use your official IIUI email."
        )

    otp = generate_otp()

    session["otp"] = otp
    session["student_email"] = student_email

    send_otp(student_email, otp)

    return render_template("verify_otp.html")


# -----------------------------
# Verify OTP
# -----------------------------
@app.route("/verify", methods=["POST"])
def verify():

    entered_otp = request.form["otp"].strip()

    if entered_otp != session.get("otp"):
        return render_template(
            "verify_otp.html",
            error="Invalid OTP. Please try again."
        )

    return redirect("/feedback")


# -----------------------------
# Feedback Form
# -----------------------------
@app.route("/feedback")
def feedback():

    if "student_email" not in session:
        return redirect("/")

    return render_template("index.html")


# -----------------------------
# Submit Feedback
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    student_name = request.form["student_name"].strip()

    student_email = session.get("student_email")

    faculty_rating = request.form["faculty_rating"]
    course_rating = request.form["course_rating"]
    facilities_rating = request.form["facilities_rating"]
    administration_rating = request.form["administration_rating"]
    overall_rating = request.form["overall_rating"]

    comments = request.form["comments"]

    # Validate student name
    if not re.fullmatch(r"[A-Za-z ]{3,50}", student_name):
        return render_template(
            "index.html",
            error="Enter a valid name using letters only."
        )

    save_feedback(
        student_name,
        student_email,
        faculty_rating,
        course_rating,
        facilities_rating,
        administration_rating,
        overall_rating,
        comments
    )

    send_thank_you(
        student_email,
        student_name
    )

    send_admin_notification(
        student_name,
        student_email,
        faculty_rating,
        course_rating,
        facilities_rating,
        administration_rating,
        overall_rating,
        comments
    )

    session.clear()

    return redirect("/success")


# -----------------------------
# Success Page
# -----------------------------
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
