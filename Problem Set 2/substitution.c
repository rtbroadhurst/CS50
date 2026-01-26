// enables you to encrypt messages using a substitution cipher
// user enters the key as a command line argument

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int valid(string key);
void encrypt(string plaintext, string key);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    if (!valid(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    encrypt(plaintext, key);

    return 0;
}

void encrypt(string plaintext, string key)
{
    printf("ciphertext: ");

    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        char c = plaintext[i];

        if (isalpha(c))
        {
            int index = toupper(c) - 'A';  
            char sub = key[index];

            if (islower(c))
            {
                sub = tolower(sub);
            }
            else
            {
                sub = toupper(sub);
            }

            putchar(sub);
        }
        else
        {
            putchar(c);
        }
    }

    putchar('\n');
}

int valid(string key)
{
    int seen[26] = {0};
    int length = 0;

    for (int i = 0; key[i] != '\0'; i++)
    {
        if (!isalpha(key[i]))
        {
            return 0;
        }

        int index = toupper(key[i]) - 'A';

        if (seen[index])
        {
            return 0;
        }

        seen[index] = 1;
        length++;
    }

    return length == 26;
}
