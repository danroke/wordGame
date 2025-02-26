import requests
from bs4 import BeautifulSoup
import random
import re

def select_word(words):
  size = len(words)
  prompt_num = random.sample(range(0,size),1)
  prompt = words[prompt_num]
  return prompt

def start_game(word):
  r = input("Welcome to Word Game! Would you like an explanation? (y/n):")
  if r == 'y' or 'Y':
    print("\nA random 5 letter word has been selected. It is your job to try to guess this word in 5 guesses or less! After each guess you will be given feedback on how close your guess was.")
    print("If your guess shares no letters with the word the feedback will look like this: ***** 0")
    print("If your guess has a correct letter it will display like this: *A*** 1")
    print("If you match a letter but it is in the wrong position it, the number after the word will display how many letters they share.")
    print("For example if the word is TABLE and you guessed ASSET the feedback would be like this: ***** 3")
    print("I hope that helps, goodluck!\n\n")
  elif r != 'n' or 'N':
    print("Error: invalid response")
    exit(1)
  else:
    # entered n, start game as normal
    guess_count = 5
    while(guess_count > 0):
      guess = input("\n Enter your guess:")
      if guess == word:
        print(" YOU WIN! \n The word was ", word)
      else:
        feedback = ""
        # check position 0
        test_0 = re.search("",guess)
        # check position 1
        test_0 = re.search("",guess)
        # check position 2
        test_0 = re.search("",guess)
        # check position 3
        test_0 = re.search("",guess)
        # check position 4
        test_0 = re.search("",guess)

      
        print("\n Feedback: ", feedback,"\n")
        guess_count -= 1
    # exceeded guess limit
    print("You have guessed to many times. The word was ",word,". Good try, thanks for playing!") 
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
      for line in table.findAll('span', style="font-weight: 400;"):
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