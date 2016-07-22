# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:06:24 2016

@author: daukes
"""
#Lists
#Construct a list
list1 = [-1,1,2,3,4]
list1.append(5)
list1.extend([6,7,8,9])
result = list1.pop(0)
list1.insert(0,0)

#accessing a single element
print(list1)
print(list1[0])
print(list1[2:4])
print(list1[:4])
print(list1[4:])
print(list1[::2])
print(list1[-1::-1])
print(type(list1) is list)

#Tuples
tup1 = (0,0)
tup2 = (1,1)
tup3 = tuple(range(5))
#list of tuples
list3 = [tup1,tup2]

#Dicts
dict1 = {}
dict1['key1']=123.45
dict1['coordinate 1'] = tup1
dict1['coordinate 2'] = tup2
dict1['all_coordinates'] = list3

#for loops
for key,value in dict1.items():
    print('the value of {0}, is {1}.'.format(key,value))


list2 = list(range(3))

#very basic indexing
for ii in range(len(list2)):
    print(list1[ii])

#more 'pythonic' indexing:
for item in list2:
    print(item)

#using list comprehensions
[print(item) for item in list2]

#string formatting
float1 = 11.37
print('the value of the first element is {0:07.1f}, as an int: {1:7d}'.format(float1,int(float1)))



#understanding types
print(isinstance(list1,list))
