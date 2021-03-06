Anish Dalal
adalal1@jhu.edu
Assignment 2

The next function will return the next available token until the eof token.
The eof token will be printed out as well. 

Usage:

./sc -s filename.txt

I had to change permissions on sc to run it the first time. You may have 
to do the same. If you get a permission denied error, run

chmod a+x sc

filename.txt is expected to have simple code. if illegal characters are found
an error message will be produced highlighting the illegal character.

This was written in Python 2.7. I wrote a shebang statement in sc specifying
the version so please run it with python 2.7.

Additional Comments:

I made a map of the keywords and symbols from the lists only so that when 
I check if a token is a keyword or symbol I would have constant access time 
checking vs linear checking if I were to search through the keyword list. 
The 2.7 docs show that using the in keyword with a dictionary automatically
hashes the value.

When entering input from stdin (not specifying filename), you need to hit 
enter, and then the eof signal (ctrl+d) for the program to generate a token
list.

When an error within the token parsing class occurs (unclosed comment or 
illegal character), the code prints out the partial list of tokens up to
the position at which the error occurred, the error message, and then exits 
the program. It does not continue parsing. The eof token is only printed if 
no error occurs. All errors except those in sc give the position at which the 
error occurred.

For comments, if a comment is not closed, an error will be printed and the
program will stop parsing. The position given is the position of the most
recently opened comment that has not been closed

all() returns a token list. it does not print tokens.printing occurs in main.
If an error occurs, it will print to stderr in all(), then the partial token
list is printed. In other words, you will see the error printed first, then
the partial token list. I checked with Dr. Froehlich to see if this format is
okay and he said it did not matter if the error was printed before or after
the token list.
