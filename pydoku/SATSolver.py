"""
Class containing the algorithmic logic to solve Boolean Satisfiability Problems.

The current implementation supports 3 heuristics:
1. The standard Davis-Putnam-Logemann-Loveland (DPLL)
2. DPLL using the random literal (RAND) branching heuristic
3. DPLL using the maximum occurences in minimal size clauses (MOMS) branching heuristic
"""

from copy import copy, deepcopy
from pydoku.HeuristicType import HeuristicType
from random import choice

class SATSolver:

  def solve(self, cnf: list, heuristic: HeuristicType) -> [bool, dict]:
    """
    Solves a boolean satisfiability problem represented in conjunctive normal form (CNF)

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF
    heuristic : HeuristicType
      an Enum value giving us an indication of the branching heuristic to use while running DPLL

    Returns
    -------
    [bool, dict]
        returns true if a satisfiable solution to the CNF was found along with a dictionary containing assignments

    See Also
    --------
    dpll : function implementing the logic for Davis–Putnam–Logemann–Loveland (DPLL) algorithm
    """
    if heuristic not in HeuristicType:
      raise TypeError('Invalid heuristic provided as input.')

    return self.dpll(cnf, dict(), heuristic)

  def dpll(self, cnf: list, assignments: dict, heuristic: HeuristicType) -> [bool, dict]:
    """
    Solves a boolean satisfiability problem represented in conjunctive normal form (CNF)

    Implementing the logic for Davis–Putnam–Logemann–Loveland (DPLL) algorithm
    and returns a bool and dictionary denoting whether a satisfiable solution was found as well as
    the assignments that satisfied the CNF.

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF
    assignments : dict
        a dictionary containing literals and their respective assignments
    heuristic : HeuristicType
        an Enum value giving us an indication of the branching heuristic to use while running DPLL

    Returns
    -------
    [bool, dict]
        returns true if a satisfiable solution to the CNF was found along with a dictionary containing assignments

    See Also
    --------
    next_literal : function implementing the logic to find the next literal to branch on
    next_unit_literal : function implementing the logic to find the next unit literal for unit propagation
    transform : function implementing the logic to transform the CNF
    """
    literal = self.next_unit_literal(cnf)

    # implement unit propagation
    while literal is not None:
      cnf, assignments = self.transform(literal, deepcopy(cnf), deepcopy(assignments))
      literal = self.next_unit_literal(cnf)

    # assign pure literals appropriate values
    cnf, assignments = self.eliminate_pure_literals(cnf, deepcopy(assignments))

    # check for presence of empty clause
    if [] in cnf:
      return False, None

    # check if all clauses are satisfied
    if len(cnf) == 0:
      return True, assignments

    # At this point, we have gone through the list of all available unit literals in the current version of the CNF
    # This means that we now need to pick the next literal from clauses with two or more unassigned literals
    literal = self.next_literal(deepcopy(cnf), heuristic)
    new_cnf, new_assignments = self.transform(literal, deepcopy(cnf), deepcopy(assignments))
    result_satisfiable, result_assignments = self.dpll(deepcopy(new_cnf), deepcopy(new_assignments), heuristic)

    if not result_satisfiable:
      negation = self.get_negation(literal)
      new_cnf, new_assignments = self.transform(negation, deepcopy(cnf), deepcopy(assignments))
      return self.dpll(deepcopy(new_cnf), deepcopy(new_assignments), heuristic)

    return result_satisfiable, result_assignments

  def eliminate_pure_literals(self, cnf: list, assignments: dict) -> [bool, dict]:
    """
    Deletes any clause in the CNF that contains a pure literal

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF
    assignments : dict
        a dictionary containing literals and their respective assignments

    Returns
    -------
    [bool, dict]
        returns true if a satisfiable solution to the CNF was found along with a dictionary containing assignments

    See Also
    --------
    unit_propagation : function implementing the logic for unit propagation
    next_literal : function implementing the logic to find the next literal to branch on
    """
    pure_literals = self.get_pure_literals(cnf)

    for literal in pure_literals:
        assignments[literal] = True

        for clause in copy(cnf):
          if literal in clause:
            cnf.remove(clause)

    return cnf, assignments

  def transform(self, literal: str, cnf: list,  assignments: dict) -> [list, dict]:
    """
    Based on the literal this function does two things:

    1. If this is a positive literal, then we set its value to True.
      Consequently, the function will remove all clauses containing the literal from the CNF
      since these can no longer contribute to making the CNF false.

    2. We remove all instances of the negation of the literal in clauses, since these
      instances cannot make their parent clause True.

    Parameters
    ----------
    literal : str
        a literal belonging to the CNF
    cnf : list
        a list of clauses that belong to the CNF
    assignments : dict
        a dictionary containing literals and their respective assignments

    Returns
    -------
    [bool, dict]
        returns true if a satisfiable solution to the CNF was found along with a dictionary containing assignments

    See Also
    --------
    unit_propagation : function implementing the logic for unit propagation
    next_literal : function implementing the logic to find the next literal to branch on
    """
    assignments[literal] = True
    negation = self.get_negation(literal)

    for clause in copy(cnf):
      if literal in clause:
        cnf.remove(clause)

      if negation in clause:
        clause.remove(negation)

    return cnf, assignments

  def next_literal(self, cnf: list, heuristic: HeuristicType) -> str:
    """
    Returns the next literal to branch on

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF

    heuristic : HeuristicType
        the type of heuristic to use while picking the next literal

    Returns
    -------
    str
        returns the literal to branch on

    See Also
    --------
    dpll : function implementing Davis-Putnam-Logemann-Loveland (DPLL) algorithm
    """
    if heuristic == HeuristicType.RANDOM_LITERAL:
      return self.random_literal(cnf)
    elif heuristic == HeuristicType.MAX_OCCURRENCES_MIN_SIZE:
      return self.max_occurences_minimal_size_literal(cnf)

    return cnf[0][0]

  def max_occurences_minimal_size_literal(self, cnf: list) -> str:
    """
    Returns the literal occurring the most times in clauses of minimal size

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF

    Returns
    -------
    str
        returns the literal to branch on

    See Also
    --------
    next_literal : function fetching the next literal based on the heuristc type supplied to it
    dpll : function implementing Davis-Putnam-Logemann-Loveland (DPLL) algorithm
    """
    minimal_clause_size = None
    literals = list()

    for clause in cnf:
      if minimal_clause_size is None:
        minimal_clause_size = len(clause)

      if len(clause) < minimal_clause_size:
        literals.clear()
        minimal_clause_size = len(clause)

      if len(clause) == minimal_clause_size:
        literals += clause

    max_occurrences = 0
    literal_counts = dict()
    max_occurring = None

    for literal in literals:
      if literal in literal_counts:
        literal_counts[literal] += 1
      else:
        literal_counts[literal] = 1

      if literal_counts[literal] > max_occurrences:
        max_occurrences = literal_counts[literal]
        max_occurring = literal

    return max_occurring


  def random_literal(self, cnf: list) -> str:
    """
    Returns a randomly selected literal from the current CNF

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF

    Returns
    -------
    str
        returns the literal to branch on

    See Also
    --------
    next_literal : function fetching the next literal based on the heuristc type supplied to it
    dpll : function implementing Davis-Putnam-Logemann-Loveland (DPLL) algorithm
    """
    literals = [literal for clause in cnf for literal in clause]

    return choice(literals)

  def get_pure_literals(self, cnf: list) -> list:
    """
    Returns a list containing all literals that occur either only positively or negatively is calculated.

    Parameters
    ----------
    cnf : list
        a list of clauses that belong to the CNF

    Returns
    -------
    list
        returns a list containing pure literals

    See Also
    --------
    eliminate_pure_literals : function implementing the logic to eliminate pure literals from the CNF
    """
    pure = []
    impure = []

    for clause in cnf:
      for literal in clause:
        if literal in impure:
          continue

        if literal not in pure:
          pure.append(literal)
        else:
          pure.remove(literal)
          impure.append(literal)

    return pure

  def next_unit_literal(self, cnf: list) -> str:
    """
    Returns the next unit literal for running unit propagation

    If no unit literal is found in the current CNF, this returns None

    Parameters
    ----------
    cnf : list
       a list of clauses that belong to the CNF

    Returns
    -------
    str
       returns the literal to branch on

    See Also
    --------
    dpll : function implementing Davis-Putnam-Logemann-Loveland (DPLL) algorithm
    """
    for clause in cnf:
      if len(clause) == 1:
        return clause[0]

  def get_negation(self, literal: str) -> str:
    """
    Returns the negation of the literal provided as parameter

    Parameters
    ----------
    literal : str
       the literal whose negation you want to obtain

    Returns
    -------
    str
       returns the negation of the literal to branch onx
    """
    literal = deepcopy(literal)
    if literal[0] == '-':
      return literal[1:len(literal)]

    return f'-{literal}'
