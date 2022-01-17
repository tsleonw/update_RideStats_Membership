from datetime import date, datetime, timedelta

from member_Error import MemberError


class HBCMember:
    
    def __init__(self, WA_Response):
        """
        store first and last name as member attributes to make referencing them 
        for error messages easier.
        """
        self.memberErrors = None
        self.first_name = WA_Response['FirstName']
        self.last_name = WA_Response['LastName']
        self.email = WA_Response['Email']
        self.membershipType = WA_Response['MembershipLevel']['Name']
        self.status = WA_Response['Status']
        self.member_ID = WA_Response['Id']
        if WA_Response.get('ProfileLastUpdated', None):
            self.profile_last_updated = WA_Response['ProfileLastUpdated'][:10]
        else:
            self.profile_last_updated = None
        self.member_since = None
        self.creation_date = None
        self.renewal_due = None
        self.mobile_Phone = '(212) 999-9999'
        # need to set this so can check when deciding to use 'birthday' or birthdate
        self.birthDate = ''
        self.is_RideLeader = False
        self.bicycle_type = 'SINGLE'
        """
        remaining values are in a list of "FieldValues".  each item in the list has
        a 'fieldName' which indicates which field it is, a 'Value' which contains the value of the field.
        the item also contains a 'systemCode' and may contain other items which are not relevent
        """
        for field in WA_Response['FieldValues']:
            if field['FieldName'] == 'Member since':
                if field['Value']:
                    self.member_since = field['Value'][:10]
                else:
                    msg = f'{self.first_name} {self.last_name} has no Member since date'
                    self.postError(msg)
            elif field['FieldName'] == 'Creation date':
                if field['Value']:
                    self.creation_date = field['Value'][:10]
                else:
                    msg = f'{self.first_name} {self.last_name} has no creation date'
                    self.postError(msg, WA_Response)
            elif field['FieldName'] == 'Gender':
                if field['Value']:
                    self.gender = field['Value']['Label'].upper()
                else:
                    self.gender = 'NEUTRAL'
            elif field['FieldName'] == 'Renewal due':
                if field['Value']:
                    self.renewal_due = field['Value'][:10]
                else:
                    msg = f'{self.first_name} {self.last_name} doesnt not have a renewal due date'
                    self.postError(msg)
            elif field['FieldName'] == 'Mobile Phone':
                if field['Value']:
                    self.mobile_Phone = self.phoneNumberFromString(field['Value'])
                else:
                    self.mobile_Phone = '(212) 999-9999'
            elif field['FieldName'] == 'Home Phone':
                if field['Value']:
                    self.home_phone = self.phoneNumberFromString(field['Value'])
                else:
                    self.home_phone = ''
            elif field['SystemCode'] == 'ReceiveNewsletters':
                self.receive_newsLetter = field['Value']
            elif field['FieldName'] == 'Address':
                self.address = field['Value']
            elif field['FieldName'] == 'City':
                self.city = field['Value']
            elif field['FieldName'] == 'State':
                state_string = field['Value'].lower()
                if state_string[:4] in {'mn', 'minn', }:
                    self.state = 'MN'
                elif state_string[:4] in {'wi', 'wisc', }:
                    self.state = 'WI'
                elif state_string in {'az', 'arizona'}:
                    self.state = 'AZ'
                elif state_string in {'tx', 'texas'}:
                    self.state = 'TX'
                else:
                    self.state = 'MN'
                    msg = f'{self.first_name} {self.last_name} does not have a valid state.'
                    self.postError(msg)
            elif field['FieldName'] == 'Postal Code':
                self.postal_code = field['Value']
            elif field['FieldName'] == 'Country':
                if len(field['Value']) == 3:
                    self.country = field['Value']
                else:
                    self.country = 'USA'
            elif field['FieldName'] == 'Emergency Contact':
                self.emergency_contact = field['Value']
            elif field["FieldName"] == "Emergency Contact Phone":
                self.emergencyContactPhone = self.phoneNumberFromString(field["Value"])
            elif field["FieldName"] == "Birthday" and (self.birthDate == ''):
                if field['Value']:
                    self.birthDate = field["Value"]
            elif field["FieldName"] == "Birthdate":
                if field['Value']:
                    self.birthDate = field["Value"][:10]
            elif field["FieldName"] == "Group participation":
                if field["Value"]:
                    for group in field["Value"]:
                        if group["Label"] == "Ride Leader":
                            self.is_RideLeader = True
            elif field["FieldName"] == "Creation Date":
                self._creationDate = (field["Value"][:10])

        # Now that the member is populated, check for missing dates.
        self.calculate_missing_dates()

    def calculate_missing_dates(self):
        if self.member_since is None:
            if self.creation_date:
                self.member_since = self.creation_date
            else:
                if self.profile_last_updated:
                    self.member_since = self.profile_last_updated
                else:
                    self.member_since = date.today().isoformat()
                    msg = f'Could not calculate member_since for {self.first_name} {self.last_name}. Using todays date.'
                    self.postError(msg)
        if self.renewal_due is None:
            self.renewal_due = date.fromisoformat(self.member_since) + timedelta(days=30)
            if self.renewal_due < datetime.date(datetime.today()):
                self.renewal_due = datetime.date(datetime.today()) + timedelta(days=30)
            self.renewal_due = self.renewal_due.isoformat()
            msg = f'calculated renewal date for {self.first_name} {self.last_name} is {self.renewal_due}'
            self.postError(msg)
                
    def postError(self, msg, exception=None):
        """
        add an error to the member's error list.  If there is no error list,
        create one.
        """
        if self.memberErrors:
            self.memberErrors.addErrorRecord(msg, exception)
        else:
            member_name = {'FirstName': self.first_name, 'LastName': self.last_name}
            self.memberErrors = MemberError(member_name, msg, exception)

    def isValid(self):
        """make sure that all required attributes of a member are present"""
        if (
            self.member_ID is None
            or self.first_name is None
            or self.last_name is None
            or self.email is None
            or self.member_since is None
            or self.renewal_due is None
            or self.renewal_due < self.member_since
        ):
            return False
        else:
            return True

    def to_dict(self):
        """
        construct a dictionary that can be used to send to RideStats
        :return: dictionary
        """
        RS_dict = {}
        RS_dict['clubMemberId'] = self.member_ID
        RS_dict['firstName'] = self.first_name
        RS_dict['lastName'] = self.last_name
        RS_dict['emailAddress'] = self.email
        RS_dict['gender'] = self.gender
        RS_dict['membershipType'] = self.membershipType.upper()
        RS_dict['membershipStart'] = self.member_since
        RS_dict['membershipEnd'] = self.renewal_due
        RS_dict['phone1'] = self.mobile_Phone
        RS_dict['phone2'] = self.home_phone
        RS_dict['rideLeader'] = self.is_RideLeader
        RS_dict['emergencyContactName'] = self.emergency_contact
        RS_dict['emergencyContactPhone'] = self.emergencyContactPhone
        RS_dict['birthDate'] = self.birthDate
        RS_dict['address'] = self.address
        RS_dict['city'] = self.city
        RS_dict['state'] = self.state
        RS_dict['country'] = self.country
        RS_dict['zipcode'] = self.postal_code
        RS_dict['bicycleType'] = self.bicycle_type
        RS_dict['ReceiveNewsLetter'] = self.receive_newsLetter
        return RS_dict

    def __str__(self):
        """
        return a string describing the member
        """
        aString = (f'Membership information for {self.first_name} {self.last_name} \
                    \t Member Id = {self.member_ID}\n')
        if self.memberErrors is None:
            return aString
        aString += "/tMember Record has errors"
        for msg in self.memberErrors.messages:
            aString += "\t\t" + msg
        return aString    
    
    @staticmethod
    def phoneNumberFromString(aString):
        """
        given a string, return the first 10 digits ignoring all non-numeric
        characters
        """
        digits = list(filter(lambda x: x.isdigit(), aString))
        phoneNumber = "".join(digits)
        if len(phoneNumber) < 7:
            return ''
        if len(phoneNumber) > 10:
            phoneNumber = phoneNumber[:10]
        if len(phoneNumber) == 7:
            phoneNumber = f'{phoneNumber[:3]}-{phoneNumber[3:7]}'
        elif len(phoneNumber) == 10:
            phoneNumber = f'({phoneNumber[:3]}) {phoneNumber[3:6]}-{phoneNumber[6:]}'
        return phoneNumber
