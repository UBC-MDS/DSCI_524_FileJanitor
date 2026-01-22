import os
import shutil
import tempfile
from FileJanitor.flatten import flatten
import pytest

# Create a test directory structure with files
def create_test_dir(base_dir):
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

# Test a non recursive flatten
def test_flatten_top_level_only():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        create_test_dir(src)
        result = flatten(src, tgt, recursive=False)

        assert result is True

        assert os.path.exists(os.path.join(tgt, "file1.txt"))
        assert os.path.exists(os.path.join(src, "sub1", "file2.txt"))
        assert os.path.exists(os.path.join(src, "sub1", "subsub1", "file3.txt"))
        assert os.path.exists(os.path.join(src, "sub2", "file4.txt"))

# Test for a recursive flatten, also test naming conflict resolution
def test_flatten_recursive():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        files = create_test_dir(src)
        result = flatten(src, tgt, recursive=True)
        assert result is True

        tgt_files = set(os.listdir(tgt))
        assert "file1.txt" in tgt_files
        assert "file2.txt" in tgt_files
        assert "file3.txt" in tgt_files
        assert "file4.txt" in tgt_files

        # Check for renamed file due to naming conflict
        assert "file1_1.txt" in tgt_files

# Test flatten with default output directory (current working directory)
def test_flatten_default_target_dir(monkeypatch):
    with tempfile.TemporaryDirectory() as src:
        create_test_dir(src)
        cwd = tempfile.mkdtemp()
        old_cwd = os.getcwd()
        monkeypatch.chdir(cwd)
        result = flatten(src, None, recursive=True)

        assert result is True
        tgt_files = set(os.listdir(cwd))
        assert "file1.txt" in tgt_files
        assert "file2.txt" in tgt_files
        assert "file3.txt" in tgt_files
        assert "file4.txt" in tgt_files

        # clean up
        monkeypatch.chdir(old_cwd)
        shutil.rmtree(cwd)

# Test for when source directory does not exist
def test_flatten_nonexistent_source():
    with pytest.raises(ValueError):
        flatten("nonexistent_dir", recursive=True)

# Test flatten when no movable files exist
def test_flatten_no_files_to_move():
    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as tgt:
        os.makedirs(os.path.join(src, "sub"))
        result = flatten(src, tgt, recursive=False)
        assert result is False

# Test when output directory does not exist
def test_flatten_nonexistent_output():
    with tempfile.TemporaryDirectory() as src:
        create_test_dir(src)
        nonexistent = os.path.join(src, "does_not_exist")
        with pytest.raises(ValueError):
            flatten(src, nonexistent, recursive=True)