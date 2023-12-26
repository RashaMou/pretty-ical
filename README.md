# Pretty print ical files
`pretty-ical` is a cli application that takes a .ical file as input and pretty
prints its contents with indentation and colored headers to make it easier to read.

You can print directly to the terminal (with both color and indentation) or save
the output to a specified file with the `--save` flag (only indentation).

Indentation defaults to 2, but you can set that option with the `--indent` flag.

## Prerequisites
- Python (version 3.x)
- Poetry for dependency management

## Installation

1. Clone the repository
```
git clone git@github.com:RashaMou/pretty-ical.git
cd pretty-ical
```
2. Install dependencies using poetry
```
poetry install
```
