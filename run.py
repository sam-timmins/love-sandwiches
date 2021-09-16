# python3 run.py

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via
    the terminal. Data must be a string of 6 numbers seperated by commas.
    The loop will repeatedly request data until it is valid
    """
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, seperated by a commas.')
        print('Example: 10,20,30,40,50,60\n')
        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string data into integers.
    Raises valueError if strings cannot be converted into int,
    or if there are not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values must be entered. You provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    return True


def update_worksheet(data, sheet):
    """
    Updates the relivant worksheet, using a list of integers recieved.

        Parameters:
            data (int(list)):   A list of integers
            sheet (string):     String of the sheet name to upadte

    """
    print(f'Updating {sheet} worksheet...\n')
    worksheet = SHEET.worksheet(f'{sheet}')
    worksheet.append_row(data)
    print(f'{sheet} worksheet updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Possitive surplus indicates waste
    - Negative surplus indicates extra made during the day as stock was out
    """
    print('Caluclating surplus data... \n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data as a list
    of lists
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')


print('Welcome to Love Sandwiches Data Automation\n')
# main()

get_last_5_entries_sales()