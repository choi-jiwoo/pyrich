import argparse


def set_args():
    parser = argparse.ArgumentParser(description="Hello👋🏼 I'm pyrich!")
    # record transaction
    parser.add_argument(
        '-t',
        '--transaction',
        type=str,
        nargs=6,
        metavar=('DATE', 'COUNTRY', 'TYPE', 'SYMBOL', 'QUANTITY', 'PRICE'),
        help='Record transaction'
    )
    # record dividends
    parser.add_argument(
        '-d',
        '--dividend',
        type=str,
        nargs=4,
        metavar=('DATE', 'SYMBOL', 'AMOUNT', 'CURRENCY'),
        help='Record dividends received'
    )
    # copy transaction data from csv file
    parser.add_argument(
        '--csv',
        type=str,
        metavar='CSV FILENAME',
        help=('Csv filename to copy data from. The file should be located '
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
        '--deletelast',
        type=str,
        metavar='TABLE NAME',
        help='Table name to delete the last row. Defaults to None'
    )
    # delete all rows in the table
    parser.add_argument(
        '--deleteall',
        type=str,
        metavar='TABLE NAME',
        help='Table name to delete all rows. Defaults to None'
    )
    parser.add_argument(
        '--cash',
        metavar=('CURRENT CASH', 'CURRENCY'),
        nargs=2,
        help='Update current cash'
    )
    # open in streamlit app
    parser.add_argument(
        '-w',
        '--web',
        action='store_true',
        help='Open dashboard in a web browser. Defaults to False'
    )
    return parser
