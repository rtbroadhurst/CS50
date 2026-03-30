# Prompt the user for a height between 1 and 8 (inclusive), repeatedly asking until valid input is given.
# Print two side-by-side pyramids of that height using '#', aligned properly with spaces and a gap of 2 between them.

def main():
    height = get_height()

    for i in range(1, height + 1):
        spaces = " " * (height - i)
        blocks = "#" * i
        print(spaces + blocks + "  " + blocks)


def get_height():
    while True:
        try:
            height = int(input("Enter height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass


if __name__ == "__main__":
    main()
