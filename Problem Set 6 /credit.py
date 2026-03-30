# Prompts the user for a credit card number
# Prints whether it is a valid American Express, MasterCard, or Visa card number

import re

def main():
    card_number = input("Number: ")

    if not luhn_check(card_number):
        print("INVALID")
    elif re.fullmatch(r"3[47]\d{13}", card_number):
        print("AMEX")
    elif re.fullmatch(r"5[1-5]\d{14}", card_number):
        print("MASTERCARD")
    elif re.fullmatch(r"4(\d{12}|\d{15})", card_number):
        print("VISA")
    else:
        print("INVALID")


def luhn_check(card_number):
    total = 0
    reversed_digits = card_number[::-1]

    for i in range(len(reversed_digits)):
        digit = int(reversed_digits[i])

        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit = digit // 10 + digit % 10

        total += digit

    return total % 10 == 0


if __name__ == "__main__":
    main()
