from datetime import datetime, timedelta

from member_Error import MemberError


class HBCMember:
    """
    HBCMember represents a member of the club in Wild Apricot
    """

    def __init__(self, aDict):
        """
        construct a member object from a dictionary.
        """
        self._setDefaultValues()
        try:
            try:
                self._firstName = aDict["FirstName"]
                self._lastName = aDict["LastName"]
            except KeyError as ex:
                msg = "Error populating member first or last name" + ex.__repr__()
                self.postError(msg, aDict, ex)
            self._email = aDict["Email"]
            self._membershipType = aDict["MembershipLevel"]["Name"]
            self._status = aDict["Status"]
            self._profileLastUpdated = datetime.now().date()
            """
            remaining values are found in a single dictionary entry called 'FieldValues' 
            that in turn contains a dictionary of fields and values.
            """

            for field in aDict["FieldValues"]:
                if field["FieldName"] == "Member since":
                    if self._status == "PendingNew":
                        self._memberSince = self._profileLastUpdated
                        msg = (
                            self._firstName
                            + " "
                            + self._lastName
                            + " is a pending new"
                            + " member.  using profile last updated date as memberSince."
                        )
                        self.postError(msg, aDict, None)
                    else:
                        if field["Value"]:
                            self._memberSince = datetime.fromisoformat(
                                (field["Value"])[:19]
                            ).date()
                        else:
                            msg = (
                                self._firstName
                                + " "
                                + self._lastName
                                + " does not have a valid member since date."
                            )
                            self.postError(msg, aDict, None)
                elif field["FieldName"] == "Gender":
                    if field["Value"] is not None:
                        self._gender = field["Value"]["Label"]
                    else:
                        self._gender = "Neutral"
                elif field["FieldName"] == "Renewal due":
                    if self._status == "PendingNew":
                        self._renewalDue = self._memberSince + timedelta(days=30)
                        msg = (
                            self._firstName
                            + " "
                            + self._lastName
                            + " is a pending new"
                            + " member.  Renewal due 30 days after profile last updated."
                        )
                        self.postError(msg, aDict, None)
                    else:
                        if field["Value"]:
                            self._renewalDue = datetime.fromisoformat(
                                field["Value"]
                            ).date()
                        else:
                            msg = (
                                self._firstName
                                + " "
                                + self._lastName
                                + " does not have a valid renewal due date."
                            )
                            self.postError(msg, aDict, None)
                elif field["FieldName"] == "Mobile Phone":
                    self._mobilePhone = self.phoneNumberFromString(field["Value"])
                elif field["FieldName"] == "Telephone":
                    self._telephone = self.phoneNumberFromString(field["Value"])
                elif field["FieldName"] == "User ID":
                    self._memberID = field["Value"]
                elif field["FieldName"] == "Alias":
                    self._alias = field["Value"]
                elif field["FieldName"] == "Address":
                    self._address = field["Value"]
                elif field["FieldName"] == "City":
                    self._city = field["Value"]
                elif field["FieldName"] == "State":
                    self._state = field["Value"]
                elif field["FieldName"] == "Postal Code":
                    self._zipCode = field["Value"]
                elif field["FieldName"] == "Emergency Contact":
                    self._emergencyContact = field["Value"]
                elif field["FieldName"] == "Emergency Contact Phone":
                    self._emergencyContactPhone = self.phoneNumberFromString(
                        field["Value"]
                    )
                    """if (self.emergencyContactPhone == '' or
                            self.emergencyContactPhone is None):
                        msg = self.firstName + ' ' + self.lastName + \
                              ' does not have an emergency contact phone number.'
                        self.postError(msg, aDict, None)"""

                elif field["FieldName"] == "Birthday":
                    self._birthDate = field["Value"]
                elif field["FieldName"] == "Group participation":
                    if field["Value"]:
                        for group in field["Value"]:
                            if group["Label"] == "Ride Leader":
                                self._isRideLeader = True
                elif field["FieldName"] == "Creation Date":
                    self._creationDate = datetime.fromisoformat(
                        field["Value"][:19]
                    ).date()
                    print(self._creationDate)
        except Exception as ex:
            msg = "Other error in member.__init__() " + ex.__repr__()
            self.postError(msg, aDict, ex)

    @property
    def memberError(self):
        """memberError is a list of errors relating to a member"""
        return self._memberError

    @memberError.setter
    def memberError(self, memberError):
        raise AttributeError("can't set memberError")

    def _setDefaultValues(self):
        """
        set default values for instance variables.  Since the information in Wild Apricot may be missing fields, we
        need to make sure that the attributes exist with default values so serialization works without checking for
        the existence of each attribute.
        """
        self._memberID = None
        self._firstName = None
        self._lastName = None
        self._birthDate = None
        self._alias = None
        self._email = None
        self._status = None
        self._mobilePhone = None
        self._telephone = None
        self._address = None
        self._city = None
        self._state = None
        self._zipCode = None
        self._membershipType = None
        self._isRideLeader = False
        self._memberSince = None
        self._creationDate = None
        self._renewalDue = None
        self._profileLastUpdated = None
        self._gender = None
        self._isValid = True
        self._memberError = None
        self._emergencyContact = None
        self._emergencyContactPhone = None
        self._memberError = None

    def postError(self, msg, aDict, exception):
        """
        add an error to the members error list.  If there is no error list,
        create one.
        """
        if self._memberError:
            self._memberError.addErrorRecord(msg, exception)
        else:
            self._memberError = MemberError(aDict, msg, exception)

    @staticmethod
    def phoneNumberFromString(aString):
        """
        given a string, return the first 10 digits ignoring all non-numeric
        characters
        """
        digits = list(filter(lambda x: x.isdigit(), aString))
        phoneNumber = "".join(digits)
        if len(phoneNumber) > 9:
            phoneNumber = phoneNumber[:10]
        return phoneNumber

    def isValid(self):
        """make sure that all required attributes of a member are present"""
        if (
            self._memberID is None
            or self._firstName is None
            or self._lastName is None
            or self._email is None
            or self._memberSince is None
            or self._renewalDue is None
            or self._renewalDue < self._memberSince
        ):
            return False
        else:
            return True

    def toDict(self):
        """
        render a dictionary representation of a member which can then be used to create a json representation.
        """
        aDict = {}
        aDict["clubMemberId"] = self._memberID
        aDict["firstName"] = self._firstName
        aDict["lastName"] = self._lastName
        aDict["alias"] = self._alias
        aDict["emailAddress"] = self._email
        aDict["gender"] = self._gender
        if self._memberSince:
            aDict["membershipStart"] = self._memberSince.isoformat()
        else:
            aDict["membershipStart"] = None
        if self._renewalDue:
            aDict["membershipEnd"] = self._renewalDue.isoformat()
        else:
            aDict["membershipEnd"] = None
        aDict["membershipType"] = self._membershipType
        aDict["phone1"] = self._mobilePhone
        aDict["phone2"] = self._telephone
        if self._isRideLeader:
            aDict["rideLeader"] = True
        else:
            aDict["rideLeader"] = False
        aDict["emergencyContactName"] = self._emergencyContact
        aDict["emergencyContactPhone"] = self._emergencyContactPhone
        if self._birthDate:
            aDict["birthDate"] = self._birthDate
        else:
            aDict["birthDate"] = ""
        aDict["address"] = self._address
        aDict["city"] = self._city
        aDict["state"] = self._state
        if self._zipCode:
            aDict["zipCode"] = self._zipCode
        else:
            aDict["zipCode"] = ""
        aDict['userLastModified'] = self._profileLastUpdated.isoformat()
        return aDict

    def __str__(self):
        """
        return a string describing the member
        """
        aString = (
            "Membership information for "
            + self._firstName
            + " "
            + self._lastName
            + " "
            + "\tMember ID = "
            + str(self._memberID)
            + "\n"
        )
        if self._memberError is None:
            return aString
        aString += "/tMember Record has errors"
        for msg in self._memberError.messages:
            aString += "\t\t" + msg
        return aString
