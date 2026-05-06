class User:
    # This class represents a user in the system (like a student or staff member)

    def __init__(self, userId, name, email, password, accessType):
        # This constructor runs when I create a new User object

        self.userId = userId
        # I store a unique ID for the user

        self.name = name
        # I store the user's name

        self.email = email
        # I store the user's email (used for login)

        self.password = password
        # I store the user's password

        self.accessType = accessType
        # I store the user's access type (like Standard or Premium)

        self.bookingHistory = []
        # I create an empty list to keep track of all bookings made by this user

    def getUserId(self):
        # This function returns the user's ID
        return self.userId

    def setUserId(self, userId):
        # This function updates the user's ID
        self.userId = userId

    def getName(self):
        # This function returns the user's name
        return self.name

    def setName(self, name):
        # This function updates the user's name
        self.name = name

    def getEmail(self):
        # This function returns the user's email
        return self.email

    def setEmail(self, email):
        # This function updates the user's email
        self.email = email

    def getPassword(self):
        # This function returns the user's password
        return self.password

    def setPassword(self, password):
        # This function updates the user's password
        self.password = password

    def getAccessType(self):
        # This function returns the user's access type object
        return self.accessType

    def setAccessType(self, accessType):
        # This function updates the user's access type
        self.accessType = accessType

    def getBookingHistory(self):
        # This function returns all bookings made by the user
        return self.bookingHistory

    def setBookingHistory(self, bookingHistory):
        # This function replaces the entire booking history list
        self.bookingHistory = bookingHistory

    def createAccount(self, name, email, password, accessType):
        # This function sets up the user's account details

        self.name = name
        # I set the user's name

        self.email = email
        # I set the user's email

        self.password = password
        # I set the user's password

        self.accessType = accessType
        # I assign the access type

    def login(self, email, password):
        # This function checks if the login details are correct

        if self.email == email and self.password == password:
            # I compare the entered email and password with stored values

            return True
            # If both match, login is successful

        return False
        # If not, login fails

    def updateProfile(self, name, email, password):
        # This function allows the user to update their profile info

        self.name = name
        # I update the name

        self.email = email
        # I update the email

        self.password = password
        # I update the password

    def viewBookingHistory(self):
        # This function returns the booking history so the user can view it
        return self.bookingHistory

    def reserveFacility(self, facility, bookingDate, timeSlot, numberOfParticipants):
        # This function tries to reserve a facility

        if self.validateBooking(facility, bookingDate, timeSlot, numberOfParticipants):
            # First, I check if the booking is valid

            return True
            # If valid, I allow reservation (actual booking handled elsewhere)

        return False
        # If not valid, I deny the reservation

    def validateBooking(self, facility, bookingDate, timeSlot, numberOfParticipants):
        # This function checks if the booking request meets all rules

        if numberOfParticipants > facility.getCapacity():
            # I check if the number of people exceeds facility capacity
            return False

        if timeSlot not in facility.getAvailableTimeSlots():
            # I check if the selected time slot is available
            return False

        # FIXED LINE
        if facility.getFacilityType() not in self.accessType.getAllowedFacilityTypes():
            # I check if the user's access type allows booking this type of facility
            return False

        return True
        # If all checks pass, booking is valid

    def upgradeAccess(self, newAccessType):
        # This function upgrades the user's access type (like Standard → Premium)

        self.accessType = newAccessType
        # I replace the old access type with the new one

    def addBooking(self, booking):
        # This function adds a new booking to the user's history

        self.bookingHistory.append(booking)
        # I append the booking object to the list

    def cancelBooking(self, bookingId):
        # This function removes a booking from history using its ID

        for booking in self.bookingHistory:
            # I loop through all bookings

            if booking.getBookingId() == bookingId:
                # I check if this is the booking I want to cancel

                self.bookingHistory.remove(booking)
                # I remove it from the list

                return True
                # I return True to show cancellation worked

        return False
        # If booking not found, return False

    def __str__(self):
        # This controls how the user object is displayed when printed

        return "User: " + self.name + ", Email: " + self.email + ", Access: " + self.accessType.getTypeName()
        # I return a readable string with name, email, and access type