"""
FileJanitor: A Python package for cleaning and organizing file systems.

"""

from FileJanitor.standardize_filename import standardize_filename
from FileJanitor.flatten import flatten
from FileJanitor.replace_pattern import replace_pattern
from FileJanitor.index_files import index_files

__all__ = [
    "standardize_filename",
    "flatten",
    "replace_pattern",
    "index_files",
]