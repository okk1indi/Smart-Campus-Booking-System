from user import User


class Administrator(User):

    def __init__(self, userId, name, email, password, accessType):
        super().__init__(userId, name, email, password, accessType)

    def viewDailyBookings(self, date, bookings):
        dailyBookings = []

        for booking in bookings:
            if booking.getBookingDate() == date:
                dailyBookings.append(booking)

        return dailyBookings

    def updateFacilityAvailability(self, facility, timeSlot, status):
        facility.updateAvailability(timeSlot, status)

    def upgradeUserAccess(self, user, accessType):
        user.setAccessType(accessType)

    def monitorFacilityUsage(self):
        usageList = []

        for booking in self.getBookingHistory():
            usageList.append(booking.displayBookingDetails())

        return usageList

    def viewFacilityStatus(self, facilities):
        return facilities

    def __str__(self):
        return "Admin: " + self.name + ", Email: " + self.email