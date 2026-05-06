class Facility:
    # This class represents a general facility (like study room, sports court, or event hall)

    # Constructor to create a facility object
    def __init__(self, facilityId, name, facilityType, location, capacity, availableTimeSlots, bookingStatus, fee):
        # This runs when I create a new facility

        self.facilityId = facilityId
        # I store a unique ID for this facility

        self.name = name
        # I store the name of the facility (like Room A or Court 1)

        self.facilityType = facilityType
        # I store the type (StudyRoom, SportCourt, EventHall)

        self.location = location
        # I store where the facility is located

        self.capacity = capacity
        # I store how many people this facility can handle

        self.availableTimeSlots = availableTimeSlots
        # I store a list of all available time slots

        self.bookingStatus = bookingStatus
        # I store whether the facility is Available or Fully Booked

        self.fee = fee
        # I store the cost per hour for using this facility

    def getFacilityId(self):
        # This returns the facility ID
        return self.facilityId

    def getName(self):
        # This returns the facility name
        return self.name

    def getFacilityType(self):
        # This returns the facility type
        return self.facilityType

    def getLocation(self):
        # This returns the location
        return self.location

    def getCapacity(self):
        # This returns the capacity
        return self.capacity

    def getAvailableTimeSlots(self):
        # This returns all available time slots
        return self.availableTimeSlots

    def getBookingStatus(self):
        # This returns the current booking status
        return self.bookingStatus

    def getFee(self):
        # This returns the hourly fee
        return self.fee

    def setFacilityId(self, facilityId):
        # This updates the facility ID
        self.facilityId = facilityId

    def setName(self, name):
        # This updates the facility name
        self.name = name

    def setFacilityType(self, facilityType):
        # This updates the facility type
        self.facilityType = facilityType

    def setLocation(self, location):
        # This updates the location
        self.location = location

    def setCapacity(self, capacity):
        # This updates the capacity
        self.capacity = capacity

    def setAvailableTimeSlots(self, availableTimeSlots):
        # This replaces the entire list of available time slots
        self.availableTimeSlots = availableTimeSlots

    def setBookingStatus(self, bookingStatus):
        # This updates whether the facility is Available or Fully Booked
        self.bookingStatus = bookingStatus

    def setFee(self, fee):
        # This updates the hourly fee
        self.fee = fee

    def displayDetails(self):
        # This function builds a full description of the facility as a string

        return ("Facility: " + self.name +
                # I show the facility name

                ", Type: " + self.facilityType +
                # I show the type of facility

                ", Location: " + self.location +
                # I show where it is located

                ", Capacity: " + str(self.capacity) +
                # I show how many people it can hold

                ", Status: " + self.bookingStatus +
                # I show if it is available or fully booked

                ", Available Slots: " + str(self.availableTimeSlots) +
                # I show all available time slots

                ", Fee: " + str(self.fee) + " AED/hour")
                # I show the hourly fee

    def checkAvailability(self, timeSlot):
        # This function checks if a specific time slot is available

        return timeSlot in self.availableTimeSlots
        # If the time slot is in the list, it returns True, otherwise False

    def updateAvailability(self, timeSlot, status):
        # This function either adds or removes a time slot depending on status

        if status == True:
            # If status is True, it means I want to make the slot available

            if timeSlot not in self.availableTimeSlots:
                # I check if the slot is not already in the list

                self.availableTimeSlots.append(timeSlot)
                # If not, I add it back

            self.bookingStatus = "Available"
            # I update the status to Available

        else:
            # If status is False, it means the slot is being booked

            if timeSlot in self.availableTimeSlots:
                # I check if the slot exists

                self.availableTimeSlots.remove(timeSlot)
                # I remove it because it's now booked

            if len(self.availableTimeSlots) == 0:
                # If no slots left

                self.bookingStatus = "Fully Booked"
                # I mark the facility as fully booked

    def calculateFee(self, duration):
        # This function calculates total cost based on duration

        return self.fee * duration
        # I multiply hourly fee by number of hours

    def __str__(self):
        # This controls how the object looks when printed

        return "Facility: " + self.name + " (" + self.facilityType + ")"
        # I return a simple readable format


class StudyRoom(Facility):
    # StudyRoom inherits everything from Facility

    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, numberOfTables):
        # This constructor runs when I create a StudyRoom

        super().__init__(facilityId, name, "StudyRoom", location, capacity, availableTimeSlots, bookingStatus, fee)
        # I call the parent constructor and automatically set type to "StudyRoom"

        self.numberOfTables = numberOfTables
        # I store how many tables are inside the room

    def getNumberOfTables(self):
        # This returns number of tables
        return self.numberOfTables

    def setNumberOfTables(self, numberOfTables):
        # This updates number of tables
        self.numberOfTables = numberOfTables

    def displayDetails(self):
        # I extend the parent display by adding tables info
        return super().displayDetails() + ", Tables: " + str(self.numberOfTables)

    def __str__(self):
        # This controls how StudyRoom prints
        return "StudyRoom: " + self.name


class SportCourt(Facility):
    # SportCourt also inherits from Facility

    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, sportType):
        # This constructor runs when I create a SportCourt

        super().__init__(facilityId, name, "SportCourt", location, capacity, availableTimeSlots, bookingStatus, fee)
        # I set the type automatically to SportCourt

        self.sportType = sportType
        # I store what sport this court is for (like Basketball, Tennis)

    def getSportType(self):
        # This returns the sport type
        return self.sportType

    def setSportType(self, sportType):
        # This updates the sport type
        self.sportType = sportType

    def displayDetails(self):
        # I extend display to include sport type
        return super().displayDetails() + ", Sport: " + self.sportType

    def __str__(self):
        # This controls print output
        return "SportCourt: " + self.name


class EventHall(Facility):
    # EventHall also inherits from Facility

    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, hasAudioSystem):
        # This constructor runs when I create an EventHall

        super().__init__(facilityId, name, "EventHall", location, capacity, availableTimeSlots, bookingStatus, fee)
        # I set type automatically to EventHall

        self.hasAudioSystem = hasAudioSystem
        # I store whether this hall has an audio system or not

    def getHasAudioSystem(self):
        # This returns True/False for audio system
        return self.hasAudioSystem

    def setHasAudioSystem(self, hasAudioSystem):
        # This updates the audio system value
        self.hasAudioSystem = hasAudioSystem

    def displayDetails(self):
        # I extend display to include audio system info
        return super().displayDetails() + ", Audio System: " + str(self.hasAudioSystem)

    def __str__(self):
        # This controls print output
        return "EventHall: " + self.name