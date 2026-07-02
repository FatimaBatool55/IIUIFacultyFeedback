import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(

        id SERIAL PRIMARY KEY,

        student_name TEXT,

        student_email TEXT,

        faculty_rating TEXT,

        course_rating TEXT,

        facilities_rating TEXT,

        administration_rating TEXT,

        overall_rating TEXT,

        comments TEXT

    )
    """)

    connection.commit()

    cursor.close()

    connection.close()


def save_feedback(
        student_name,
        student_email,
        faculty_rating,
        course_rating,
        facilities_rating,
        administration_rating,
        overall_rating,
        comments
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    INSERT INTO feedback(

        student_name,
        student_email,
        faculty_rating,
        course_rating,
        facilities_rating,
        administration_rating,
        overall_rating,
        comments

    )

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)

    """,

    (

        student_name,
        student_email,
        faculty_rating,
        course_rating,
        facilities_rating,
        administration_rating,
        overall_rating,
        comments

    ))

    connection.commit()

    cursor.close()

    connection.close()
