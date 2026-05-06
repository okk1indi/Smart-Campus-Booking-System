class AccessType:
    # Constructor to create access type (Standard / Premium)
    def __init__(self, typeName, allowedFacilityTypes, priorityAccess, maxFacilityTypes):
        self.typeName = typeName                          # name of access type (e.g., Standard, Premium)
        self.allowedFacilityTypes = allowedFacilityTypes  # list of facility types user can book
        self.priorityAccess = priorityAccess              # True if user gets priority booking
        self.maxFacilityTypes = maxFacilityTypes          # max number of facility types allowed

    # ---------- Getters ----------
    def getTypeName(self):
        return self.typeName                              # return access type name

    def getAllowedFacilityTypes(self):
        return self.allowedFacilityTypes                  # return allowed facility types

    def getPriorityAccess(self):
        return self.priorityAccess                        # return priority status

    def getMaxFacilityTypes(self):
        return self.maxFacilityTypes                      # return max allowed facility types

    # ---------- Setters ----------
    def setTypeName(self, typeName):
        self.typeName = typeName                          # update type name

    def setAllowedFacilityTypes(self, allowedFacilityTypes):
        self.allowedFacilityTypes = allowedFacilityTypes  # update allowed facilities

    def setPriorityAccess(self, priorityAccess):
        self.priorityAccess = priorityAccess              # update priority access

    def setMaxFacilityTypes(self, maxFacilityTypes):
        self.maxFacilityTypes = maxFacilityTypes          # update max facility types

    # ---------- Logic ----------
    def canBook(self, facilityType):
        # Check if the facility type is allowed for this access type
        if facilityType in self.allowedFacilityTypes:
            return True
        return False

    # ---------- String ----------
    def __str__(self):
        return "Access Type: " + self.typeName
