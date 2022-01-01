class MemberError:
    """
    container for errorList and warnings about a given member.
    This will be added to the errorList array and needs to print in a nice
    fashion.  Maybe can be converted to a dataclass at somepoint.
    """

    exceptions = None
    memberRecord = None

    def __init__(self,
                 memberRecord,
                 msg,
                 exception=None):
        self.firstName = memberRecord['FirstName']
        self.lastName = memberRecord['LastName']
        self.memberRecord = memberRecord
        self.messages = [msg]
        if exception:
            self.exceptions = [exception]

    def addErrorRecord(self, msg, exception=None):
        """
        add an error to an existing error list
        """
        self.messages.append(msg)
        if exception:
            if self.exceptions:
                self.exceptions.append(exception)
            else:
                self.exceptions = [exception]

    def __str__(self):
        error_string = ''
        for msg in self.messages:
            error_string = error_string + msg + '\n'
        return error_string

    def __repr__(self):
        return self.__str__()