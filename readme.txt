OwnBackup home assignment - Marcelo Gitelman


1. Instructions

This .zip contains the following files:
readme.txt => this file
csvcompare.py => Python source code of the application
csvcompare.exe => Executable file
                  To execute, type csvcompare path1\file1.csv path2\file2.csv, where file1.csv and file2.csv are the names of the files to compare
                  If you don't enter the arguments, the program will ask you to input them
*.csv files => files used to test the application

In the source file, I left the code of the unit tests guided by the list in item 4.


2. My assumptions:

2.1 - About large files: since the Python CSV reader reads the file line by line, it can deal with large files. In a real case, I would check the application specification (or ask the client) and test with the largest possible file to ensure that it works correctly. If a problem appeared, I would use another library such as Pandas.

3. If it was released as a production code I would add it to a VCS repository to keep track of changes and enable collaboration, I would write documentation explaining its usage, specifications, and limitations, and write test documentation concerning the list in item 4 and a test report with the results. 
     A feature that could be added is customizing the separators.
     If it was intended for a final user, it could also generate a git-like report with the differences between the files with different colors for deleted, added, or changed.

4. My test is based on checking the following list:

Errors/Validation:
4.1 file1 and/or file2 has invalid path
4.2 file1 and/or file2 inexistent
4.3 user without privilege to read file1 and/or file2
4.4 file1 and/or file2 is not a valid .csv
4.5 file1 and file2 headers are not equal
4.6 file1 and/or file2 ID is not a number
4.7 file1 and/or file2 ID is not sorted
4.8 file1 and/or file2 field structure is different from expected based on the headers
4.9 file1 and/or file2 with some problem in the middle of the file (corrupted)

Test cases:
4.10 IDs in file1 greater than the biggest ID of file2
4.11 IDs in file1 smaller than the smallest ID of file2
4.12 IDs in file1 in the middle of the boundaries IDs of file2
4.13 IDs in file2 greater than the biggest ID of file1
4.14 IDs in file2 smaller than the smallest ID of file1
4.15 IDs in file2 in the middle of the boundaries IDs of file1
4.16 file1 with more records than file2
4.17 file2 with more records than file1
4.18 test first record of file1 in every situation: added, changed, not changed(same ID and equal fields)
4.19 test last record of file1 in every situation: added, changed, not changed
4.20 test first record of file2 in every situation: deleted, changed, not changed
4.21 test last record of file2 in every situation: deleted, changed, not changed
4.22 Test the following sequence of operations
added - deleted - changed
added - changed - deleted
deleted - added - changed
deleted - changed - added
changed - deleted - added
changed - added - deleted
I used the files combinations.csv and combinations2.csv to test these sequences:
The operations that occurred were the following ( where a=add, d=delete, c=change): 
a1 d4 c5 | a8 c10 d11 | d16 d17 d18 a19 c22 | d23 d24 c28 a31 | c35 d36 a37 | c40 a45 d50
(added ID1, then deleted ID4 and so on...)
(the | characters are just to make it clearer - please ignore them)

4.23 Add the not changed to the test in item 4.22 (Not implemented)
added - deleted - changed - not changed
added - deleted - not changed - changed
added - changed - deleted - not changed
added - changed - not changed - deleted
added - not changed - deleted - changed
added - not changed - changed - deleted
deleted - added - changed - not changed
deleted - added - not changed - changed
deleted - changed - added - not changed
deleted - changed - not changed - added
deleted - not changed - added - changed
deleted - not changed - changed - added
changed - added - deleted - not changed
changed - added - not changed - deleted
changed - deleted - added - not changed
changed - deleted - not changed - added
changed - not changed - deleted - added
changed - not changed - added - deleted

4.24 Analysing the code, we see that there is a decision point when the ID of file2 is smaller than the ID of file1. In this case, we have some other decisions to make. I consider it important to test 3 cases:
1. When ID2 < ID1 and after some records of file2 we have the same ID of ID1 and the rest of the record did not change
2. When ID2 < ID1 and after some records of file2 we have the same ID of ID1 and the rest of the record did change
3. When ID2 < ID1 and after some records of file2 we have an ID2 bigger than ID1
I implemented this test with the files smaller1.csv and smaller2.csv






