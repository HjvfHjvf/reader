#!/usr/bin/env python3
#coding: utf-8

import re

class Parser() :

  """
    1. read first string
    2. read trailer
    3. build trailer dict
    4. build Xref table
    5. build document tree
  """

  def __init__(self, name) :
    self.name    = "%s.pdf" % name
    self.file    = open(self.name, 'rb')
    self.version = None
    self.trailer = None


  def setVersion(self) :
    template = re.compile(r'PDF-\d.\d')
    self.version = ((self.file).readline()).decode('utf-8')
    res = template.search(self.version)
    self.version = res.group()


  def __buildTrailer(self) :
    """
      1. read last 200 bytes
      2. extract the dict
      3. extract the offset of start xref table
      4. return the tuple(dict, offset)
    """
    self.file.seek(-200, 2)
    string = ((self.file).read()).decode('utf-8')

    template = re.compile(r'<<.*>>', re.DOTALL)
    template = template.search(string)
    diction  = template.group()

    template = re.compile(r'startxref.*EOF', re.DOTALL)
    template = template.search(string)
    string   = template.group()
    template = re.compile(r'\d+')
    template = template.search(string)
    string   = eval(template.group())

    return diction, string


  def __buildDict(self, string) :
    templateNamed     = re.compile(r'/[A-Za-z0-9]+')
    templateNumber    = re.compile(r'\d+')
    templateReference = re.compile(r'\d+ \d R')
    def searchArray(line) :
      if line[0] != '[' :
        return None
      else :
        count = 0
        result = ''
        for symbol in line :
          if symbol == '[' : count += 1
          if symbol == ']' : count -= 1
          result += symbol
          if count == 0 : return result, len(line)
    templateArray = searchArray

    def search(substring) :
      print(substring)
      nonlocal templateNumber, templateNamed,\
               templateReference, templateArray
      if templateArray(substring) :
        print("searching array")
        result = templateArray(substring)
        return result
      elif templateReference.match(substring) :
        print('searching reference')
        result = templateReference.match(substring)
        return result.group(), result.endpos
      elif templateNamed.match(substring) :
        print('searching named')
        result = templateNamed.match(substring)
        return result.group(), result.endpos
      elif templateNumber.match(substring) :
        print('searching number')
        result = templateNumber.match(substring)
        return result.group(), result.endpos
      else :
        print('no matches')
        return 'None', 0

    def checkNext(symbol) :
      if symbol == ' ' or symbol == '\n' :
        return True
      else : return False

    pointer = 2
    end   = 0
    finish = len(string)
    diction = dict()
    while True :
      # 1. read key
      # 2. read whitespace
      # 3. read value
      # 4. update dict
      key = search(string[pointer:])
      pointer = key[1]
      key = key[0]

      if checkNext(string[pointer+1]) :
        pointer += 1

      value = search(string[pointer:])
      pointer = value[1]
      value = value[0]

      if checkNext(string[pointer+1]) :
        pointer += 1

      diction.update({key: value})

      if string[pointer] == '>' :
        break

    return diction


  def setTrailer(self) :
    self.trailer = self.__buildTrailer()
