// takes two words as input from each player and returns which one scored higher in a scrabble style points game

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

int calculateValue(string word);

int main(void)
{
    string wordOne = get_string("Player 1: ");
    string wordTwo = get_string("Player 2: ");

    int scoreOne = calculateValue(wordOne);
    int scoreTwo = calculateValue(wordTwo);

    if (scoreOne > scoreTwo)
    {
        printf("Player 1 wins!\n");
    }

    else if (scoreOne < scoreTwo)
    {
        printf("Player 2 wins\n");
    }

    else
    {
        printf("Tie!\n");
    }
}

int calculateValue(string word)
{
    int score = 0;
    const int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int i = 0;

    while (word[i] != '\0')
    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }

        i++;
    }

    return score;
}

