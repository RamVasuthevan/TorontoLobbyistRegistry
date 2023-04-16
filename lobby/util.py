from dataclasses import dataclass
from typing import List, Dict, Any, Union, Optional

FILE_NAMES = {"active": "lobbyactivity-active.xml",
              "closed": "lobbyactivity-closed.xml"}


@dataclass
class BusinessAddress:
    AddressLine1: str
    AddressLine2: str
    City: str
    Province: str
    Country: str
    PostalCode: str
    Phone: str = None


@dataclass
class Registrant:
    RegistrationNUmber: str
    RegistrationNUmberWithSoNum: str
    Status: str
    EffectiveDate: str
    Type: str
    Prefix: str
    FirstName: str
    MiddleInitials: str
    LastName: str
    Suffix: str
    PositionTitle: str
    PreviousPublicOfficeHolder: str
    PreviousPublicOfficeHoldPosition: str
    PreviousPublicOfficePositionProgramName: str
    PreviousPublicOfficeHoldLastDate: str
    BusinessAddress: BusinessAddress


@dataclass
class Communication:
    PreviousPublicOfficeHolder: str  # Not in the README
    PreviousPublicOfficeHoldPosition: str  # Not in the README
    PreviousPublicOfficePositionProgramName: str  # Not in the README
    PreviousPublicOfficeHoldLastDate: str  # Not in the README
    POH_Office: str
    POH_Type: str  # In the README this is POH_Ty
    POH_Position: str
    POH_Name: str
    CommunicationDate: str
    CommunicationGroupId: str 
    LobbyistNumber: str
    LobbyistType: str
    LobbyistPrefix: str
    LobbyistFirstName: str
    LobbyistMiddleInitials: str
    LobbyistLastName: str
    LobbyistSuffix: str
    LobbyistBusiness: str
    LobbyistPositionTitle: str
    CommunicationMethod: Optional[List[str]] = None  # In the README, this is a string
    LobbyistPublicOfficeHolder: str = None
    LobbyistPreviousPublicOfficeHoldPosition: str = None
    LobbyistPreviousPublicOfficePositionProgramName: str = None
    LobbyistPreviousPublicOfficeHoldLastDate: str = None
    LobbyistBusinessAddress: BusinessAddress = None


@dataclass
class Firm:
    Type: str
    Name: str
    TradeName: str
    FiscalStart: str
    FiscalEnd: str
    Description: str
    BusinessType: str
    BusinessAddress: BusinessAddress


@dataclass
class Grassroot:
    Community: str
    StartDate: str
    EndDate: str
    Target: str


@dataclass
class Beneficiary:
    Type: str
    Name: str
    TradeName: str
    FiscalStart: str
    FiscalEnd: str
    BusinessAddress: BusinessAddress


@dataclass
class Privatefunding:
    Funding: str
    Contact: str
    Agent: str
    AgentContact: str


@dataclass
class POH:
    Name: str
    Office: str
    Title: str
    Type: str



@dataclass
class Lobbyist:
    Number: str
    Prefix: str
    FirstName: str
    MiddleInitials: str
    LastName: str
    Suffix: str
    Business: str
    Type: str


@dataclass
class Meeting:
    Committee: str
    Desc: str
    Date: str
    POHS: Optional[List[POH]] = None
    Lobbyists: Optional[List[Lobbyist]] = None


@dataclass(eq=True, frozen=True)
class Gmtfunding:
    GMTName: str
    Program: str


@dataclass
class SubjectMatter:  # This is SM in the XML,
    SMNumber: str
    Status: str
    Type: str
    # Is the string SubjectMatter in the XMl, I converted it to TBD
    SubjectMatter: List[str]
    SubjectMatterDefinition: str  # This is not in the README
    Particulars: List[str]  # In the README, this is a string
    InitialApprovalDate: str
    EffectiveDate: str
    ProposedStartDate: str
    ProposedEndDate: str
    Registrant: Registrant
    Firms: List[Firm]
    Communications: Optional[List[Communication]] = None
    Grassroots: Optional[List[Grassroot]] = None
    Beneficiaries: Optional[List[Beneficiary]] = None
    Privatefundings: Optional[List[Privatefunding]] = None
    # XML says GMTFUNDINGS, but GMTFUNDINGS and Gmtfundings are both in the XML
    Gmtfundings: Optional[Gmtfunding] = None
    Meetings: Optional[List[Meeting]] = None
