import requests
from bs4 import BeautifulSoup
import random
import re

def toLowerCase(match):
  return match.group(1).lower()

def select_word(words):
  size = len(words)
  prompt_num = random.sample(range(0,size),1)
  prompt = words[prompt_num[0]]
  # convert prompt to all lower case for easier matching
  prompt = prompt.upper()
  return prompt

def replace_char(new_char, word, pos):
  if pos == 0:
    return new_char + word[1:]
  if pos == 4:
    return word[:4] + new_char
  return word[:pos] + new_char + word[pos + 1:]

def letter_search(guess, word):
  correct_letters = []
  for letter in guess:
    if letter in word:
      correct_letters.append(letter)
  return correct_letters
      

def update_lists(guessed_list, word, remainder_list):
  # returns tuple of updated lists
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

  # track used letters
  guessed_letters = []
  remaining_letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  
  # entered n/N, start game as normal
  guess_count = 5
  while(guess_count > 0):
    print("You have",guess_count," guess(es) remaining.")
    guess = input("\n Enter your guess: ")
    # change to all lower for better matching
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
      # get a shortlist of shared letters between the guess and the word
      
      #matches = letter_search(guess, word)
      
      # check if each character has a match in the string
      # check position 0
      if re.search(guess[0],word):
        feedback_count += 1
      # check position 1
      if re.search(guess[1],word):
        feedback_count += 1
      # check position 2
      if re.search(guess[2],word):
        feedback_count += 1
      # check position 3
      if re.search(guess[3],word):
        feedback_count += 1
      # check position 4
      if re.search(guess[4],word):
        feedback_count += 1
      # now check for exact matches, and add to feedback if so
      char_0 = guess[0] + "...."
      char_1 = "." + guess[1] + "..."
      char_2 = ".." + guess[2] + ".."
      char_3 = "..." + guess[3] + "."
      char_4 = "...." + guess[4]

      if re.search(char_0, word):
        feedback = replace_char(guess[0],feedback,0)
        feedback_count -= 1
      if re.search(char_1, word):
        feedback = replace_char(guess[1],feedback,1)
        feedback_count -= 1
      if re.search(char_2, word):
        feedback = replace_char(guess[2],feedback,2)
        feedback_count -= 1
      if re.search(char_3, word):
        feedback = replace_char(guess[3],feedback,3)
        feedback_count -= 1
      if re.search(char_4, word):
        feedback = replace_char(guess[4],feedback,4)
        feedback_count -= 1

      # at this point if the feedback_count != len(matches), there are duplicate letters

      list_tuple = update_lists(guessed_letters, guess, remaining_letters)
      guessed_letters = list_tuple[0]
      remaining_letters = list_tuple[1]  
      print("\n Feedback: ", feedback," ", feedback_count,"\n")
      print("Guessed letters: ", guessed_letters)
      print("\nLetters that have not been used: ", remaining_letters)
      guess_count -= 1

  # exceeded guess limit
  print("You have guessed to many times. The word was",word,"\nGood try, thanks for playing!") 
  return

def main():
  url = "https://byjus.com/english/5-letter-words/"

  # Send an HTTP request to fetch the page content
  response = requests.get(url)
  words = []

  # request page data from url
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # inspect html to find where data we want is stored
    #with open("debug.txt", "w") as file:
    #  file.write(response.text)
    
    # search html for the table
    table = soup.find('table', class_ = "table table-bordered")
    if table:
      # seperate table into each element/word
      for line in table.find_all('span', style="font-weight: 400;"):
        # append each word into our array
        word = line.get_text()
        words.append(word)
  else:
    print("Error: failed to reach word source website")
    exit(1)

  # now all words are saved in our array
  # select a random word for this game
  game_word = select_word(words)
  start_game(game_word)
  return
main()