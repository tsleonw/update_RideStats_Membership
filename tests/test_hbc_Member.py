from src.ursm.hbc_Member import HBCMember
from datetime import datetime, timedelta

def test_HBCMember_base_case():
    WA_response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                   'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '2019-07-19T00:09:19-05:00',
                   'MembershipLevel': {'Id': 230757,
                                       'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                       'Name': 'Household'},
                   'Status': 'Active',
                   'FieldValues': [
                       {'FieldName': 'Member emails and newsletters', 'Value': True,
                        'SystemCode': 'ReceiveNewsletters'},
                       {'FieldName': 'Profile last updated', 'Value': '2019-07-19T00:09:19-05:00',
                        'SystemCode': 'LastUpdated'},
                       {'FieldName': 'Creation date', 'Value': '2011-12-15T17:18:41-06:00',
                        'SystemCode': 'CreationDate'},
                       {'FieldName': 'Terms of use accepted', 'Value': True,
                        'SystemCode': 'SystemRulesAndTermsAccepted'},
                       {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                       {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                       {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                       {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                       {'FieldName': 'Mobile Phone', 'Value': '651-788-2946', 'SystemCode': 'Phone'},
                       {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                       {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster', 'SystemCode': 'custom-2496544'},
                       {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                        'SystemCode': 'custom-2496545'},
                       {'FieldName': 'Member since', 'Value': '2009-06-17T00:00:00-05:00', 'SystemCode': 'MemberSince'},
                       {'FieldName': 'Renewal due', 'Value': '2022-10-17T00:00:00', 'SystemCode': 'RenewalDue'},
                       {'FieldName': 'Membership status',
                        'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active', 'SelectedByDefault': False,
                                  'Position': 0}, 'SystemCode': 'Status'},
                       {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00', 'SystemCode': 'custom-13004052'},
                       {'FieldName': 'Group participation',
                        'Value': [{'Id': 75110, 'Label': 'Ride Leader'}, {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                        'SystemCode': 'Groups'},
                       {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                        'SystemCode': 'custom-2626787'},
                       {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                       {'FieldName': 'Address', 'Value': '1769 Stanford Ave', 'SystemCode': 'custom-2483519'},
                       {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                       {'FieldName': 'State', 'Value': 'MN', 'SystemCode': 'custom-2483522'},
                       {'FieldName': 'Postal Code', 'Value': '55105-2043', 'SystemCode': 'custom-2483521'},
                       {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                   'Id': 6063831, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                   'IsAccountAdministrator': True,
                   'TermsOfUseAccepted': True}

    expected_output = {'clubMemberId': 6063831, 'firstName': 'Leon', 'lastName': 'Webster',
                       'emailAddress': 'leon@leonwebster.com', 'gender': 'MALE', 'membershipType': 'HOUSEHOLD',
                       'membershipStart': '2009-06-17', 'membershipEnd': '2022-10-17', 'phone1': '(651) 788-2946',
                       'phone2': '', 'rideLeader': True, 'emergencyContactName': 'Lindy Webster',
                       'emergencyContactPhone': '(651) 675-7565', 'birthDate': '1950-03-06',
                       'address': '1769 Stanford Ave',
                       'city': 'ST. Paul', 'state': 'MN', 'country': 'USA', 'zipcode': '55105-2043',
                       'bicycleType': 'SINGLE', 'ReceiveNewsLetter': True}
    test_member = HBCMember(WA_response)
    assert test_member.to_dict() == expected_output
    assert test_member.isValid()
    assert test_member.memberErrors is None


def test_missing_mobile_phone():
    """
    if mobile phone is missing in Wild Apricot, it should be replaced with the default value: '(212) 999-9999'
    :return: None
    """

    WA_response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                   'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '2019-07-19T00:09:19-05:00',
                   'MembershipLevel': {'Id': 230757,
                                       'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                       'Name': 'Household'},
                   'Status': 'Active',
                   'FieldValues': [
                       {'FieldName': 'Member emails and newsletters', 'Value': True,
                        'SystemCode': 'ReceiveNewsletters'},
                       {'FieldName': 'Profile last updated', 'Value': '2019-07-19T00:09:19-05:00',
                        'SystemCode': 'LastUpdated'},
                       {'FieldName': 'Creation date', 'Value': '2011-12-15T17:18:41-06:00',
                        'SystemCode': 'CreationDate'},
                       {'FieldName': 'Terms of use accepted', 'Value': True,
                        'SystemCode': 'SystemRulesAndTermsAccepted'},
                       {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                       {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                       {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                       {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                       {'FieldName': 'Mobile Phone', 'Value': '', 'SystemCode': 'Phone'},
                       {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                       {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster', 'SystemCode': 'custom-2496544'},
                       {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                        'SystemCode': 'custom-2496545'},
                       {'FieldName': 'Member since', 'Value': '2009-06-17T00:00:00-05:00', 'SystemCode': 'MemberSince'},
                       {'FieldName': 'Renewal due', 'Value': '2022-10-17T00:00:00', 'SystemCode': 'RenewalDue'},
                       {'FieldName': 'Membership status',
                        'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active', 'SelectedByDefault': False,
                                  'Position': 0}, 'SystemCode': 'Status'},
                       {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00', 'SystemCode': 'custom-13004052'},
                       {'FieldName': 'Group participation',
                        'Value': [{'Id': 75110, 'Label': 'Ride Leader'}, {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                        'SystemCode': 'Groups'},
                       {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                        'SystemCode': 'custom-2626787'},
                       {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                       {'FieldName': 'Address', 'Value': '1769 Stanford Ave', 'SystemCode': 'custom-2483519'},
                       {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                       {'FieldName': 'State', 'Value': 'MN', 'SystemCode': 'custom-2483522'},
                       {'FieldName': 'Postal Code', 'Value': '55105-2043', 'SystemCode': 'custom-2483521'},
                       {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                   'Id': 6063831, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                   'IsAccountAdministrator': True,
                   'TermsOfUseAccepted': True}

    test_member = HBCMember(WA_response)
    # assert test_member.to_dict() == expected_output
    assert test_member.mobile_Phone == '(212) 999-9999'
    assert test_member.memberErrors is None


def test_missing_gender():
    """
    if gender is missing, gender should be 'NEUTRAL'
    :return: None
    """
    WA_response = {'FirstName': 'Karen',
                   'LastName': 'K',
                   'Email': 'klkellermc@gmail.com',
                   'DisplayName': 'K, Karen',
                   'ProfileLastUpdated': '2019-11-25T23:39:07.37-06:00',
                   'MembershipLevel': {'Id': 230758, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230758', 'Name': 'Individual'},
                   'Status': 'Active',
                   'FieldValues': [
                       {'FieldName': 'Member emails and newsletters', 'Value': True, 'SystemCode': 'ReceiveNewsletters'},
                       {'FieldName': 'Profile last updated', 'Value': '2019-11-25T23:39:07.37-06:00', 'SystemCode': 'LastUpdated'},
                       {'FieldName': 'Creation date', 'Value': '2019-07-13T16:27:23-05:00', 'SystemCode': 'CreationDate'},
                       {'FieldName': 'Terms of use accepted', 'Value': True, 'SystemCode': 'SystemRulesAndTermsAccepted'},
                       {'FieldName': 'User ID', 'Value': 51417701, 'SystemCode': 'MemberId'},
                       {'FieldName': 'First name', 'Value': 'Karen', 'SystemCode': 'FirstName'},
                       {'FieldName': 'Last name', 'Value': 'K', 'SystemCode': 'LastName'},
                       {'FieldName': 'e-Mail', 'Value': 'klkellermc@gmail.com', 'SystemCode': 'Email'},
                       {'FieldName': 'Mobile Phone', 'Value': '952-380-7274', 'SystemCode': 'Phone'},
                       {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                       {'FieldName': 'Emergency Contact', 'Value': 'Lynne McMullen', 'SystemCode': 'custom-2496544'},
                       {'FieldName': 'Emergency Contact Phone', 'Value': '575-635-5603', 'SystemCode': 'custom-2496545'},
                       {'FieldName': 'Member since', 'Value': '2019-07-13T00:00:00-05:00', 'SystemCode': 'MemberSince'},
                       {'FieldName': 'Renewal due', 'Value': '2022-07-13T00:00:00', 'SystemCode': 'RenewalDue'},
                       {'FieldName': 'Membership status', 'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active', 'SelectedByDefault': False, 'Position': 0}, 'SystemCode': 'Status'},
                       {'FieldName': 'Birthdate', 'Value': '1962-07-30T00:00:00', 'SystemCode': 'custom-13004052'},
                       {'FieldName': 'Group participation', 'Value': [], 'SystemCode': 'Groups'},
                       {'FieldName': 'Gender', 'Value': None, 'SystemCode': 'custom-2626787'},
                       {'CustomAccessLevel': 'Members', 'FieldName': 'Birthday', 'Value': '', 'SystemCode': 'custom-2504934'},
                       {'FieldName': 'Address', 'Value': '4525 Park Commons Dr #210', 'SystemCode': 'custom-2483519'},
                       {'FieldName': 'City', 'Value': 'St Louis Park', 'SystemCode': 'custom-2483520'},
                       {'FieldName': 'State', 'Value': 'MN', 'SystemCode': 'custom-2483522'},
                       {'FieldName': 'Postal Code', 'Value': '55416', 'SystemCode': 'custom-2483521'},
                       {'FieldName': 'Country', 'Value': '', 'SystemCode': 'custom-2483523'}],
                   'Id': 51417701, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/51417701',
                   'IsAccountAdministrator': False,
                   'TermsOfUseAccepted': True}
    test_member = HBCMember(WA_response)
    assert test_member.gender == 'NEUTRAL'
    assert test_member.memberErrors is None


def test_state_code():
    """
    If state code is missing or invalid, Use 'MN' and create a message
    """
    WA_Response = WA_response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                   'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '2019-07-19T00:09:19-05:00',
                   'MembershipLevel': {'Id': 230757,
                                       'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                       'Name': 'Household'},
                   'Status': 'Active',
                   'FieldValues': [
                       {'FieldName': 'Member emails and newsletters', 'Value': True,
                        'SystemCode': 'ReceiveNewsletters'},
                       {'FieldName': 'Profile last updated', 'Value': '2019-07-19T00:09:19-05:00',
                        'SystemCode': 'LastUpdated'},
                       {'FieldName': 'Creation date', 'Value': '2011-12-15T17:18:41-06:00',
                        'SystemCode': 'CreationDate'},
                       {'FieldName': 'Terms of use accepted', 'Value': True,
                        'SystemCode': 'SystemRulesAndTermsAccepted'},
                       {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                       {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                       {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                       {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                       {'FieldName': 'Mobile Phone', 'Value': '', 'SystemCode': 'Phone'},
                       {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                       {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster', 'SystemCode': 'custom-2496544'},
                       {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                        'SystemCode': 'custom-2496545'},
                       {'FieldName': 'Member since', 'Value': '2009-06-17T00:00:00-05:00', 'SystemCode': 'MemberSince'},
                       {'FieldName': 'Renewal due', 'Value': '2022-10-17T00:00:00', 'SystemCode': 'RenewalDue'},
                       {'FieldName': 'Membership status',
                        'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active', 'SelectedByDefault': False,
                                  'Position': 0}, 'SystemCode': 'Status'},
                       {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00', 'SystemCode': 'custom-13004052'},
                       {'FieldName': 'Group participation',
                        'Value': [{'Id': 75110, 'Label': 'Ride Leader'}, {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                        'SystemCode': 'Groups'},
                       {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                        'SystemCode': 'custom-2626787'},
                       {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                       {'FieldName': 'Address', 'Value': '1769 Stanford Ave', 'SystemCode': 'custom-2483519'},
                       {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                       {'FieldName': 'State', 'Value': 'XX', 'SystemCode': 'custom-2483522'},
                       {'FieldName': 'Postal Code', 'Value': '55105-2043', 'SystemCode': 'custom-2483521'},
                       {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                   'Id': 6063831, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                   'IsAccountAdministrator': True,
                   'TermsOfUseAccepted': True}
    test_member = HBCMember(WA_response)
    assert test_member.state == 'MN'
    assert test_member.memberErrors.messages[0] == 'Leon Webster does not have a valid state.'

def test_missing_member_since_date():
    """
    if missing a member_since date, use creation date
    :type: None
    """
    WA_Response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                                 'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '2019-07-19T00:09:19-05:00',
                                 'MembershipLevel': {'Id': 230757,
                                                     'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                                     'Name': 'Household'},
                                 'Status': 'Active',
                                 'FieldValues': [
                                     {'FieldName': 'Member emails and newsletters', 'Value': True,
                                      'SystemCode': 'ReceiveNewsletters'},
                                     {'FieldName': 'Profile last updated', 'Value': '2019-07-19T00:09:19-05:00',
                                      'SystemCode': 'LastUpdated'},
                                     {'FieldName': 'Creation date', 'Value': '2011-12-15T17:18:41-06:00',
                                      'SystemCode': 'CreationDate'},
                                     {'FieldName': 'Terms of use accepted', 'Value': True,
                                      'SystemCode': 'SystemRulesAndTermsAccepted'},
                                     {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                                     {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                                     {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                                     {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                                     {'FieldName': 'Mobile Phone', 'Value': '', 'SystemCode': 'Phone'},
                                     {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                                     {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster',
                                      'SystemCode': 'custom-2496544'},
                                     {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                                      'SystemCode': 'custom-2496545'},
                                     {'FieldName': 'Member since', 'Value': '', 'SystemCode': 'MemberSince'},
                                     {'FieldName': 'Renewal due', 'Value': '2022-10-17T00:00:00',
                                      'SystemCode': 'RenewalDue'},
                                     {'FieldName': 'Membership status',
                                      'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active',
                                                'SelectedByDefault': False,
                                                'Position': 0}, 'SystemCode': 'Status'},
                                     {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00',
                                      'SystemCode': 'custom-13004052'},
                                     {'FieldName': 'Group participation',
                                      'Value': [{'Id': 75110, 'Label': 'Ride Leader'},
                                                {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                                      'SystemCode': 'Groups'},
                                     {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                                      'SystemCode': 'custom-2626787'},
                                     {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                                     {'FieldName': 'Address', 'Value': '1769 Stanford Ave',
                                      'SystemCode': 'custom-2483519'},
                                     {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                                     {'FieldName': 'State', 'Value': 'XX', 'SystemCode': 'custom-2483522'},
                                     {'FieldName': 'Postal Code', 'Value': '55105-2043',
                                      'SystemCode': 'custom-2483521'},
                                     {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                                 'Id': 6063831,
                                 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                                 'IsAccountAdministrator': True,
                                 'TermsOfUseAccepted': True}
    test_member = HBCMember(WA_Response)
    # should use creation date as member since date
    assert test_member.member_since == '2011-12-15'
    assert test_member.memberErrors.messages[0] == 'Leon Webster has no Member since date'\

def test_default_membership_since_date():
    """
    if Member since missing and creation date missing and profile last updated missing use today's date.
    :return: None
    """
    WA_Response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                                 'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '',
                                 'MembershipLevel': {'Id': 230757,
                                                     'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                                     'Name': 'Household'},
                                 'Status': 'Active',
                                 'FieldValues': [
                                     {'FieldName': 'Member emails and newsletters', 'Value': True,
                                      'SystemCode': 'ReceiveNewsletters'},
                                     {'FieldName': 'Profile last updated', 'Value': '',
                                      'SystemCode': 'LastUpdated'},
                                     {'FieldName': 'Creation date', 'Value': '',
                                      'SystemCode': 'CreationDate'},
                                     {'FieldName': 'Terms of use accepted', 'Value': True,
                                      'SystemCode': 'SystemRulesAndTermsAccepted'},
                                     {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                                     {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                                     {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                                     {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                                     {'FieldName': 'Mobile Phone', 'Value': '', 'SystemCode': 'Phone'},
                                     {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                                     {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster',
                                      'SystemCode': 'custom-2496544'},
                                     {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                                      'SystemCode': 'custom-2496545'},
                                     {'FieldName': 'Member since', 'Value': '', 'SystemCode': 'MemberSince'},
                                     {'FieldName': 'Renewal due', 'Value': '2022-10-17T00:00:00',
                                      'SystemCode': 'RenewalDue'},
                                     {'FieldName': 'Membership status',
                                      'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active',
                                                'SelectedByDefault': False,
                                                'Position': 0}, 'SystemCode': 'Status'},
                                     {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00',
                                      'SystemCode': 'custom-13004052'},
                                     {'FieldName': 'Group participation',
                                      'Value': [{'Id': 75110, 'Label': 'Ride Leader'},
                                                {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                                      'SystemCode': 'Groups'},
                                     {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                                      'SystemCode': 'custom-2626787'},
                                     {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                                     {'FieldName': 'Address', 'Value': '1769 Stanford Ave',
                                      'SystemCode': 'custom-2483519'},
                                     {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                                     {'FieldName': 'State', 'Value': 'MN', 'SystemCode': 'custom-2483522'},
                                     {'FieldName': 'Postal Code', 'Value': '55105-2043',
                                      'SystemCode': 'custom-2483521'},
                                     {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                                 'Id': 6063831,
                                 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                                 'IsAccountAdministrator': True,
                                 'TermsOfUseAccepted': True}
    test_member = HBCMember(WA_Response)
    today = datetime.date(datetime.today()).isoformat()
    assert test_member.member_since == today
    assert test_member.memberErrors.messages[0] == 'Leon Webster has no creation date'
    assert test_member.memberErrors.messages[1] == 'Leon Webster has no Member since date'
    assert test_member.memberErrors.messages[2] == 'Could not calculate member_since for Leon Webster. Using todays date.'

def test_calculate_renewal_due():
    WA_response = {'FirstName': 'Leon', 'LastName': 'Webster', 'Email': 'leon@leonwebster.com',
                   'DisplayName': 'Webster, Leon', 'ProfileLastUpdated': '2019-07-19T00:09:19-05:00',
                   'MembershipLevel': {'Id': 230757,
                                       'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/MembershipLevels/230757',
                                       'Name': 'Household'},
                   'Status': 'Active',
                   'FieldValues': [
                       {'FieldName': 'Member emails and newsletters', 'Value': True,
                        'SystemCode': 'ReceiveNewsletters'},
                       {'FieldName': 'Profile last updated', 'Value': '2019-07-19T00:09:19-05:00',
                        'SystemCode': 'LastUpdated'},
                       {'FieldName': 'Creation date', 'Value': '2011-12-15T17:18:41-06:00',
                        'SystemCode': 'CreationDate'},
                       {'FieldName': 'Terms of use accepted', 'Value': True,
                        'SystemCode': 'SystemRulesAndTermsAccepted'},
                       {'FieldName': 'User ID', 'Value': 6063831, 'SystemCode': 'MemberId'},
                       {'FieldName': 'First name', 'Value': 'Leon', 'SystemCode': 'FirstName'},
                       {'FieldName': 'Last name', 'Value': 'Webster', 'SystemCode': 'LastName'},
                       {'FieldName': 'e-Mail', 'Value': 'leon@leonwebster.com', 'SystemCode': 'Email'},
                       {'FieldName': 'Mobile Phone', 'Value': '651-788-2946', 'SystemCode': 'Phone'},
                       {'FieldName': 'Home Phone', 'Value': '', 'SystemCode': 'custom-2491306'},
                       {'FieldName': 'Emergency Contact', 'Value': 'Lindy Webster', 'SystemCode': 'custom-2496544'},
                       {'FieldName': 'Emergency Contact Phone', 'Value': '651-675-7565',
                        'SystemCode': 'custom-2496545'},
                       {'FieldName': 'Member since', 'Value': '2009-06-17T00:00:00-05:00', 'SystemCode': 'MemberSince'},
                       {'FieldName': 'Renewal due', 'Value': '', 'SystemCode': 'RenewalDue'},
                       {'FieldName': 'Membership status',
                        'Value': {'Id': 1, 'Label': 'Active', 'Value': 'Active', 'SelectedByDefault': False,
                                  'Position': 0}, 'SystemCode': 'Status'},
                       {'FieldName': 'Birthdate', 'Value': '1950-03-06T00:00:00', 'SystemCode': 'custom-13004052'},
                       {'FieldName': 'Group participation',
                        'Value': [{'Id': 75110, 'Label': 'Ride Leader'}, {'Id': 531561, 'Label': 'HBC_ADMINS'}],
                        'SystemCode': 'Groups'},
                       {'FieldName': 'Gender', 'Value': {'Id': 1797240, 'Label': 'Male'},
                        'SystemCode': 'custom-2626787'},
                       {'FieldName': 'Birthday', 'Value': '03/06/1950', 'SystemCode': 'custom-2504934'},
                       {'FieldName': 'Address', 'Value': '1769 Stanford Ave', 'SystemCode': 'custom-2483519'},
                       {'FieldName': 'City', 'Value': 'ST. Paul', 'SystemCode': 'custom-2483520'},
                       {'FieldName': 'State', 'Value': 'MN', 'SystemCode': 'custom-2483522'},
                       {'FieldName': 'Postal Code', 'Value': '55105-2043', 'SystemCode': 'custom-2483521'},
                       {'FieldName': 'Country', 'Value': 'USA', 'SystemCode': 'custom-2483523'}],
                   'Id': 6063831, 'Url': 'https://api.wildapricot.org/v2.1/accounts/53245/Contacts/6063831',
                   'IsAccountAdministrator': True,
                   'TermsOfUseAccepted': True}
    today_plus_30 = datetime.date(datetime.today()) + timedelta(days=30)
    today_plus_30 = today_plus_30.isoformat()
    test_member = HBCMember(WA_response)
    # will use 30 days from today since membersince date is over 30 days in the past
    assert test_member.renewal_due == today_plus_30
    assert test_member.memberErrors.messages[0] == 'Leon Webster doesnt not have a renewal due date'
    assert test_member.memberErrors.messages[1] == f'calculated renewal date for Leon Webster is {today_plus_30}'

    test_member.member_since = ''
    test_member.creation_date = ''
    test_member.calculate_missing_dates()
    #will calculate 30 days from today.
    assert test_member.member_since == datetime.date(datetime.today()).isoformat()
    assert test_member.renewal_due == today_plus_30
    assert test_member.memberErrors.messages[0] == 'Leon Webster doesnt not have a renewal due date'
    assert test_member.memberErrors.messages[1] == f'calculated renewal date for Leon Webster is {today_plus_30}'



def test_phone_number_from_string():
    # test 7 digit phone number
    assert HBCMember.phoneNumberFromString('7882946') == '788-2946'
    assert HBCMember.phoneNumberFromString('788-2946') == '788-2946'
    # test 10 digit phone number
    assert HBCMember.phoneNumberFromString('651.788.2946') == '(651) 788-2946'
    assert HBCMember.phoneNumberFromString('6517882946') == '(651) 788-2946'
    # test invalid phone numbers
    assert HBCMember.phoneNumberFromString('abcde') == ''
    assert HBCMember.phoneNumberFromString('12345') == ''
