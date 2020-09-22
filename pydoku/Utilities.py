"""
The class contains commonly used helper functions
"""
from copy import deepcopy
import math

class Utilities:

  @staticmethod
  def to_dimacs(sudoku):
    sudoku_values = []
    sudoku = sudoku.strip()
    side = int(math.sqrt(len(sudoku)))

    for i, value in enumerate(sudoku):
      if value != ".":
        row = (i // side) + 1
        column = (i % side) + 1
        rcv = f'{row}{column}{value} 0'
        sudoku_values.append(rcv)

    # list to string with \n between each clause
    return "\n".join(sudoku_values)

  @staticmethod
  def evaluate(cnf: list, assignments: dict) -> bool:
    """
    Returns a randomly selected literal from the current CNF

    Parameters
    ----------
    cnf : list
        a list of clauses defining a CNF
    assignments : list
        a list of clauses defining a CNF

    Returns
    -------
    bool
        returns true if the assignments provided satisfy the CNF
    """
    for clause in cnf:
      valid = True
      for literal in clause:
        atom = literal
        if literal[0] == '-':
          atom = literal[1:len(literal)]

        valid = valid or assignments[atom]

        if not valid:
          return False

    return True

  @staticmethod
  def to_dimacs(sudoku):
    """
    Takes in a string defining a sudoku as parameter and encodes it into dimacs

    Parameters
    ----------
    sudoku: string
        a definition of the puzzle in dimacs format

    Returns
    -------
    string
        returns string describing the sudoku puzzle in dimacs format
    """
    sudoku_values = []  # each clause/row in a DIMACS file
    sudoku = sudoku.strip()  # remove white spaces
    size = math.sqrt(len(sudoku))  # nr of rows/columns

    for i, value in enumerate(sudoku):

      # only look at the non-empty values
      if value != ".":

        row = (i // int(size)) + 1  # row nr remains same for each rc values
        column = (i % int(size)) + 1  # col nr is 1 till rc for each rc values

        rcv = f'{row}{column}{value} 0'
        sudoku_values.append(rcv)

    # list to string with \n between each clause
    return '\n'.join(sudoku_values)

