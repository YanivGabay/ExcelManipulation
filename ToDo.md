## To-Do List

### Task 6: Renaming .jpeg Files
- Big bug with new files
- original formula said address is only 6 digits.
- but in new files its 7 digits, should we push everything 1 forward?
- original formulas gave say 6, need to confirm with gal


### Task 3: Renaming .jpeg Files
- **Description:** Change the name of all .jpeg files to {address-from מכתבי יידוע לפתוח}+"moment".png. Ensure folder names match addresses for easy search. All files should be in the same folder as מכתבי יידוע לפיתוח. Address matching between files from Tahbora and מכתבי ידוע לפיתוח is crucial.
- are folder names is after we seperate 1 from costumer?
- **Status:** Almost finished
- just need to make sure the name
- but its working, currently
- on the same folder as excel file 
- after extracted
- **Due Date:** TBD



### Task 5: Data Adjustments in מכתב יידוע לפיתוח
- **Description:** 
  
    -what is bad dont export
    -what is export despite nothing etc

   - Ensure at least one value in columns L, M, or N; separate entries without values.
   - Mark rows in light blue (still export but highlight) or sign if מיקום דיווח יישוב values are in English in the final output file.
   - Populate columns E-J from the first loaded excel file.
   
- **Status:** Pending
- **Due Date:** TBD

### Task6: Final Formatting and names:
- **Descripition:**
- we need to change the names of the קובץ ידוע פיתוח 
- colms.
- and than also decide which cols to input in the final file
- the first 3 cells in response
- from  תחבורה is the costumer_Id
- who calls the request, the 4 cell is the response type 1 for good
-
-need to change the file name col
- to each record file name of image left
-
-remove empty first col in tree view

- BIG FIX: ID col should be equal to address value from TAHBURA!!!!!!!!

- remove combined_family or FullName
- col its useless
-
  - update: output file with fullname is tottaly valid can change the last name
- names of files:
- output excel file name: '"to_dfus_" + {date.today}' 
- image that left from extracting zip file
- her file name should be: 'Id_moment'



### Completed Task 2: מכתבי יידוע לפיתוח Main Screen
- **Description:** Set מכתבי ייוע לפתיוח as the main screen. Ensure fields are mapped correctly.
- **Completion Date:** 25/1
- **Status:** Finished and working

### Semi Completed Task 5: Data Adjustments in מכתב יידוע לפיתוח
- **Description:** 
    - 1 in all number of offences
    - approval date is date of today
    - Remove the word כביש from Colum N מיקום דיווח כביש.
    - Delete columns AE (kilometer) and AC (barcode).
### Task 4: Final Output Checks Before Sending to Letter Company
- **Description:** Perform cross-checks before the final output: Compare תאריך דיווח from מכתבי יידוע לפיתוח and the ownership date. If the ownership date is newer, exclude from the letter mailing list. Consider removing QR picture and license plate image to avoid issues.
- **Status:** finished,if item has bad tag it wont be exported,get bad tag if newowner
- **Due Date:** TBD
### Notes:

