import smtplib
import random

from email.message import EmailMessage


import os

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")


# ---------------------------------------
# Send Thank You Email
# ---------------------------------------

def send_thank_you(student_email, student_name):

    try:

        message = EmailMessage()

        message["Subject"] = "Thank You - IIUI Faculty Feedback"
        message["From"] = SENDER_EMAIL
        message["To"] = student_email

        message.set_content(f"""
Dear {student_name},

Thank you for completing the IIUI Faculty Feedback Survey.

Your valuable feedback helps improve teaching quality, university facilities, and student services.

We appreciate your time and contribution.

Regards,

International Islamic University Islamabad (IIUI)

Faculty Feedback Committee
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(message)

    except Exception as e:
        print("Thank You Email Error:", e)


# ---------------------------------------
# Send Admin Notification
# ---------------------------------------

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

    try:

        message = EmailMessage()

        message["Subject"] = "New Faculty Feedback Received"
        message["From"] = SENDER_EMAIL
        message["To"] = SENDER_EMAIL

        message.set_content(f"""
A new faculty feedback form has been submitted.

-----------------------------------------

Student Name : {student_name}

Student Email : {student_email}

-----------------------------------------

Faculty Rating : {faculty_rating}

Course Rating : {course_rating}

Facilities Rating : {facilities_rating}

Administration Rating : {administration_rating}

Overall Rating : {overall_rating}

-----------------------------------------

Comments

{comments}

-----------------------------------------

This email was generated automatically by the IIUI Faculty Feedback System.
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(message)

    except Exception as e:
        print("Admin Email Error:", e)


# ---------------------------------------
# Generate OTP
# ---------------------------------------

def generate_otp():

    otp = ""

    for _ in range(6):
        otp += str(random.randint(0, 9))

    return otp


# ---------------------------------------
# Send OTP Email
# ---------------------------------------

def send_otp(student_email, otp):

    try:

        message = EmailMessage()

        message["Subject"] = "IIUI Email Verification OTP"
        message["From"] = SENDER_EMAIL
        message["To"] = student_email

        message.set_content(f"""
Dear Student,

Your One-Time Password (OTP) for IIUI Faculty Feedback Verification is:

{otp}

This OTP is valid for only one verification.

Do not share this code with anyone.

Regards,

IIUI Faculty Feedback System
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(message)

    except Exception as e:
        print("OTP Email Error:", e)
