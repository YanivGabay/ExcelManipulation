# Title of the Notes

## Date 7/4/24

## Last Updated 09/06/2024

1. Where does the software will be installed?
Answer: on a pc we DONT access to. its a GOV pc.
2. What is the OS of the pc?
3. What is the software?
4. How does we install?
5. is there limitations?premissioins?

## Detailed Notes

### What we currently have

-
-
-

### What still need to be done

- The first part is: we download the excel file (קובץ ידוע פיתוח) with the zip files, than we need to create a text file to the ministry, by a certain formula, and than that file will be uploaded to the ministry. 
- There is the formula on the third col on the file "To Mot Converter" , we need to "fix" the formula, the last number should start at 
- 74 (position 74) and not 78.
  
- so the flow of the TO MOT part should be:
- 1. open the program
- 2. choose TO MOT
- 3. UPLOAD the excel file called מכתב יידוע לפיתוח
- 4. than the program take the neccesary cols (a and k) and create a new text file with the formula , and call it whatever name the user wants or predefined (date to mot etc.) (utf -8 windows crlf)

so the flow of the FROM MOT part should be:

- 1. the user recives a text file from the ministry, and he needs to upload it to the program.
- 2. open the program (the same program)
- 3. choose FROM MOT
- 4. UPLOAD the following files (MUST):
- 4.1 the text file from the ministry (FROM_MOT)
- 4.2 the excel file called מכתב יידוע לפיתוח
- 4.3 CHOOSE THE FOLDER WHERE THE ZIP FILES ARE LOCATED
- 5. we need to extract all the zip files, they will be 1:1 with the excel file מכתב יידוע לפיתוח the first col on that file, will be the names of the zip files
- 6. transfer the data from the text file to the excel file, and create a new excel file with the results, the results should also have the appropriate image name (מספר זיהוי.jpg) .
- 7. and create the excel file with the results.

- 
- translate everything to hebrew!!
- 
- Redesign the program to 2 sections creat a basic screen mockups


## What i need Data
- Process from ministiry, data, New excel file, and New response file. (we will act as the zip files and images acting is the same).
- new data send to ministry, New excel file, New formula results, New response from the given txt file (after the formula).
- 

## For WorkFlow

1. divide the same program into two (inside the same program), one is Send to Ministiry , and the other is Process from ministiry.
2. just uplaod necc files by step (better to guide them) and export the files as needed

