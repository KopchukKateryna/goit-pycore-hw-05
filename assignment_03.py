"""
Розробіть Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл,
переданий як аргумент командного рядка, і виводити статистику за рівнями логування
наприклад, INFO, ERROR, DEBUG. Також користувач може вказати рівень логування як другий
аргумент командного рядка, щоб отримати всі записи цього рівня.
"""

import argparse
from pathlib import Path
from collections import Counter
from tabulate import tabulate
from helpers.log_level_colorize import colorize


def parse_log_line(line: str) -> dict:
    """
    Parses a single line from the log file into a dictionary.
    Takes a log line as input, splits it into its components
    (date, time, log level, and message), and returns these components in a
    dictionary with appropriate keys.

    Args:
        * line (str): A single line from the log file, expected to contain
            the date, time, log level, and message separated by spaces.

    Returns:
        * dict: A dictionary containing the parsed log details with the following keys:
            - 'date'(str): The date of the log entry.
            - 'time'(str): The time of the log entry.
            - 'log_level'(str): The log level (e.g., INFO, ERROR, DEBUG).
            - 'msg'(str): The log message.
    """
    parts = line.split(" ", 3)
    if len(parts) < 4:
        raise ValueError(
            "Incorrect log line format, expected at least three spaces to "
            "separate the components."
        )
    return dict(zip(["date", "time", "log_level", "msg"], parts))


def load_logs(file_path: Path) -> list:
    """
    Loads and parses log entries from a log file.
    Reads a log file line by line, parses each line using the
    `parse_log_line` function, and returns a list of parsed log entries.
    Each log entry is expected to be in a specific format that can be processed
    by the `parse_log_line` function.

    Args:
        * file_path (Path): The path to the log file to be read.

    Returns:
        * list: A list of parsed log entries, where each entry is a dictionary
            containing the log details.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        return [parse_log_line(line.strip()) for line in file]


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Filters log entries by a specific log level.
    Iterates through a list of log entries and returns a new list
    containing only the entries that match the specified log level.

    Args:
        * logs (list): A list of log entries, where each entry is a dictionary
            containing at least a 'log_level' key.
        * level (str): The log level to filter by (e.g., 'ERROR', 'INFO').

    Returns:
        * list: A list of log entries that match the specified log level.
    """
    return list(filter(
        lambda log: log["log_level"] == level, logs
    ))


def count_logs_by_level(logs: list) -> dict:
    """
    Counts the number of log entries for each log level.
    Iterates through a list of log entries, extracts the log levels,
    and counts the occurrences of each log level using the `Counter` from the
    `collections` module. It returns a dictionary where the keys are log levels
    and the values are the counts of entries for each level.

    Args:
        * logs (list): A list of log entries, where each entry is a dictionary 
            containing at least a 'log_level' key.

    Returns:
        * dict: A dictionary with log levels as keys and the count of entries for each
            level as values.
    """
    return dict(Counter([log["log_level"] for log in logs]))


def display_log_counts(counts: dict):
    """
    Displays a table of log counts by log level.
    Formats and prints a table showing the number of log entries
    for each log level. It uses the `tabulate` module to create a well-formatted
    table with headers "Рівень логування" (Log Level) and "Кількість" (Count).
    The log levels are colorized for better readability. =)

    Args:
        * counts (dict): A dictionary where keys are log levels (str) and values are the
            number of log entries for each level (int).

    Returns:
        * None
    """
    headers = ["Рівень логування", "Кількість"]
    table_data = [(colorize(key)(key), value) for key, value in counts.items()]
    print(tabulate(table_data, headers, tablefmt="presto", stralign="center"))


def display_filtered_logs(logs: list, level: str):
    """
    Displays logs filtered by a specific level.
    Prints out the details of log entries that match
    the specified log level. It formats the output to show the date,
    time, and message of each log entry.

    Args:
        * logs (list): A list of log entries, where each entry is a dictionary
            containing 'date', 'time', and 'msg' keys.
        * level (str): The log level to filter and display (e.g., 'ERROR', 'INFO').

    Returns:
        * None
    """
    print(f"Деталі логів для рівня '{colorize(level)(level)}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['msg']}")


def parse_arguments():
    """
    Parses command line arguments for the log processing script.
    Uses the argparse library to define and parse the
    required and optional arguments for the script. The arguments
    include the path to the log file and an optional log level to filter by.

    Args:
        * None

    Returns:
        * argparse.Namespace: An object containing the parsed arguments:
            - file_path (str): The path to the log file.
            - level (str, optional): The log level to filter by. Default is None.
    """
    parser = argparse.ArgumentParser(description="Process log file.")
    parser.add_argument("file_path", type=str, help="Path to the log file")
    parser.add_argument(
        "level",
        type=str,
        nargs="?",
        help="Log level to filter by (optional)",
        default=None,
    )
    return parser.parse_args()


def validate_path(path: str) -> Path:
    """
    Validates path to the log file.

    Args:
        * path (str): Path to the log file.

    Returns:
        * path(Path): Validated path to the log file.
    """
    path = Path(path).expanduser().resolve(strict=True)
    if not path.is_file():
        raise FileNotFoundError("The path is not a file.")
    if path.stat().st_size == 0:
        raise ValueError("The file is empty.")
    return path


def process_logs(path: Path, level: str = None):
    """
    Process log file and display counts and details for the specified level.

    Args:
        * path(Path): Path to the log file.
        * level(str): Log level to filter by (optional).

    Returns:
        * None
    """
    logs_list = load_logs(path)
    counts = count_logs_by_level(logs_list)
    display_log_counts(counts)

    if level:
        level = level.upper()
        filtered_logs = filter_logs_by_level(logs_list, level)
        if filtered_logs:
            display_filtered_logs(filtered_logs, level)
        else:
            level = colorize(level)(level)
            print(f"No logs for level '{level}' or invalid value entered")


def main():
    """
    Main function. Parses command line arguments,
    validates the file path and starts the logging process.

    Args:
        * None
    Returns:
        * None
    """
    args = parse_arguments()
    try:
        file_path = validate_path(args.file_path)
        process_logs(file_path, args.level)
    except FileNotFoundError as e:
        print(f"[Error] resolving the path: {e}")
    except ValueError as e:
        print(f"[Error] processing the log file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
