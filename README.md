
# wordGame

This project is a wordle like game clone I made in python. \
Please make sure to run the following commands before executing the main.py:

* pip install requests
* pip install BeautifulSoup4

## Explanation

A random 5 letter word has been selected. It is your job to try to guess this word in 5 guesses or less! After each guess you will be given feedback on how close your guess was.\
If your guess shares no letters with the word the feedback will look like this: * * * * * 0\
If your guess has a correct letter it will display like this: * A * * * 0\
If you match a letter but it is in the wrong position it, the number after the word will display how many letters they share.\
For example, if the word is TABLE and you guessed ASSET the feedback would be like this: * * * * * 3 \
Another example, if the word is TABLE and you guessed TRADE the feedback would be like this: T * * * E 1 \
I hope that helps, goodluck!

### Issues

Double letters cause in a solution word can cause some oddities in hints.\
eg. The word is "BUILT". You guessed "STILT". The feedback will be "**ILT 1" due the first T matching to the T at the end of the word.
