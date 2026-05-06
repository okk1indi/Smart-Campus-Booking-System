import pickle   # used to save/load data in binary files
# I am importing pickle because it helps me store data (like users, bookings, etc.) into files and load them back later

class DataManager:
    # This class is responsible for handling all saving and loading of data in my system

    def __init__(self, usersFile, facilitiesFile, bookingsFile, confirmationRecordsFile):
        # This constructor runs when I create a DataManager object

        self.usersFile = usersFile
        # I store the file name where user data will be saved

        self.facilitiesFile = facilitiesFile
        # I store the file name where facilities data will be saved

        self.bookingsFile = bookingsFile
        # I store the file name where bookings data will be saved

        self.confirmationRecordsFile = confirmationRecordsFile
        # I store the file name where confirmation records will be saved

    def saveUsers(self, users):
        # This function is used when I want to save all users into a file

        with open(self.usersFile, "wb") as file:
            # I open the users file in write-binary mode ("wb") so I can store data

            pickle.dump(users, file)
            # I use pickle to convert the users list into a binary format and save it in the file

    def saveFacilities(self, facilities):
        # This function saves all facilities into a file

        with open(self.facilitiesFile, "wb") as file:
            # I open the facilities file in write-binary mode

            pickle.dump(facilities, file)
            # I store the facilities list inside the file

    def saveBookings(self, bookings):
        # This function saves all bookings into a file

        with open(self.bookingsFile, "wb") as file:
            # I open the bookings file in write-binary mode

            pickle.dump(bookings, file)
            # I save the bookings list into the file

    def saveConfirmationRecords(self, records):
        # This function saves all confirmation records into a file

        with open(self.confirmationRecordsFile, "wb") as file:
            # I open the confirmation records file in write-binary mode

            pickle.dump(records, file)
            # I save the records into the file

    def loadUsers(self):
        # This function is used when I want to load users from the file

        try:
            # I try to open and read the file safely

            with open(self.usersFile, "rb") as file:
                # I open the users file in read-binary mode ("rb")

                return pickle.load(file)
                # I use pickle to read the data and convert it back into Python objects (list of users)

        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # If something goes wrong (file not found, empty file, or corrupted file)

            return []
            # I return an empty list so the program doesn't crash

    def loadFacilities(self):
        # This function loads facilities from the file

        try:
            # I try to safely read the file

            with open(self.facilitiesFile, "rb") as file:
                # I open the facilities file in read-binary mode

                return pickle.load(file)
                # I load and return the facilities list

        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # If there is any error

            return []
            # I return an empty list instead

    def loadBookings(self):
        # This function loads bookings from the file

        try:
            # I try to safely read the file

            with open(self.bookingsFile, "rb") as file:
                # I open the bookings file in read-binary mode

                return pickle.load(file)
                # I load and return the bookings list

        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # If something goes wrong

            return []
            # I return an empty list

    def loadConfirmationRecords(self):
        # This function loads confirmation records from the file

        try:
            # I try to safely read the file

            with open(self.confirmationRecordsFile, "rb") as file:
                # I open the confirmation records file in read-binary mode

                return pickle.load(file)
                # I load and return the records list

        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            # If any error happens

            return []
            # I return an empty list so the system keeps running