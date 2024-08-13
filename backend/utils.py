import datetime
import logging
import os
import json

logging_format = "Module: %(name)s\tFilename: %(filename)s:%(lineno)d\tFunction: %(funcName)s" \
                 "\n\t%(levelname)s: %(message)s"
logging.basicConfig(format=logging_format)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
# file_sh = logging.FileHandler('./debug.log')
# file_sh.setFormatter(logging.Formatter(logging_format))


def convert_seconds_to_timestamp(seconds):
    """
    Converts `seconds = 3661.123` to a timestamp format: 01:01:01.123

    Args:
        seconds (float): the number of seconds to be converted.

    Returns:
        Returns (str) timestamp string
    """
    td = datetime.timedelta(seconds=seconds)  # Convert seconds to a timedelta object
    hours, remainder = divmod(td.seconds, 3600)  # Extract hours, minutes, seconds, and milliseconds
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"  # Format the timestamp


def sentences_to_srt(sentences_list: dict) -> str:
    """
    Converts a list of "sentence" objects from deepgram into an SRT formatted string.

    Args:
        sentences_list (dict): the list of sentences provided by deepgram transcription service.

    Returns:
        output (str): SRT formatted string.
    """

    output = ""
    for sdx, sentence in enumerate(sentences_list):
        start_ts = convert_seconds_to_timestamp(sentence["start"])
        end_ts = convert_seconds_to_timestamp(sentence["end"])
        output += f"{sdx}\n{start_ts} --> {end_ts}\n{sentence['text']}\n\n"
    return output


def write_json(filename: str, data: dict) -> None:
    """
    Writes a json file.

    Args:
        filename (str): filepath to save.
        data (dict): contents of the output file.

    Returns:
        None
    """
    with open(filename, "w", encoding="utf8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    logger.info(f"{filename} written to file.")


def read_json(filename: str):
    """
    Reads a json file.

    Args:
        filename (str): name of the file to read.

    Returns:
        data (dict): the data contained in the file.
    """
    assert os.path.isfile(filename), f"{filename} does not exist."
    with open(filename, "r", encoding="utf8") as file:
        data = json.load(file)
    logger.info(f"{filename} read in.")
    return data


def write_string_to_file(filename: str, contents: str):
    """
    Write a string to file.

    Args:
        filename (str): the file where the contents will be written.
        contents (str): the string contents to write to file.

    Returns:
        None.
    """
    with open(filename, 'w', encoding='utf8') as file:
        file.write(contents)
    logger.info(f'{filename} has been written.')


def main():
    # Example usage
    seconds = 3661.123  # Example float value
    timestamp = convert_seconds_to_timestamp(seconds)
    print(timestamp)  # Output: 01:01:01.123


if __name__ == '__main__':
    main()
