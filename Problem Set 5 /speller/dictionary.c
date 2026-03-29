// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

int word_count = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Declare constant for number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Convert word to lowercase copy
    char lower[LENGTH + 1];
    int i = 0;
    for (; word[i] != '\0'; i++)
    {
        lower[i] = tolower((unsigned char) word[i]);
    }
    lower[i] = '\0';

    // Hash the word
    int index = hash(lower);

    // Start with the head of the linked list
    node *cursor = table[index];

    while (cursor != NULL)
    {
        // Compare word to current node's word
        if (strcmp(cursor->word, lower) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = hash_value * 31 + tolower((unsigned char) word[i]);
    }

    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the file
    FILE *file = fopen(dictionary, "r");

    // If file fails to open, return false
    if (file == NULL)
    {
        return false;
    }

    // Create buffer
    char word[LENGTH + 1];

    // Loop through dictionary
    while (fscanf(file, "%s", word) != EOF)
    {
        // Create new node for the word
        node *new_node = malloc(sizeof(node));

        // If malloc fails, close file and return false
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }

        // Copy the word from the buffer into the node
        strcpy(new_node->word, word);

        // Hash the word to generate the index
        int index = hash(word);

        // Insert new node into the start of the linked list in the correct bucket
        new_node->next = table[index];
        table[index] = new_node;

        // Increment the word count
        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop through each bucket
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        // Traverse the linked list in this bucket
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
