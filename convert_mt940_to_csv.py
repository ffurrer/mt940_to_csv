#!/usr/bin/env python

import csv
import os
import argparse
from mt940 import MT940

parser = argparse.ArgumentParser(description='Convert MT940 to CSV files.')
parser.add_argument('input_file', type=str,
                    help='The path to the input file.')
parser.add_argument('output_file', type=str,
                    help='The path to the output file.')

args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file


mt940 = MT940(input_file)
if len(mt940.statements) != 1:
    print("Just evaluating first statement. Multiple statements is not handled for now.")
statement, = mt940.statements


start_balance = statement.start_balance
end_balance = statement.end_balance

with open(output_file, mode='w') as transaction_file:
    transaction_writer = csv.writer(
        transaction_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    transaction_writer.writerow(
        ["Statement Account", statement.account, "Statement Information", statement.information])
    transaction_writer.writerow(
        ["Start Balance", start_balance.date, start_balance.currency + " " + str(start_balance.amount)])
    transaction_writer.writerow(
        ["End Balance", end_balance.date, end_balance.currency + " " + str(end_balance.amount)])

    transaction_writer.writerow([])
    transaction_writer.writerow(['transaction.booking', 'transaction.amount',
                                 'transaction.id', 'transaction.additional_data', 'transaction.description'])
    for transaction in statement.transactions:
        transaction_writer.writerow([transaction.booking, transaction.amount,
                                     transaction.id, transaction.additional_data, transaction.description])
