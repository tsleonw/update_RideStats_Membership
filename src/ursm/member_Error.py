class MemberError:
    """
    container for errorList and warnings about a given member.
    This will be added to the errorList array and needs to print in a nice
    fashion.  Maybe can be converted to a dataclass at some point.

    Note:  change this to make it a list of RideStats errors and rename it
    MemberErrors

    Created on Sat Jan  5 11:37:44 2019

    @author: Leon Webster

    ©2022, RideStats, LLC..
    """

    exceptions = None

    def __init__(self,
                 memberRecord,
                 msg,
                 exception=None):
        self._firstName = memberRecord['FirstName']
        self._lastName = memberRecord['LastName']
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
