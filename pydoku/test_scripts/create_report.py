from pydoku.SATSolver import SATSolver
from pydoku.FileHandler import FileHandler
from pydoku.HeuristicType import HeuristicType

import time
from copy import deepcopy
import math
import csv

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
  sizes = [4, 9]
  heuristic_ids = [ 1, 2, 3 ]

  for size in sizes:

    sudoku_examples = f'pydoku/test_files/{size}x{size}/examples.txt'
    sudoku_rules = f'pydoku/test_files/{size}x{size}/rules.txt'
    sudoku_file = f'pydoku/test_files/{size}x{size}/dimacs.txt'

    rules = FileHandler.parse(sudoku_rules)
    examples = open(sudoku_examples, 'r')

    with open(f'pydoku/test_files/reports/{size}x{size}.csv', 'w', newline = '') as file:
      csv_writer = csv.writer(file)
      csv_writer.writerow([ 'Heuristic', 'Size', 'Satisfied', 'Backtracks', 'Splits', 'Run Time' ])

      for line in examples:
        dimacs = to_dimacs(line)

        # write the dimacs to a file, this will allow us to mimic reading the CNF from files
        write_file = open(sudoku_file, '+w')
        write_file.write(dimacs)
        write_file.close()

        sudoku = FileHandler.parse(sudoku_file)
        cnf = sudoku + rules

        for heuristic_id in heuristic_ids:
          start_time = time.time()
          heuristic = HeuristicType(heuristic_id)

          solver = SATSolver()
          satisfied, result_assignments, backtracks, splits = solver.solve(deepcopy(cnf), heuristic)

          # check if the returned assignments are valid
          valid = evaluate(cnf, result_assignments)

          if valid:
            print(f'DPLL Output: Satisfied. Backtracks: {backtracks}')
          else:
            print('DPLL Output: Unsatisfied')

          runtime = time.time() - start_time
          print('--- %s seconds ---' % runtime)
          print('--- %s backtracks ---' % backtracks)

          csv_writer.writerow([heuristic, f'{size}x{size}', satisfied, backtracks, splits, runtime])

      file.close()