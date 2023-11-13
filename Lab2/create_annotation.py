import csv
import os
import logging
import json


logging.basicConfig(level=logging.INFO)


def create_csv_list(directory: str, classes: str) -> list:
    """This function creates list filled with absolute path, relative path and class"""
    csv_list = list()
    for c in classes:
        count = len(os.listdir(os.path.join(directory, c)))
        for i in range(count):
            row = [[os.path.abspath(os.path.join(directory, c, f"{i:04}.txt")), os.path.join(directory, c, f"{i:04}.txt"), c]]
            csv_list += row
    return csv_list


def write_into_csv(name: str, csv_list: list) -> None:
    """This function creates csv file and writes row to the csv file"""
    try:
        for c in csv_list:
            with open(f"{name}.csv", "a") as file:
                write = csv.writer(file, lineterminator="\n")
                write.writerow(c)
    except Exception as exc: 
        logging.error(f"Can not save/write data: {exc.message}\n{exc.args}\n")


if __name__ == "__main__":
    with open(os.path.join("Lab2", "settings.json"), "r") as settings:
        settings = json.load(settings)
    l = create_csv_list(settings["main_folder"], settings["classes"])
    write_into_csv(f"{settings["csv"]}/{settings["main_folder"]}", l)