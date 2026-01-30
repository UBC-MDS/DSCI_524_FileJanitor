import os
import tempfile
from FileJanitor.replace_pattern import replace_pattern
import pytest

def create_test_dir(base_dir):
    """
    Create a test directory structure with files
    """

    os.makedirs(os.path.join(base_dir, "sub1", "subsub1"))
    os.makedirs(os.path.join(base_dir, "sub2"))
    files = [
        os.path.join(base_dir, "file1.txt"),
        os.path.join(base_dir, "sub1", "file2.txt"),
        os.path.join(base_dir, "sub1", "file1.txt"),
        os.path.join(base_dir, "sub1", "subsub1", "file3.txt"),
        os.path.join(base_dir, "sub2", "file4.txt"),
    ]
    for f in files:
        with open(f, "w") as fp:
            fp.write("test")
    return files

def test_replace_pattern_basic():
    """
    Test 1: Basic pattern replacement functionality
    """

    with tempfile.TemporaryDirectory() as test_dir:
        # Create files with underscores in top-level directory
        with open(os.path.join(test_dir, "file_test.txt"), "w") as fp:
            fp.write("test")
        with open(os.path.join(test_dir, "report_v1_final.pdf"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern("_", " & ", test_dir)
        
        assert result is True
        assert os.path.exists(os.path.join(test_dir, "file & test.txt"))
        assert os.path.exists(os.path.join(test_dir, "report & v1 & final.pdf"))

def test_replace_pattern_naming_conflict_and_extension():
    """
    Test 2: Naming conflict resolution and extension preservation
    """

    with tempfile.TemporaryDirectory() as test_dir:
        # Create files that will cause naming conflict
        with open(os.path.join(test_dir, "file_test.txt"), "w") as fp:
            fp.write("test")
        with open(os.path.join(test_dir, "file&test.txt"), "w") as fp:
            fp.write("test")
        # Test extension preservation
        with open(os.path.join(test_dir, "file.name.txt"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern("_", "&", test_dir)
        
        assert result is True
        tgt_files = set(os.listdir(test_dir))
        assert "file&test.txt" in tgt_files
        assert "file&test_1.txt" in tgt_files
        # Extension preserved: file.name.txt has no underscore so unchanged
        assert "file.name.txt" in tgt_files

def test_replace_pattern_no_matches_and_subdirectories():
    """
    Test 3: No matches and subdirectories are skipped
    """

    with tempfile.TemporaryDirectory() as test_dir:
        create_test_dir(test_dir)
        
        # Test with pattern that doesn't exist in top level files
        result = replace_pattern("X", "Y", test_dir)
        assert result is False
        # Top-level file should still exist
        assert os.path.exists(os.path.join(test_dir, "file1.txt"))
        # Subdirectory files should be unchanged
        assert os.path.exists(os.path.join(test_dir, "sub1", "file2.txt"))
        assert os.path.exists(os.path.join(test_dir, "sub1", "subsub1", "file3.txt"))

def test_replace_pattern_nonexistent_dir():
    """
    # Test 4: Error handling: nonexistent directory
    """
    
    with pytest.raises(ValueError):
        replace_pattern("_", " ", "nonexistent_dir")

def test_replace_pattern_edge_cases():
    """
    Test 5: Edge cases: empty pattern and empty directory
    """

    with tempfile.TemporaryDirectory() as test_dir:
        # Test empty pattern
        with open(os.path.join(test_dir, "test_file.txt"), "w") as fp:
            fp.write("test")
        result = replace_pattern("", "X", test_dir)
        assert result is False
        assert os.path.exists(os.path.join(test_dir, "test_file.txt"))
        
        # Test empty directory
        with tempfile.TemporaryDirectory() as empty_dir:
            result = replace_pattern("_", " ", empty_dir)
            assert result is False