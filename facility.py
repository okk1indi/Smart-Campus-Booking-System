class Facility:
    # Constructor to create a facility object
    def __init__(self, facilityId, name, facilityType, location, capacity, availableTimeSlots, bookingStatus, fee):
        self.facilityId = facilityId
        self.name = name
        self.facilityType = facilityType
        self.location = location
        self.capacity = capacity
        self.availableTimeSlots = availableTimeSlots
        self.bookingStatus = bookingStatus
        self.fee = fee

    # Getters
    def getFacilityId(self):
        return self.facilityId

    def getName(self):
        return self.name

    def getFacilityType(self):
        return self.facilityType

    def getLocation(self):
        return self.location

    def getCapacity(self):
        return self.capacity

    def getAvailableTimeSlots(self):
        return self.availableTimeSlots

    def getBookingStatus(self):
        return self.bookingStatus

    def getFee(self):
        return self.fee

    # Setters
    def setFacilityId(self, facilityId):
        self.facilityId = facilityId

    def setName(self, name):
        self.name = name

    def setFacilityType(self, facilityType):
        self.facilityType = facilityType

    def setLocation(self, location):
        self.location = location

    def setCapacity(self, capacity):
        self.capacity = capacity

    def setAvailableTimeSlots(self, availableTimeSlots):
        self.availableTimeSlots = availableTimeSlots

    def setBookingStatus(self, bookingStatus):
        self.bookingStatus = bookingStatus

    def setFee(self, fee):
        self.fee = fee

    # Display facility information
    def displayDetails(self):
        return ("Facility: " + self.name +
                ", Type: " + self.facilityType +
                ", Location: " + self.location +
                ", Capacity: " + str(self.capacity) +
                ", Status: " + self.bookingStatus +
                ", Available Slots: " + str(self.availableTimeSlots) +
                ", Fee: " + str(self.fee) + " AED/hour")

    # Check if a time slot is available
    def checkAvailability(self, timeSlot):
        return timeSlot in self.availableTimeSlots

    # Add or remove a time slot
    def updateAvailability(self, timeSlot, status):
        if status == True:
            if timeSlot not in self.availableTimeSlots:
                self.availableTimeSlots.append(timeSlot)
            self.bookingStatus = "Available"
        else:
            if timeSlot in self.availableTimeSlots:
                self.availableTimeSlots.remove(timeSlot)
            if len(self.availableTimeSlots) == 0:
                self.bookingStatus = "Fully Booked"

    # Calculate booking fee
    def calculateFee(self, duration):
        return self.fee * duration

    def __str__(self):
        return "Facility: " + self.name + " (" + self.facilityType + ")"


class StudyRoom(Facility):
    # StudyRoom inherits from Facility
    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, numberOfTables):
        super().__init__(facilityId, name, "StudyRoom", location, capacity, availableTimeSlots, bookingStatus, fee)
        self.numberOfTables = numberOfTables

    def getNumberOfTables(self):
        return self.numberOfTables

    def setNumberOfTables(self, numberOfTables):
        self.numberOfTables = numberOfTables

    def displayDetails(self):
        return super().displayDetails() + ", Tables: " + str(self.numberOfTables)

    def __str__(self):
        return "StudyRoom: " + self.name


class SportCourt(Facility):
    # SportCourt inherits from Facility
    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, sportType):
        super().__init__(facilityId, name, "SportCourt", location, capacity, availableTimeSlots, bookingStatus, fee)
        self.sportType = sportType

    def getSportType(self):
        return self.sportType

    def setSportType(self, sportType):
        self.sportType = sportType

    def displayDetails(self):
        return super().displayDetails() + ", Sport: " + self.sportType

    def __str__(self):
        return "SportCourt: " + self.name


class EventHall(Facility):
    # EventHall inherits from Facility
    def __init__(self, facilityId, name, location, capacity, availableTimeSlots, bookingStatus, fee, hasAudioSystem):
        super().__init__(facilityId, name, "EventHall", location, capacity, availableTimeSlots, bookingStatus, fee)
        self.hasAudioSystem = hasAudioSystem

    def getHasAudioSystem(self):
        return self.hasAudioSystem

    def setHasAudioSystem(self, hasAudioSystem):
        self.hasAudioSystem = hasAudioSystem

    def displayDetails(self):
        return super().displayDetails() + ", Audio System: " + str(self.hasAudioSystem)

    def __str__(self):
        return "EventHall: " + self.name