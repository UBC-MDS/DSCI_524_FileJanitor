import os
import tempfile
from FileJanitor.replace_pattern import replace_pattern
import pytest

# Create a test directory structure with files
def create_test_dir(base_dir):
    files = [
        os.path.join(base_dir, "file_janitors.txt"),
        os.path.join(base_dir, "report_v1_final.pdf"),
        os.path.join(base_dir, "normal_file.txt"),
        os.path.join(base_dir, "test_file_name.csv"),
        os.path.join(base_dir, ".hidden_file.txt"),
    ]
    for f in files:
        with open(f, "w") as fp:
            fp.write("test")
    return files

# Test basic pattern replacement
def test_replace_pattern_basic():
    with tempfile.TemporaryDirectory() as test_dir:
        create_test_dir(test_dir)
        result = replace_pattern(test_dir, pattern="_", replacement=" & ")
        
        assert result is True
        
        assert os.path.exists(os.path.join(test_dir, "file & janitors.txt"))
        assert os.path.exists(os.path.join(test_dir, "report & v1 & final.pdf"))
        assert os.path.exists(os.path.join(test_dir, "normal_file.txt"))
        assert os.path.exists(os.path.join(test_dir, "test & file & name.csv"))
        assert os.path.exists(os.path.join(test_dir, ".hidden & file.txt"))

# Test pattern replacement with naming conflict resolution
def test_replace_pattern_naming_conflict():
    with tempfile.TemporaryDirectory() as test_dir:
        # Create files that will cause naming conflict
        with open(os.path.join(test_dir, "file_test.txt"), "w") as fp:
            fp.write("test")
        with open(os.path.join(test_dir, "file&test.txt"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern(test_dir, pattern="_", replacement="&")
        
        assert result is True
        
        tgt_files = set(os.listdir(test_dir))
        assert "file&test.txt" in tgt_files
        assert "file&test_1.txt" in tgt_files

# Test that files without pattern are not renamed
def test_replace_pattern_no_match():
    with tempfile.TemporaryDirectory() as test_dir:
        files = [
            os.path.join(test_dir, "normal_file.txt"),
            os.path.join(test_dir, "another_file.pdf"),
        ]
        for f in files:
            with open(f, "w") as fp:
                fp.write("test")
        
        result = replace_pattern(test_dir, pattern="X", replacement="Y")
        
        assert result is False
        
        assert os.path.exists(os.path.join(test_dir, "normal_file.txt"))
        assert os.path.exists(os.path.join(test_dir, "another_file.pdf"))

# Test that extension is preserved (pattern only replaced in root)
def test_replace_pattern_preserves_extension():
    with tempfile.TemporaryDirectory() as test_dir:
        with open(os.path.join(test_dir, "file.txt"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern(test_dir, pattern=".", replacement="-")
        
        assert result is True
        
        # Extension should still be .txt, only root changed
        assert os.path.exists(os.path.join(test_dir, "file-txt"))
        assert not os.path.exists(os.path.join(test_dir, "file.txt"))

# Test for when source directory does not exist
def test_replace_pattern_nonexistent_dir():
    with pytest.raises(ValueError):
        replace_pattern("nonexistent_dir", pattern="_", replacement=" ")

# Test replace_pattern when no files to rename exist
def test_replace_pattern_no_files_to_rename():
    with tempfile.TemporaryDirectory() as test_dir:
        # Create empty directory
        result = replace_pattern(test_dir, pattern="_", replacement=" ")
        assert result is False

# Test replace_pattern with subdirectories (should skip them)
def test_replace_pattern_skips_subdirectories():
    with tempfile.TemporaryDirectory() as test_dir:
        os.makedirs(os.path.join(test_dir, "subdir"))
        with open(os.path.join(test_dir, "file_test.txt"), "w") as fp:
            fp.write("test")
        with open(os.path.join(test_dir, "subdir", "nested_file.txt"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern(test_dir, pattern="_", replacement=" ")
        
        assert result is True
        
        assert os.path.exists(os.path.join(test_dir, "file test.txt"))
        assert os.path.exists(os.path.join(test_dir, "subdir", "nested_file.txt"))

# Test replace_pattern with empty pattern (edge case)
def test_replace_pattern_empty_pattern():
    with tempfile.TemporaryDirectory() as test_dir:
        with open(os.path.join(test_dir, "test_file.txt"), "w") as fp:
            fp.write("test")
        
        result = replace_pattern(test_dir, pattern="", replacement="X")
        
        assert result is False
        assert os.path.exists(os.path.join(test_dir, "test_file.txt"))