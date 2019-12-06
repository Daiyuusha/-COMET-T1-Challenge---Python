# Class for creating Student instances
# Students can take or drop classes
class Student:
    idNum = 12000000

    def __init__(self, username, password, name, age, program, college):
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.program = program
        Student.idNum += 1
        self.idNum = Student.idNum
        self.college = college
        self.courses = []
        self.passedcourses = []

    def addPassedCourse(self, student, course): #Adding courses completed by the student
        if student is None:
            self.passedcourses.append(course)
        if course not in self.courses: #Student can only finish courses that he is currently taking
            print("Sorry, you cannot add this to your completed courses.")
            return
        if course in self.passedcourses: #If course has already been passed
            print("Sorry, you have already passed this course before.")
            return

        self.passedcourses.append(course) # Adds to list of courses passed
        self.courses.remove(course) # Removes from current list of courses
        course.removeStudent(self) #Removes student from the course class list
        print(course.code, "is successfully added to passed courses.")


    def addCourse(self, course): #Function for enrolling in a class
        if course in self.courses: #If Student already has the course
            print("You already have that class.")
            return

        if course in self.passedcourses: #If Student already passed the course
            print("You have already passed this course.")
            return

        if course.addStudent(self): # Success condition
            print("Successfully added the course.")
            self.courses.append(course)
        else: # Requirements for student enrollment is ninvalid
            print("Course was not added successfully. Requirements were not met.")
            return

    def removeCourse(self, course): #Function for dropping of classes
        if course not in self.courses: #If a student removes a non-existing course from his list
            print("You do not have a course named", course.name, " in your list of courses.")
            return
        for elem in self.courses: # Iterates to check the course
            if course == elem:
                self.courses.remove(elem)
                course.removeStudent(self)
                print("Course removed successfully.")
                return

    def display(self): #Used to display the updated details of the student
        print(" ____ ____ ____ ____ ____ ____ ____ \n",
              "||S |||t |||u |||d |||e |||n |||t ||\n",
              "||__|||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|/__\|\n",
              " ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ \n",
              "||I |||n |||f |||o |||r |||m |||a |||t |||i |||o |||n ||\n",
              "||__|||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|\n")

        print("Full Name: ", self.name)
        print("Age: ", self.age)
        print("Program: ", self.program)
        print("College: ", self.college)
        print("ID Number: ", self.idNum)
        print("\n\nCourses: ")
        self.displayCourses(self.courses)
        print("\n\nPassed Courses: ")
        self.displayCourses(self.passedcourses)

    def displayCourses(self, courses):
        print(
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("{0:30} {1:30} {2:30} {3:30} {4:30} {5:30} {6:30} {7:30}".format("CLASSNBR", "COURSE", "SECTION", "DAYS","TIME", "ROOM", "ENRL CAP", "ENROLLED"))
        print(
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for elem in courses:
            print("{0:<30} {1:30} {2:30} {3:30} {4:30} {5:30} {6:<30} {7:<30}".format(elem.classNbr, elem.name,
                                                                                      elem.section, elem.days,
                                                                                      elem.time, elem.room,
                                                                                      elem.capacity,
                                                                                      len(elem.students)))
        print(
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")


# Class to represent a subject/course offered to students
class Course:

    def __init__(self, name, code, units, professor, days, time, section, classNbr, room, capacity):
        self.name = name
        self.code = code
        self.units = units
        self.professor = professor
        self.days = days
        self.time = time
        self.section = section
        self.classNbr = classNbr
        self.room = room
        self.capacity = capacity

        self.students = [] # Class list
        self.prerequisites = []

    def addStudent(self, student): # Adds a student to the class
        # Returns boolean values for further validation
        if len(self.students) < self.capacity and self.validate(student): #If course can still handle student in terms of capacity
            self.students.append(student)
            return True
        else:
            print("Enrollment is not possible.")
            return False

    def validate(self, student):  #Student validation process: Prereq checking
        for elem in self.prerequisites:
            if elem not in student.passedcourses:
                return False

        return True

    def removeStudent(self, student): #Removes a student from the class
        for elem in self.students:
            if elem == student: # Checks if student is in the class/list of students from the course
                self.students.remove(student)

    def addPrereq(self, prereq): #Function to add a prerequisite to a class
        self.prerequisites.append(prereq)



# This class represents the admin entity of the project and its properties
class Admin:
    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name

    def addCourse(self, courses, course): # Adds a course to the current list of courses
        for elem in courses:
            if course.classNbr == elem.classNbr: # ClassNbr is an identifier for a course / This checks the validity of the classnumber
                print("Course Number already exists in the current courses")
                return

        courses.append(course) # Course is added to the list
        print("Successfully added the course.")

    def removeCourse(self, courses, course, enrollment): # Removes a course from the current list of courses
        if course in courses: # Checks if course is existing, remove from courses
            courses.remove(course)
            for student in enrollment.students: #Removes the instances of the course from students currently enrolling in the course
                if course in student.courses:
                    student.courses.remove(course)

            print("Successfuly removed the course .")
            return

        else:
            print("The course you have entered is not in the course offerings.")

# The Enrollment class provides the primary interactions among Student, Admin, and Course objects
class Enrollment:
    def __init__(self):
        self.students = []
        self.courses = []
        self.admins = []

    def addCourse(self, admin): # Function for the admin to add a course
        print(" ____ ____ ____ _________ ____ ____ ____  \n",
              "||A |||d |||d |||       |||N |||e |||w ||\n",
              "||__|||__|||__|||_______|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|\n",
              " ____ ____ ____ ____ ____ ____ \n",
              "||C |||o |||u |||r |||s |||e ||\n",
              "||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|\n")
        print("Course Name: ", end="")
        name = input()
        print("Course Code: ", end="")
        code = input()
        print("Number of Units:  ", end="")
        units = input()
        print("Course Instructor: ", end="")
        professor = input()
        print("Course Schedule (Days of the Week):  [M,T,W,H,F,S] ", end="")
        days = input()
        print("Course Schedule (Time: 24 Hour Format): ", end="")
        time = input()
        print("Course Section: ", end="")
        section = input()
        print("Course Number (Class Number):", end="")
        classNbr = input()
        print("Course Venue: ", end="")
        room = input()
        print("Course Capacity:  ", end="")
        capacity = input()

        course = Course(name, code, (int)(units), professor, days, time, section, classNbr, room, (int)(capacity))
        if admin.addCourse(self.classes, course):
            print("Successfully added the course.")

    def removeCourse(self, admin): # Function for the admin to remove a course
        print(" ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ ____ ____ \n",
              "||R |||e |||m |||o |||v |||e |||       |||C |||o |||u |||r |||s |||e ||\n",
              "||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|\n")
        self.displayCourses()
        print("Enter the Class Number of the course you wish to remove: ", end="")
        classNbr = input()
        for elem in self.courses:
            if (classNbr == elem.classNbr):
                course = elem
                admin.removeCourse(self.courses, course, self)
                return

        print("The course you have entered is not in the course offerings.")

    def displayCourses(self): # Utility function to display the updated information of courses
        print(" ____ ____ ____ ____ ____ ____\n",
              "||C |||o |||u |||r |||s |||e ||\n",
              "||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|\n",
              " ____ ____ ____ ____ ____ ____ ____ ____ ____ \n",  # ʕ•́ᴥ•̀ʔっ ʕ•́ᴥ•̀ʔっ ʕ•́ᴥ•̀ʔっ ʕ•́ᴥ•̀ʔっʕ•́ᴥ•̀ʔっʕ•́ᴥ•̀ʔっʕ•́ᴥ•̀ʔっʕ•́ᴥ•̀ʔっ
              "||O |||f |||f |||e |||r |||i |||n |||g |||s ||\n",
              "||__|||__|||__|||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|\n")
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        print("{0:20} {1:20} {2:20} {3:20} {4:20} {5:20} {6:20} {7:20} {8:<20}".format("CLASSNBR", "COURSE", "SECTION",
                                                                                       "DAYS", "TIME", "ROOM",
                                                                                       "ENRL CAP", "ENROLLED",
                                                                                       "PREREQ"))
        print(
            "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        for i in range(len(self.courses)):
            pres = ''
            for j in range(len(self.courses[i].prerequisites)):
                pres = pres + self.courses[i].prerequisites[j].code #Concetenation of prerequisite courses
            print("{0:<20} {1:20} {2:20} {3:20} {4:20} {5:20} {6:<20} {7:<20} {8:<20}".format(self.courses[i].classNbr,
                                                                                              self.courses[i].name,
                                                                                              self.courses[i].section,
                                                                                              self.courses[i].days,
                                                                                              self.courses[i].time,
                                                                                              self.courses[i].room,
                                                                                              self.courses[
                                                                                                  i].capacity,
                                                                                              len(self.courses[
                                                                                                      i].students),
                                                                                              pres))
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

    def addStudent(self):
        print(" ____ ____ ____ _________ ____ _________ ____ ____ ____ ____ ____ ____ ____ \n",
              "||A |||d |||d |||       |||a |||       |||S |||t |||u |||d |||e |||n |||t ||\n",
              "||__|||__|||__|||_______|||__|||_______|||__|||__|||__|||__|||__|||__|||__||\n",
              "|/__\|/__\|/__\|/_______\|/__\|/_______\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|\n")

        print("Fullname of Student: ", end='')
        name = input()
        print("Username Assigned to Student:", end='')
        username = input()
        print("Password of Student: ", end='')
        password = input()
        print("Age of Student: ", end='')
        age = input()
        print("Degree Program of Student: ", end='')
        program = input()
        print("College of Student: ", end='')
        college = input()
        self.students.append(Student(username, password, name, age, program, college)) # Created student is added to the list of students

    def initAddStudent(self, student):
        self.students.append(student)

    def initAddAdmin(self, admin):
        self.admins.append(admin)


# Initialiaztion for Simulation (ɔ◔‿◔)ɔ ♥



comet = Course("COMET", "COMET", 3, "Darth Vader", "TH", "0730-1000", "S16", "1002", "G302B", 50)

csmath2 = Course("Algebra", "CSMATH2", 3, "Duke Delos Santos", "WF", "0915-1045", "S11", "2001", "G204", 40)
csmath2.addPrereq(comet)

gefili1 = Course("Filipino", "GEFILI1", 3, "Lilibeth Quiore", "TH", "0730-0900", "S11", "2002", "G206", 5)
gefili1.addPrereq(comet)

ccprog3 = Course("OOP", "CCPROG3", 3, "Shirley Chu", "WF", "0730-0900", "S16", "2003", "G302B", 10)

csalgcm = Course("Algo", "CSALGCM", 3, "Neil Del Gallego", "TH", "1430-1600", "S16", "2004", "G208", 35)

csadprg = Course("Language", "CSADPRG", 3, "Charibeth Cheng", "MW", "0915-1045", "S12", "2005", "G210", 20)
csadprg.addPrereq(comet)

enroll = Enrollment()

bryce = Student("bryce", "p@ssword", "Bryce Ramirez", 19, "BSCS-ST", "CCS")
enroll.initAddStudent(bryce)

pj = Student("pjong", "1234", "Patrick Ong", 19, "BSCS-CSE", "CCS")
enroll.initAddStudent(pj)
pj.addPassedCourse(None, comet)

trisha = Student("trisha", "3sha", "Trisha Pelagio", 19, "BSCS-NE", "CCS")
enroll.initAddStudent(trisha)

tony = Admin("toeknee", "winteriscomming", "Toe Knee")
enroll.initAddAdmin(tony)




tony.addCourse(enroll.courses, comet)
tony.addCourse(enroll.courses, csmath2)
tony.addCourse(enroll.courses, gefili1)
tony.addCourse(enroll.courses, ccprog3)
tony.addCourse(enroll.courses, csalgcm)
tony.addCourse(enroll.courses, csadprg)


# 3 Student Accounts are initially created:
#
# 1.
# username: bryce
# password: p@ssword
#
# 2.
# username: pjong
# password: 1234
#
# 3.
# username: trisha
# password: 3sha

# 1 Admin account is initially created:
#
# username: toeknee
# password: winteriscomming


# Main Program Run

program = True
while program:
    user = 0
    while user == 0:
        print("@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@@@@ %%@@@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@@@% %%%@@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@@@  %%%@@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@@   %%%%@@@@@@@@@@@@@@@@\n",
              "@@@@@@@@@@@@@@@%   %%%%%@@@@@@@@@@@@@@@\n",
              "%%%%%%%%%%%%%%%    %%%%%%%%%%%%%%%%%%%%\n",
              "@@@%   %%%%%%%%%%  %%%%         %%%%@@@\n",
              "@@@@@@       %%%%% %%    %%%%%%%%@@@@@@\n",
              "@@@@@@@@%          %%%%%%%%%%%%@@@@@@@@\n",
              "@@@@@@@@@@@% %%%%% %%    %%%@@@@@@@@@@@\n",
              "@@@@@@@@@@@%%%%%%  %%%%    %@@@@@@@@@@@\n",
              "@@@@@@@@@@@%%%%    #%%%%    @@@@@@@@@@@\n",
              "@@@@@@@@@@%%%%     %%%%%%%  #@@@@@@@@@@\n",
              "@@@@@@@@@@%%    %@@@@@%%%%%  %@@@@@@@@@\n",
              "@@@@@@@@@%%  %@@@@@@@@@@@%%%  @@@@@@@@@\n",
              "@@@@@@@@%% @@@@@@@@@@@@@@@@@%%%@@@@@@@@\n",
              "@@@@@@@@%% @@@@@@@@@@@@@@@@@%%%@@@@@@@@\n")
        print(" \t    /\  _ . _ _  _   (~._ _|_\n",
              "\t   /~~\| ||| | |(_)  _)|/_ | ")
        print("\n\nWelcome to Animo Sizt!")
        print("Username: ", end='')
        username = input()

        for elem in enroll.students:
            if username == elem.username:
                user = elem
                break
        for elem in enroll.admins:
            if username == elem.username:
                user = elem
                break

        if user == 0:
            print("There are no users with that username.")

    passwordval = False

    while not passwordval:
        print("Password: ", end='')
        password = input()
        if password == user.password:
            print("Login is successful. Welcome", user.username)
            passwordval = True
        else:
            print("Wrong password.")

    if type(user) == Student:
        menu = 0
        while menu != 6:
            print("\n\n\n【﻿Ｅｎｒｏｌｌｍｅｎｔ　Ｓｙｓｔｅｍ】\n")
            print("【﻿Ｍｅｎｕ】")
            print(
                "[1] Enrollment: Add Classes\n[2] Enrollment: Remove Classes\n[3] View Student Data\n[4] Add Completed Courses\n[5] Change Password\n[6] Sign out")
            menu = int(input())

            if menu == 1:
                print("List of available courses: \n")
                enroll.displayCourses()
                print("Enter Course Class Number to add: ", end='')
                course = 0
                classnum = input()
                for elem in enroll.courses:
                    if (elem.classNbr == classnum):
                        course = elem
                if course != 0:
                    user.addCourse(course)
                else:
                    print("Input is invalid. Try again.")

            elif menu == 2:
                print("Courses Added: ")
                user.displayCourses(user.courses)
                print("Enter Course Class Number to remove ", end='')
                course = 0
                classnum = input()
                for elem in user.courses:
                    if (elem.classNbr == classnum):
                        course = elem
                if course != 0:
                    user.removeCourse(course)
                else:
                    print("Input is invalid. Try again.")

            elif menu == 3:
                print('\n')
                user.display()
                print("Press Enter to Proceed: ")

            elif menu == 4:
                user.displayCourses(user.courses)
                print("Enter Course Class Number to add ", end='')
                inp = input()
                course = 0
                for elem in user.courses:
                    if elem.classNbr == inp:
                        course = elem
                if course != 0:
                    user.addPassedCourse(user, course)
                else:
                    print("Input is invalid.")

            elif menu == 5:
                print("Current Username: ", user.username)
                print("Current Password: ", user.password)
                print("\nEnter New Password:", end='')
                password = input()
                user.password = password
                print("\nPassword Changed Successfully.")
            elif menu == 6:
                print("Thank you for using Animo Sizt. Signing out.\n\n\n")
            else:
                print("Input is invalid.")
    else:
        menu = 0
        while menu != 6:
            print("\n\n\n【﻿Ｅｎｒｏｌｌｍｅｎｔ　Ｓｙｓｔｅｍ】\n")
            print("【﻿Ｍｅｎｕ】")
            print("[1] Add Courses\n[2] Remove Courses\n[3] Display Current Courses\n[4] Change Password\n[5] Add Student\n[6] Sign Out")
            menu = int(input())
            if menu == 1:
                enroll.addCourse(user)
            elif menu == 2:
                enroll.removeCourse(user)
            elif menu == 3:
                enroll.displayCourses()
            elif menu == 4:
                print("Current Username: ", user.username)
                print("Current Password: ", user.password)
                print("\nEnter New Password:", end='')
                password = input()
                user.password = password
            elif menu == 5:
                enroll.addStudent()
            elif menu == 6:
                print("Thank you for using Animo Sizt. Signing out.\n\n\n")
            else:
                print("Input is invalid.")

