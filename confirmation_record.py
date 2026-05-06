class ConfirmationRecord:
    # This class represents a confirmation receipt that is created after a booking is successfully confirmed

    # Constructor to create a confirmation record object
    def __init__(self, confirmationId, booking, facilityName, location, date, timeSlot, duration, cost):
        # This constructor runs when I create a new confirmation record (like generating a receipt after booking)

        self.confirmationId = confirmationId
        # I store a unique confirmation ID so this record can be identified later

        self.booking = booking
        # I store the booking object itself so I can access all its details when needed

        self.facilityName = facilityName
        # I store the name of the facility (like Study Room A or Court 1)

        self.location = location
        # I store where the facility is located

        self.date = date
        # I store the date of the booking

        self.timeSlot = timeSlot
        # I store the time slot that was booked

        self.duration = duration
        # I store how long the booking lasts

        self.cost = cost
        # I store the final cost of the booking

    def getConfirmationId(self):
        # When I call this, I just want to get the confirmation ID
        return self.confirmationId

    def getBooking(self):
        # This returns the full booking object
        return self.booking

    def getFacilityName(self):
        # This returns the facility name
        return self.facilityName

    def getLocation(self):
        # This returns the location of the facility
        return self.location

    def getDate(self):
        # This returns the booking date
        return self.date

    def getTimeSlot(self):
        # This returns the time slot
        return self.timeSlot

    def getDuration(self):
        # This returns the duration of the booking
        return self.duration

    def getCost(self):
        # This returns the total cost
        return self.cost

    def setConfirmationId(self, confirmationId):
        # If I ever need to change the confirmation ID
        self.confirmationId = confirmationId

    def setBooking(self, booking):
        # If I want to update the booking object linked to this record
        self.booking = booking

    def setFacilityName(self, facilityName):
        # If I want to change the facility name
        self.facilityName = facilityName

    def setLocation(self, location):
        # If I want to change the location
        self.location = location

    def setDate(self, date):
        # If I want to update the date
        self.date = date

    def setTimeSlot(self, timeSlot):
        # If I want to update the time slot
        self.timeSlot = timeSlot

    def setDuration(self, duration):
        # If I want to update how long the booking lasts
        self.duration = duration

    def setCost(self, cost):
        # If I want to update the cost
        self.cost = cost

    def generateRecord(self):
        # This function builds the full receipt text step by step

        return (
            "SMART CAMPUS BOOKING RECEIPT\n"
            # This is the title of the receipt

            "----------------------------------------\n"
            # This is just a line to separate sections visually

            "Confirmation ID: " + str(self.confirmationId) + "\n"
            # I show the confirmation ID

            "Booking ID: " + str(self.booking.getBookingId()) + "\n"
            # I get the booking ID from the booking object

            "User Name: " + self.booking.getUser().getName() + "\n"
            # I go inside the booking → then the user → then get their name

            "Access Type: " + self.booking.getUser().getAccessType().getTypeName() + "\n\n"
            # I also show the user’s access type (Standard or Premium)

            "Facility Details:\n"
            # Section title for facility info

            "Facility Name: " + self.facilityName + "\n"
            # I show the facility name

            "Facility Type: " + self.booking.getFacility().getFacilityType() + "\n"
            # I get the facility type from the facility object

            "Location: " + self.location + "\n"
            # I show where the facility is located

            "Capacity: " + str(self.booking.getFacility().getCapacity()) + "\n\n"
            # I show how many people the facility can hold

            "Booking Details:\n"
            # Section title for booking info

            "Date: " + self.date + "\n"
            # I show the booking date

            "Time Slot: " + str(self.timeSlot) + "\n"
            # I show the time slot

            "Duration: " + str(self.duration) + " hour(s)\n\n"
            # I show how long the booking is

            "Cost Calculation:\n"
            # Section title for cost details

            "Rate: " + str(self.booking.getFacility().getFee()) + " AED/hour\n"
            # I show the hourly rate of the facility

            "Total Cost: " + str(self.cost) + " AED\n\n"
            # I show the final total cost

            "Booking Status: " + self.booking.getStatus() + "\n"
            # I show if the booking is Confirmed or Cancelled

            "----------------------------------------"
            # Ending line for the receipt
        )

    def displayRecord(self):
        # This function is just used to display the receipt
        return self.generateRecord()
        # It calls generateRecord and returns the full receipt text

    def __str__(self):
        # This controls what is shown when I print the object
        return "ConfirmationRecord " + str(self.confirmationId)
        # I return a simple string with the confirmation ID