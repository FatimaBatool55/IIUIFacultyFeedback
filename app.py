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

    student_email = session.get("student_email")

    # Extract first name from email
    # fatima.bscs4932@student.iiu.edu.pk -> Fatima
    username = student_email.split("@")[0]
    first_name = username.split(".")[0].capitalize()

    return render_template(
        "index.html",
        first_name=first_name
    )


# -----------------------------
# Submit Feedback
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    first_name = request.form["first_name"].strip()
    last_name = request.form["last_name"].strip()

    # Validate last name
    if not re.fullmatch(r"[A-Za-z]{2,30}", last_name):
        return render_template(
            "index.html",
            first_name=first_name,
            error="Enter a valid last name using letters only."
        )

    student_name = first_name + " " + last_name

    student_email = session.get("student_email")

    hide_identity = request.form.get("hide_identity") == "yes"

    faculty_rating = request.form["faculty_rating"]
    course_rating = request.form["course_rating"]
    facilities_rating = request.form["facilities_rating"]
    administration_rating = request.form["administration_rating"]
    overall_rating = request.form["overall_rating"]

    comments = request.form["comments"]

    # Save actual data to database
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

    # Send thank you email
    try:
        print("Sending thank you email...")
        send_thank_you(student_email, student_name)
        print("Thank you email sent.")
    except Exception as e:
        print("THANK YOU EMAIL ERROR:", str(e))

    # Send admin email
    try:
        print("Sending admin email...")
        send_admin_notification(
            student_name,
            student_email,
            faculty_rating,
            course_rating,
            facilities_rating,
            administration_rating,
            overall_rating,
            comments,
            hide_identity
        )
        print("Admin email sent.")
    except Exception as e:
        print("ADMIN EMAIL ERROR:", str(e))

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
