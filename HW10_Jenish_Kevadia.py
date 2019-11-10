"""
    @author Jenish Kevadia

    Script adds new functionality to repository of the university
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
        self._majors = dict()

        try:
            self._get_majors(os.path.join(dir, 'majors.txt'))
            self._get_students(os.path.join(dir, 'students.txt'))
            self._get_instructors(os.path.join(dir, 'instructors.txt'))
            self._get_grades(os.path.join(dir, 'grades.txt'))
        except ValueError as v:
            raise ValueError(v)
        except FileNotFoundError as f:
            raise FileNotFoundError(f)
        else:
            if pt:
                print(f'******** Majors summary table ********')
                self.majors_table()

                print(f'******** Student summary table ********')
                self.student_table()

                print(f'******** Instructor summary table ********')
                self.instructor_table()
        
    def _get_students(self, path):
        """ Read student details from the path and add to student dictionary """ 
        for cwid, name, major in file_reading_gen(path, 3, sep=';', header=True):
            if major not in self._majors:
                print(f'Student {cwid} {name} has an unknown major {major}')
            else:
                self._students[cwid] = Student(cwid, name, self._majors[major])

    def _get_instructors(self, path):
        """ Read instructor details from the path and add to instructor dictionary """ 
        for cwid, name, dept in file_reading_gen(path, 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, dept)
    
    def _get_grades(self, path):
        """ Read from grade file and assign the values to appropriate student and instructor """
        for std_cwid, course, grade, ins_cwid in file_reading_gen(path, 4, sep='|', header=True):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Grade for unknown student {std_cwid}')

            if ins_cwid in self._instructors:
                self._instructors[ins_cwid].add_student(course)
            else:
                print(f'Grade for unknown instructor {ins_cwid}')

    def _get_majors(self, path):
        """ Read major details from majors file """
        for dept, flag, course in file_reading_gen(path, 3, sep='\t', header=True):
            if dept not in self._majors:
                self._majors[dept] = Major(dept)
            
            self._majors[dept].add_course(course, flag)

    def majors_table(self):
        """ Summary of majors table """
        ptable = PrettyTable(field_names = Major.ptable_header)

        for major in self._majors.values():
            ptable.add_row(major.ptable_row())

        print(ptable)

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


class Major:
    """ Majors class """
    ptable_header = ['Dept', 'Required', 'Electives']
    pass_grade = {'A', 'A-', 'B+', 'B-', 'C+', 'C'}

    def __init__(self, dept):
        """ Initialize major details """
        self._dept = dept
        self._required = set()
        self._electives = set()

    def add_course(self, course, check):
        """ Add courses to its respective category of required and electives """
        if check == 'R':
            self._required.add(course)
        elif check == 'E':
            self._electives.add(course)
        else:
            raise ValueError(f'Invalid course type: "{check}" ')

    def remaining(self, completed):
        """ Add remaining courses """
        passed = {course for course, grade in completed.items() if grade in Major.pass_grade}
        required_left = self._required - passed

        if self._electives.intersection(passed):
            electives_left = None
        else:
            electives_left = self._electives

        return self._dept, passed, required_left, electives_left

    def ptable_row(self):
        """ Return a row for majors' pretty table """
        return [self._dept, sorted(self._required), sorted(self._electives)]


class Student:
    """ Student class """
    ptable_header = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

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
        major, passed, required_left, electives_left = self._major.remaining(self._courses)
        return [self._cwid, self._name, major, sorted(passed), required_left, electives_left]


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