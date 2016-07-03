''' chapter 15 Classes and Objects '''
#----------  15.1 User-defined types -------------
class Point: #(object):
    ''' Represents a point in 2D space '''
print Point   # <class '__main__.Point'>
blank = Point()
print blank   # <__main__.Point instance at 0xb7e... >
#---------- 15.2 Attributes -----------------------
blank.x = 3.0
blank.y = 4.0
print blank.__dict__
#---------- 15.3 Rectangles -----------------------
class Rectangle(object):
    ''' Represents a rectangle
    attributes: width, height,corner
    '''
box = Rectangle()
box.width = 100.0
box.height = 200.0
box.corner = Point()
box.corner.x = 0.0
box.corner.y = 0.0
def print_point(p):
    print '(%g,%g)' %(p.x,p.y)
print box.__dict__
#---------- 15.3 Rectangles -----------------------
def find_center(rect):
    p = Point()
    p.x = rect.corner.x + rect.width/2.0
    p.y = rect.corner.y + rect.height/2.0
    return p
center = find_center(box)
print_point(center)
#---------- 15.5 Objects are mutable  --------------
def grow_rectangle(rect,dwidth,dheight):
    ''' Inside this function, rect is alias for Rectangle object'''
    rect.width += dwidth
    rect.height += dheight
print box.width, box.height
grow_rectangle(box,50,100)
print box.width, box.height
#---------- 15.6 Copying ----------------------------
# Aliasing can make a program difficult to read because
# changes in one place might have unexpected effects in
# another place
p1 = Point()
p1.x = 3.0
p1.y = 4.0
import copy
p2 = copy.copy(p1)
print p1 is p2      # False
print p1 == p2      # False
# If use copy.copy to duplicate a Rectangle, it copies the Rectangle object
# but not the embedded Point
box2 = copy.copy(box)
print box2 is box                 # False
print box2.corner is box.corner   # True
#--------- copy.deepcopy ------------------------------------
box3 = copy.deepcopy(box)
print box3.corner is box.corner   # False


