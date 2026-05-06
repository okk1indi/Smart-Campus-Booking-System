class User:

    def __init__(self, userId, name, email, password, accessType):
        self.userId = userId
        self.name = name
        self.email = email
        self.password = password
        self.accessType = accessType
        self.bookingHistory = []

    def getUserId(self):
        return self.userId

    def setUserId(self, userId):
        self.userId = userId

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def getAccessType(self):
        return self.accessType

    def setAccessType(self, accessType):
        self.accessType = accessType

    def getBookingHistory(self):
        return self.bookingHistory

    def setBookingHistory(self, bookingHistory):
        self.bookingHistory = bookingHistory

    def createAccount(self, name, email, password, accessType):
        self.name = name
        self.email = email
        self.password = password
        self.accessType = accessType

    def login(self, email, password):
        if self.email == email and self.password == password:
            return True
        return False

    def updateProfile(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def viewBookingHistory(self):
        return self.bookingHistory

    def reserveFacility(self, facility, bookingDate, timeSlot, numberOfParticipants):
        if self.validateBooking(facility, bookingDate, timeSlot, numberOfParticipants):
            return True
        return False

    def validateBooking(self, facility, bookingDate, timeSlot, numberOfParticipants):

        if numberOfParticipants > facility.getCapacity():
            return False

        if timeSlot not in facility.getAvailableTimeSlots():
            return False

        # FIXED LINE
        if facility.getFacilityType() not in self.accessType.getAllowedFacilityTypes():
            return False

        return True

    def upgradeAccess(self, newAccessType):
        self.accessType = newAccessType

    def addBooking(self, booking):
        self.bookingHistory.append(booking)

    def cancelBooking(self, bookingId):
        for booking in self.bookingHistory:
            if booking.getBookingId() == bookingId:
                self.bookingHistory.remove(booking)
                return True
        return False

    def __str__(self):
        return "User: " + self.name + ", Email: " + self.email + ", Access: " + self.accessType.getTypeName()