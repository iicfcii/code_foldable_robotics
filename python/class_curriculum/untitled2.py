# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:38:41 2016

@author: daukes
"""

def function1(variable1,variable2):
    return variable1+variable2
    

result = function1(1,5)
print(result)

list1 = [0,1,2,3,4]
list2 = [5,6,7,8,9]

result = function1(list1,list2)
print(result)

# functions are type agnostic
# can use a function in multiple ways

class Contact(object):
    def __init__(self,first_name,last_name):
        self.first_name = first_name
        self.last_name = last_name
    def __str__(self):
        return 'Contact({0},{1})'.format(self.last_name,self.first_name)
    def __repr__(self):
        return str(self)
    def formatted_name(self):
        return '{0} {1}'.format(self.first_name,self.last_name)
    def __lt__(self,other):
        return self.last_name.lower()<other.last_name.lower() or self.first_name.lower()<other.first_name.lower()
        
class AddressBook(object):
    def __init__(self,*contacts):
        self.contacts = list(contacts)
    def print_all(self):
        for item in self.contacts:
            print(item.formatted_name())


contact1 = Contact('Ben','Aukes')
contact2 = Contact('Rob','Wood')
contact3 = Contact('Yun','Chen')
contact4 = Contact('claire','Aukes')

address_book = AddressBook(contact1,contact2,contact3,contact4)
print(contact1)
address_book.print_all()
address_book.contacts.sort()
address_book.print_all()
