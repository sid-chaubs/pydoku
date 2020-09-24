from pydoku.SATSolver import SATSolver
from pydoku.FileHandler import FileHandler
from pydoku.HeuristicType import HeuristicType

import time
from copy import deepcopy
import math

def to_dimacs(sudoku: str) -> str:
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
  sudoku_values = []
  sudoku = sudoku.strip()
  side = int(math.sqrt(len(sudoku)))

  for i, value in enumerate(sudoku):
    if value != '.':
      row = (i // side) + 1
      column = (i % side) + 1
      rcv = f'{row}{column}{value} 0'
      sudoku_values.append(rcv)

  return '\n'.join(sudoku_values)

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

if __name__ == '__main__':
  heuristic_id = 1
  heuristic = HeuristicType(heuristic_id)

  sudoku_examples = 'pydoku/test_files/sudoku-examples.txt'
  sudoku_rules = 'pydoku/test_files/sudoku-rules.txt'
  sudoku_file = 'pydoku/test_files/sudoku-dimacs.txt'

  rules = FileHandler.parse(sudoku_rules)
  examples = open(sudoku_examples, 'r')

  for line in examples:
    dimacs = to_dimacs(line)

    # write the dimacs to a file, this will allow us to mimic reading the CNF from files
    write_file = open(sudoku_file, '+w')
    write_file.write(dimacs)
    write_file.close()

    sudoku = FileHandler.parse(sudoku_file)
    cnf = sudoku + rules

    start_time = time.time()

    solver = SATSolver()
    satisfied, result_assignments, backtracks = solver.solve(deepcopy(cnf), heuristic)

    # check if the returned assignments are valid
    valid = evaluate(cnf, result_assignments)

    if valid:
      print(f'DPLL Output: Satisfied. Backtracks: {backtracks}')
    else:
      print('DPLL Output: Unsatisfied')

    print('--- %s seconds ---' % (time.time() - start_time))
    print('--- %s backtracks ---' % backtracks)