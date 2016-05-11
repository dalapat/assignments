#!/bin/bash

echo "starting test"

echo "test 1"

./sc -s ../compilers4/test2.txt
./sc -c ../compilers4/test2.txt
./sc -t ../compilers4/test2.txt
./sc -a ../compilers4/test2.txt

echo "test 2"

./sc -c ../compilers4/test2.txt > test_cst.txt
echo "diff1"
diff ~/Downloads/random.cst test_cst.txt

./sc -t ../compilers4/test2.txt > test_st.txt
echo "diff2"
diff ~/Downloads/random.st test_st.txt

./sc -a ../compilers4/test2.txt > test_ast.txt
echo "diff3"
diff ~/Downloads/random.ast test_ast.txt

echo "test3"
./sc -a ../compilers4/test.txt
./sc -a ../compilers4/test2.txt
./sc -a test5.txt
./sc -a test6.txt
