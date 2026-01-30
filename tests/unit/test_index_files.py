import pytest
import os
from pathlib import Path
import tempfile
from FileJanitor.index_files import index_files

@pytest.fixture
def temp_dir():
    """
    Create a temporary (and cleaned up) directory for testing
    """
    
    with tempfile.TemporaryDirectory() as temp_path:
        yield temp_path

def test_basic_ordering(temp_dir):
    """ 
    Test 1: Basic file ordering with numerical prefixes 
    """

    Path(temp_dir, "c.txt").touch()
    Path(temp_dir, "a.txt").touch()
    Path(temp_dir, "b.txt").touch()
    
    order = ["a.txt", "b.txt", "c.txt"]
    result = index_files(temp_dir, order)
    
    assert result == True
    assert Path(temp_dir, "01_a.txt").exists()
    assert Path(temp_dir, "02_b.txt").exists()
    assert Path(temp_dir, "03_c.txt").exists()

def test_unlisted_hide_default(temp_dir):
    """ 
    Test 2: Hide unlisted files and move to unlisted folder 
    """

    Path(temp_dir, "ordered.txt").touch()
    Path(temp_dir, "unlisted.txt").touch()
    
    order = ["ordered.txt"]
    index_files(temp_dir, order)
    
    assert Path(temp_dir, "01_ordered.txt").exists()
    assert Path(temp_dir, "_unlisted", "unlisted.txt").exists()

def test_unlisted_keep(temp_dir):
    """ 
    Test 3: Keep unlisted files with sequential numbers 
    """

    Path(temp_dir, "first.txt").touch()
    Path(temp_dir, "unlisted.txt").touch()
    
    order = ["first.txt"]
    index_files(temp_dir, order, unlisted="keep")
    
    assert Path(temp_dir, "01_first.txt").exists()
    assert Path(temp_dir, "02_unlisted.txt").exists()

def test_file_not_found_error():
    """ 
    Test 4: FileNotFoundError when path does not exist 
    """

    with pytest.raises(FileNotFoundError):
        index_files("/nonexistent/path", ["file.txt"])

def test_not_a_directory_error(temp_dir):
    """ 
    Test 5: NotADirectoryError when path points to a file 
    """

    file_path = Path(temp_dir, "file.txt")
    file_path.touch()
    with pytest.raises(NotADirectoryError):
        index_files(str(file_path), ["something.txt"])

def test_empty_order_list(temp_dir):
    """ 
    Test 6: ValueError when order list is empty 
    """

    with pytest.raises(ValueError):
        index_files(temp_dir, [])

def test_duplicate_filenames(temp_dir):
    """ 
    Test 7: ValueError when order contains duplicates 
    """

    Path(temp_dir, "file.txt").touch()
    
    with pytest.raises(ValueError):
        index_files(temp_dir, ["file.txt", "other.txt", "file.txt"])

def test_empty_directory(temp_dir):
    """ 
    Test 8: Handle edge cases 
    Test with empty directory should not raise an error
    """

    order = ["nonexistent.txt", "another.txt"]
    result = index_files(temp_dir, order)

    assert result == False
    assert len(list(Path(temp_dir).iterdir())) == 0

