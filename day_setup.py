import os
import sys
import requests
import pickle
from datetime import datetime
from time import sleep

"""Sets up the folders for the next Advent of Code day.
Creates new directory for next day with format 'Day X'
Creates new text file for the puzzle input with format 'input.txt'
Creates python file with format 'dayX.py'

Args:
    *year: changes the default year directory you want to work in
    *tokenID: The sessionID for your web browser of choice
"""


def get_values():
    """
    Returns the dictionary of saved values from 'values.pkl' using pickle
    """
    values_file = 'values.pkl'

    if not os.path.exists(values_file):
        print(
            f"Error: The file '{values_file}' was not found in current directory.\nCreating file...")
        with open(values_file, 'wb') as file:    # Creates the file with empty dictionary
            pickle.dump({}, file)
        print('File created. Use flag "-h" or "--help" for help.')
        sys.exit(1)

    with open(values_file, 'rb') as file:
        values = pickle.load(file)

    if len(sys.argv) == 1:
        return values

    first_arg: str = sys.argv[1]

    if first_arg in ['-h', '--help']:
        print("""Optional arguments (only one at a time)
              *year (int): The default year directory you want to work in
              *tokenID (str): The sessionID for the web browser of your choice. e.g. "session=..."
                              Requires "session" keyword to be present and the token to start after "=" """)
        sys.exit(1)

    if first_arg.isnumeric():
        # Change the default year
        values['year'] = int(first_arg)
        print('Default year changed')

        with open(values_file, 'wb') as file:
            pickle.dump(values, file)
    else:
        # Change the sessionID token
        if first_arg.find('session') != -1:
            verify_change = input(
                "Are you sure you want to change sessionID? Type 'YES' to confirm\n")
            if verify_change == 'YES':
                values['sessionID'] = first_arg[first_arg.find('=') + 1:]
                with open(values_file, 'wb') as values_file:
                    pickle.dump(values, values_file)
                print('sessionID changed')
            else:
                print('Wrong confirmation. sessionID NOT changed')
        else:
            print('Argument has wrong format. Use flag "-h" or "--help" for help.')
        sys.exit(1)

    return values


def download_input(day: int, values: dict, times_tried: int) -> str:
    """Fetches the input of the day from the Advent of Code website

    Args:
        day (int): The day of the puzzle to get
        values (dict): contains year and sessionID, use get_values() to extract

    Returns:
        str: The input of the day. If error occurs, returns empty
    """
    # URL for the input file
    url = f"https://adventofcode.com/{values['year']}/day/{day}/input"

    # Headers for the request
    headers = {
        "Cookie": f"session={values['sessionID']}",
        "User-Agent": "AdventOfCodeInputDownloader"
    }

    # Request the input file
    response = requests.get(url, headers=headers, timeout=3)

    if response.status_code != 200:
        print(
            f"Failed to download input for the {times_tried} time. Status code: {response.status_code}")
        if response.status_code == 400:
            print(response.text)
            sys.exit(1)
        elif response.status_code == 404:
            print("The puzzle might not be released yet.")
        elif response.status_code == 500:
            print("Check your session token")
            sys.exit(1)
        elif response.status_code == None:
            print("Check internet connection.")
        return ''

    print(f"Input for Day {day} downloaded successfully")

    return response.text[:-1]


def setup():

    values = get_values()

    if datetime.today().year < values['year']:
        print('The puzzles for that year have not been released yet. Use flag "-h" or "--help" for help.')

    year_path = str(values['year'])
    next_day = 1
    if os.path.exists(year_path):
        for day in range(1, 26):
            day_path = f'{year_path}\\Day {day}'
            if not os.path.exists(day_path):
                next_day = day
                break
        else:
            print('The selected year has been completed. Please change the default year')
            sys.exit(1)

    if datetime.today().now() < datetime(values['year'], 12, next_day, 4, 59):
        print('The puzzle has not yet been released. Please try again later')
        sys.exit(1)

    while datetime.today().now() < datetime(values['year'], 12, next_day, 5):
        sleep(0.5)  # Wait 0.5 seconds before trying again
    for i in range(10):
        # Try to get the input in increasing delay
        input_text = download_input(next_day, values, i)
        if input_text:
            break
        sleep(1.5**(i-2))
    else:
        print('Was not able to fetch the input!')
        sys.exit(1)

    # Create directory for day
    day_path = f'{year_path}\\Day {next_day}'
    os.makedirs(day_path, exist_ok=True)

    # Create python file and input file
    py_path = f'{day_path}\\day{next_day}.py'
    input_path = f'{day_path}\\input.txt'
    with open(py_path, 'w') as file:
        file.write(python_starter)
    with open(input_path, 'w') as file:
        file.write(input_text)

    print(f'Successfully created files {py_path} and {input_path}')


python_starter = """\
# Import input.txt as str
with open('input.txt') as input:
    input_text = input.read()
"""

if __name__ == "__main__":
    setup()
