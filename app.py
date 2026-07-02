from flask import Flask, render_template, request, redirect

import re

from database import (
    create_database,
    save_feedback,
    email_exists
)

from email_service import (
    send_thank_you,
    send_admin_notification
)

app = Flask(__name__)

create_database()


# ------------------------------
# Home Page
# ------------------------------

@app.route("/")
def home():
    return render_template(
        "index.html",
        error=""
    )


# ------------------------------
# Submit Feedback
# ------------------------------

@app.route("/submit", methods=["POST"])
def submit():

    student_name = request.form["student_name"].strip()

    student_email = request.form["student_email"].strip().lower()

    anonymous = request.form.get("anonymous")

    faculty_rating = request.form["faculty_rating"]

    course_rating = request.form["course_rating"]

    facilities_rating = request.form["facilities_rating"]

    administration_rating = request.form["administration_rating"]

    overall_rating = request.form["overall_rating"]

    comments = request.form["comments"].strip()

    # ----------------------------------------
    # Name Validation
    # ----------------------------------------

    if not re.fullmatch(r"[A-Za-z ]{3,60}", student_name):

        return render_template(
            "index.html",
            error="Student name must contain only letters and spaces."
        )

    # ----------------------------------------
    # IIUI Email Validation
    # ----------------------------------------

    if not student_email.endswith("@iiu.edu.pk"):

        return render_template(
            "index.html",
            error="Only IIUI email addresses are allowed."
        )

    # ----------------------------------------
    # Email Format Validation
    # ----------------------------------------

    email_pattern = r'^[A-Za-z0-9._%+-]+@iiu\.edu\.pk$'

    if not re.fullmatch(email_pattern, student_email):

        return render_template(
            "index.html",
            error="Enter a valid IIUI email address."
        )

    # ----------------------------------------
    # Duplicate Feedback Check
    # ----------------------------------------

    if email_exists(student_email):

        return render_template(
            "index.html",
            error="Feedback has already been submitted using this email."
        )

    # ----------------------------------------
    # Comments Validation
    # ----------------------------------------

    if len(comments) < 10:

        return render_template(
            "index.html",
            error="Comments should contain at least 10 characters."
        )

    # ----------------------------------------
    # Anonymous Feedback
    # ----------------------------------------

    if anonymous == "yes":

        display_name = "Anonymous"

        anonymous_value = "Yes"

    else:

        display_name = student_name

        anonymous_value = "No"

    # ----------------------------------------
    # Save Feedback
    # ----------------------------------------

    save_feedback(

        student_name,

        student_email,

        anonymous_value,

        faculty_rating,

        course_rating,

        facilities_rating,

        administration_rating,

        overall_rating,

        comments

    )

    # ----------------------------------------
    # Send Thank You Email
    # ----------------------------------------

    send_thank_you(

        student_email,

        student_name

    )

    # ----------------------------------------
    # Notify Administrator
    # ----------------------------------------

    send_admin_notification(

        display_name,

        student_email,

        faculty_rating,

        course_rating,

        facilities_rating,

        administration_rating,

        overall_rating,

        comments

    )

    return redirect("/success")


# ------------------------------
# Success Page
# ------------------------------

@app.route("/success")
def success():

    return render_template(
        "success.html"
    )


# ------------------------------
# Run Application
# ------------------------------

if __name__ == "__main__":
    app.run(
        debug=True
    )
