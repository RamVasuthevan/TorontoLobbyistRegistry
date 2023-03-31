from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import Mapped
from sqlalchemy import Table

from lobby import parser, downloader
import pprint as pp
import json
from typing import List, Dict, Any, Union, Optional

Base = declarative_base()

class SubjectMatterToCommunication(Base):
    __tablename__ = "subjectMatter_to_communication"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    communication_id  = Column(Integer, ForeignKey("communication.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="Communications")
    Communication = relationship("Communication")


class SubjectMatterToFirm(Base):
    __tablename__ = "subjectMatter_to_firm"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    firm_id  = Column(Integer, ForeignKey("firm.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="Firms")
    Firm = relationship("Firm")

class SubjectMatterToGrassroot(Base):
    __tablename__ = "subjectMatter_to_grassroot"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    grassroot_id  = Column(Integer, ForeignKey("grassroot.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="Grassroots")
    Grassroot = relationship("Grassroot")

class SubjectMatterToBeneficiary(Base):
    __tablename__ = "subjectMatter_to_beneficiary"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    beneficiary_id  = Column(Integer, ForeignKey("beneficiary.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="Beneficiaries")
    Beneficiary = relationship("Beneficiary")

class SubjectMatterToPrivateFunding(Base):
    __tablename__ = "subjectMatter_to_privateFunding"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    privateFunding_id  = Column(Integer, ForeignKey("private_funding.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="PrivateFundings")
    PrivateFunding = relationship("PrivateFunding")

class SubjectMatterToGmtFunding(Base):
    __tablename__ = "subjectMatter_to_gmtFunding"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    gmtFunding_id  = Column(Integer, ForeignKey("gmt_funding.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="GmtFundings")
    GmtFunding = relationship("GmtFunding")

class SubjectMatterToMeeting(Base):
    __tablename__ = "subjectMatter_to_meeting"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    meeting_id  = Column(Integer, ForeignKey("meeting.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="Meetings")
    Meeting = relationship("Meeting")

class MeetingToPOH(Base):
    __tablename__ = "meeting_to_POH"
    meeting_id  = Column(Integer, ForeignKey("meeting.id"), primary_key=True)
    POH_id = Column(Integer, ForeignKey("poh.id"), primary_key=True)
    Meeting = relationship("Meeting", back_populates="POHS")
    POH = relationship("POH")

class MeetingToLobbyist(Base):
    __tablename__ = "meeting_to_lobbyist"
    meeting_id  = Column(Integer, ForeignKey("meeting.id"), primary_key=True)
    lobbyist_id = Column(Integer, ForeignKey("lobbyist.id"), primary_key=True)
    Meeting = relationship("Meeting", back_populates="Lobbyists")
    Lobbyist = relationship("Lobbyist")

class BusinessAddress(Base):
    __tablename__ = 'business_address'
    id = Column(Integer, primary_key=True)
    AddressLine1 = Column(String)
    AddressLine2 = Column(String)
    City = Column(String)
    Province = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String)

class Registrant(Base):
    __tablename__ = 'registrant'
    id = Column(Integer, primary_key=True)
    RegistrationNUmber = Column(String)
    RegistrationNumberWithSoNum = Column(String)
    Status = Column(String)
    EffectiveDate = Column(String)
    Type = Column(String)
    Prefix = Column(String)
    FirstName = Column(String)
    MiddleInitials = Column(String)
    LastName = Column(String)
    Suffix = Column(String)
    PositionTitle = Column(String)
    PreviousPublicOfficeHolder = Column(String)
    PreviousPublicOfficeHoldPosition = Column(String)
    PreviousPublicOfficePositionProgramName = Column(String)
    PreviousPublicOfficeHoldLastDate = Column(String)
    BusinessAddress = relationship("BusinessAddress", backref=backref("registrant", uselist=False))
    BusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))

class Communication(Base):
    __tablename__ = 'communication'
    id = Column(Integer, primary_key=True)
    PreviousPublicOfficeHolder = Column(String) 
    PreviousPublicOfficeHoldPosition = Column(String)  
    PreviousPublicOfficePositionProgramName = Column(String)
    PreviousPublicOfficeHoldLastDate = Column(String)
    POH_Office  = Column(String)
    POH_Type = Column(String)
    POH_Position = Column(String)
    POH_Name = Column(String)
    CommunicationDate = Column(String)
    CommunicationGroupId = Column(String)
    LobbyistNumber = Column(String)
    LobbyistType = Column(String)
    LobbyistPrefix = Column(String)
    LobbyistFirstName = Column(String)
    LobbyistMiddleInitials = Column(String)
    LobbyistLastName = Column(String)
    LobbyistSuffix = Column(String)
    LobbyistBusiness = Column(String)
    LobbyistPositionTitle = Column(String)
    CommunicationMethod = Column(String)
    LobbyistPublicOfficeHolder = Column(String)
    LobbyistPreviousPublicOfficeHoldPosition = Column(String)
    LobbyistPreviousPublicOfficePositionProgramName = Column(String)
    LobbyistPreviousPublicOfficeHoldLastDate = Column(String)
    LobbyistBusinessAddress = relationship("BusinessAddress", backref=backref("communication", uselist=False))
    LobbyistBusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))

class Firm(Base):
    __tablename__ = 'firm'
    id = Column(Integer, primary_key=True)
    Type = Column(String)
    Name = Column(String)
    TradeName = Column(String)
    FiscalStart = Column(String)
    FiscalEnd = Column(String)
    Description = Column(String)
    BusinessType = Column(String)
    BusinessAddress = relationship("BusinessAddress", backref=backref("firm", uselist=False))
    BusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))

class Grassroot(Base):
    __tablename__ = 'grassroot'
    id = Column(Integer, primary_key=True)
    Community= Column(String)
    StartDate=  Column(String)
    EndDate =Column(String)
    Target= Column(String)

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    id = Column(Integer, primary_key=True)
    Type = Column(String)
    Name = Column(String)
    TradeName = Column(String)
    FiscalStart = Column(String)
    FiscalEnd = Column(String)
    BusinessAddress = relationship("BusinessAddress", backref=backref("beneficiary", uselist=False))
    BusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))

class PrivateFunding(Base):
    __tablename__ = 'private_funding'
    id = Column(Integer, primary_key=True)
    Funding = Column(String)
    Contact = Column(String)
    Agent = Column(String)
    AgentContact = Column(String)

class GmtFunding(Base):
    __tablename__ = 'gmt_funding'
    id = Column(Integer, primary_key=True)
    GMTName = Column(String)
    GMTContact = Column(String)

class POH(Base):
    __tablename__ = 'poh'
    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Office = Column(String)
    Title = Column(String)
    Type = Column(String)

class Meeting(Base):
    __tablename__ = 'meeting'
    id = Column(Integer, primary_key=True)
    Committee = Column(String)
    Desc = Column(String)
    Date = Column(String) 
    POHS : Mapped[List[MeetingToPOH]] = relationship(back_populates="Meeting")
    Lobbyists : Mapped[List[MeetingToLobbyist]] = relationship(back_populates="Meeting")

class Lobbyist(Base):
    __tablename__ = 'lobbyist'
    id = Column(Integer, primary_key=True)
    Number = Column(String)
    Prefix = Column(String)
    FirstName = Column(String)
    MiddleInitials = Column(String)
    LastName = Column(String)
    Suffix = Column(String)
    Business = Column(String)
    Type = Column(String)

class SubjectMatter(Base):
    __tablename__ = 'subject_matter'
    SMNumber = Column(String,primary_key=True)
    Status = Column(String)
    Type = Column(String)
    SubjectMatter = Column(String)
    SubjectMatterDefinition = Column(String)
    Particulars = Column(String)
    InitialApprovalDate = Column(String)
    EffectiveDate = Column(String)
    ProposedStartDate = Column(String)
    ProposedEndDate = Column(String)
    Registrant = relationship("Registrant", backref=backref("subject_matter", uselist=True))
    Registrant_id = Column(Integer, ForeignKey('registrant.id'))
    Firms: Mapped[List[SubjectMatterToFirm]] = relationship(back_populates="SubjectMatter")
    Communications: Mapped[List[SubjectMatterToCommunication]] = relationship(back_populates="SubjectMatter")
    Grassroots: Mapped[List[SubjectMatterToGrassroot]] = relationship(back_populates="SubjectMatter")
    Beneficiaries: Mapped[List[SubjectMatterToBeneficiary]] = relationship(back_populates="SubjectMatter")
    PrivateFundings: Mapped[List[SubjectMatterToPrivateFunding]] = relationship(back_populates="SubjectMatter")
    GmtFundings: Mapped[List[SubjectMatterToGmtFunding]] = relationship(back_populates="SubjectMatter")
    Meetings: Mapped[List[SubjectMatterToMeeting]] = relationship(back_populates="SubjectMatter")

import os
if os.path.exists("TorontoLobbyistRegistry.db"):
    os.remove("TorontoLobbyistRegistry.db")

engine = create_engine("sqlite:///TorontoLobbyistRegistry.db", echo=True, future=True)
Base.metadata.create_all(engine)

lobbyactivity_xml = downloader.Downloader().download_lobbyactivity_xml()
results = parser.Parse(lobbyactivity_xml).get_results_dataclasses()[:100]

with Session(engine) as session:
    for result in results:

        subjectMatter = SubjectMatter(**{key:val for key,val in result.__dict__.items() if key in [c.name for c in SubjectMatter.__table__.columns]})
        registrant = Registrant(**{key:val for key,val in result.Registrant.__dict__.items() if key in [c.name for c in Registrant.__table__.columns]})
        businessAddress = BusinessAddress(**{key:val for key,val in result.Registrant.BusinessAddress.__dict__.items() if key in [c.name for c in BusinessAddress.__table__.columns]})
        firms = [Firm(**{key:val for key,val in firm.__dict__.items() if key in [c.name for c in Firm.__table__.columns]}) for firm in result.Firms]

        firms = []
        subjectmatter_to_firm_associations = []
        for val in result.Firms:
            firm = Firm(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Firm.__table__.columns]})
            subjectmatter_to_firm_association = SubjectMatterToFirm(SubjectMatter=subjectMatter, Firm=firm)
            firms.append(firm)
            subjectmatter_to_firm_associations.append(subjectmatter_to_firm_association)

            firm_businessAddress = BusinessAddress(**{key:val for key,val in val.BusinessAddress.__dict__.items() if key in [c.name for c in BusinessAddress.__table__.columns]})
            firm.BusinessAddress = firm_businessAddress

        if result.Communications is not None:
            communications = []
            subjectMatter_to_communication_associations = []
            for val in result.Communications:
                communication = Communication(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Communication.__table__.columns]})
                subjectMatter_to_communication_association = SubjectMatterToCommunication(SubjectMatter=subjectMatter, Communication=communication)
                communications.append(communication)
                subjectMatter_to_communication_associations.append(subjectMatter_to_communication_association)

                communication_LobbyistBusinessAddress = BusinessAddress(**{key:val for key,val in val.LobbyistBusinessAddress.__dict__.items() if key in [c.name for c in BusinessAddress.__table__.columns]})
                communication.LobbyistBusinessAddress = communication_LobbyistBusinessAddress

                if communication.CommunicationMethod is not None:
                    communication.CommunicationMethod = "TODO"
        
        if result.Grassroots is not None:
            grassroots = []
            subjectMatter_to_grassroot_associations = []
            for val in result.Grassroots:
                grassroot = Grassroot(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Grassroot.__table__.columns]})
                subjectMatter_to_grassroot_association = SubjectMatterToGrassroot(SubjectMatter=subjectMatter, Grassroot=grassroot)
                grassroots.append(grassroot)
                subjectMatter_to_grassroot_associations.append(subjectMatter_to_grassroot_association)
        
        if result.Beneficiaries is not None:
            beneficiaries = []
            subjectMatter_to_beneficiary_associations = []
            for val in result.Beneficiaries:
                beneficiary = Beneficiary(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Beneficiary.__table__.columns]})
                subjectMatter_to_beneficiary_association = SubjectMatterToBeneficiary(SubjectMatter=subjectMatter, Beneficiary=beneficiary)
                beneficiaries.append(beneficiary)
                subjectMatter_to_beneficiary_associations.append(subjectMatter_to_beneficiary_association)

                beneficiary_BusinessAddress = BusinessAddress(**{key:val for key,val in val.BusinessAddress.__dict__.items() if key in [c.name for c in BusinessAddress.__table__.columns]})
                beneficiary.BusinessAddress = beneficiary_BusinessAddress

        if result.Privatefundings is not None:
            privatefundings = []
            subjectMatter_to_privatefunding_associations = []
            for val in result.Privatefundings:
                privatefunding = PrivateFunding(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in PrivateFunding.__table__.columns]})
                subjectMatter_to_privatefunding_association = SubjectMatterToPrivateFunding(SubjectMatter=subjectMatter, PrivateFunding=privatefunding)
                privatefundings.append(privatefunding)
                subjectMatter_to_privatefunding_associations.append(subjectMatter_to_privatefunding_association)

        if result.Gmtfundings is not None:
            gmtfundings = []
            subjectMatter_to_gmtfunding_associations = []
            for val in result.Gmtfundings:
                gmtfunding = GmtFunding(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in GmtFunding.__table__.columns]})
                subjectMatter_to_gmtfunding_association = SubjectMatterToGmtFunding(SubjectMatter=subjectMatter, GmtFunding=gmtfunding)
                gmtfundings.append(gmtfunding)
                subjectMatter_to_gmtfunding_associations.append(subjectMatter_to_gmtfunding_association)
        
        if result.Meetings is not None:
            meetings = []
            subjectMatter_to_meeting_associations = []
            meeting_to_POHS_associations = []
            metting_to_lobbyists_associations = []
            for val in result.Meetings:
                meeting = Meeting(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Meeting.__table__.columns]})
                subjectMatter_to_meeting_association = SubjectMatterToMeeting(SubjectMatter=subjectMatter, Meeting=meeting)
                meetings.append(meeting)
                subjectMatter_to_meeting_associations.append(subjectMatter_to_meeting_association)
                

                if meeting.POHS is not None:
                    for val in meeting.POHS:
                        POH = POH(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in POH.__table__.columns]})
                        meeting_to_POH_association = MeetingToPOH(Meeting=meeting, POH=POH)
                        meeting_to_POHS_associations.append(meeting_to_POH_association)
                
                if meeting.Lobbyists is not None:
                    for val in meeting.Lobbyists:
                        lobbyist = Lobbyist(**{key:val for key,val in val.__dict__.items() if key in [c.name for c in Lobbyist.__table__.columns]})
                        meeting_to_lobbyist_association = MeetingToLobbyist(Meeting=meeting, Lobbyist=lobbyist)
                        metting_to_lobbyists_associations.append(meeting_to_lobbyist_association)
            
        subjectMatter.SubjectMatter = "TODO"
        subjectMatter.Particulars = "TODO"

        session.add(subjectMatter)
        session.add(registrant)
        session.add(businessAddress)
        session.add_all(firms)

        if result.Communications is not None:
            session.add_all(communications)
        if result.Grassroots is not None:
            session.add_all(grassroots)
        if result.Beneficiaries is not None:
            session.add_all(beneficiaries)
        if result.Privatefundings is not None:
            session.add_all(privatefundings)
        if result.Gmtfundings is not None:
            session.add_all(gmtfundings)
        if result.Meetings is not None:
            session.add_all(meetings)

        session.flush()

        subjectMatter.Registrant_id = registrant.id
        registrant.BusinessAddress_id = businessAddress.id

        for firm,subjectMatterToFirm in zip(firms, subjectmatter_to_firm_associations):
            subjectMatterToFirm.Firm_id = firm.id
            subjectMatterToFirm.SubjectMatter_SMNumber = subjectMatter.SMNumber

            firm.BusinessAddress_id = firm.BusinessAddress.id
        
        if result.Communications is not None:
            for communication,subjectMatterToCommunication in zip(communications, subjectMatter_to_communication_associations):
                subjectMatterToCommunication.Communication_id = communication.id
                subjectMatterToCommunication.SubjectMatter_SMNumber = subjectMatter.SMNumber

                communication.BusinessAddress_id = communication.LobbyistBusinessAddress.id
        
        if result.Grassroots is not None:
            for grassroot,subjectMatterToGrassroot in zip(grassroots, subjectMatter_to_grassroot_associations):
                subjectMatterToGrassroot.Grassroot_id = grassroot.id
                subjectMatterToGrassroot.SubjectMatter_SMNumber = subjectMatter.SMNumber
        
        if result.Beneficiaries is not None:
            for beneficiary,subjectMatterToBeneficiary in zip(beneficiaries, subjectMatter_to_beneficiary_associations):
                subjectMatterToBeneficiary.Beneficiary_id = beneficiary.id
                subjectMatterToBeneficiary.SubjectMatter_SMNumber = subjectMatter.SMNumber

                beneficiary.BusinessAddress_id = beneficiary.BusinessAddress.id
        
        if result.Privatefundings is not None:
            for privatefunding,subjectMatterToPrivateFunding in zip(privatefundings, subjectMatter_to_privatefunding_associations):
                subjectMatterToPrivateFunding.Privatefunding_id = privatefunding.id
                subjectMatterToPrivateFunding.SubjectMatter_SMNumber = subjectMatter.SMNumber
        
        if result.Gmtfundings is not None:
            for gmtfunding,subjectMatterToGmtFunding in zip(gmtfundings, subjectMatter_to_gmtfunding_associations):
                subjectMatterToGmtFunding.Gmtfunding_id = gmtfunding.id
                subjectMatterToGmtFunding.SubjectMatter_SMNumber = subjectMatter.SMNumber
        
        if result.Meetings is not None:
            for meeting,subjectMatterToMeeting in zip(meetings, subjectMatter_to_meeting_associations):
                subjectMatterToMeeting.Meeting_id = meeting.id
                subjectMatterToMeeting.SubjectMatter_SMNumber = subjectMatter.SMNumber

            for meeting_to_POHS_association in meeting_to_POHS_associations:
                meeting_to_POHS_association.Meeting_id = meeting_to_POHS_association.Meeting.id
                meeting_to_POHS_association.POHS_id = meeting_to_POHS_association.POHS.id

            for meeting_to_lobbyists_association in metting_to_lobbyists_associations:
                meeting_to_lobbyists_association.Meeting_id = meeting_to_lobbyists_association.Meeting.id
                meeting_to_lobbyists_association.Lobbyist_id = meeting_to_lobbyists_association.Lobbyist.id
        
        session.flush()

    
    session.commit()

