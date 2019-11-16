"""
    @author Jenish Kevadia

    Script imports methods from 'HW11_Jenish_Kevadia.py' script and implements test cases
"""

import unittest
import os
import sqlite3
from HW11_Jenish_Kevadia import file_reading_gen, Repository, Student, Instructor, Major

class TestRepository(unittest.TestCase):
    """ Test for repository """

    def test_Instructor_attributes(self):
        """ Testing instructors table """
        calculated = list()

        db = sqlite3.connect('C:\\Jenish\\Python-SSW810B\\testdb.db')


        expected = {('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),     
                    ('98762', 'Hawking, S', 'CS', 'CS 501', 1),     
                    ('98762', 'Hawking, S', 'CS', 'CS 546', 1),     
                    ('98762', 'Hawking, S', 'CS', 'CS 570', 1),     
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),     
                    ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4)}
        
        query = 'SELECT Instructors.CWID, Instructors.Name, Instructors.Dept, Grades.Course, count(*) AS    Students FROM Instructors JOIN Grades ON Instructors.CWID = Grades.InstructorCWID GROUP BY Instructors.Name, Grades.Course;'

        for row in db.execute(query):
            calculated.append(row)

        self.assertEqual(expected, calculated)


if __name__ == "__main__":
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
