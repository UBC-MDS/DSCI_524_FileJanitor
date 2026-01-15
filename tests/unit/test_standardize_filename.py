import pytest
import tempfile
import os
from FileJanitor.standarize_filename import standardize_filename

# test 1: test case conversion
def test_case_conversion():
    original_files = [
        "this_is_a_test1.txt",
        "THIS_IS_A_TEST2.txt",
        "This_Is_A_Test3.txt",
        "ThiS_Is_A_TEST4.txt",
    ]

    test_cases = {
        "lower": [
            "this_is_a_test1.txt",
            "this_is_a_test2.txt",
            "this_is_a_test3.txt",
            "this_is_a_test4.txt",
        ],
        "upper": [
            "THIS_IS_A_TEST1.TXT",
            "THIS_IS_A_TEST2.TXT",
            "THIS_IS_A_TEST3.TXT",
            "THIS_IS_A_TEST4.TXT",
        ],
        "title": [
            "This_Is_A_Test1.Txt",
            "This_Is_A_Test2.Txt",
            "This_Is_A_Test3.Txt",
            "This_Is_A_Test4.Txt",
        ],
    }
    
    for case, expected_names in test_cases.items():
        with tempfile.TemporaryDirectory() as test_dir:
            for name in original_files:
                open(os.path.join(test_dir, name), "w").close()

            result = standardize_filename(dir=test_dir, case=case, sep="_")

            assert result is True
            for expected in expected_names:
                assert os.path.exists(os.path.join(test_dir, expected))

# test 2: test spacing conversion
def test_space_conversion():
    original_files = [
        "this_is_a_test1.txt",
        "this is a test2.txt",
        "this-is-a-test3.txt",
        "this_is-a test4.txt",
    ]

    test_cases = {
        "_": [
            "this_is_a_test1.txt",
            "this_is_a_test2.txt",
            "this_is_a_test3.txt",
            "this_is_a_test4.txt",
        ],
        "-": [
            "this-is-a-test1.txt",
            "this-is-a-test2.txt",
            "this-is-a-test3.txt",
            "this-is-a-test4.txt",
        ],
        " ": [
            "this is a test1.txt",
            "this is a test2.txt",
            "this is a test3.txt",
            "this is a test4.txt",
        ],
    }
    
    for sep, expected_names in test_cases.items():
        with tempfile.TemporaryDirectory() as test_dir:
            for name in original_files:
                open(os.path.join(test_dir, name), "w").close()

            result = standardize_filename(dir=test_dir, case="lower", sep=sep)

            assert result is True
            for expected in expected_names:
                assert os.path.exists(os.path.join(test_dir, expected))

# test 3: test remove duplicate punctuation
def test_remove_duplicate_punctuation():
    original_files = [
        "this__is--a  test1.txt",
        "this___is---a__test2.txt",
    ]

    expected = [
        "this_is_a_test1.txt",
        "this_is_a_test2.txt",
    ]

    with tempfile.TemporaryDirectory() as test_dir:
        for name in original_files:
            open(os.path.join(test_dir, name), "w").close()

        with pytest.raises(ValueError):
            standardize_filename(dir=test_dir, case="lower", sep="_")


# test 4: test for value error if two files will have the same name when standardized
def test_filename_collision():
    original_files = [
        "this_is_a_test.txt",
        "this-is-a-test.txt",
    ]

    with tempfile.TemporaryDirectory() as test_dir:
        for name in original_files:
            open(os.path.join(test_dir, name), "w").close()

        with pytest.raises(ValueError):
            standardize_filename(dir=test_dir, case="lower", sep='_')

# test 5: test for value error if provided directory does not exist
def test_directory_not_exist():
    with pytest.raises(ValueError):
        standardize_filename(dir="non_existent_dir", case="lower", sep='_')