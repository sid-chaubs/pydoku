"""
Usage: SAT --help
       SAT (-S1 | -S2 | -S3) [FILE]

Process the DIMACS file defining a formula in Conjunctive Normal Form (CNF).
Returns True if the formula is satisfiable and a list of satisfiable assignments.

Arguments:
  FILE File defining the CNF in DIMACS format

Options:
  -h --help
  -S1 Relative path for a DIMACS file defining a CNF to be solved using the Davis-Putnam-Logemann-Loveland algorithm
  -S2 Relative path for a DIMACS file defining a CNF to be solved using random literal selection as the branching heuristic.
  -S3 Relative path for a DIMACS file defining a CNF to be solved using Maximum Occurences in Minimal Size as the branching heuristic.

"""
from pydoku.SATSolver import SATSolver
from pydoku.FileHandler import FileHandler
from pydoku.HeuristicType import HeuristicType
from docopt import docopt
from termcolor import colored, cprint
import sys

ARG_KEY_HELP = '--help'
ARG_KEY_SOLVE = '-S'
ARG_KEY_DPLL = '-1'
ARG_KEY_RAND = '-2'
ARG_KEY_MOMS = '-3'
ARG_KEY_FILEPATH = 'FILE'

def error(message: str) -> None:
  """
  Prints out an error message in the terminal

  Parameters
  ----------
  message : str
      message to display the user

  Returns
  -------
  None

  See Also
  --------
  interpret : function interpreting the command line input and providing heuristic directive to the SAT solver
  """
  cprint(message, 'red', attrs = ['bold'], file = sys.stderr)

def success(message: str) -> None:
  """
  Prints out a success message in the terminal

  Parameters
  ----------
  message : str
      message to display the user

  Returns
  -------
  None

  See Also
  --------
  interpret : function interpreting the command line input and providing heuristic directive to the SAT solver
  """
  cprint(message, 'green', attrs = ['bold'], file = sys.stderr)

def interpret():
  """
  Interprets command line input and provides appropriate input to the SAT solver.
  If our SAT solver is able to find a suitable solution to the input CNF, the solution is written to the output file in DIMACS format.

  Returns
  -------
  None

  See Also
  --------
  success : function printing success messages to terminal
  error : function printing error messages to terminal
  """
  args = docopt(__doc__)

  if args[ARG_KEY_SOLVE] is None:
    error('Invalid input for command line utility.')
    exit(0)

  if args[ARG_KEY_DPLL]:
    heuristic = HeuristicType.STANDARD_DPLL
  elif args[ARG_KEY_RAND]:
    heuristic = HeuristicType.RANDOM_LITERAL
  elif args[ARG_KEY_MOMS]:
    heuristic = HeuristicType.MAX_OCCURRENCES_MIN_SIZE
  else:
    error('Invalid heuristic provided as input.')
    exit(0)

  filepath = args[ARG_KEY_FILEPATH]
  output_filepath = f'{filepath}.out'
  try:
    cnf = FileHandler.parse(filepath)
  except:
    error('Error: An error occurred while reading the file provided.')
    exit(0)

  try:
    solver = SATSolver()
    satisfied, assignments = solver.solve(cnf, heuristic)

    if satisfied:
      FileHandler.output(output_filepath, assignments)
      success('Satisfiable solution for the formula found!')
      success(f'Truth assignments satisfying the CNF can be found here: {output_filepath}')
    else:
      error('Formula provided is unsatisfiable.')

  except:
    error('Error: An error occurred while solving the provided CNF formula.')
    exit(0)

if __name__ == "__main__":
  interpret()


