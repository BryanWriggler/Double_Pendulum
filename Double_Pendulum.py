'''
author: Bryan Hsieh
Project: double pendulum simulation

    Required constant:
        gravitational constant g: (9.8 m/s^2)
        change in time dt: 0.01 s

    constants need as input: (in meters, and kilograms)
        length 1 l_1
        length 2 l_2
        mass 1 m_1
        mass 2 m_2

    variables needing the initial condition: (in radians)
        angle 1 t_1
        angle 2 t_2
        angular velocity 1 w_1
        angular velocity 2 w_2

    variables needing calculation:
        angular acceleration 1 a_1
        angular acceleration 2 a_2
'''

'''
    0. using Euler-Lagrange Method, we can reduce the a_1 and a_2 into 2 equations based on other constants or known variables, 
        use the inverse matrix formula can solve for these 2 unknown variables, and get essential information for the next
        instant.

    1. after finding the acceleration, find the t_1, t_2, w_1, w_2 for the next instant, where:
        t_1 = t_1 + w_1 * dt
        t_2 = t_2 + w_2 * dt
        w_1 = w_1 + a_1 * dt
        w_2 = w_2 + a_2 * dt
'''


#imports
import numpy
import math
import turtle
import time

#the class to define the motion at every instant
class Double_Pendulum:
    #constants
    g = 9.8
    dt = 0.01

    def __init__(self, l1, l2, m1, m2, t1, t2, w1, w2):
        #length of the pendulum arm
        self.l_1 = l1
        self.l_2 = l2

        #mass of the pendulum
        self.m_1 = m1
        self.m_2 = m2

        #angle of the pendulum
        self.t_1 = t1
        self.t_2 = t2

        #angular velocity of the pendulum
        self.w_1 = w1
        self.w_2 = w2

        #angular acceleration
        self.a_1 = 0.0
        self.a_2 = 0.0

        #time
        self.time = 0.0

    #return the solution of vector [a_1, a_2] at the specific instant (succeed)
    def update_acceleration(self):
        #define the elements in the matrix: [[a, b], [c, d]]
        a = (self.m_1 + self.m_2) * ((self.l_1)**2)
        b = self.m_2 * self.l_1 * self.l_2 * math.cos(self.t_1 - self.t_2)
        c = b
        d = self.m_2 * ((self.l_2)**2)

        vector_augmented = [0 -((self.m_1 + self.m_2) * Double_Pendulum.g * math.sin(self.t_1) * self.l_1) - (self.m_2 * self.l_1 * self.l_2 * ((self.w_2)**2) * math.sin(self.t_1 - self.t_2)),
                            self.m_2 * self.l_1 * self.l_2 * (self.w_1**2) * math.sin(self.t_1 - self.t_2) - self.m_2 * Double_Pendulum.g * math.sin(self.t_2) * self.l_2]
        
        inverse_matrix = numpy.array([[d, -b], [-c, a]]) / (a*d - b*c)

        #multiply the inverse matrix with the augmented vector, and get the vector solution [a1, a2]
        solution_vector = numpy.dot(inverse_matrix, vector_augmented)

        self.a_1 = solution_vector[0]
        self.a_2 = solution_vector[1]
    
    #update rest of the information based on the known acceleration
    def update_information_Eulers_Method(self):
        self.t_1 = self.t_1 + self.w_1 * Double_Pendulum.dt
        self.t_2 = self.t_2 + self.w_2 * Double_Pendulum.dt
        self.w_1 = self.w_1 + self.a_1 * Double_Pendulum.dt
        self.w_2 = self.w_2 + self.a_2 * Double_Pendulum.dt


#ask for user input in l1, l2, m1, m2, t1, t2, w1, w2
l1 = float(input("length 1 (m)"))
l2 = float(input("length 2 (m)"))
m1 = float(input("mass 1 (kg)"))
m2 = float(input("mass 2 (kg)"))

#conversion to radians, as input is in degrees
t1 = float(input("angle 1 (degree)")) * math.pi/180
t2 = float(input("angle 2 (degree)")) * math.pi/180
w1 = float(input("angular velocity 1 (degree / sec)")) * math.pi/180
w2 = float(input("angular velocity 2 (degree / sec)")) * math.pi/180


#creating the object
pend1 = Double_Pendulum(l1, l2, m1, m2, t1, t2, w1, w2)


#make the animation of the simulation
screen = turtle.Screen()
screen.setup(600, 600)
screen.tracer(0)

don = turtle.Turtle()
don.speed(0)
don.width(3)
don.hideturtle()

for x in range(1000):
    don.clear()

    # Get the position of the pendulums
    x1 = pend1.l_1 * math.sin(pend1.t_1) * 100
    x2 = x1 + pend1.l_2 * math.sin(pend1.t_2) * 100
    y1 = -pend1.l_1 * math.cos(pend1.t_1) * 100
    y2 = y1 - pend1.l_2 * math.cos(pend1.t_2) * 100

    # Set to the initial point - the pivot
    don.goto(0, 0)
    don.dot()

    # Turn to the direction of the first point
    angle = math.atan(y1/ x1) * 180 / math.pi
    if(x1 < 0):
        angle += 180
    elif (x1 > 0 and y2 <0):
        angle += 360

    # Go to the position of pendulum 1 and draw
    don.setheading(angle)
    don.pendown()
    don.forward(pend1.l_1 * 100)
    don.penup()

    #draw the first mass
    don.setheading(0)
    don.back(10)
    don.right(90)
    don.pendown()
    don.fillcolor("red")
    don.begin_fill()
    don.circle(10)
    don.end_fill()
    don.penup()
    don.left(90)
    don.forward(10)


    # Turn to the direction of the second point
    don.setheading(0)
    angle2 = math.atan((y2 - y1)/ (x2 - x1)) * 180 / math.pi
    if(x2 - x1 < 0):
        angle2 += 180
    elif (x2 - x1 > 0 and y2 - y1 <0):
        angle2 += 360


    # Go to the position of pendulum 2 and draw
    don.setheading(angle2)
    don.pendown()
    don.forward(pend1.l_2 * 100)
    don.penup()

    #draw the second mass
    don.setheading(0)
    don.back(10)
    don.right(90)
    don.pendown()
    don.fillcolor("blue")
    don.begin_fill()
    don.circle(10)
    don.end_fill()
    don.penup()

    # Update the position
    pend1.update_acceleration()
    pend1.update_information_Eulers_Method()

    # Update the screen
    screen.update()
    time.sleep(0.01) #??????

    