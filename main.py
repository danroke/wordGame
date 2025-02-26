import requests
from bs4 import BeautifulSoup
import random
import re

def select_word(words):
  size = len(words)
  prompt_num = random.sample(range(0,size),1)
  prompt = words[prompt_num[0]]
  print("before:",prompt)
  # convert prompt to all lower case for easier matching
  #prompt = re.sub(r'([A-Z])\1',lambda pat: pat.group(1).lower(), prompt)
  callback = lambda pattern: pattern.group(1).lower()
  re.sub(r'([A-Z])\1',callback, prompt)
  print("after:",prompt)
  return prompt

def replace_char(new_char, word, pos):
  if pos == 0:
    return new_char + word[1:]
  if pos == 4:
    return word[:3] + new_char
  return word[:pos] + new_char + word[pos + 1:]

def start_game(word):
  explain = input("Welcome to Word Game! Would you like an explanation? (y/n):")
  if explain == ('y' or 'Y'):
    print("\nA random 5 letter word has been selected. It is your job to try to guess this word in 5 guesses or less! After each guess you will be given feedback on how close your guess was.")
    print("If your guess shares no letters with the word the feedback will look like this: ***** 0")
    print("If your guess has a correct letter it will display like this: *A*** 1")
    print("If you match a letter but it is in the wrong position it, the number after the word will display how many letters they share.")
    print("For example if the word is TABLE and you guessed ASSET the feedback would be like this: ***** 3")
    print("I hope that helps, goodluck!\n\n")
  elif explain != ('n' or 'N' or 'y' or 'Y'):
    print("Error: invalid response")
    exit(1)
  
  # entered n/N, start game as normal
  guess_count = 5
  while(guess_count > 0):
    ### for debugging , PLEASE REMOVE
    print("~~ ",word," ~~")
    ###
    print("You have",guess_count," guess(es) remaining.")
    guess = input("\n Enter your guess: ")
    if len(guess) != 5:
      print("That guess was not length 5, try again!\n")
      continue

    if guess == word:
      print(" YOU WIN! \n The word was ", word)
      exit(0)

    else:
      feedback = "*****"
      feedback_count = 0
      # firstly, check if each character has a match in the string
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
      if re.search(char_1, word):
        feedback = replace_char(guess[1],feedback,1)
      if re.search(char_2, word):
        feedback = replace_char(guess[2],feedback,2)
      if re.search(char_3, word):
        feedback = replace_char(guess[3],feedback,3)
      if re.search(char_4, feedback):
        feedback = replace_char(guess[4],feedback,4)
        
      print("\n Feedback: ", feedback," ", feedback_count,"\n")
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