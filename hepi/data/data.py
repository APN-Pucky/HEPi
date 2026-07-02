import importlib.resources
import os

def get_json_dir():
    """
    Get the path to the data directory

    Returns
    -------
    str
            Path to the data directory

    """
    return importlib.resources.files(".".join(__name__.split(".")[:-1])).joinpath(
        "json"
    )


def list_files():
    """
    List all files in the data directory

    Returns
    -------
    list
            List of files in the data directory

    """
    return [
        os.path.basename(b)
        for b in get_json_dir()
        .iterdir()
    ]


def get_file(filename : str):
    """
    Get the content of a file in the data directory

    Parameters
    ----------
    filename : str
            Name of the file

    Returns
    -------
    str
            Content of the file

    """
    return (
        importlib.resources.files(".".join(__name__.split(".")[:-1]))
        .joinpath("json")
        .joinpath(filename)
    )
