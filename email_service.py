import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "hajabatool01@gmail.com"
APP_PASSWORD = "ngmn bpob qpyq klxh"


def send_thank_you(student_email, student_name):
    message = EmailMessage()

    message["Subject"] = "Thank You for Your Feedback"
    message["From"] = SENDER_EMAIL
    message["To"] = student_email

    message.set_content(f"""
Dear {student_name},

Thank you for completing the IIUI Faculty Feedback Survey.

Your feedback is valuable and will help us improve the quality of education and student services.

Regards,

IIUI Administration
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(message)


def send_admin_notification(
    student_name,
    student_email,
    faculty_rating,
    course_rating,
    facilities_rating,
    administration_rating,
    overall_rating,
    comments
):
    message = EmailMessage()

    message["Subject"] = "New Faculty Feedback Submitted"
    message["From"] = SENDER_EMAIL
    message["To"] = SENDER_EMAIL

    message.set_content(f"""
A new faculty feedback form has been submitted.

Student Name: {student_name}
Student Email: {student_email}

Faculty Rating: {faculty_rating}
Course Content Rating: {course_rating}
Facilities Rating: {facilities_rating}
Administration Rating: {administration_rating}
Overall Rating: {overall_rating}

Comments:
{comments}
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(message)