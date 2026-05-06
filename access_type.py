class AccessType:
    # I am creating a class called AccessType, which represents the type of access a user has (like Standard or Premium)

    # Constructor to create access type (Standard / Premium)
    def __init__(self, typeName, allowedFacilityTypes, priorityAccess, maxFacilityTypes):
        # This function runs automatically when I create a new AccessType object

        self.typeName = typeName
        # I am saving the name of the access type (for example: "Standard" or "Premium") inside the object

        self.allowedFacilityTypes = allowedFacilityTypes
        # I am storing a list of facility types that this user is allowed to book (like StudyRoom, SportsCourt, etc.)

        self.priorityAccess = priorityAccess
        # I am saving whether this access type has priority booking (True means yes, False means no)

        self.maxFacilityTypes = maxFacilityTypes
        # I am saving the maximum number of different facility types this user is allowed to book

    def getTypeName(self):
        # This function is used when I want to get (read) the access type name from the object
        return self.typeName
        # I return the stored type name back

    def getAllowedFacilityTypes(self):
        # This function is used when I want to know which facility types are allowed
        return self.allowedFacilityTypes
        # I return the list of allowed facility types

    def getPriorityAccess(self):
        # This function checks if the user has priority booking
        return self.priorityAccess
        # I return True or False

    def getMaxFacilityTypes(self):
        # This function returns the maximum number of facility types allowed
        return self.maxFacilityTypes
        # I return that number

    def setTypeName(self, typeName):
        # This function updates the access type name
        self.typeName = typeName
        # I replace the old type name with the new one

    def setAllowedFacilityTypes(self, allowedFacilityTypes):
        # This function updates the allowed facility types list
        self.allowedFacilityTypes = allowedFacilityTypes
        # I replace the old list with the new one

    def setPriorityAccess(self, priorityAccess):
        # This function updates whether the user has priority booking
        self.priorityAccess = priorityAccess
        # I update it to True or False

    def setMaxFacilityTypes(self, maxFacilityTypes):
        # This function updates the maximum number of facility types allowed
        self.maxFacilityTypes = maxFacilityTypes
        # I update the number

    def canBook(self, facilityType):
        # This function checks if the user is allowed to book a certain facility type

        if facilityType in self.allowedFacilityTypes:
            # I check if the requested facility type exists in the allowed list
            return True
            # If yes, I allow the booking

        return False
        # If not, I deny the booking

    def __str__(self):
        # This function controls what gets printed when I print the object
        return "Access Type: " + self.typeName
        # I return a simple text showing the access type name