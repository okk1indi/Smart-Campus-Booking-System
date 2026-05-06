class Booking:
    def __init__(self, bookingId, bookingDate, timeSlot, duration, numberOfParticipants, totalCost, status, user, facility):
        self.bookingId = bookingId
        self.bookingDate = bookingDate
        self.timeSlot = timeSlot
        self.duration = duration
        self.numberOfParticipants = numberOfParticipants
        self.totalCost = totalCost
        self.status = status
        self.user = user
        self.facility = facility
        self.confirmationRecord = None

    # ---------- Getters ----------
    def getBookingId(self):
        return self.bookingId

    def getBookingDate(self):
        return self.bookingDate

    def getTimeSlot(self):
        return self.timeSlot

    def getDuration(self):
        return self.duration

    def getNumberOfParticipants(self):
        return self.numberOfParticipants

    def getTotalCost(self):
        return self.totalCost

    def getStatus(self):
        return self.status

    def getUser(self):
        return self.user

    def getFacility(self):
        return self.facility

    def getConfirmationRecord(self):
        return self.confirmationRecord

    # ---------- Setters ----------
    def setBookingId(self, bookingId):
        self.bookingId = bookingId

    def setBookingDate(self, bookingDate):
        self.bookingDate = bookingDate

    def setTimeSlot(self, timeSlot):
        self.timeSlot = timeSlot

    def setDuration(self, duration):
        self.duration = duration

    def setNumberOfParticipants(self, numberOfParticipants):
        self.numberOfParticipants = numberOfParticipants

    def setTotalCost(self, totalCost):
        self.totalCost = totalCost

    def setStatus(self, status):
        self.status = status

    def setUser(self, user):
        self.user = user

    def setFacility(self, facility):
        self.facility = facility

    def setConfirmationRecord(self, confirmationRecord):
        self.confirmationRecord = confirmationRecord

    # ---------- Logic ----------
    def calculateCost(self):
        self.totalCost = self.facility.calculateFee(self.duration)
        return self.totalCost

    def validateBooking(self):
        if self.duration <= 0:
            return False

        if self.numberOfParticipants <= 0:
            return False

        if self.numberOfParticipants > self.facility.getCapacity():
            return False

        if self.timeSlot not in self.facility.getAvailableTimeSlots():
            return False

        if not self.user.getAccessType().canBook(self.facility.getFacilityType()):
            return False

        return True

    def confirmBooking(self):
        from confirmation_record import ConfirmationRecord

        if not self.validateBooking():
            return None

        self.status = "Confirmed"
        self.calculateCost()

        self.facility.updateAvailability(self.timeSlot, False)

        if len(self.facility.getAvailableTimeSlots()) == 0:
            self.facility.setBookingStatus("Fully Booked")
        else:
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

        return self.confirmationRecord

    def cancelBooking(self):
        self.status = "Cancelled"

        self.facility.updateAvailability(self.timeSlot, True)

        if len(self.facility.getAvailableTimeSlots()) == 0:
            self.facility.setBookingStatus("Fully Booked")
        else:
            self.facility.setBookingStatus("Available")

        return True

    def modifyBooking(self, newDate, newTimeSlot, newDuration, newParticipants):
        oldTimeSlot = self.timeSlot

        self.facility.updateAvailability(oldTimeSlot, True)

        if newDuration <= 0:
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newParticipants <= 0:
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newParticipants > self.facility.getCapacity():
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if newTimeSlot not in self.facility.getAvailableTimeSlots():
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        if not self.user.getAccessType().canBook(self.facility.getFacilityType()):
            self.facility.updateAvailability(oldTimeSlot, False)
            return False

        self.bookingDate = newDate
        self.timeSlot = newTimeSlot
        self.duration = newDuration
        self.numberOfParticipants = newParticipants
        self.calculateCost()

        self.facility.updateAvailability(newTimeSlot, False)

        if len(self.facility.getAvailableTimeSlots()) == 0:
            self.facility.setBookingStatus("Fully Booked")
        else:
            self.facility.setBookingStatus("Available")

        if self.confirmationRecord is not None:
            self.confirmationRecord.setDate(newDate)
            self.confirmationRecord.setTimeSlot(newTimeSlot)
            self.confirmationRecord.setDuration(newDuration)
            self.confirmationRecord.setCost(self.totalCost)

        return True

    def displayBookingDetails(self):
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

    def __str__(self):
        return "Booking " + str(self.bookingId) + " (" + self.status + ")"