import os
import shutil

def flatten(nested_directory: str, output_directory: str | None = None, recursive: bool = False) -> bool:
    """
    Flatten a directory by moving all files from nested subdirectories
    into a target directory. 

    By default, only files directly inside 'nested_directory' are moved.
    If 'recursive' is True, files from all nested subdirectories
    are also moved. If any naming conflicts occur, files are renamed
    by appending a counter to their base names.

    Parameters
    ----------
    nested_directory : str
        Root directory containing files and nested subdirectories to flatten.
    output_directory : str, optional
        Directory where flattened files will be moved. 
        If None, the current working directory is used.
    recursive : bool, optional
        If True, flatten files from all nested subdirectories.
        If False, only flatten files directly under `nested_directory`.

    Returns
    -------
    bool
        True if the operation was successful, False otherwise.

    Examples
    --------
    Flatten only top-level files:
    >>> flatten("./assignments", "./")
    True

    Flatten all nested files:
    >>> flatten("./images", recursive=True)
    True
    """
    # checks for source and target directories
    if not os.path.isdir(nested_directory):
        raise ValueError("Source directory does not exist.")
    
    if output_directory is None:
            output_directory = os.getcwd()

    if not os.path.exists(output_directory):
            raise ValueError("Target directory does not exist.")
    files_moved = False

    # flattening for recursive case
    if recursive:
        for root, _, files in os.walk(nested_directory):
            for file in files:
                file_to_be_moved = os.path.join(root, file)
                move_to = os.path.join(output_directory, file)
                # check that we are not moving file onto itself
                if os.path.abspath(file_to_be_moved) == os.path.abspath(move_to):
                    continue
                base, ext = os.path.splitext(file)

                counter = 1
                # if file exists in target directory, modify name
                while os.path.exists(move_to):
                    move_to = os.path.join(output_directory, f"{base}_{counter}{ext}")
                    counter += 1
                
                # move file
                shutil.move(file_to_be_moved, move_to)
                files_moved = True

    # flattening for non recursive case
    else:
        for file in os.listdir(nested_directory):
            file_to_be_moved = os.path.join(nested_directory, file)
            if os.path.isfile(file_to_be_moved):
                move_to = os.path.join(output_directory, file)
                # check that we are not moving file onto itself
                if os.path.abspath(file_to_be_moved) == os.path.abspath(move_to):
                    continue
                base, ext = os.path.splitext(file)

                counter = 1
                # if file exists in target directory, modify name
                while os.path.exists(move_to):
                    move_to = os.path.join(output_directory, f"{base}_{counter}{ext}")
                    counter += 1

                # move file
                shutil.move(file_to_be_moved, move_to)
                files_moved = True

    return files_moved
   