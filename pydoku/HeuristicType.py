"""
The class contains enums defining the available heuristics for the SAT solver
"""
from enum import IntEnum, unique

@unique
class HeuristicType(IntEnum):
  STANDARD_DPLL = 1
  RANDOM_LITERAL = 2
  MAX_OCCURRENCES_MIN_SIZE = 3