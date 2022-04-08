import os
from pyrich import parse
from pyrich.transaction import Transaction


def run():
    parser = parse.set_args()
    args = parser.parse_args()
    options = vars(args)
    new_record = Transaction(options)

