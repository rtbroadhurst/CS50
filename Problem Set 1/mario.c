// Prompts the user for a height between 1 and 8 and prints two aligned pyramids with a gap between them.

#include <stdio.h>
void printPyramid(int n);

int main(void)
{
    while (1)
    {
        int n;

        printf("How tall should the pyramid be (1, 8 inclusive)? ");
        scanf("%i", &n);

        if (n > 0 && n < 9)
        {
            printPyramid(n);
            break;
        }
    }

    return 0;
}

void printPyramid(int n)
{
    int i;
    int k;
    int x;
    int y = n - 1;

    for (i = 0; i < n; i++)
    {

        for (x = 0; x < y; x++)
        {
            printf(" ");
        }

        for (k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        printf("  ");

        for (k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        printf("\n");
        y--;
    }

    return;
}
