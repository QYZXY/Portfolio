# SI 206 HW4
# Your name: Qingyuan Yang
# Your student id: 40417928
# Your email: yangqy@umich.edu
# Who you worked with on this homework:

from random import randint
import unittest

class Student:
    ''' respresents a student who can order food at a dining hall '''

    def __init__(self, name, blue_bucks = 0.0):
        ''' initializes the name, blue_bucks, and location '''
        self.name = name             # the student's name
        self.blue_bucks = blue_bucks # amount of money in blue_bucks
        self.location = None         # either dining hall object or None

    def __str__(self):
        ''' returns the name'''
        return self.name

    def buy_blue_bucks(self, amount):
        ''' adds the passed amount to the blue_bucks '''
        self.blue_bucks += amount

    def enter_dining_hall(self, dining_hall):
        ''' Finish the enter_dining_hall method
            1) First check if the student's location is not None and if it is
               not then print "Already in a dining hall" and return False.
            2) Otherwise call can_enter on the dining_hall.  If the result is
               False print "Too full - try later" and return False. Otherwise
               change the student's location to the dining hall and add them to
               the student_list for the dining hall, and then return True.
        '''
        if self.location != None:
            print ("Already in a dining hall")
            return False
        else:
            if dining_hall.can_enter(self) == False:
                print("Too full - try later")
                return False
            else:
                self.location = dining_hall
                dining_hall.student_list.append(self)
                return True

    def leave_dining_hall(self):
        ''' finish the leave_dining_hall method
            1) If the student's location is None print "Not in a dining hall"
               and return False
            2) Otherwise remove the student from the dining hall's student_list
               and set the student's location to None and return True
        '''
        if self.location == None:
            print("Not in a dining hall")
            return False
        else:
            self.location.student_list.remove(self)
            self.location = None
            return True

    def order_food(self, food_list):
        ''' 1) Calculate the total cost of the order by totaling the price for each
               food object in the food_list.
            2) Check if the student has the total cost or more in their blue_bucks.
               If they do not have enough money then print "Insufficient funds"
               and return False.
            3) If they have enough money, check if their location is None.
               If it is None print "You must be in dining hall to order food", and 
               return False.
            4) Call fill_order(food_list) on the dining hall object. If fill_order 
               returns True remove the total cost from blue_bucks and return True.
               Otherwise, return False.
        '''
        price = 0
        for i in food_list:
            price += i.price
        if self.blue_bucks < price:
            print("Insufficient funds")
            return False
        else:
            if self.location == None:
                print("You must be in dining hall to order food")
                return False
            elif self.location.fill_order(food_list) == True:
                self.blue_bucks -= price
                return True
            else:
                return False

# The Food class
class Food:

    def __init__(self, name, price):
        ''' initializes the name and price '''
        self.name = name
        self.price = price

    def __str__(self):
        ''' returns the name and price '''
        return self.name + " " + str(self.price)


class Dining_Hall:
    ''' Represents a dining hall '''

    def __init__(self, name, capacity):
        ''' initializes the name and capacity to the passed values.
            Sets the student_list to an empty list and inventory to an
            empty dictionary.
        '''
        self.name = name
        self.capacity = capacity
        self.student_list = []
        self.inventory = {}

    def __str__(self):
        ''' returns a string with the name and the number of students in the
            student_list
        '''
        return self.name + " with " + str(len(self.student_list)) + " students"

    def inside(self, student):
        ''' Returns True if the passed student is in the student_list and
            False otherwise '''
        return student in self.student_list

    def can_enter(self, student):
        ''' Returns True if the dining hall has not reached capacity and False
            otherwise.
        '''
        return len(self.student_list) < self.capacity

    def add_inventory(self, food, quantity):
        ''' If the food is already in the inventory then add the passed quantity
            to the existing value.  Otherwise set the value for the food
            in the inventory dictionary.
        '''
        if food not in self.inventory:
            self.inventory.update({food : quantity})
        else: 
            self.inventory.update({food : quantity + self.inventory[food]})


    def fill_order(self, food_list):
        ''' Checks that there is enough food for an order and if not returns False,
            otherwise it subtracts the food item from the quantity in the inventory
            and returns True.
        '''

        for food in food_list:
            quantity = food_list.count(food)
            if food not in self.inventory or self.inventory[food] < quantity: #or (food not in self.inventory):(self.inventory[food] < quantity): 
                return False
            else:
                self.inventory[food] = self.inventory[food] - quantity
                return True
    def lottery(self):
        if self.student_list != []:
            index = randint(0,len(self.student_list))
            self.student_list[index].buy_blue_bucks(10)



class TestAllMethods(unittest.TestCase):
    ''' Here are all the test cases:
        Please do not edit test cases outside of the one below.
        As you are working on one test case, 
            feel free to comment out the test cases that you are not working on, 
            but be sure to uncomment all test cases before you turn in your homework.

        Task: You are supposed to only modify test_dining_hall_entrance_and_exit_corner_cases.
        For extra credit: You are supposed to creat a new test case called test_lottery
    '''

    def setUp(self):
        self.orange_chicken = Food('Orange Chicken',10.00)
        self.sandwich = Food('sandwich', 7.50)
        self.cookie = Food('cookie', 2.50)
        self.pizza = Food('pizza', 5.00)

    # Check the constructors
    def test_student_constructor(self):
        bob = Student(name='Bob',blue_bucks=18)
        self.assertEqual(bob.name, 'Bob')
        self.assertEqual(bob.blue_bucks, 18)

    def test_food_constructor(self):
        self.assertEqual(self.cookie.name, 'cookie')
        self.assertAlmostEqual(self.cookie.price, 2.50,1)
        self.assertEqual(self.pizza.name, 'pizza')
        self.assertAlmostEqual(self.pizza.price, 5.00, 0)

    def test_dining_hall_constructor(self):
        north_quad = Dining_Hall(name='North Quad', capacity=3)
        south_quad = Dining_Hall(name='South Quad', capacity=5)
        self.assertEqual(north_quad.name,'North Quad')
        self.assertEqual(north_quad.capacity,3)
        self.assertEqual(south_quad.name,'South Quad')
        self.assertEqual(south_quad.capacity,5)

   # Check the buy_blue_bucks method for student
    def test_student_buy_blue_bucks(self):
        s1 = Student(name='S1',blue_bucks=11.50)
        s1.buy_blue_bucks(10)
        self.assertAlmostEqual(s1.blue_bucks, 21.50, 1)

    # Check the order_food method for student
    def test_student_order_food_1(self):
        s2 = Student(name='S2',blue_bucks=20)
        north_quad = Dining_Hall(name='North Quad', capacity=3)
        north_quad.add_inventory(self.pizza,5)
        north_quad.add_inventory(self.cookie,2)
        s2.enter_dining_hall(north_quad)

        self.assertEqual(s2.order_food([self.pizza]),True)
        self.assertAlmostEqual(s2.blue_bucks,15,1)

        s2.order_food([self.pizza, self.cookie])
        s2.order_food([self.pizza])

        self.assertAlmostEqual(s2.blue_bucks, 2.5)

        # try to buy food that isn't in the dining hall
        self.assertEqual(s2.order_food([self.orange_chicken]),False)
        self.assertAlmostEqual(s2.blue_bucks, 2.5)


    # Check the method for student entering and exiting dining hall
    def test_dining_hall_entrance_exit(self):

        alice = Student(name='Alice',blue_bucks=50)
        north_quad = Dining_Hall(name='North Quad', capacity=3)

        self.assertEqual(alice.enter_dining_hall(north_quad),True)
        self.assertEqual(alice.location,north_quad)

        self.assertEqual(north_quad.inside(alice),True)

        self.assertEqual(alice.leave_dining_hall(),True)
        self.assertEqual(alice.location,None)
        self.assertEqual(north_quad.inside(alice),False)


    # Check all methods related to entering and exiting a dining hall
    # Check for capacity and corner cases
    def test_dining_hall_entrance_and_exit_corner_cases(self):
        #test_dining_hall_entrace_and_exit_corner_cases has three test cases. 
        #   The first one has the correct expected values, but the other two do not.  
         #   Fix the tests to use the correct values

        south_quad = Dining_Hall(name='South Quad', capacity=5)

        alice = Student(name='Alice',blue_bucks=50)
        north_quad = Dining_Hall(name='North Quad', capacity=3)

        stu_list = [Student(name='S'+str(i),blue_bucks=20) for i in range(5)]

        result_list = []

        # Case 1: exceed the capacity
        for i in stu_list:
            result_list.append(i.enter_dining_hall(north_quad))

        self.assertEqual(result_list,[True,True,True,False,False])

        result_list = []
        for i in stu_list:
            result_list.append(i.leave_dining_hall())

        self.assertEqual(result_list,[True,True,True,False,False])

        # Case 2: attempt to enter while already in one dining hall
        res1 = alice.enter_dining_hall(north_quad)
        res2 = alice.enter_dining_hall(south_quad)

        self.assertEqual(res2,False)
        self.assertEqual(alice.location,north_quad)
        self.assertEqual(south_quad.inside(alice),False)

        out1 = alice.leave_dining_hall()

        # Case 3: attempt to leave while not in any dining hall
        out2 = alice.leave_dining_hall()

        self.assertEqual(out2,False)
        self.assertEqual(alice.location,None)
        self.assertEqual(north_quad.inside(alice),False)

    '''Check the methods related to inventory'''
    def test_add_inventory(self):

        south_quad = Dining_Hall(name='South Quad', capacity=5)
        north_quad = Dining_Hall(name='North Quad', capacity=3)

        north_quad.add_inventory(self.orange_chicken,2)
        north_quad.add_inventory(self.pizza, 5)
        north_quad.add_inventory(self.orange_chicken, 1)
        south_quad.add_inventory(self.cookie,2)

        self.assertEqual(north_quad.inventory[self.orange_chicken],3)
        self.assertEqual(north_quad.inventory[self.pizza],5)
        self.assertEqual(south_quad.inventory[self.cookie],2)

    def test_order_food(self):

        alice = Student(name='Alice',blue_bucks=50)
        north_quad = Dining_Hall(name='North Quad', capacity=3)

        north_quad.add_inventory(self.orange_chicken,2)

        alice.buy_blue_bucks(20)
        alice.enter_dining_hall(north_quad)

        self.assertEqual(alice.order_food([self.orange_chicken]), True)
        self.assertEqual(north_quad.inventory[self.orange_chicken],1)

        alice.leave_dining_hall()

    def test_order_food_corner_cases(self):

        alice = Student(name='Alice',blue_bucks=50)

        south_quad = Dining_Hall(name='Sorth Quad', capacity=5)
        north_quad = Dining_Hall(name='North Quad', capacity=3)

        north_quad.add_inventory(self.orange_chicken,2)
        south_quad.add_inventory(self.cookie,2)

        alice.buy_blue_bucks(20)
        alice.enter_dining_hall(north_quad)

        # Case 1: Out of stock
        res = alice.order_food([self.orange_chicken])
        self.assertEqual(res, True)
        self.assertEqual(north_quad.inventory[self.orange_chicken],1)

        res = alice.order_food([self.orange_chicken])
        self.assertEqual(res, True)
        self.assertEqual(north_quad.inventory[self.orange_chicken],0)

        res = alice.order_food([self.orange_chicken])
        self.assertEqual(res, False)
        self.assertEqual(north_quad.inventory[self.orange_chicken],0)

        # Case 2: Restock
        north_quad.add_inventory(self.orange_chicken,1)

        res = alice.order_food([self.orange_chicken])
        self.assertEqual(res, True)
        self.assertEqual(north_quad.inventory[self.orange_chicken],0)

        # Case 3: Try to order unexisting food
        res = alice.order_food([self.cookie])
        self.assertEqual(res, False)

        alice.leave_dining_hall() 

    def test_lottery(self):
        stu_list = [Student(name='S'+str(i),blue_bucks=20) for i in range(5)]
        south_quad = Dining_Hall(name='Sorth Quad', capacity=5)
        south_quad.lottery()
        result1_list = []
        result2_list = []
        #no students
        for i in south_quad.student_list:
            result1_list.append(i.blue_bucks)
        self.assertEqual(result1_list, [])

        #when it has students, let them in first
        for i in stu_list:
            i.enter_dining_hall(south_quad)
        
        south_quad.lottery()

        for i in south_quad.student_list:
            result2_list.append(i.blue_bucks)
        
        num_unchanged = 0
        num_changed = 0
        
        for i in result2_list:
            if i == 30:
                num_changed += 1
            elif i == 20:
                num_unchanged += 1
        self.assertEqual(num_changed, 1) 
        self.assertEqual(num_unchanged, 4)
        



def main():
    ''' You are not required to write anything in main()
    '''
    pass

if __name__ == '__main__':
    unittest.main() # Run all the unittest cases
    main()
