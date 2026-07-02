import sqlite3


def get_connection():
    return sqlite3.connect("feedback.db")


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_name TEXT NOT NULL,

        student_email TEXT UNIQUE NOT NULL,

        anonymous TEXT,

        faculty_rating INTEGER,

        course_rating INTEGER,

        facilities_rating INTEGER,

        administration_rating INTEGER,

        overall_rating INTEGER,

        comments TEXT

    )
    """)

    connection.commit()

    connection.close()


def email_exists(student_email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "SELECT id FROM feedback WHERE student_email=?",

        (student_email,)

    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def save_feedback(

        student_name,
        student_email,
        anonymous,
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

        anonymous,

        faculty_rating,

        course_rating,

        facilities_rating,

        administration_rating,

        overall_rating,

        comments

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """,

    (

        student_name,

        student_email,

        anonymous,

        faculty_rating,

        course_rating,

        facilities_rating,

        administration_rating,

        overall_rating,

        comments

    )

    )

    connection.commit()

    connection.close()


def get_all_feedback():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

    SELECT *

    FROM feedback

    ORDER BY id DESC

    """)

    data = cursor.fetchall()

    connection.close()

    return data
