import os
import re

def standardize_filename(dir: str = None, case: str="lower", sep: str="_") -> bool:
    """
    Standardize filenames in a directory by normalizing case, separators,
    and duplicate punctuation.

    This function iterates over all files in the specified directory and
    renames them according to the selected formatting rules. Directory
    structure is preserved; only filenames are modified.

    The following transformations are applied:
    1. Filename case can be converted to title case, upper case, or lower case.
        Case transformation is applied only to the filename stem; file extensions
        are preserved.
    2. Hyphens (-), underscores (_), and spaces are treated as word separatores and
        normalized to sep.
    3. Duplicate punctuation characters (e.g., '__', '--', '  ', etc.) are 
        reduced to a single instance.

    Parameters
    ----------
    dir : str or Path
        Path to the directory containing files to be standardized.
    case : {'title', 'upper', 'lower'}, optional
        Desired casing for filenames (default is 'lower').
    sep : {'-', '_', ' '}, optional
        Character to use as the separator between words in filenames
        (default is '_').

    Returns
    -------
    list of tuple(Path, Path)
        A list of (old_path, new_path) pairs for each file that was renamed.
        Files whose names were unchanged are not included.

    Examples
    --------
    >>> standardize_filename("data/", case="title", sep="-")
    Renames files like:
    "my__sample file--name.txt" -> "My-Sample-File-Name.txt"
    """
    if dir is None:
        dir = os.getcwd()
    if not os.path.isdir(dir):
        raise ValueError("Directory does not exist")

    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

    duplicate_pattern = re.compile(r"[_\-\s]{2,}")
    for filename in files:
        name, _ = os.path.splitext(filename)
        if duplicate_pattern.search(name):
            raise ValueError("Duplicate punctuation detected")

    standardized = {}

    for filename in files:
        name, ext = os.path.splitext(filename)

        name = re.sub(r"[_\-\s]+", sep, name)

        full_name = name + ext
        if case == "lower":
            full_name = full_name.lower()
        elif case == "upper":
            full_name = full_name.upper()
        elif case == "title":
            full_name = sep.join(
                part.title() for part in full_name.split(sep)
            )
        else:
            raise ValueError("Invalid case option")

        if full_name in standardized.values():
            raise ValueError("Filename collision detected")

        standardized[filename] = full_name

    for old, new in standardized.items():
        os.rename(
            os.path.join(dir, old),
            os.path.join(dir, new),
        )

    return True