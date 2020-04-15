from argparse import ArgumentParser
import csv


def log_reader(file_name)->str:
    try:
        with open(file_name, 'r') as file:
            log_file = file.read()

    except FileNotFoundError as e:
        print(e, 'please type file name to open!')
        quit()

    else:
        return log_file


def argument_parser():
    parser = ArgumentParser(description='log-file parser')
    parser.add_argument('file_folder', type=str, help='log-file')
    parser.add_argument('time_start', type=str, nargs='?', help='begin of time interval')
    parser.add_argument('time_end', type=str, nargs='?', help='end of time interval')

    args = parser.parse_args()

    file_folder = args.file_folder

    time_start = args.time_start

    time_end = args.time_end

    return {'file_folder': file_folder, 'time_start': time_start, 'time_end': time_end}


class Barrel:
    def __init__(self):
        self.time_start = ''
        self.time_end = ''

        self.log_string = None
        self.barrel_log_list = None

        self.barrel_size = 0
        self.water_level_in_start = 0
        self.current_water_level = 0
        self.water_level_in_the_end = 0

        self.top_up_tries = 0
        self.success_top_up_tries = 0
        self.top_up_err_in_percent = 0
        self.water_top_up_level = 0

        self.scoop_tries = 0
        self.success_scoop_tries = 0
        self.scoop_err_in_percent = 0
        self.water_scoop_level = 0

        self.barrel_params_init()

        self.time_interval_init()

        self.barrel_life_circle()

    def time_interval_init(self):
        time_start = argument_parser()['time_start']
        time_end = argument_parser()['time_end']

        if type(time_start) == str and time_start[10] == 'T':
            if time_start in self.log_string:
                self.time_start = time_start

        if type(time_end) == str and time_end[10] == 'T':
            if time_end in self.log_string:
                self.time_end = time_end

        if self.time_start != '':
            position_start = self.log_string.find(self.time_start)
        else:
            position_start = None

        if self.time_end != '':
            position_end = self.log_string.find(self.time_end)
        else:
            position_end = None
        self.barrel_log_list = self.barrel_log_list[position_start:position_end]

    def barrel_params_init(self):
        self.log_string = log_reader(argument_parser()['file_folder'])
        self.barrel_log_list = self.log_string.split('\n')
        self.barrel_size = int(self.barrel_log_list[1])
        self.water_level_in_start = int(self.barrel_log_list[2])

    def barrel_life_circle(self):
        self.current_water_level = self.water_level_in_start

        for note in self.barrel_log_list:
            self.check_water_action(note)

        try:
            self.top_up_err_in_percent = 100 - self.success_top_up_tries / self.top_up_tries * 100
        except ZeroDivisionError:
            self.top_up_err_in_percent = 0

        try:
            self.scoop_err_in_percent = 100 - self.success_scoop_tries / self.scoop_tries * 100
        except ZeroDivisionError:
            self.scoop_err_in_percent = 0

        if self.current_water_level == 0:
            self.current_water_level = self.water_level_in_start
        records = [
            ["Попыток налить воды всего", self.top_up_tries],
            ["Процент ошибок при попытке налить", f'{self.top_up_err_in_percent}%'],
            ["Всего воды налито (л.)", self.water_top_up_level],
            ["Попыток набрать воды всего", self.scoop_tries],
            ["Процент ошибок при попытке набрать", f'{self.scoop_err_in_percent}%'],
            ["Всего воды набрано (л.)", self.water_scoop_level],
            ["Объем воды в начале (л.)", self.water_level_in_start],
            ["Объем воды в конце (л.)", self.current_water_level]
        ]

        csv_writer(records)

    def check_water_action(self, note):

        if "top up" in note:
            index = note.find("up") + 2
            litres_want_to_up = int(note[index:-1])

            if litres_want_to_up + self.current_water_level <= self.barrel_size:
                self.current_water_level += litres_want_to_up
                self.top_up_tries += 1
                self.success_top_up_tries += 1
                self.water_top_up_level += litres_want_to_up

            else:
                self.top_up_tries += 1

        if "scoop" in note:
            index = note.find("scoop") + 5
            litres_want_to_scoop = int(note[index:-1])

            if self.current_water_level - litres_want_to_scoop >= 0:
                self.current_water_level -= litres_want_to_scoop
                self.scoop_tries += 1
                self.success_scoop_tries += 1
                self.water_scoop_level += litres_want_to_scoop

            else:
                self.scoop_tries += 1


def csv_writer(records):

    file_rec = "results.csv"

    with open(file_rec, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(records)


if __name__ == '__main__':
    barrel = Barrel()
