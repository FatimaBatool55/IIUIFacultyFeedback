from flask import Flask, render_template, request, redirect
from database import create_database, save_feedback
from email_service import send_thank_you, send_admin_notification

app = Flask(__name__)
create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    student_name = request.form["student_name"]
    student_email = request.form["student_email"]

    faculty_rating = request.form["faculty_rating"]
    course_rating = request.form["course_rating"]
    facilities_rating = request.form["facilities_rating"]
    administration_rating = request.form["administration_rating"]
    overall_rating = request.form["overall_rating"]

    comments = request.form["comments"]

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

    return redirect("/success")

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)