import random

# Get user's name
name = input("What is your name? ")
print("Good Luck!", name)

# List of words
words = [
    'rainbow', 'computer', 'science', 'programming',
    'python', 'mathematics', 'player', 'condition',
    'reverse', 'water', 'board', 'geeks'
]

# Select a random word
word = random.choice(words)

print("\nGuess the characters")

# Store guessed characters
guesses = ''

# Number of attempts
turns = 12

# Main game loop
while turns > 0:

    failed = 0

    # Display guessed characters and hidden letters
    for char in word:
        if char in guesses:
            print(char, end=" ")
        else:
            print("_", end=" ")
            failed += 1

    print()

    # Check if the word has been guessed
    if failed == 0:
        print("You Win")
        print("The word is:", word)
        break

    # Get user input
    guess = input("Guess a character: ").lower()

    # Validate input length
    if len(guess) != 1:
        print("Please enter a single character.")
        continue

    # Check for duplicate guesses
    if guess in guesses:
        print("You already guessed that character.")
        continue

    # Store the guess
    guesses += guess

    # Handle incorrect guesses
    if guess not in word:
        turns -= 1
        print("Wrong")
        print("You have", turns, "more guesses")

        # Check if user has lost
        if turns == 0:
            print("You Lose")
            print("The word was:", word)