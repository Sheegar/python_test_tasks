from argparse import ArgumentParser
import logging


logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s %(message)s')


def num_converter(nb=1, base='base')-> str:
    """base – система счисления.
Например, «01» - двоичная, «012» - троичная, «0123456789abcdef» - шестнадцатиричная,
«мартышки» - система счисления в мартышках."""
    try:
        if type(nb) is not int:
            raise TypeError('parameter "nb" must have int-type')
        num = nb

        if str(base) != base:
            raise TypeError('parameter "base" must have str-type')

        if base == '':
            raise ValueError('parameter "base" must contain 1 symbol at least')

        table = base

    except TypeError as e:
        logging.error(f"incorrect usage: {e}")
        quit()

    except ValueError as e:
        logging.error(f"incorrect usage: {e}")
        quit()

    else:

        table_size = len(table)
        result = ''
        if len(table) == 1:
            return table * num
        if num < len(table):
            return table[num]

        while num:
            num, y = divmod(num, table_size)
            result = table[y] + result

        return result


def main():

    parser = ArgumentParser(description='numeric converter')
    parser.add_argument('number', type=int, help='integer number (unsigned)')
    parser.add_argument('base', type=str, help='base table of number system (string)')

    args = parser.parse_args()
    number = args.number
    table_base = args.base

    print(num_converter(number, table_base))


if __name__ == '__main__':

    main()

