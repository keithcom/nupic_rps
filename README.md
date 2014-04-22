nupic_rps
=======

Match your wits against NuPIC's CLA in the classic 'Rock, Paper, Scissors' game

This is a simple text based python version of the game.  The CLA model uses continuous learning to try and predict your next move.  With this prediction, it selects the move that will beat it.

The game tracks the overall win/lose/draw stats for the session and prints it after each round.

The model currently uses the scalar encoder with values of 1, 5 and 10 for rock, paper, scissors respectively. 

For more information on NuPIC and the CLA, please visit:
http://numenta.org
