author = 'Weston Anderson'
assignment = 'CS480 Lab 3'

import math
import re
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Equation import Expression

#regular expression searches
perentheses = ''
addition = ''
subraction = ''
multiplcation = ''



sub_equations = {}


def get_info():
    """Determine the number of perentheses, and operations in a calculation and sort them into"""
    #while regex != null keep getting perentheses

def is_operand(character):
    """
    Simply tries to cast character as integer
    throws exception and returns false if not
    :param character:
    :return:
    """
    try:
        int(character)
        return True
    except ValueError:
        return False

def is_operator(character):
    """
    Simle function to determine if character
    is an operator or not.

    :param character: single character from equation
    :return: True if operand False if not
    """
    operators = ['+','-','*','/','^']

    if character in operators:
        return True
    else:
        return False

def has_precedence(character_operator, stack_operator):
    """
    Function analyzes both character operands
    returns False if stack has precedence,
    True if character has precedence

    :param character_operator: current operator from equation
    :param stack_operator: previous stack operand
    :return:
    """
    order = {'^':1, '*':2, '/':3, '+':4, '-':5}

    character_order = order[character_operator]
    stack_order = order[stack_operator]

    if character_order > stack_order:
        return False
    else:
        return True

def evaluate_equation(x, y, operator):
    """
    given two operand and an operator perform the indicated
    operation on x and y. Then return the result.

    :param x: first value from stack
    :param y: second value from the stack
    :param operator: operation to perform on x and y
    :return: the result of the operation on x and y
    """
    x = float(x)
    y = float(y)

    if operator == '+':
        return x + y
    elif operator == '-':
        return y - x
    elif operator == '*':
        return x * y
    elif operator == '/':
        return y / x
    elif operator == '^':
        return y**x

def validate_input():
    """
    Check contents of txtbx.txt for invalid input
    :return: return true if valid
    """
    test_string = str(txtbx.text())

    perenths = {'(':0, ')':0}
    if test_string == '':
        return False
    #check for invalid characters
    for character in test_string:
        if is_operator(character) != True and is_operand(character) != True and character != '(' and character != ')':
            return False
        if character == '(':
            perenths['('] += 1
        if character == ')':
            perenths[')'] += 1

    if perenths['('] != perenths[')']:
        return False

    if not re.search('(\d)', test_string):
        return False
    #really ugly regex checks if any calculations are actually made
    if not re.search('(\+)', test_string) and not re.search('(\-)', test_string)\
        and not re.search('(\/)', test_string) and not re.search('(\*)', test_string)\
        and not re.search('(\^)', test_string) and not re.search('(\+$)', test_string)\
            and not re.search('(\-$), test_string') and not re.search('(\/$)', test_string)\
            and not re.search('(\*$)', test_string) and not re.search('(\^$)', test_string):
        return False

    return True

@pyqtSlot()
def on_click():
    """
    Click listener for calculate button
    once clicked interpret problem then solve
    displays result in display_lbl
    """
    #check if string invalid
    if validate_input() == True:

        equation = str(txtbx.text()) #get equation
        #regex strings
        multi_digit = '(\d\d+)' #check for multiple digits next to each other
        per_mul = '(\)\^)' #check if perentheses are next to each other
        per_exp = '(\)\^)' #check for perentheses exponents
        left_num_per = '(\d\()' #check if number is multiplying perentheses
        right_num_per = '(\)\d)' #check if number is multiplying perentheses

        #regex to search equation for special cases
        if re.search(multi_digit, equation) or re.search(per_mul, equation)\
                or re.search(per_exp, equation) or re.search(left_num_per, equation)\
                or re.search(right_num_per, equation) or re.search('(^\+)', equation)\
                or re.search('(^\-)', equation) or re.search('(^\/)', equation)\
                or re.search('(^\*)', equation) or re.search('(^\^)', equation):
            expression = Expression(equation)
            if str(expression) == 'None':
                display_lbl.setText('Invalid equation syntax')
            else:
                display_lbl.setText(str(expression()))
        else:
            #convert equation to postfix and begin parsing
            operand_stack = []
            postfix = ''
            error = ''

            #convert infix to postfix
            for character in equation:
                if is_operand(character) == True: #if character is a number
                    postfix += character
                if character == '(':
                    operand_stack.append(character)
                if character == ')':
                    while operand_stack != [] and operand_stack[-1] != '(':
                        postfix += operand_stack.pop()
                    if operand_stack[-1] == '(':
                        operand_stack.pop()
                if is_operator(character):       #if character is a math operator
                    if operand_stack == [] or operand_stack[-1] == '(':
                        operand_stack.append(character)
                    else:
                        while operand_stack != [] and operand_stack[-1] != '(' and has_precedence(character, operand_stack[-1]):
                            postfix += operand_stack.pop()
                        operand_stack.append(character)

            print postfix

            while operand_stack != []:
                postfix += operand_stack.pop()

            print
            print postfix

            #using operand_stack evaluate the expression
            for item in postfix:
                if is_operand(item) == True:
                    operand_stack.append(item)
                if is_operator(item) == True:
                    x = operand_stack.pop()
                    y = operand_stack.pop()
                    result = evaluate_equation(x, y, item)
                    operand_stack.append(result)
            # print('The answer is: ', result)

            display_lbl.setText(str(result))
    else:
        display_lbl.setText('Invalid equation syntax')

if __name__ == '__main__':
    #initialize UI
    window = QApplication(sys.argv)
    widget = QWidget()

    #set widget size
    # widget.resize(320, 240)
    widget.resize(540, 380)
    widget.setWindowTitle("Calculator")

    #create input label
    inputlbl = QLabel(widget)
    inputlbl.move(10, 10)
    inputlbl.setText('Enter Calculation...')

    #create display label font
    display_font = QFont()
    display_font.setFamily('Arial')
    display_font.setFixedPitch(True)
    display_font.setPointSize(20)

    #create display label
    display_lbl = QLabel(widget)
    display_lbl.move(175, 100) # x, y
    display_lbl.resize(200, 80)
    display_lbl.setText('')
    display_lbl.setFont(display_font)
    display_lbl.setAlignment(Qt.AlignCenter)


    #create calculation text box
    txtbx = QLineEdit(widget)
    txtbx.move(100, 250)
    txtbx.resize(350, 30)

    #add button
    calculate_button = QPushButton('Calculate', widget)
    calculate_button.setToolTip('Click to perform the indicated operation.')
    calculate_button.clicked.connect(on_click)
    calculate_button.resize(calculate_button.sizeHint())
    calculate_button.move(225, 300)

    widget.show()

    sys.exit(window.exec_())