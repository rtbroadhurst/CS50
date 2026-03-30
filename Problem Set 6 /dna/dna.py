# Identifies a person from a DNA sequence by comparing STR counts against a database

import csv
import sys


def main():

    # Check for correct number of command-line arguments
    if len(sys.argv) != 3:
        sys.exit("Incorrect number of command-line arguments")

    # Parse the command line arguments
    csv_file = sys.argv[1]
    text_file = sys.argv[2]

    # Read database file into a variable
    rows = []
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    with open(text_file, "r") as f:
        sequence = f.read()

    # Find longest match of each STR in DNA sequence
    strs = [key for key in rows[0].keys() if key != "name"]
    results = {}
    for str_name in strs:
        results[str_name] = longest_match(sequence, str_name)

    # Check database for matching profiles
    for row in rows:
        match = True
        for str_name in strs:
            if int(row[str_name]) != results[str_name]:
                match = False
                break
        if match:
            print(row["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()
