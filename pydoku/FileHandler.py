"""
Class containing a helper methods to parse and write DIMACS files
"""

class FileHandler:

  @staticmethod
  def parse(filepath: str) -> list:
    """
    Parses a file provided to it in DIMACS format and returns the appropriate CNF as a list

    Parameters
    ----------
    filepath : str
        Path of the file defining a CNF in DIMACS format

    Returns
    -------
    list
        returns CNF containing

    """
    file = open(filepath, 'r')

    cnf = list()
    cnf.append(list())

    for line in file:
      tokens = line.split()
      if len(tokens) != 0 and tokens[0] not in ('p', 'c'):
        for literal in tokens:
          if literal == "0":
            cnf.append(list())
          else:
            cnf[-1].append(literal)

    cnf.pop()
    file.close()

    for clause in cnf:
      if len(clause) == 0:
        print(cnf)
        exit(0)

    return cnf

  @staticmethod
  def output(output_path: str, assignments: dict) -> None:
    """
    Parses a file provided to it in DIMACS format and returns the appropriate CNF as a list

    Parameters
    ----------
    output_path : str
      file to write the output to

    assignments : dict
      a dictionary containing assignments that satisfy the CNF

    Returns
    -------
    None
    """
    output = list()
    for key, value in assignments.items():
      if value is True:
        output.append(f'{key} 0')

    dimacs = f'p cnf {len(output)} {len(output)}\n'
    dimacs += '\n'.join(output)

    file = open(output_path, '+w')
    file.write(dimacs)
    file.close()