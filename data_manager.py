import pickle   # used to save/load data in binary files

class DataManager:
    def __init__(self, usersFile, facilitiesFile, bookingsFile, confirmationRecordsFile):
        self.usersFile = usersFile
        self.facilitiesFile = facilitiesFile
        self.bookingsFile = bookingsFile
        self.confirmationRecordsFile = confirmationRecordsFile

    # ---------- Save Methods ----------
    def saveUsers(self, users):
        with open(self.usersFile, "wb") as file:
            pickle.dump(users, file)

    def saveFacilities(self, facilities):
        with open(self.facilitiesFile, "wb") as file:
            pickle.dump(facilities, file)

    def saveBookings(self, bookings):
        with open(self.bookingsFile, "wb") as file:
            pickle.dump(bookings, file)

    def saveConfirmationRecords(self, records):
        with open(self.confirmationRecordsFile, "wb") as file:
            pickle.dump(records, file)

    # ---------- Load Methods ----------
    def loadUsers(self):
        try:
            with open(self.usersFile, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return []

    def loadFacilities(self):
        try:
            with open(self.facilitiesFile, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return []

    def loadBookings(self):
        try:
            with open(self.bookingsFile, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return []

    def loadConfirmationRecords(self):
        try:
            with open(self.confirmationRecordsFile, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            return []