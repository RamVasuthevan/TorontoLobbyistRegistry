from enum import Enum

class DataSource(Enum):
    ACTIVE = "lobbyactivity-active.xml"
    CLOSED = "lobbyactivity-closed.xml"

class LobbyingReportStatus(Enum):
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    CLOSED_BY_LRO = 'Closed by LRO'

class LobbyingReportType(Enum):
    CONSULTANT = 'Consultant'
    IN_HOUSE = 'In-house'
    VOLUNTARY = 'Voluntary'

class RegistrantStatus(Enum):
    ACTIVE = 'Active'
    SUPERSEDED = 'Superseded'
    NOT_ACCEPTED = 'Not Accepted'
    FORCE_CLOSED = 'Force Closed'

class RegistrantType(Enum):
    CONSULTANT = 'Consultant'
    IN_HOUSE = 'In-house'

class BeneficiaryType(Enum):
    CLIENT = 'Client'
    COALITION_MEMBER = 'Coalition Member'
    CONTROLLING_INTEREST = 'Controlling Interest'
    CONTROLLING_INTEREST_HOLDER = 'Controlling Interest Holder' #Delete me
    PARENT_COMPANY = 'Parent Company'
    PERSON_WITH_SIGNIFICANT_CONTROL = 'Person with Significant Control'
    SUBSIDIARY_COMPANY = 'Subsidiary Company'
    OTHER = 'Other'

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None

class FirmType(Enum):
    CONSULTANT = 'Consultant'
    IN_HOUSE = 'In-house'
    PARENT = 'Parent'
    SUBSIDIARY = 'Subsidiary'
    OTHER = 'Other'

class FirmBusinessType(Enum):
    BUSINESS_INDUSTRY_TRADE_ASSOCIATION = 'Business/ Industry/ Trade Association'
    CORPORATION = 'Corporation'
    NOT_FOR_PROFIT_GRANT_APPLICANT = 'Not-for-profit grant applicant'
    PARTNERSHIP = 'Partnership'
    PROFESSIONAL_LABOUR_ASSOCIATION = 'Professional/ Labour Association'
    SOLE_PROPRIETOR = 'Sole Proprietor'

class PersonPrefix(Enum):
    NONE = "" #remove me. None is None
    MR = "Mr"
    MRS = "Mrs"
    MS = "Ms"
    MISS = "Miss"
    DR = "Dr"
    PROFESSOR = "Professor"
    HON = "Hon"
    MME = "Mme"
    ERROR = "Error"

class OfficeHolder(Enum):
    MEMBER_OF_COUNCIL = 'Member of Council'
    STAFF_OF_MEMBER_OF_COUNCIL = 'Staff of Member of Council'
    EMPLOYEE_OF_THE_CITY = 'Employee of the City'
    
class LobbyistType(Enum):
    COMMITTEE_MEMBER = 'Committee Member'
    IN_HOUSE_LOBBYIST = 'In-House Lobbyist'
    SR_OFFICER = 'Sr. Officer'

