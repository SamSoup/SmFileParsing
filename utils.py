from typing import Tuple, List
from constants import DIFFICULTY_MAPPER, CHART_TYPES
import re
import os
import glob

def prompt_user() -> Tuple[str, str, str, int, int]:
    """
    Prompt the user to select a chart difficulty level, and the beginning
    and ending measure number to section off the chart from
    """
    dir = input("Enter the directory containing the StepMania file (default=cwd): ") or os.getcwd()
    chart_type = input(f"Enter chart type ({CHART_TYPES}): ")
    difficulty = input(f"Enter chart difficulty ({DIFFICULTY_MAPPER.keys()}): ")
    measure_start = int(input("Enter the starting (0-indexed), inclusive) measure: "))
    measure_end = int(input("Enter the ending (0-indexed), inclusive) measure: "))

    return dir, DIFFICULTY_MAPPER[difficulty], chart_type, measure_start, measure_end

def get_smfile_contents(dir: str) -> str:
    """
    Scans a directory for a StepMania (.sm) song file and return its contents

    Args:
        dir (str): The directory containing the .sm file.

    Returns:
        str: The contents of the .sm file in string format
    """
    # Get all .sm files in current directory
    sm_files = glob.glob('*.sm', root_dir=dir)

    # Check if there is exactly one .sm file
    if len(sm_files) != 1:
        raise Exception(f"Error: There should be exactly one .sm file in {dir}.")

    sm_file = sm_files[0]
    with open(os.path.join(dir, sm_file), 'r') as f:
        contents = f.read()

    return contents

def get_measures(contents: str, difficulty: str, chart_type: str) -> Tuple[str, List[str]]:
    f"""
    Return the beats/measures section of the contents of the sm file, given a 
    particular difficulty

    Args:
        contents (str): all components  of a .sm file
        difficulty (str): one of {DIFFICULTY_MAPPER.keys()}
        chart_type (str): one of {CHART_TYPES}
    Returns:
        Tuple[str, ]: the chart header and the meaures of the specified difficulty
    """
    match = re.search(
        rf"#NOTES:\n\s+{chart_type}:\n.+:\n\s+{difficulty}:\n.+:\n.+:\n", 
        contents
    )
    if match:
        chart_start = match.end()
        chart_end = contents.find(f";", chart_start)
    else:
        raise Exception(f"Error: Could not find {chart_type} - {difficulty} chart.")
    
    chart_header = contents[match.start():match.end()]
    chart_measures = contents[chart_start:chart_end] # includes end ;
    chart_measures = re.split(",|;", chart_measures)
    return chart_header, chart_measures

def get_metadata(contents: str, chart_type: str) -> str:
    f"""
    Get the metadata of a song, which consists of the initial lines starting
    with #, until the start of the first (easiest) difficulty chart

    Args:
        contents (str): the contents of a .sm file
        chart_type (str): one of {CHART_TYPES}

    Returns:
        str: header tags metadata
    """
    metadata_end = contents.find(f"//---------------{chart_type} - ----------------")
    chart_metadata = contents[:metadata_end]
    return chart_metadata

def write_to_file(filename: str, metadata: str, chart_type: str, header: str, 
                  measures: List[str], measure_start: int, measure_end: int):
    f"""
    Write the desired sub-section of measures to a specified file

    Args:
        filename (str): name of file to output to
        metadata (str): metadata (header tags) of the overall song
        chart_type (str): one of {CHART_TYPES}
        header (str): #NOTES section of a specified difficulty
        measures (List[str]): all measures of a specified difficulty
        measure_start (int): the index of the first measure to include
        measure_end (int): the index of the last measure to include
    """

    print(f"Writing {filename}.")
    # write to current directory because I do not want to contaminate original folder 
    with open(filename, 'w') as f:
        f.write(metadata)
        f.write(f"//---------------{chart_type} - ----------------")
        f.write(f"{header}")
        for i in range(measure_start, measure_end+1):
            separator = "," if i != measure_end else ";"
            f.write(f"{measures[i]}{separator}")
        f.write("\n")
