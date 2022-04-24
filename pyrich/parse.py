import argparse


def set_args():
    parser = argparse.ArgumentParser(description="Hello👋🏼 I'm pyrich!")
    # record transaction date
    parser.add_argument(
        '-d',
        '--date',
        type=str,
        default='1900-1-1',
        metavar='DATE',
        help='Date of the transaction made. Defaults to 1900-1-1'
    )
    # record country
    parser.add_argument(
        '-c',
        '--country',
        default='USA',
        type=str,
        metavar='COUNTRY CODE',
        help='Country code of where stock is listed. Defaults to USA'
    )
    # symbol to record
    parser.add_argument(
        '-s',
        '--symbol',
        type=str,
        metavar='SYMBOL',
        help='Symbol of a stock'
    )
    # check for cryptocurrency
    parser.add_argument(
        '--crypto',
        action='store_true',
        help='Mark the stock as crypto. Defaults to False'
    )
    # record transaction type
    parser.add_argument(
        '-t',
        '--type',
        type=str,
        choices=['buy', 'sell', 'dividend'],
        metavar='TRANSACTION TYPE',
        help="Choose among transaction type 'buy', 'sell', 'dividend'"
    )
    parser.add_argument(
        '-q',
        '--quantity',
        type=int,
        metavar='QUANTITY',
        help='Transaction amounts'
    )
    parser.add_argument(
        '-p',
        '--price',
        type=float,
        metavar='PRICE',
        help='Traded price'
    )
    # copy transaction data from csv file
    parser.add_argument(
        '--csv',
        type=str,
        metavar='CSV FILENAME',
        help=('Csv filename to copy data from. The file should be located'
              'in the root directory of the package')
    )
    # display database table
    parser.add_argument(
        '--show',
        type=str,
        metavar='TABLE NAME',
        help='Table name to display'
    )
    # delete last row of the table
    parser.add_argument(
        '--delete',
        type=str,
        metavar='TABLE NAME',
        help='Table name to delete the last row. Defaults to None'
    )
    # open in streamlit app
    parser.add_argument(
        '-w',
        '--web',
        action='store_true',
        help='Open dashboard in a web browser. Defaults to False'
    )
    return parser
