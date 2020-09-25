<p align="center">
  <a href="https://github.com/sid-chaubs/pydoku">
    <img src="/images/logo.png" alt="pydoku" width="125" />
  </a>
</p>
<h3 align="center">pydoku</h3> 
<p align="center">
  A SAT Solver, that will make you smile.
</p>

## Table of Contents

- [Key Features](#key-features)
- [Download](#download)
- [Usage](#usage)
- [Contributors](#contributors)

## Key Features

* A simple command line interface (CLI) to solve Boolean Satisfiability problems.
* Input and output in the Conjunctive Normal Form DIMACS file format.
* Support for three key branching heuristics:
  - Standard Davis-Putnam-Logemann-Loveland (DPLL)
  - Random literal (RAND)
  - Maximum Occurrences in Clauses of Minimal Size (MOMS)
* Cross platform
  - Windows, macOS and Linux ready.

## Download

To clone and run this application, you'll need [Git](https://git-scm.com) and [python3](https://www.python.org/download/releases/3.0/) (which comes with [pip](https://pypi.org/project/pip/)) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/sid-chaubs/pydoku

# Go into the repository
$ cd pydoku

# Install CLI tool and dependencies
$ pip install .

# Run the help command
$ SAT --help
```

## Usage

Once you have followed the download and installation instructions, the command line utility (CLI) should be available for use on your computer. You can find a list of available tools offered by the CLI by typing in `SAT --help` command.

In order to use the CLI to solve a Satisfiability problem, we require that you provide the CLI an input file describing a propositional logic formula in Conjunctive Normal Form (CNF) using DIMACS.

As mentioned in the [Key Features](#key-features) section, the current version of this project supports three heuristics by to solve CNFs. In order to choose a specific heuristic to run using the CLI, you only need to supply the CLI with one of the following option flags: `-S1`, `-S2`, or `-S3`. The mapping between each of these option flags and the heuristic used to solve the CNF is outlined in the table below:

Option|Heuristic
------|---------
`-S1` | Standard Davis-Putnam-Logemann-Loveland (DPLL)
`-S2` | Random literal (RAND)
`-S3` | Maximum Occurrences in Clauses of Minimal Size (MOMS)


##### Sample Usage
```
  SAT -S1 [DIMACS_INPUT_FILE] // will run DPLL on the CNF defined in the DIMACS_INPUT_FILE
  SAT -S2 [DIMACS_INPUT_FILE] // will use RAND as the branching heuristic while solving the CNF
  SAT -S3 [DIMACS_INPUT_FILE] // will use MOMS as the branching heuristic while solving the CNF
```

If a satisifiable solution for the provided CNF is found, the CLI will output a file in DIMACS format containing the assignments which satisfied the input CNF. This file will be output in the same directory as the original input file provided albeit with a `.out` extension. 

So, if your input file was `~/Desktop/9x9-sudoku-dimacs.txt`, the output file will be `~/Desktop/9x9-sudoku-dimacs.txt.out`.

## Contributors

<a href="https://github.com/ikramez"><img src="https://avatars1.githubusercontent.com/u/43179802?v=4" width="100px"/></a> | <a href="https://github.com/iershh"><img src="https://avatars2.githubusercontent.com/u/39951197?v=4" width="100px"/></a> | <a href="https://github.com/SeyfullahB"><img src="https://avatars3.githubusercontent.com/u/71129894?v=4" width="100px"/></a> | <a href="https://github.com/sid-chaubs"><img src="https://avatars0.githubusercontent.com/u/35002570?v=4" width="100px"/></a>
:-:|:-:|:-:|:-:
<a href="https://github.com/ikramez">Ikrame Zirar</a> | <a href="https://github.com/iershh">Iris Lau</a> | <a href="https://github.com/SeyfullahB">Seyfullah Bakirci</a> | <a href="https://github.com/sid-chaubs" align="center">Sid Chaubal</a> 
