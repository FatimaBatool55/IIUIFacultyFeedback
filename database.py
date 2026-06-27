import sqlite3


def create_database():

    connection = sqlite3.connect("feedback.db")

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

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

    connection = sqlite3.connect("feedback.db")

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

    VALUES(?,?,?,?,?,?,?,?)

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

    connection.close()