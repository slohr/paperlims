class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DataFileTypeError(Error):
    """Exception raised for unknown data file types."""

class DataFilenameError(Error):
    """Exception raised for data file parsing errors."""

class OutputFilenameError(Error):
    """Exception raised for output file handling errors."""

class DuplicateFileError(Error):
    """Exception raised when checking for existing files."""

class GenericFilenameError(Error):
    """Exception raised for output file handling errors."""
