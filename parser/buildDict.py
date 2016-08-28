#!/usr/bin/env python3
#coding: utf-8

import re

def BuildDict(string) :
  string = string[2:]
  string = string[:len(string)-2]
  print(string)
  templateNumber = re.compile(r'\d+')
  templateNamed  = re.compile(r'/[A-Za-z0-9]+')
  templateReference = re.compile(r'\d+ \d+ R')
  def searchArray(string) :
    if string[0] != '[' : return None
    else :
      count = 0
      result = ''
      for symbol in string :
        if symbol == '[' : count += 1
        if symbol == ']' : count -= 1
        result += symbol
        if count == 0 : return result, len(result)
  templateArray = searchArray

  def search(substring) :
    nonlocal templateNamed, templateNumber, templateReference, templateArray

    if templateArray(substring) :
      result = templateArray(substring)
      return result
    elif templateReference.search(substring) :
      result = templateReference(substring)
      return result.group(), result.endpos
    elif templateNamed.search(substring) :
      result = templateNamed.search(substring)
      return result.group(), result.endpos
    elif templateNumber.search(substring) :
      result = templateNumber.search(substring)
      return result.group(), result.endpos
    else :
      return 'None', len(substring)

  pointer = 0
  finish = len(string)
  while True :
    



if __name__ == '__main__' :
  string = open('trailer.txt', 'r').read()
  BuildDict(string)