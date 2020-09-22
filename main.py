from pydoku.SATSolver import SATSolver
from pydoku.FileReader import FileReader
from pydoku.HeuristicType import HeuristicType
from pydoku.Utilities import Utilities

import time
from copy import deepcopy

if __name__ == '__main__':
  heuristic_id = 3
  heuristic = HeuristicType(heuristic_id)

  sudoku_examples = f'pydoku/test_files/sudoku-examples.txt'
  sudoku_rules = f'pydoku/test_files/sudoku-rules.txt'
  sudoku_file = f'pydoku/test_files/sudoku-dimacs.txt'
  rules = FileReader.parse(sudoku_rules)

  examples = open(sudoku_examples, 'r')

  for line in examples:
    dimacs = Utilities.to_dimacs(line)

    # write the dimacs to a file, this will allow us to mimic reading the CNF from files
    write_file = open(sudoku_file, '+w')
    write_file.write(dimacs)
    write_file.close()

    sudoku = FileReader.parse(sudoku_file)
    cnf = sudoku + rules

    start_time = time.time()

    solver = SATSolver()
    satisfied, result_assignments = solver.solve(deepcopy(cnf), heuristic)

    # check if the returned assignments are valid
    valid = Utilities.evaluate(cnf, result_assignments)

    if valid:
      print('DPLL Output: Satisfied')
    else:
      print('DPLL Output: Unsatisfied')

    print('--- %s seconds ---' % (time.time() - start_time))
