// implements the Coleman-Liau index formula to show the reading level of text

#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>

int calculateLevel(const string text);

int main(void)
{
    string text = get_string("Text: ");
    int level = calculateLevel(text);

    if (level > 16)
    {
        printf("Grade 16+\n");
    }

    else if (level < 1)
    {
        printf("Before Grade 1\n");
    }

    else
    {
        printf("Grade %d\n", level);
    }
}

int calculateLevel(const string text)
{
    int i = 0;
    int letters = 0;
    int words = 1;
    int sentences = 0;

    while (text[i] != '\0')
    {
        if (isalpha(text[i]))
        {
            letters++;
        }

        else if (text[i] == ' ')
        {
            words++;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }

        i++;
    }

    float L = (letters * 100.0) / words;
    float S = (sentences * 100.0) / words;
    return (int) round(0.0588 * L - 0.296 * S - 15.8);
}
