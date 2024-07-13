import sys
from pathlib import Path
from collections import Counter
from tabulate import tabulate
from helpers.log_level_colorize import colorize


def parse_log_line(line: str) -> dict:
    return dict(zip(["date", "time", "log_level", "msg"], line.split(" ", 3)))


def load_logs(file_path: str) -> list:
    with open(file_path, 'r', encoding="utf-8") as file:
        return [parse_log_line(line.strip()) for line in file]


def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(
        lambda log: log["log_level"] == level.upper(), logs
    ))


def count_logs_by_level(logs: list) -> dict:
    return dict(Counter([log["log_level"] for log in logs]))


def display_log_counts(counts: dict):
    headers = ["Рівень логування", "Кількість"]
    table_data = [(colorize(key)(key), value) for key, value in counts.items()]
    print(tabulate(table_data, headers, tablefmt="presto", stralign="center"))


def display_filtered_logs(logs: list, level: str):
    print(f"Деталі логів для рівня '{colorize(level.upper())(level.upper())}':")
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['msg']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please run script with a directory path ")
    else:
        directory_path = sys.argv[1]
        try:
            path = Path(directory_path).expanduser().resolve(strict=True)
            if not path.is_file():
                raise FileNotFoundError('The path is not a file.')
            logs_list = load_logs(path)
            counts = count_logs_by_level(logs_list)
            display_log_counts(counts)
            if len(sys.argv) >= 3:
                level = sys.argv[2]
                filtered_logs = filter_logs_by_level(logs_list, level)
                if filtered_logs:
                    display_filtered_logs(filtered_logs, level)
                else:
                    level = colorize(level.upper())(level.upper())
                    print(
                        f"Немає логів для рівня '{level}' або введенно некоректне значення"
                    )
        except FileNotFoundError as e:
            print(f"[Error] resolving the path: {e}")
