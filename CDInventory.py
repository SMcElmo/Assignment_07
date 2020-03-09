#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SMcElmurry, 2020Mar01, Added additional functions, to remove need for code in main body
# SMcElmurry, 2020Mar0X, Updates include adding error exceptions throughtout script,
#                        creation of yes/no function, and read/write capabilities of binary files

# TODone TODO - Use this comment to find completed/to be completed tasks with highlights
#------------------------------------------#



import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    # TODone add functions for processing here
    @staticmethod
    def find_Row(idToFind):
        """Function to locate an ID number in lstTbl. Deletes row if user is using delete option.

        Args:
            idToFind (int): Key ID to locate within lstTbl.

        Returns:
            idkFound (Boolean): True if the row exists in lstTbl.
        """
        if not lstTbl:
            return False
        intRowNr = -1
        idFound = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == idToFind:
                # For deletion
                if strChoice == "d":
                    del lstTbl[intRowNr]
                idFound = True
                break
        return idFound

    @staticmethod
    def check_Duplicate(dupID, dupTitle, dupArtist):
        """Function to check for duplicate entries in lstTbl.

        Args:
            dupID (int): CD ID to be checked.
            dupTitle (string): CD Title to be checked.
            dupArtist (string): CD Artist to be checked.

        Returns:
            idMatch (Boolean): True if the ID exists in lstTbl.
            dupAlbumArtist (Boolean): True if the album/artist pairing exists in lstTbl.
        """
        if not lstTbl:
            return False, False
        dupAlbumArtist = False
        idMatch = DataProcessor.find_Row(dupID) # Returns boolean
        for entryRow in lstTbl:
            if entryRow['Title'] == dupTitle and entryRow['Artist'] == dupArtist:
                dupAlbumArtist = True
                break
        return idMatch, dupAlbumArtist



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table, menuChoice):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Raises:
            FileNotFoundError: If 'file_name' does not exist in local directory

        Returns:
            None.
        """
        try:
            with open(file_name + ".dat", "rb") as objFile:
                table = pickle.load(objFile)
            print("File " + file_name + ".dat loaded.")
        except Exception as e:
            IO.exception_Message(e, file_name + ".dat does not exist. \nChecking for .txt version. \n...\n...\n...")
            try:
                objFile = open(file_name+".txt", 'r')
                table.clear()  # this clears existing data and allows to load data from file
                for line in objFile:
                    data = line.strip().split(',')
                    dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                    table.append(dicRow)
                objFile.close()
                print("File " + file_name + ".txt loaded.")
            except Exception as e:
                if menuChoice == "l" and table:
                    IO.exception_Message(e, "Saved inventory does not exist. Current data not overwritten.")
                elif menuChoice == "l":
                    IO.exception_Message(e, "Saved inventory does not exist, please add CDs to inventory.")
                    table = []
                else:
                    IO.exception_Message(e, "Inventory does not exist. No file loaded.")

    @staticmethod
    def write_file(file_name, table):
        """Function to write data from lstTbl to a .txt file.

        Args:
            file_name (string): name of file used to read the data from.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        objFile = open(strFileName+".dat", 'wb')
        pickle.dump(lstTbl, objFile)
        objFile.close()
        print("File saved.")


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def add_CD(cdID, cdTitle, cdArtist):
        """Function that adds CDs to lstTbl

        Args:
            cdID (int): ID to be added to lstTbl
            cdTitle (string): Album title to be added to lstTbl
            cdArtist (string): Album artist to be added to lstTble

        Returns:
            None
        """
        dicRow = {'ID': cdID, 'Title': cdTitle, 'Artist': cdArtist}
        doubleID, repeatEntry = DataProcessor.check_Duplicate(cdID, cdTitle, cdArtist)
        if repeatEntry:
            print("Album and artist already in library.")
        elif doubleID:
            newID = IO.value_Errors(int, "Unique numeric ID required. \nTo add to library, enter a new ID: ", "Please enter a valid ID Number")
            IO.add_CD(newID, cdTitle, cdArtist)
        else:
            lstTbl.append(dicRow)

    @staticmethod
    def CD_Entry():
        """
        Asks the user for information to add to their inventory

        Args:
            None

        Returns:
            Length 3 tuple with an integer, string, and string.
        """
        intID = IO.value_Errors(int, "Enter an ID number: ", "Entry is not an integer value.")
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return intID, strTitle, stArtist

    @staticmethod
    def yes_No(userYN):
        """
        Evaluates user's answer to a yes/no question. Asks again if answer is not yes(y) or no(n)

        Args:
            userYN (string): User's answer to a yes or no question

        Returns:
            (string) containing either 'y' or 'n'
        """
        while True:
            if userYN == "y" or userYN == "yes":
                return "y"
            elif userYN == "n" or userYN == "no":
                return "n"
            userYN = input("Please choose yes or no (y/n): ")

    @staticmethod
    def exception_Message(exError, exMessage):
        """
        Prints raised exceptions to user
        
        Args:
            exError (Exception): exception raised by the parent function
            exMessage (string): custom colloquial error message for user
        
        Returns:
            None
        """
        print(exError.__class__, exError)
        print(exError.__doc__)
        print(exMessage, "\n")

    @staticmethod
    def value_Errors(newType, userPrompt, errorMessage):
        """
        Checks if user input can be converted to the required data type.
        Displays errors to user if choice is invalid.

        Args:
            newType (data type): data type to convert user input to
            userPrompt (string): question to ask to user
            errorMessage (string): custom colloquial error message for user

        Raises:
            ValueError: if user input cannot be converted to declared data type

        Returns:
            Converted user value to new data type
        """
        while True:
            try:
                new_value = newType(input(userPrompt))
                return new_value
            except Exception as e:
                IO.exception_Message(e, errorMessage)


# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl, "")
if lstTbl:
    IO.show_inventory(lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        if lstTbl:
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.', end=' ')
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
            if IO.yes_No(strYesNo.lower()) == 'y':
                print('reloading...\n')
                FileProcessor.read_file(strFileName, lstTbl, strChoice)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
        else:
            FileProcessor.read_file(strFileName, lstTbl, strChoice)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # TODone move IO code into function
        intID, strTitle, stArtist = IO.CD_Entry()
        # 3.3.2 Add item to the table
        # TODone move processing code into function (Note: moved portion that adds CD to IO due to new user questions)
        DataProcessor.check_Duplicate(intID, strTitle, stArtist)
        IO.add_CD(intID, strTitle, stArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        intIDDel = IO.value_Errors(int, "Which ID would you like to deleted? ", "Please enter an integer value. ")
        # 3.5.2 search thru table and delete CD
        # TODone move processing code into function
        blnCDRemoved = DataProcessor.find_Row(intIDDel)
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if IO.yes_No(strYesNo) == 'y':
            # 3.6.2.1 save data
            # TODone move processing code into function
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




