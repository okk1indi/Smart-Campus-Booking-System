from user import User
# I am importing the User class because Administrator will inherit from it

class Administrator(User):
    # This class represents an Admin, and it inherits everything from the User class

    def __init__(self, userId, name, email, password, accessType):
        # This is the constructor for Administrator

        super().__init__(userId, name, email, password, accessType)
        # I am calling the constructor of the parent class (User) to initialize all the user details

    def viewDailyBookings(self, date, bookings):
        # This function is used to view all bookings for a specific date

        dailyBookings = []
        # I create an empty list to store bookings that match the given date

        for booking in bookings:
            # I loop through all bookings in the list

            if booking.getBookingDate() == date:
                # I check if the booking date matches the date given

                dailyBookings.append(booking)
                # If it matches, I add that booking to the dailyBookings list

        return dailyBookings
        # I return the list of bookings for that specific date

    def updateFacilityAvailability(self, facility, timeSlot, status):
        # This function updates the availability of a facility for a specific time slot

        facility.updateAvailability(timeSlot, status)
        # I call the facility's method to update its availability (like making it booked or available)

    def upgradeUserAccess(self, user, accessType):
        # This function upgrades a user's access type (for example from Standard to Premium)

        user.setAccessType(accessType)
        # I update the user's access type using the setter method

    def monitorFacilityUsage(self):
        # This function is used to monitor how facilities are being used

        usageList = []
        # I create an empty list to store usage details

        for booking in self.getBookingHistory():
            # I loop through all bookings made by this admin (inherited from User)

            usageList.append(booking.displayBookingDetails())
            # I get the details of each booking and add it to the usage list

        return usageList
        # I return the list containing all booking usage details

    def viewFacilityStatus(self, facilities):
        # This function returns the list of all facilities and their current status

        return facilities
        # I simply return the facilities list (status is inside each facility object)

    def __str__(self):
        # This function controls how the Admin object is displayed when printed

        return "Admin: " + self.name + ", Email: " + self.email
        # I return a string showing the admin's name and email