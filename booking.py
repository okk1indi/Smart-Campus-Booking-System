class Booking:
    # This class represents a full booking process, like when a student books a study room or court

    def __init__(self, bookingId, bookingDate, timeSlot, duration, numberOfParticipants, totalCost, status, user, facility):
        # This constructor runs the moment I create a new booking object

        self.bookingId = bookingId
        # First thing I do is store a unique ID so I can identify this booking later

        self.bookingDate = bookingDate
        # I store the exact date the user wants to book the facility

        self.timeSlot = timeSlot
        # I store the specific time slot (for example 10:00–12:00)

        self.duration = duration
        # I store how long the booking will last (like 2 hours)

        self.numberOfParticipants = numberOfParticipants
        # I store how many people will attend this booking

        self.totalCost = totalCost
        # I store the cost, even though it might be recalculated later

        self.status = status
        # I store the current status (maybe "Pending", "Confirmed", or "Cancelled")

        self.user = user
        # I store which user made this booking

        self.facility = facility
        # I store which facility is being booked (like StudyRoom or SportsCourt)

        self.confirmationRecord = None
        # At the beginning, there is no confirmation record yet because booking is not confirmed

    def getBookingId(self):
        # When I call this, I just want to know the booking ID
        return self.bookingId

    def getBookingDate(self):
        # This returns the date of the booking
        return self.bookingDate

    def getTimeSlot(self):
        # This returns the time slot chosen
        return self.timeSlot

    def getDuration(self):
        # This returns how long the booking is
        return self.duration

    def getNumberOfParticipants(self):
        # This returns how many people are attending
        return self.numberOfParticipants

    def getTotalCost(self):
        # This returns the total cost of the booking
        return self.totalCost

    def getStatus(self):
        # This returns the current status of the booking
        return self.status

    def getUser(self):
        # This returns the user who made the booking
        return self.user

    def getFacility(self):
        # This returns the facility being booked
        return self.facility

    def getConfirmationRecord(self):
        # This returns the confirmation record if it exists
        return self.confirmationRecord

    def setBookingId(self, bookingId):
        # If I want to change the booking ID, I use this
        self.bookingId = bookingId

    def setBookingDate(self, bookingDate):
        # If I want to update the booking date, I use this
        self.bookingDate = bookingDate

    def setTimeSlot(self, timeSlot):
        # If I want to change the time slot, I use this
        self.timeSlot = timeSlot

    def setDuration(self, duration):
        # If I want to change how long the booking is
        self.duration = duration

    def setNumberOfParticipants(self, numberOfParticipants):
        # If I want to update how many people are coming
        self.numberOfParticipants = numberOfParticipants

    def setTotalCost(self, totalCost):
        # If I want to manually update the cost
        self.totalCost = totalCost

    def setStatus(self, status):
        # If I want to change the booking status (like cancelling it)
        self.status = status

    def setUser(self, user):
        # If I want to change which user owns this booking
        self.user = user

    def setFacility(self, facility):
        # If I want to change the facility for some reason
        self.facility = facility

    def setConfirmationRecord(self, confirmationRecord):
        # Once booking is confirmed, I attach a confirmation record here
        self.confirmationRecord = confirmationRecord

    def calculateCost(self):
        # Here I calculate the cost of the booking based on the facility rules

        self.totalCost = self.facility.calculateFee(self.duration)
        # I ask the facility: "Based on this duration, how much should I charge?"

        return self.totalCost
        # Then I return the updated cost

    def validateBooking(self):
        # Before confirming, I go through a checklist to make sure everything is valid

        if self.duration <= 0:
            # First, I check if duration even makes sense (it can't be 0 or negative)
            return False

        if self.numberOfParticipants <= 0:
            # Then I check if there are participants (can't have 0 people)
            return False

        if self.numberOfParticipants > self.facility.getCapacity():
            # I make sure the facility can handle that many people
            return False

        if self.timeSlot not in self.facility.getAvailableTimeSlots():
            # I check if the time slot is actually available
            return False

        if not self.user.getAccessType().canBook(self.facility.getFacilityType()):
            # I check if the user is even allowed to book this type of facility
            return False

        return True
        # If everything passed, then booking is valid

    def confirmBooking(self):
        # This is where the actual booking confirmation happens

        from confirmation_record import ConfirmationRecord
        # I import the ConfirmationRecord class to create a record

        if not self.validateBooking():
            # If something is wrong, I stop immediately
            return None

        self.status = "Confirmed"
        # I change the status to Confirmed

        self.calculateCost()
        # I calculate the final cost

        self.facility.updateAvailability(self.timeSlot, False)
        # I mark this time slot as no longer available

        if len(self.facility.getAvailableTimeSlots()) == 0:
            # If no time slots are left, facility is fully booked
            self.facility.setBookingStatus("Fully Booked")
        else:
            # Otherwise, it's still available
            self.facility.setBookingStatus("Available")

        self.confirmationRecord = ConfirmationRecord(
            self.bookingId,
            self,
            self.facility.getName(),
            self.facility.getLocation(),
            self.bookingDate,
            self.timeSlot,
            self.duration,
            self.totalCost
        )
        # I create a confirmation record with all details, like a receipt

        return self.confirmationRecord
        # I return the confirmation record to show booking was successful

    def cancelBooking(self):
        # This is what happens when a user cancels a booking

        self.status = "Cancelled"
        # I change the status to Cancelled

        self.facility.updateAvailability(self.timeSlot, True)
        # I free up the time slot again so others can book it

        if len(self.facility.getAvailableTimeSlots()) == 0:
            self.facility.setBookingStatus("Fully Booked")
        else:
            self.facility.setBookingStatus("Available")

        return True
        # I return True to show cancellation worked

    def modifyBooking(self, newDate, newTimeSlot, newDuration, newParticipants):
        # This is used when a user wants to change their booking

        oldTimeSlot = self.timeSlot
        # I save the old time slot so I can free it temporarily

        self.facility.updateAvailability(oldTimeSlot, True)
        # I make the old slot available again

        if newDuration <= 0:
            # I check if the new duration is valid
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newParticipants <= 0:
            # I check if participants are valid
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newParticipants > self.facility.getCapacity():
            # I check capacity again
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newTimeSlot not in self.facility.getAvailableTimeSlots():
            # I check if new slot is available
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if not self.user.getAccessType().canBook(self.facility.getFacilityType()):
            # I check access permissions again
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        self.bookingDate = newDate
        # I update the date

        self.timeSlot = newTimeSlot
        # I update the time slot

        self.duration = newDuration
        # I update the duration

        self.numberOfParticipants = newParticipants
        # I update participants

        self.calculateCost()
        # I recalculate cost

        self.facility.updateAvailability(newTimeSlot, False)
        # I reserve the new slot

        if len(self.facility.getAvailableTimeSlots()) == 0:
            self.facility.setBookingStatus("Fully Booked")
        else:
            self.facility.setBookingStatus("Available")

        if self.confirmationRecord is not None:
            # If there was already a confirmation, I update it too
            self.confirmationRecord.setDate(newDate)
            self.confirmationRecord.setTimeSlot(newTimeSlot)
            self.confirmationRecord.setDuration(newDuration)
            self.confirmationRecord.setCost(self.totalCost)

        return True
        # I return True to show modification worked

    def displayBookingDetails(self):
        # This function is like printing a summary of the booking

        return (
            "Booking ID: " + str(self.bookingId) +
            ", Date: " + self.bookingDate +
            ", Time: " + str(self.timeSlot) +
            ", Duration: " + str(self.duration) +
            ", Participants: " + str(self.numberOfParticipants) +
            ", Facility: " + self.facility.getName() +
            ", Cost: " + str(self.totalCost) + " AED" +
            ", Status: " + self.status
        )
        # I combine everything into one readable sentence

    def __str__(self):
        # This is what shows when I print the booking object
        return "Booking " + str(self.bookingId) + " (" + self.status + ")"