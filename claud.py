#Python 3.10.8
import mysql.connector
import re
from flask import flash
# create a connection to the database with SSL/TLS encryption


# test input data at all input filds
def sanitize_input(input_string):
    if input_string.find('--'):
        category = "danger"
        flash(["Simbols -- ; and others are not allowed for security reasons use only , . ! @"], category)  
    semicolon_index = input_string.find(';')
    if semicolon_index >= 0:
        input_string = input_string[:semicolon_index]
    sanitized_string = re.sub(r'[^A-Za-z0-9.,!@]', '', input_string)
    return  sanitized_string
  
# data modification function  
def convert_tuple_to_dict(tuples_list):
    result_list = []
    for tuple_item in tuples_list:
        dict_item = {}
        for index in range(len(tuple_item)):
            dict_item[index] = tuple_item[index]
        result_list.append(dict_item)
    return result_list
  

"""Function prototype >> execude(query, (tuple_values))
  to execute query as strings values implement (0),(1),(2)...
  returns list of dic with numeric keys""" 
def execute(query,tuple_values):
    print(query[:6])
    if query[:6] == "SELECT":
      cursor = cnx.cursor()
      cursor.execute(query,tuple_values)
      results = cursor.fetchall()
      cursor.close()
      cnx.close()
      return convert_tuple_to_dict(results)
    elif query[:6] == "INSERT":
      char_count=0
      for string in tuple_values:
      # Loop through each character in the string
        for char in string:
          char_count = char_count +1
      if char_count>2250:
        category = "danger"
        flash(["Too many symbols, please use max 250 for title and max 2000 for text"], category)  
      valu=[]
      for val in tuple_values:
        valu.append(sanitize_input(val))
      values=tuple(valu)
      cursor = cnx.cursor()
      cursor.execute(query, values)
      cnx.commit()
      cursor.close()
      cnx.close()
      return True
      
    elif query[:6] == "UPDATE":
      char_count=0
      for string in tuple_values:
      # Loop through each character in the string
        for char in string:
          char_count= char_count +1
      if char_count>2250:
        category = "danger"
        flash(["Too many symbols, please use max 250 for title and max 2000 for text"], category)  
      valu=[]
      for val in tuple_values:
        valu.append(sanitize_input(val))
      values=tuple(valu)
      cursor = cnx.cursor()
      cursor.execute(query, values)
      cnx.commit()
      cursor.close()
      cnx.close()
      return True
    elif query[:6] == "DELETE":
      cursor = cnx.cursor()
      cursor.execute(query, tuple_values)
      cnx.commit()
      cursor.close()
      cnx.close()
      return True
    else:
      pass
      


