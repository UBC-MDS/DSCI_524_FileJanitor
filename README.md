# Welcome to 524GroupProject

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/524groupproject.svg)](https://pypi.org/project/524groupproject/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/524groupproject.svg)](https://pypi.org/project/524groupproject/)  |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

*TODO: the above badges that indicate python version and package version will only work if your package is on PyPI.
If you don't plan to publish to PyPI, you can remove them.*

## Summary

FileJanitor is a package that cleans, standardizes, and organizes file names and folder structures.

## Contributors

* **Sean Brown** ([@SeanBrown12345](https://github.com/SeanBrown12345))
* **Sam Lokanc** ([@SamLokanc](https://github.com/SamLokanc))
* **Rabin Duran** ([@rabin0208](https://github.com/rabin0208))
* **Luis Alonso Alvarez** ([@luisalonso8](https://github.com/luisalonso8))

## Overview usage

FileJanitor provides a set of utility functions to automate common-file system housekeeping tasks, such as renaming files, standardizing name conventions, ordering files, and restructuring directories. All functions operate on all files in a specialized folder unless specified.

## Get started

You can install this package into your preferred Python environment using pip:

```bash
$ pip install 524groupproject
```

TODO: Add a brief example of how to use the package to this section

To use 524groupproject in your code:

```python
>>> import 524groupproject
>>> 524groupproject.hello_world()
```

## Features

## Function 1: Timestamp files

Adds a timestamp to each file name in a folder. 
•	The timestamp is included directly in the file name.
•	The timestamp is added as a prefix.
•	It works on all files in the specified directory.

```bash
report.pdf → 2023-10-14_09-32-11_report.pdf
```

## Function 2: Pattern Replacement in File Names
Replaces the input pattern in file names with a new pattern or character. This function will:
•	Support replacing characters or strings (_ -> &)
•	Capitalize the first word of the file name.
•	Apply changes to all files in the folder.

```bash
file_janitors.txt → File & janitors.txt
```
## Function 3: File name standardization
This function standardizes file names according to consistent formatting rules. This can be helpful when dealing with large collections of inconsistently named files.
•	Replaces spaces and invalid characters with underscores (_).
•	Converts dashes (-)  and spaces to underscores (_).
•	Removes duplicate punctuation (..)
•	Preserves file extensions

```bash
___Final-csv.csv → FINAL_CSV.csv
other 03-file.csv → OTHER_03_FILE.csv
```
## Function 4. Indexing files
This function orders the files in each folder according to a defined order.

Consider the following folder:

```bash
my_thesis_folder/
├── discussion.pdf
├── intro.pdf
├── conclusions.pdf
└── analysis.pdf
```
Then, the desired order should be like this:

```bash
order = [
    "intro.pdf",
    "analysis.pdf",
    "discussion.pdf",
    "conclusions.pdf"
]
```
Output:
```bash
my_thesis_folder/
├── intro.pdf
├── analysis.pdf
├── discussion.pdf
└── conclusions.pdf
```

## Function 5. Flattening and Unflattening Directories

**Flatten:**

This function will move all files from nested subfolders into a single target directory. This is useful in case someone wants all files at the same directory level. The folder structure is ignored during flattening.

```bash
project_root/
├── data/
│   ├── raw/
│   │   └── file1.csv
│   └── processed/
│       └── file2.csv
```

```bash
project_root/
├── file1.csv
├── file2
```

**Unflatten:**

Restores files into predefined folders based on a specified structure or rule. So, the files are returned to their original or previous directories.

```bash
project_root/
├── file1.csv
├── file2.csv
```

```bash
project_root/
├── data/
│   ├── raw/
│   │   └── file1.csv
│   └── processed/
│       └── file2.csv
```


## Copyright

- Copyright © 2026 Sean Brown, Sam Lokanc, Rabin Duran, Luis Alonso Alvarez.
- Free software distributed under the [MIT License](./LICENSE).
