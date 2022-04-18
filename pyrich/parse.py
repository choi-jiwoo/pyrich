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
        help='Record date of the action.'
    )
    # record country
    parser.add_argument(
        '-c',
        '--country',
        default='USA',
        type=str,
        metavar='COUNTRY CODE',
        help='Country code of where stock is listed.'
    )
    # symbol to record
    parser.add_argument(
        '-s',
        '--symbol',
        type=str,
        metavar='SYMBOL',
        help='Symbol to record.'
    )
    # record transaction type
    parser.add_argument(
        '-t',
        '--type',
        type=str,
        choices=['buy', 'sell', 'dividend'],
        metavar='TRANSACTION TYPE',
        help='Record transaction type.'
    )
    parser.add_argument(
        '-q',
        '--quantity',
        type=int,
        metavar='QUANTITY',
        help='Record transaction amounts.'
    )
    parser.add_argument(
        '-p',
        '--price',
        type=float,
        metavar='PRICE',
        help='Record traded price.'
    )
    # check for cryptocurrency
    parser.add_argument(
        '--crypto',
        action='store_true',
        help='Check if crypto.'
    )
    # open in streamlit app
    parser.add_argument(
        '-w',
        '--web',
        action='store_true',
        help='Open dashboard in a web browser.'
    )
    return parser
