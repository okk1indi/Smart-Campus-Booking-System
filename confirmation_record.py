class ConfirmationRecord:
    # Constructor to create a confirmation record object
    def __init__(self, confirmationId, booking, facilityName, location, date, timeSlot, duration, cost):
        self.confirmationId = confirmationId
        self.booking = booking
        self.facilityName = facilityName
        self.location = location
        self.date = date
        self.timeSlot = timeSlot
        self.duration = duration
        self.cost = cost

    # Getters
    def getConfirmationId(self):
        return self.confirmationId

    def getBooking(self):
        return self.booking

    def getFacilityName(self):
        return self.facilityName

    def getLocation(self):
        return self.location

    def getDate(self):
        return self.date

    def getTimeSlot(self):
        return self.timeSlot

    def getDuration(self):
        return self.duration

    def getCost(self):
        return self.cost

    # Setters
    def setConfirmationId(self, confirmationId):
        self.confirmationId = confirmationId

    def setBooking(self, booking):
        self.booking = booking

    def setFacilityName(self, facilityName):
        self.facilityName = facilityName

    def setLocation(self, location):
        self.location = location

    def setDate(self, date):
        self.date = date

    def setTimeSlot(self, timeSlot):
        self.timeSlot = timeSlot

    def setDuration(self, duration):
        self.duration = duration

    def setCost(self, cost):
        self.cost = cost

    # Generate confirmation receipt details
    def generateRecord(self):
        return (
            "SMART CAMPUS BOOKING RECEIPT\n"
            "----------------------------------------\n"
            "Confirmation ID: " + str(self.confirmationId) + "\n"
            "Booking ID: " + str(self.booking.getBookingId()) + "\n"
            "User Name: " + self.booking.getUser().getName() + "\n"
            "Access Type: " + self.booking.getUser().getAccessType().getTypeName() + "\n\n"
            "Facility Details:\n"
            "Facility Name: " + self.facilityName + "\n"
            "Facility Type: " + self.booking.getFacility().getFacilityType() + "\n"
            "Location: " + self.location + "\n"
            "Capacity: " + str(self.booking.getFacility().getCapacity()) + "\n\n"
            "Booking Details:\n"
            "Date: " + self.date + "\n"
            "Time Slot: " + str(self.timeSlot) + "\n"
            "Duration: " + str(self.duration) + " hour(s)\n\n"
            "Cost Calculation:\n"
            "Rate: " + str(self.booking.getFacility().getFee()) + " AED/hour\n"
            "Total Cost: " + str(self.cost) + " AED\n\n"
            "Booking Status: " + self.booking.getStatus() + "\n"
            "----------------------------------------"
        )

    # Display confirmation record
    def displayRecord(self):
        return self.generateRecord()

    def __str__(self):
        return "ConfirmationRecord " + str(self.confirmationId)