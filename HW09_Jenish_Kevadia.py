"""
    @author Jenish Kevadia

    Script creates the repository of the university
"""

import os
from prettytable import PrettyTable
from collections import defaultdict
from HW08_Jenish_Kevadia import file_reading_gen

class Repository:
    """ Repository to store information of students and instructors """
    def __init__(self, dir, pt=True):
        """ Initialize directory and dictionary """
        self._dir = dir
        self._students = dict()
        self._instructors = dict()

        try:
            self._get_students(os.path.join(dir, 'students.txt'))
            self._get_instructors(os.path.join(dir, 'instructors.txt'))
            self._get_grades(os.path.join(dir, 'grades.txt'))
        except ValueError as v:
            raise ValueError(v)
        except FileNotFoundError as f:
            raise FileNotFoundError(f)
        else:
            if pt:
                print(f'******** Student summary table ********')
                self.student_table()

                print(f'******** Instructor summary table ********')
                self.instructor_table()
        
    def _get_students(self, path):
        """ Read student details from the path and add to student dictionary """ 
        for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=False):
            self._students[cwid] = Student(cwid, name, major)

    def _get_instructors(self, path):
        """ Read instructor details from the path and add to instructor dictionary """ 
        for cwid, name, dept in file_reading_gen(path, 3, sep='\t', header=False):
            self._instructors[cwid] = Instructor(cwid, name, dept)
    
    def _get_grades(self, path):
        """ Read from grade file and assign the values to appropriate student and instructor """
        for std_cwid, course, grade, ins_cwid in file_reading_gen(path, 4, sep='\t', header=False):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Grade for unknown student {std_cwid}')

            if ins_cwid in self._instructors:
                self._instructors[ins_cwid].add_student(course)
            else:
                print(f'Grade for unknown instructor {ins_cwid}')
    
    def student_table(self):
        """ Summary of student table """
        ptable = PrettyTable(field_names = Student.ptable_header)

        [ptable.add_row(student.ptable_row()) for student in self._students.values()]
            
        print(ptable)
    
    def instructor_table(self):
        """ Summary of instructor table """
        ptable = PrettyTable(field_names = Instructor.ptable_header)

        for instructor in self._instructors.values():
            for row in instructor.ptable_row():
                ptable.add_row(row)
        
        print(ptable)


class Student:
    """ Student class """
    ptable_header = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid, name, major):
        """ Initialize student details """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._courses = dict()

    def add_course(self, course, grade):
        """ Add course with grade """
        self._courses[course] = grade

    def ptable_row(self):
        """ Return a row for student's prettytable """ 
        return [self._cwid, self._name, sorted(self._courses.keys())] 


class Instructor:
    """ Instructor class """
    ptable_header = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid, name, dept):
        """ Initialize instructor details """
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int)

    def add_student(self, course):
        """ Count the number of students took the course with this instructor """
        self._courses[course] += 1

    def ptable_row(self):
        """ Yield the rows for instructor prettytable """
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


def main():
    """ Pass the directory to Repository class """
    dir = 'C:\Jenish\Python-SSW810B'

    Repository(dir)


if __name__ == '__main__':
    """ Run main function on start """
    main()