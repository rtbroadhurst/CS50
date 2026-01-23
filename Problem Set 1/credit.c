// implements Luhn’s algorithm to check if a credit card number is syntactically valid
// if it is valid, prints the provider
// else prints INVALID

#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

bool checkValid(char *number);
int checkProvider(char *number);

int main(void)
{
    string number = get_string("Number: ");

    if (!checkValid(number))
    {
        printf("INVALID\n");
        return 0;
    }

    int provider = checkProvider(number);

    if (provider == 0)
        printf("AMEX\n");
    else if (provider == 1)
        printf("MASTERCARD\n");
    else if (provider == 2)
        printf("VISA\n");
    else
        printf("INVALID\n");

    return 0;
}

bool checkValid(char *number)
{
    int total = 0;
    int k = strlen(number) - 1;
    bool should_double = false;

    while (k >= 0)
    {
        int digit = number[k] - '0';

        if (should_double)
        {credit
            digit *= 2;
            if (digit > 9)
                digit -= 9;
        }

        total += digit;
        should_double = !should_double;
        k--;
    }

    return (total % 10 == 0);
}

int checkProvider(char *number)
{
    int len = strlen(number);

    // AMEX: 15 digits, starts with 34 or 37
    if (len == 15 && number[0] == '3' && (number[1] == '4' || number[1] == '7'))
        return 0;

    // MASTERCARD: 16 digits, starts with 51–55
    if (len == 16 && number[0] == '5' && (number[1] >= '1' && number[1] <= '5'))
        return 1;

    // VISA: 13 or 16 digits, starts with 4
    if ((len == 13 || len == 16) && number[0] == '4')
        return 2;

    return -1;
}
