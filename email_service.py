import os
import random
import smtplib
from email.message import EmailMessage


# ---------------------------------------
# Environment Variables
# ---------------------------------------

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")


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

This OTP is valid for one verification only.

Do not share this OTP with anyone.

Regards,

IIUI Faculty Feedback System
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(SENDER_EMAIL, APP_PASSWORD)

            smtp.send_message(message)

        print("OTP email sent successfully.")

    except Exception as e:

        print("OTP Email Error:", str(e))


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

We sincerely appreciate your participation.

Regards,

International Islamic University Islamabad (IIUI)

Faculty Feedback Committee
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(SENDER_EMAIL, APP_PASSWORD)

            smtp.send_message(message)

        print("Thank You email sent successfully.")

    except Exception as e:

        print("Thank You Email Error:", str(e))


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
A new Faculty Feedback Form has been submitted.

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

Comments:

{comments}

-----------------------------------------

This email was generated automatically by the IIUI Faculty Feedback System.
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(SENDER_EMAIL, APP_PASSWORD)

            smtp.send_message(message)

        print("Admin notification email sent successfully.")

    except Exception as e:

        print("Admin Email Error:", str(e))
