from argparse import ArgumentParser


def strings_equality_checker(string_1='', string_2='')->str:

    result = None

    string_1_full = string_1

    string_2_full = string_2

    if string_1 == string_2:
        result = 'OK'

    find_list_1 = []
    find_list_2 = []

    for s in string_2:

        if s in string_1:
            find_list_1.append(string_1.find(s))
            find_list_2.append(string_2.find(s))

            string_1 = string_1.replace(s, ' ', 1)
            string_2 = string_2.replace(s, ' ', 1)

        elif s != '*':
            result = 'KO'

    if string_1_full[-1:] != string_2_full[-1:] and string_2_full[-1:] != '*':
        result = 'KO'

    if string_1_full[0] != string_2_full[0] and string_2_full[0] != '*':
        result = 'KO'

    for num in find_list_1:

        try:
            if find_list_1[num+1] > find_list_1[num]:
                pass

            else:
                result = 'KO'

        except IndexError:
            break

    string_2_cut = string_2.replace('*', '')

    if result is None and string_1 == string_2_cut:
        result = 'OK'

    if result is None:

        was_not_found_list = []

        for char in string_1:

            index = string_1.find(char)

            if index not in find_list_1:
                was_not_found_list.append(index)

        for num in was_not_found_list:
            string_cut = string_2[num-1:]

            if string_cut.find('*') < 0:
                result = 'KO'
            else:
                result = 'OK'

    list_from_string_2 = string_2_full.split('*')

    for item in list_from_string_2:
        if item not in string_1_full:
            result = 'KO'

    return f'''"{string_1_full}" "{string_2_full}" - {result}
                  '''


def main():

    parser = ArgumentParser(description='checking 2 strings for equality')
    parser.add_argument('string_1', type=str, help='first string')
    parser.add_argument('string_2', type=str, help='second string')

    args = parser.parse_args()
    str_1 = args.string_1
    str_2 = args.string_2

    print(strings_equality_checker(str_1, str_2))


if __name__ == '__main__':

    main()
