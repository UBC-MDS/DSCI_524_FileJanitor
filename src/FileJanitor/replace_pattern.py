import os

def replace_pattern(dir: str, pattern: str, replacement: str) -> bool:
    """
    Replace specific patterns in filenames within a directory.
    
    This function iterates over all files in the specified directory and 
    renames them by substituting a target string or character with a new one. 
    This is useful for targeted batch updates, such as swapping delimiters 
    or correcting specific naming errors.
    
    The following transformations are applied:
    1. All occurrences of the input pattern within the filename root are 
       replaced by the replacement string.
    2. File extensions are preserved and excluded from the replacement logic.
    3. Directory structure remains unchanged; only the filenames are modified.
    
    Parameters
    ----------
    dir : str
        Path to the directory containing files to be modified.
    pattern : str
        The substring or character pattern to search for in filenames.
    replacement : str
        The string or character to insert in place of the found pattern.
    
    Returns
    -------
    bool
        True if any files were renamed, False otherwise.

    Raises
    ------
    FileNotFoundError
        If the specified directory path does not exist.
    NotADirectoryError
        If the path points to a file instead of a directory.
    PermissionError
        If insufficient permissions to rename files in the directory.

    Examples
    --------
    >>> replace_pattern("docs/", pattern="_", replacement=" & ")
    Renames files like:
    "file_janitors.txt" -> "file & janitors.txt"
    "report_v1_final.pdf" -> "report & v1 & final.pdf"

    Notes
    -----
    - Only the filename root is modified; file extensions are always preserved
    - All occurrences of the pattern within each filename are replaced
    - Directory structure remains unchanged
    - Files without the pattern in their name are left unchanged
    - Hidden files (starting with .) are processed unless explicitly excluded
    """
    # Check if directory exists
    if not os.path.isdir(dir):
        raise ValueError("Source directory does not exist.")
    
    files_renamed = False
    
    # Iterate through all files in the directory
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        
        # Skip if it's not a file (e.g., subdirectories)
        if not os.path.isfile(file_path):
            continue
        
        # Split filename into root and extension
        base, ext = os.path.splitext(file)
        
        # Replace pattern in filename root only
        new_base = base.replace(pattern, replacement)
        
        # Only rename if the filename actually changed
        if new_base != base:
            new_filename = new_base + ext
            new_file_path = os.path.join(dir, new_filename)
            
            # Check that we are not renaming file onto itself
            if os.path.abspath(file_path) == os.path.abspath(new_file_path):
                continue
            
            # Check if target filename already exists
            counter = 1
            while os.path.exists(new_file_path):
                new_filename = f"{new_base}_{counter}{ext}"
                new_file_path = os.path.join(dir, new_filename)
                counter += 1
            
            # Rename the file
            os.rename(file_path, new_file_path)
            files_renamed = True
    
    return files_renamed