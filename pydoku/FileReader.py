"""
Class containing a static helper method to parse DIMACS files
"""
class FileReader:

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