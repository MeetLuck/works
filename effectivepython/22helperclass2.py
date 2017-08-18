# item 22: Prefer Helper Classes Over Bookkeeping with Dicts and Tuples
# using namedtuple
#
' 1-3  Grade Book '
# mid: 40%, final: 60%
#      |     math      english   chemistry     physics
# -----+---------------------------------------------------
# Jim  |    90,80      80,70       70,90       50,40
# Jane |    70,90      90,70       60,40       95,80
# Tom  |    70,30      60,40       40,40       25,40
# Jerry|    92,94      90,98       95,97       95,96

import collections
Grade = collections.namedtuple('Grade',('score','weight'))

class Subject(object): # math, english, physics, chemistry,...
    def __init__(self):
        self.grades = []
    def report_grade(self,score,weight):
        self.grades.append( Grade(score,weight) )
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self.grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total/total_weight
    def __str__(self):
        return str(self.grades)

class Student(object):
    def __init__(self):
        self.subjects = dict()
    def subject(self,name):
        if name not in self.subjects:
            self.subjects[name] = Subject()
        return self.subjects[name]
    def average_grade(self):
        total, count = 0,0
        for subject in self.subjects.values():
            total += subject.average_grade()
            count += 1
        return total/count

class Gradebook(object):
    def __init__(self):
        self.students = dict()
    def student(self,name):
        if name not in self.students:
            self.students[name] = Student()
        return self.students[name]

if __name__ == '__main__':
    book = Gradebook()
    jim   = book.student('Jim')
    jane  = book.student('Jane')
    tom   = book.student('Tom')
    jerry = book.student('Jerry')
    math = jim.subject('Math')
    math.report_grade(90,0.4)
    math.report_grade(80,0.6)
    eng = jim.subject('English')
    eng.report_grade(80,0.4)
    eng.report_grade(70,0.6)
    chem = jim.subject('Chemistry')
    chem.report_grade(70,0.4)
    chem.report_grade(90,0.6)
    phy = jim.subject('Physics')
    phy.report_grade(50,0.4)
    phy.report_grade(40,0.6)
    # ...
#   print book.__dict__
#   print jim.__dict__
#   print math.__dict__
     
    for name,subject in jim.subjects.items():
        scores = list()
        for grade in subject.grades:
#           print grade
            scores.append(grade.score)
#       grades = subject.grades[0].score,subject.grades[1].score
        print name
#       print subject
        print scores
#       print subject.grades
#       print jim.subjects[subject]
#       print jim.subjects[subject].__dict__
#       print subject
#       print subject.average_grade()

#   print math.average_grade()
#   print eng.average_grade()
#   print chem.average_grade()
#   print phy.average_grade()
#   print jim.average_grade()
