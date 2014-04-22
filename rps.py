#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""A simple client to create a CLA model to play Rock/Paper/Scissors."""

import sys
import random
import logging

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.data.inference_shifter import InferenceShifter

import description


R = 1
P = 5
S = 10

# uncomment for repeatable testing data
#random.seed("NuPIC")

# number of records to train on
TRAINING = 3


#-----------------------------------------------------------------------------
# nupic functions
#-----------------------------------------------------------------------------
def createModel():
  return ModelFactory.create(description.config)


def get_throw(val):
  global R
  global P
  global S

  if val < R+((P-R)/2):
    # Predicting Rock, so throw Paper to beat it
    return P
  elif val < P+((S-P)/2):
    # Predicting Paper, so throw Scissors
    return S
  else:
	# Predicting Scissors, so throw Rock
    return R


def get_print_val(val):
  global R
  global P
  global S
  if val == R:
    return 'R'
  elif val == P:
    return 'P'
  elif val == S:
    return 'S'
  else:
    return '?'


def print_result(text, arrow, choice, choice_cla, win, lose, draw):
  c1 = get_print_val(choice)
  c2 = get_print_val(choice_cla)
  print c1, arrow, c2, " - ", text, " - Record:", win, lose, draw


def runGame():
  global R
  global P
  global S
  global TRAINING
  win = 0
  lose = 0
  draw = 0

  choicelist = [R,P,S]

  model = createModel()
  model.enableInference({'predictionSteps': [1], 'predictedField': 'choice', 'numRecords': 1000})
  inf_shift = InferenceShifter();

  # Train initial values
  for i in range(0, TRAINING):
    for c in choicelist:
      record = {'choice': c}
      result = inf_shift.shift(model.run(record))

  # Train on random choices
  #for i in range(0, TRAINING):
  #  c = random.choice(choicelist)
  #  record = {'choice': c}
  #  result = inf_shift.shift(model.run(record))

  # - Get the initial predicted value
  #inferred = result.inferences['multiStepPredictions'][1]
  #predicted = sorted(inferred.items(), key=lambda x: x[1])[-1][0]
  predicted = 0.0
  total_probability = 0.0
  for key, value in result.inferences['multiStepPredictions'][1].iteritems():
      predicted += float(key) * float(value)
      total_probability += float(value)
  predicted = predicted / total_probability
  choice_cla = get_throw(predicted)

  # - Start playing the game
  print
  print "Play 'Rock, Paper, Scissors' with the CLA."
  print
  print "Enter 1 or 'r' for Rock, 2 or 'p' for Paper, and 3 or 's' for Scissors ('q' to quit):"
  choice = raw_input()
  while choice != 'q':

	# Interpret the user's choice
    if choice == '1' or choice == 'r':
      choice = R
    elif choice == '2' or choice == 'p':
      choice = P
    elif choice == '3' or choice == 's':
      choice = S
    else:
      print "Unknown value, try again."
      choice = raw_input()
      continue

    # Compare the two choices
    if choice == choice_cla:
      draw = draw + 1
      print_result("It's a draw", " == ", choice, choice_cla, win, lose, draw)
    elif choice == R and choice_cla == P:
      lose = lose + 1
      print_result("You lose!  ", " ==>", choice, choice_cla, win, lose, draw)
    elif choice == R and choice_cla == S:
      win = win + 1
      print_result("You win!   ", "<== ", choice, choice_cla, win, lose, draw)
    elif choice == P and choice_cla == S:
      lose = lose + 1
      print_result("You lose!  ", " ==>", choice, choice_cla, win, lose, draw)
    elif choice == P and choice_cla == R:
      win = win + 1
      print_result("You win!   ", "<== ", choice, choice_cla, win, lose, draw)
    elif choice == S and choice_cla == R:
      lose = lose + 1
      print_result("You lose!  ", " ==>", choice, choice_cla, win, lose, draw)
    elif choice == S and choice_cla == P:
      win = win + 1
      print_result("You win!   ", "<== ", choice, choice_cla, win, lose, draw)
    else:
      print_result("ERROR!!!   ", ">--<", choice, choice_cla, win, lose, draw)
      
    # Feed their choice to the model and get the next predicted value
    record = {'choice': choice}
    result = inf_shift.shift(model.run(record))
    #inferred = result.inferences['multiStepPredictions'][1]
    #predicted = sorted(inferred.items(), key=lambda x: x[1])[-1][0]
    predicted = 0.0
    total_probability = 0.0
    for key, value in result.inferences['multiStepPredictions'][1].iteritems():
        predicted += float(key) * float(value)
        total_probability += float(value)
    predicted = predicted / total_probability
    choice_cla = get_throw(predicted)
    choice = raw_input()



if __name__ == "__main__":
  runGame()
  print "Thanks for playing!"

