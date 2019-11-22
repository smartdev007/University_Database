"""
    @author Jenish Kevadia

    Script implements flask and creates a website that displays university database
"""

import os
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/students')
def student_courses():
    path = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(path, 'stevens.db')

    try:
        db = sqlite3.connect(db_file)
    except sqlite3.OperationalError:
        return f'Unable to open database at path {db_file}'
    else:
        query = """SELECT Instructors.CWID, Instructors.Name, Instructors.Dept, Grades.Course, COUNT(*) AS Students
                    From Instructors JOIN Grades
                    ON Instructors.CWID = Grades.InstructorCWID
                    GROUP BY Instructors.Name, Grades.Course;
                """
        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'students': students} for cwid, name, dept, course, students in db.execute(query)]

        db.close()

        return render_template(
            'stevens.html',
            title = 'Stevens Repository',
            table_title = 'Number of completed courses by student',
            students = data
        )
    
app.run(debug=True)


