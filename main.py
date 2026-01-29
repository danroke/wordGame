import requests
from bs4 import BeautifulSoup
import random
import re

def select_word(words):
  # Select a random word from the list for the player to guess
  size = len(words)
  prompt_num = random.sample(range(0,size),1)
  prompt = words[prompt_num[0]]
  # Convert prompt to all upper case for easier matching
  prompt = prompt.upper()
  return prompt

def replace_char(new_char, word, pos):
  if pos == 0:
    return new_char + word[1:]
  if pos == 4:
    return word[:4] + new_char
  return word[:pos] + new_char + word[pos + 1:]

      
def update_lists(guessed_list, word, remainder_list):
  # Returns tuple of updated lists
  for letter in word:
    if letter not in guessed_list:
      guessed_list.append(letter.upper())
      if letter in remainder_list:
        remainder_list.remove(letter.upper())
    else:
      continue
  guessed_list.sort()
  remainder_list.sort()
  return (guessed_list, remainder_list)


def start_game(word):
  explain = input("\nWelcome to Word Game! Would you like an explanation? (y/n):")
  if explain == ('y' or 'Y'):
    print("\nA random 5 letter word has been selected. It is your job to try to guess this word in 5 guesses or less! After each guess you will be given feedback on how close your guess was.")
    print("If your guess shares no letters with the word the feedback will look like this: ***** 0")
    print("If your guess has a correct letter it will display like this: *A*** 0")
    print("If you match a letter but it is in the wrong position it, the number after the word will display how many letters they share.")
    print("For example, if the word is TABLE and you guessed ASSET the feedback would be like this: ***** 3")
    print("Another example, if the word is TABLE and you guessed TRADE the feedback would be like this: T***E 1")
    print("\nI hope that helps, goodluck!\n\n")
  elif explain != ('n' or 'N' or 'y' or 'Y'):
    print("Error: invalid response")
    exit(1)

  # Track used letters
  guessed_letters = []
  remaining_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  feedback_collection = []
  
  # Entered n/N, start game as normal
  guess_count = 5
  while(guess_count > 0):
    print("You have",guess_count," guess(es) remaining.")
    guess = input("\n Enter your guess: ")
    # Change to all upper case for better matching
    guess = guess.upper()

    if len(guess) != 5:
      print("That guess was not length 5, try again!\n")
      continue

    if guess == word:
      print(" YOU WIN! \n The word was ", word)
      exit(0)

    else:
      feedback = "*****"
      feedback_count = 0
      # Get a shortlist of shared letters between the guess and the word
      # Check if each character has a match in the string
      letter_pos = 0
      for letter in guess:
        if re.search(letter, word):
          # Add the letter to feedback as lowercase (yellow match = right letter, wrong position)
          feedback = replace_char(letter.lower(), feedback, letter_pos)
          feedback_count += 1
        letter_pos += 1

      # Now check for exact matches, and add to feedback as uppercase (replace yellow matches with green matches)
      char_0 = guess[0] + "...."
      char_1 = "." + guess[1] + "..."
      char_2 = ".." + guess[2] + ".."
      char_3 = "..." + guess[3] + "."
      char_4 = "...." + guess[4]
      # Insert correct letters into feedback, and decrements feedback count
      if re.search(char_0, word):
        feedback = replace_char(guess[0].upper(),feedback,0)
        feedback_count -= 1
      if re.search(char_1, word):
        feedback = replace_char(guess[1].upper(),feedback,1)
        feedback_count -= 1
      if re.search(char_2, word):
        feedback = replace_char(guess[2].upper(),feedback,2)
        feedback_count -= 1
      if re.search(char_3, word):
        feedback = replace_char(guess[3].upper(),feedback,3)
        feedback_count -= 1
      if re.search(char_4, word):
        feedback = replace_char(guess[4].upper(),feedback,4)
        feedback_count -= 1


      list_tuple = update_lists(guessed_letters, guess, remaining_letters)
      guessed_letters = list_tuple[0]
      remaining_letters = list_tuple[1]  
      
      print("\n Feedback: ", feedback," ", feedback_count,"\n")
      if feedback_collection:
        print("Previous feedbacks:", feedback_collection)
      print("Guessed letters: ", guessed_letters)
      print("Letters that have not been used: ", remaining_letters,"\n")

      feedback_collection.append((feedback, feedback_count))
      guess_count -= 1

  # Exceeded guess limit
  print("You have guessed to many times. The word was",word,"\nGood try, thanks for playing!") 
  return

def main():
  url = "https://byjus.com/english/5-letter-words/"

  # Send an HTTP request to fetch the page content
  response = requests.get(url)
  words = []

  # Request page data from url
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search html for the table
    table = soup.find('table', class_ = "table table-bordered")
    if table:
      # Seperate table into each element/word
      for line in table.find_all('span', style="font-weight: 400;"):
        # Append each word into our array
        word = line.get_text()
        words.append(word)
  else:
    print("Error: failed to reach word source website")
    exit(1)

  # Now all words are saved in our array,
  # select a random word for this game
  game_word = select_word(words)
  start_game(game_word)
  return
main()