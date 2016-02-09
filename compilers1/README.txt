Anish Dalal
adalal1@jhu.edu
Compilers and Interpreters Spring 2016
Assignment 1

For this problem, I needed to learn some basics of IO as I had not really encountered IO specific issues in class nor in any internships. I have not really reviewed IO even though it's such a fundamental topic. I needed to know the syntax of how to read in from stdin in each of the languages, but also make sure that what I am reading in bytes. Subsequently, I needed to learn the syntax for writing to stdout as a byte array.

I decided to use Python, Java, and Julia. 
 
Python - I chose python primarily because I am most familiar with it, and hence did not need to spend time looking up syntax rules. Also, reading from stdin and writing stdout was trivial

Java - I chose Java because I am familiar with it but I had not coded in it for quite some time so I wanted to make sure I had not forgotten all of it. 

Julia - This was the most pythonic language next to python and was also quite trivial to read from stdin and write to stdout. However though I tested my code with several inputs I am still not entirely sure if it works because this is my first time writing in Julia.  

I will be using Python 2.7 for the rest of the course. 

To build: You will need python 2.7, java, and julia installed. I tested my programs as follows:

$ cat inputfile.jpg | python cat.py > outputfile.jpg

$ cat input.jpg | java Cat > outputfile.jpg

$ cat input.jpg | julia cat.jl > outputfile.jpg 

