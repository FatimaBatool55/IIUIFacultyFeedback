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


# -----------------------------------
# Login Page
# -----------------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------------
# Send OTP
# -----------------------------------
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


# -----------------------------------
# Verify OTP
# -----------------------------------
@app.route("/verify", methods=["POST"])
def verify():

    entered_otp = request.form["otp"].strip()

    if entered_otp != session.get("otp"):
        return render_template(
            "verify_otp.html",
            error="Invalid OTP. Please try again."
        )

    return redirect("/feedback")


# -----------------------------------
# Feedback Page
# -----------------------------------
@app.route("/feedback")
def feedback():

    if "student_email" not in session:
        return redirect("/")

    student_email = session["student_email"]

    # Extract first name from email
    username = student_email.split("@")[0]

    # fatima.bscs4932 -> Fatima
    first_name = username.split(".")[0].capitalize()

    return render_template(
        "index.html",
        first_name=first_name
    )


# -----------------------------------
# Submit Feedback
# -----------------------------------
@app.route("/submit", methods=["POST"])
def submit():

    student_email = session.get("student_email")

    if not student_email:
        return redirect("/")

    username = student_email.split("@")[0]
    first_name = username.split(".")[0].capitalize()

    last_name = request.form["last_name"].strip()

    if not re.fullmatch(r"[A-Za-z ]{2,30}", last_name):
        return render_template(
            "index.html",
            first_name=first_name,
            error="Please enter a valid last name."
        )

    student_name = f"{first_name} {last_name}"

    faculty_rating = request.form["faculty_rating"]
    course_rating = request.form["course_rating"]
    facilities_rating = request.form["facilities_rating"]
    administration_rating = request.form["administration_rating"]
    overall_rating = request.form["overall_rating"]

    comments = request.form["comments"]

    hide_identity = request.form.get("hide_identity")

    # -----------------------
    # Save REAL data
    # -----------------------

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

    # -----------------------
    # Thank You Email
    # -----------------------

    try:
        send_thank_you(
            student_email,
            student_name
        )
    except Exception as e:
        print("THANK YOU EMAIL ERROR:", e)

    # -----------------------
    # Hide identity for admin
    # -----------------------

    if hide_identity:

        admin_name = "********"

        admin_email = "********"

    else:

        admin_name = student_name

        admin_email = student_email

    # -----------------------
    # Admin Email
    # -----------------------

    try:

        send_admin_notification(

            admin_name,

            admin_email,

            faculty_rating,

            course_rating,

            facilities_rating,

            administration_rating,

            overall_rating,

            comments

        )

    except Exception as e:

        print("ADMIN EMAIL ERROR:", e)

    session.clear()

    return redirect("/success")


# -----------------------------------
# Success Page
# -----------------------------------
@app.route("/success")
def success():

    return render_template("success.html")


# -----------------------------------
# Run App
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
