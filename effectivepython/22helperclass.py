# item 22: Prefer Helper Classes Over Bookkeeping with Dicts and Tuples

class SimpleGradebook(object):
    def __init__(self):
        self.grades = dict()
    def add_student(self,name):
        self.grades[name] = list()
    def report_grade(self,name,score):
        self.grades[name].append(score)
    def average_grade(self,name):
        grades = self.grades[name]
        return sum(grades)/len(grades)
class BySubjectGradebook(object):
    def __init__(self):
        self.grades = dict()
    def add_student(self,name):
        self.grades[name] = dict()
    def report_grade(self,name, subject, grade):
        bysubject = self.grades[name]
        grade_list = bysubject.setdefault(subject,[])
        grade_list.append(grade)
    def average_grade(self,name):
        bysubject = self.grades[name]
        total, count = 0, 0
        for grades in bysubject.values():
            total += sum(grades)
            count += len(grades)
        return total/count

def test_simplebook():
    book = SimpleGradebook()
    book.add_student('Jim')
    book.report_grade('Jim',90)
    print book.average_grade('Jim')

def test_bysubjectbook():
    book = BySubjectGradebook()
    book.add_student('Jane')
    book.report_grade('Jane','Math',75)
    book.report_grade('Jane','Math',65)
    book.report_grade('Jane','Gym',90)
    book.report_grade('Jane','Gym',95)
    print book.grades['Jane']
    print book.average_grade('Jane')

if __name__ == '__main__':
#   test_simplebook()
    test_bysubjectbook()
