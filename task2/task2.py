# -*- coding: utf-8 -*-
from argparse import ArgumentParser


class FiguresInspector:

    def __init__(self):
        self.file_path = None
        self.x1 = None
        self.y1 = None
        self.z1 = None

        self.x2 = None
        self.y2 = None
        self.z2 = None

        self.a = None
        self.b = None
        self.c = None
        self.R = None

        self.main()

    def main(self):
        parser = ArgumentParser(description='figures_crossing_inspector')
        parser.add_argument('file_folder', type=str, help='name of the file with parameters')

        args = parser.parse_args()

        self.file_path = args.file_folder

        self.parameters_parser()

        self.figures_crossing_inspector()

    def parameters_parser(self):
        try:
            with open(self.file_path, 'r') as file:
                file_to_str = file.read()

        except FileNotFoundError as e:
            print(e, 'please type file name with figure parameters!')
            quit()

        else:
            string_format = file_to_str.replace('sphere', '"sphere"')
            string_format = string_format.replace('center', '"center"')
            string_format = string_format.replace('radius', '"radius"')
            string_format = string_format.replace('line', '"line"')
            string_format = string_format.replace('[', '(')
            string_format = string_format.replace(']', ')')

            params_dict = eval(string_format)

            lines_params_list = list(params_dict['line'])

            self.x1 = lines_params_list[0][0]
            self.y1 = lines_params_list[0][1]
            self.z1 = lines_params_list[0][2]

            self.x2 = lines_params_list[1][0]
            self.y2 = lines_params_list[1][1]
            self.z2 = lines_params_list[1][2]

            sphere_params = params_dict['sphere']
            sphere_center = sphere_params['center']

            self.a = sphere_center[0]
            self.b = sphere_center[1]
            self.c = sphere_center[2]

            self.R = sphere_params['radius']


    def figures_crossing_inspector(self):
        C1 = (self.x2 - self.x1) / (self.y2 - self.y1)
        C2 = (-self.y1 * self.x2 + self.x1 * self.y2) / (self.y2 - self.y1)

        C3 = (self.z2 - self.z1) / (self.y2 - self.y1)
        C4 = (-self.y1 * self.z2 + self.z1 * self.y2) / (self.y2 - self.y1)

        C5 = C2 - self.a
        C6 = C4 - self.c

        A = C1 ** 2 + C3 ** 2 + 1
        B = 2 * C1 * C5 - 2 * self.b + 2 * C3 * C6
        C = C5 ** 2 + self.b ** 2 + C6 ** 2 - self.R ** 2

        desc = B ** 2 - 4 * A * C

        if desc < 0:
            print('Коллизий не найдено')
            quit()

        try:
            ys1 = (-B + desc ** 0.5) / (2 * A)
            ys2 = (-B - desc ** 0.5) / (2 * A)

        except ZeroDivisionError:
            print('Коллизий не найдено')

        else:
            xs1 = ys1 * C1 + C2

            zs1 = ys1 * C3 + C4

            print([xs1, ys1, zs1], '\n')

            if desc != 0:
                xs2 = ys2 * C1 + C2
                zs2 = ys2 * C3 + C4

                print([xs2, ys2, zs2], '\n')


if __name__ == '__main__':
    figure_inspector = FiguresInspector()
