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

import pprint as pp
import json
from typing import List, Dict, Any, Union, Optional
from lobby import downloader, parser
from itertools import chain


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

class SubjectMatterToGroup(Base):
    __tablename__ = "subjectMatter_to_group"
    Subject_matter_SMNumber = Column(String, ForeignKey("subject_matter.SMNumber"), primary_key=True)
    subjectMatterGroup_id  = Column(Integer, ForeignKey("subject_matter_group.id"), primary_key=True)
    SubjectMatter = relationship("SubjectMatter", back_populates="SubjectMatterGroups")
    SubjectMatterGroup = relationship("SubjectMatterGroup")
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

class PreviousPublicOfficeHolder(Base):
    __tablename__ = 'previous_public_office_holder'
    id = Column(Integer, primary_key=True)
    Position = Column(String,)
    PositionProgramName = Column(String)
    HoldLastDate = Column(String)

class BusinessAddress(Base):
    __tablename__ = 'business_address'
    id = Column(Integer, primary_key=True)
    AddressLine1 = Column(String)
    AddressLine2 = Column(String)
    City = Column(String)
    Province = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String,)

class RegistrantStatus(Base):
    __tablename__ = 'registrant_status'
    id = Column(Integer, primary_key=True)
    Status = Column(String)

class RegistrantType(Base):
    __tablename__ = 'registrant_type'
    id = Column(Integer, primary_key=True)
    Type = Column(String)

class RegistrantPrefix(Base):
    __tablename__ = 'registrant_prefix'
    id = Column(Integer, primary_key=True)
    Prefix = Column(String)
class Registrant(Base):
    __tablename__ = 'registrant'
    id = Column(Integer, primary_key=True)
    RegistrationNUmber = Column(String)
    RegistrationNumberWithSoNum = Column(String)
    Status_id = Column(Integer, ForeignKey('registrant_status.id'))
    EffectiveDate = Column(String)
    Type = Column(String)
    Prefix = Column(String)
    FirstName = Column(String)
    MiddleInitials = Column(String)
    LastName = Column(String)
    Suffix = Column(String)
    PositionTitle = Column(String)
    PreviousPublicOfficeHolder = relationship("PreviousPublicOfficeHolder", backref=backref("registrant", uselist=False))
    PreviousPublicOfficeHolder_id = Column(Integer, ForeignKey('previous_public_office_holder.id'), nullable=True)
    BusinessAddress = relationship("BusinessAddress", backref=backref("registrant", uselist=False))
    BusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))

class CommunicationMethod(Base):
    __tablename__ = 'communication_method'
    id = Column(Integer, primary_key=True)
    Method = Column(String)
class Communication(Base):
    __tablename__ = 'communication'
    id = Column(Integer, primary_key=True)
    PreviousPublicOfficeHolder = relationship("PreviousPublicOfficeHolder", backref=backref("communication", uselist=False))
    PreviousPublicOfficeHolder_id = Column(Integer, ForeignKey('previous_public_office_holder.id'), nullable=True)
    POH = relationship("POH", backref=backref("communication", uselist=False))   
    POH_id = Column(Integer, ForeignKey('poh.id'))
    CommunicationDate = Column(String)
    CommunicationGroupId = Column(String)
    Lobbyist = relationship("Lobbyist", backref=backref("communication", uselist=False))
    Lobbyist_id = Column(Integer, ForeignKey('lobbyist.id'))
    CommunicationMethod = relationship("CommunicationMethod", backref=backref("communication", uselist=False))
    CommunicationMethod_id = Column(Integer, ForeignKey('communication_method.id'))
    LobbyistBusinessAddress = relationship("BusinessAddress", backref=backref("communication", uselist=False))
    LobbyistBusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))
class FirmType(Base):
    __tablename__ = 'firm_type'
    id = Column(Integer, primary_key=True)
    Type = Column(String)

class FirmBusinessType(Base):
    __tablename__ = 'firm_business_type'
    id = Column(Integer, primary_key=True)
    Type = Column(String)

class Firm(Base):
    __tablename__ = 'firm'
    id = Column(Integer, primary_key=True)
    Type = relationship("FirmType", backref=backref("firm", uselist=False))
    Type_id = Column(Integer, ForeignKey('firm_type.id'))
    Name = Column(String)
    TradeName = Column(String)
    FiscalStart = Column(String)
    FiscalEnd = Column(String)
    Description = Column(String)
    BusinessType = relationship("FirmBusinessType", backref=backref("firm", uselist=False))
    BusinessType_id = Column(Integer, ForeignKey('firm_business_type.id'))
    BusinessAddress = relationship("BusinessAddress", backref=backref("firm", uselist=False))
    BusinessAddress_id = Column(Integer, ForeignKey('business_address.id'))
class Grassroot(Base):
    __tablename__ = 'grassroot'
    id = Column(Integer, primary_key=True)
    Community= Column(String)
    StartDate=  Column(String)
    EndDate =Column(String)
    Target= Column(String)

class BeneficiaryType(Base):
    __tablename__ = 'beneficiary_type'
    id = Column(Integer, primary_key=True)
    Type = Column(String)

class Beneficiary(Base):
    __tablename__ = 'beneficiary'
    id = Column(Integer, primary_key=True)
    Type = relationship("BeneficiaryType", backref=backref("beneficiary", uselist=False))
    Type_id = Column(Integer, ForeignKey('beneficiary_type.id'))
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
    Program = Column(String)
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

class LobbyistType(Base):
    __tablename__ = 'lobbyist_type'
    id = Column(Integer, primary_key=True)
    Type = Column(String)
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

class SubjectMatterStatuses(Base):
    __tablename__ = 'subject_matter_statuses'
    id = Column(Integer, primary_key=True)
    Status = Column(String)
class SubjectMatterTypes(Base):
    __tablename__ = 'subject_matter_types'
    id = Column(Integer, primary_key=True)
    Type = Column(String)

class SubjectMatterGroup(Base):
    __tablename__ = 'subject_matter_group'
    id = Column(Integer, primary_key=True)
    Group = Column(String)

class SubjectMatterDefinition(Base):
    __tablename__ = 'subject_matter_definition'
    id = Column(Integer, primary_key=True)
    Definition = Column(String)
class SubjectMatter(Base):
    __tablename__ = 'subject_matter'
    SMNumber: Mapped[int] = Column(String,primary_key=True)
    status: Mapped[] = relationship("SubjectMatterStatuses", backref=backref("subject_matter", uselist=False)) #Fix me should be uppercase
    Status_id = Column(Integer, ForeignKey('subject_matter_statuses.id'))
    Type = relationship("SubjectMatterTypes", backref=backref("subject_matter", uselist=False))
    Type_id = Column(Integer, ForeignKey('subject_matter_types.id'))
    SubjectMatterGroups: Mapped[List[SubjectMatterToGroup]] = relationship(back_populates="SubjectMatter")
    SubjectMatterDefinition = relationship("SubjectMatterDefinition", backref=backref("subject_matter", uselist=True))
    SubjectMatterDefinition_id = Column(Integer, ForeignKey('subject_matter_definition.id'))
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

def get_firm_types(results):
    firm_types = set()
    isNone = False
    for result in results:
        for firms in result.Firms:
            if firms.Type is None:
                isNone = True
            else:
                firm_types.add(firms.Type)
    firm_types = sorted(list(firm_types))
    if isNone:
        firm_types.append(None)
    return firm_types

def get_firm_bussiness_type(results):
    firm_bussiness_type = set()
    isNone = False
    for result in results:
        if result.Firms is not None:
            for firm in result.Firms:
                if firm.BusinessType is None:
                    isNone = True
                else:
                    firm_bussiness_type.add(firm.BusinessType)
    firm_bussiness_type = sorted(list(firm_bussiness_type))
    if isNone:
        firm_bussiness_type.append(None)
    return firm_bussiness_type

def get_lobbist_types(results):
    lobbyist_types = set()
    isNone = False
    for result in results:
        if result.Meetings is not None:
            for meeting in result.Meetings:
                if meeting.Lobbyists is not None:
                    for lobbyist in meeting.Lobbyists:
                        if lobbyist.Type is None:
                            isNone = True
                        else:
                            lobbyist_types.add(lobbyist.Type)
        if result.Communications is not None:
            for communication in result.Communications:
                if communication.LobbyistType is None:
                    isNone = True
                else:
                    lobbyist_types.add(communication.LobbyistType)
    lobbyist_types = sorted(list(lobbyist_types))
    if isNone:
        lobbyist_types.append(None)
    return lobbyist_types

def get_beneficiary_types(results):
    beneficiary_types = set()
    isNone = False
    for result in results:
        if result.Beneficiaries is not None:
            for beneficiary in result.Beneficiaries:
                if beneficiary.Type is None:
                    isNone = True
                else:
                    beneficiary_types.add(beneficiary.Type)
    beneficiary_types = sorted(list(beneficiary_types))
    if isNone:
        beneficiary_types.append(None)
    return beneficiary_types

def clean_PreviousPublicOfficeHolder(val):
    if val.PreviousPublicOfficeHolder in  [None,"No","no"]: 
        #TODO Look into this
        #if val.PreviousPublicOfficeHoldPosition is not  None and val.PreviousPublicOfficeHoldLastDate is not None:
        #    raise ValueError(f"PreviousPublicOfficeHolder is falsey but PreviousPublicOfficeHoldPosition and PreviousPublicOfficeHoldLastDate are not None: {communication.PreviousPublicOfficeHoldPosition} {communication.PreviousPublicOfficeHoldLastDate}")
        return False
    elif val.PreviousPublicOfficeHolder in ["Yes","yes"]:
        return True
    raise ValueError(f"Unexpected value for PreviousPublicOfficeHolder: {val.PreviousPublicOfficeHolder}")

if __name__ == "__main__":
    import os
    if os.path.exists("TorontoLobbyistRegistry1.db"):
        os.remove("TorontoLobbyistRegistry1.db")
        pass

    engine = create_engine("sqlite:///TorontoLobbyistRegistry1.db", echo=False, future=True)
    Base.metadata.create_all(engine)

    lobbyactivity_xml = downloader.Downloader().download_lobbyactivity_xml()
    results = parser.Parse(lobbyactivity_xml).get_results_dataclasses()

    with Session(engine) as (session):
        for status in sorted(list(set(result.Status for result in results))):
            session.add(SubjectMatterStatuses(Status=status))

        for type in sorted(list(set(result.Type for result in results))):
            session.add(SubjectMatterTypes(Type=type))
        
        for group in sorted(list(set(chain.from_iterable(result.SubjectMatter for result in results)))):
            session.add(SubjectMatterGroup(Group=group))
        

        for definition in sorted(list(set(result.SubjectMatterDefinition for result in results)), key=lambda x: (x is None, x)):
            session.add(SubjectMatterDefinition(Definition=definition))
        
        for status in sorted(list(set(result.Registrant.Status for result in results))):
            session.add(RegistrantStatus(Status=status))
        
        for type in sorted(list(set(result.Registrant.Type for result in results))):
            session.add(RegistrantType(Type=type))
        
        for prefix in sorted(list(set(result.Registrant.Prefix for result in results)), key=lambda x: (x is None, x)):
            session.add(RegistrantPrefix(Prefix=prefix))
        
        for firmType in get_firm_types(results):
            session.add(FirmType(Type=firmType))
        
        for firm_bussiness_type in get_firm_bussiness_type(results):
            session.add(FirmBusinessType(Type=firm_bussiness_type))

        for lobbyistType in get_lobbist_types(results):
            session.add(LobbyistType(Type=lobbyistType))
        
        for beneficiaryType in get_beneficiary_types(results):
            session.add(BeneficiaryType(Type=beneficiaryType))
        
        session.commit()

    with Session(engine) as (session):
        
        for idx,result in enumerate(results):
            print(f"{idx+1}/{len(results)}")
            
            subjectMatter = SubjectMatter()
            subjectMatter.SMNumber = result.SMNumber
            subjectMatter.Status = session.query(SubjectMatterStatuses).filter(SubjectMatterStatuses.Status == result.Status).one()
            subjectMatter.Status_id = subjectMatter.Status.id
            subjectMatter.Type = session.query(SubjectMatterTypes).filter(SubjectMatterTypes.Type == result.Type).one()
            subjectMatter.Type_id = subjectMatter.Type.id

            for group in result.SubjectMatter:
                subjectMatterGroup = session.query(SubjectMatterGroup).filter(SubjectMatterGroup.Group == group).one()
                subjectMatterToGroup = SubjectMatterToGroup(Subject_matter_SMNumber = subjectMatter.SMNumber, subjectMatterGroup_id = subjectMatterGroup.id, SubjectMatter = subjectMatter, SubjectMatterGroup = subjectMatterGroup)
                subjectMatter.SubjectMatterGroups.append(subjectMatterToGroup)
                session.add(subjectMatterGroup)
                session.add(subjectMatterToGroup)
                session.flush()
                subjectMatterToGroup.Subject_matter_SMNumber = subjectMatter.SMNumber
                subjectMatterToGroup.subjectMatterGroup_id = subjectMatterGroup.id
            
            subjectMatter.SubjectMatterDefinition = session.query(SubjectMatterDefinition).filter(SubjectMatterDefinition.Definition == result.SubjectMatterDefinition).one()
            subjectMatter.SubjectMatterDefinition_id = subjectMatter.SubjectMatterDefinition.id
            
            subjectMatter.Particulars = result.Particulars
            subjectMatter.InitialApprovalDate = result.InitialApprovalDate
            subjectMatter.EffectiveDate = result.EffectiveDate
            subjectMatter.ProposedStartDate = result.ProposedStartDate
            subjectMatter.ProposedEndDate = result.ProposedEndDate
            
            registrant = Registrant()
            registrant.RegistrationNUmber = result.Registrant.RegistrationNUmber
            registrant.RegistrationNUmberWithSoNum = result.Registrant.RegistrationNUmberWithSoNum
            registrant.Status = session.query(RegistrantStatus).filter(RegistrantStatus.Status == result.Registrant.Status).one().id
            registrant.EffectiveDate = result.Registrant.EffectiveDate
            registrant.Type = session.query(RegistrantType).filter(RegistrantType.Type == result.Registrant.Type).one().id
            registrant.Prefix = session.query(RegistrantPrefix).filter(RegistrantPrefix.Prefix == result.Registrant.Prefix).one().id
            registrant.FirstName = result.Registrant.FirstName
            registrant.MiddleInitials = result.Registrant.MiddleInitials
            registrant.LastName = result.Registrant.LastName
            registrant.Suffix = result.Registrant.Suffix
            registrant.PositionTitle = result.Registrant.PositionTitle
            if clean_PreviousPublicOfficeHolder(result.Registrant):
                        registrant.PreviousPublicOfficeHolder = PreviousPublicOfficeHolder()
                        registrant.PreviousPublicOfficeHolder.Position = result.Registrant.PreviousPublicOfficeHoldPosition
                        registrant.PreviousPublicOfficeHolder.PositionProgramName = result.Registrant.PreviousPublicOfficePositionProgramName
                        registrant.PreviousPublicOfficeHolder.HoldLastDate = result.Registrant.PreviousPublicOfficeHoldLastDate
                        session.add(registrant.PreviousPublicOfficeHolder)
                        session.flush()
                        registrant.PreviousPublicOfficeHolder_id = registrant.PreviousPublicOfficeHolder.id
            registrant.BusinessAddress = session.query(BusinessAddress).filter(BusinessAddress.AddressLine1 == result.Registrant.BusinessAddress.AddressLine1).first()
            if registrant.BusinessAddress is None:
                registrant.BusinessAddress = BusinessAddress(AddressLine1=result.Registrant.BusinessAddress.AddressLine1,AddressLine2=result.Registrant.BusinessAddress.AddressLine2,City=result.Registrant.BusinessAddress.City,Province=result.Registrant.BusinessAddress.Province,Country=result.Registrant.BusinessAddress.Country,PostalCode=result.Registrant.BusinessAddress.PostalCode,Phone=result.Registrant.BusinessAddress.Phone)
                session.add(registrant.BusinessAddress)
                session.flush()
            registrant.BusinessAddress_id = registrant.BusinessAddress.id
            subjectMatter.Registrant = registrant
            subjectMatter.Registrant_id = subjectMatter.Registrant.id
            
            businessAddress = session.query(BusinessAddress).filter(BusinessAddress.AddressLine1 == result.Registrant.BusinessAddress.AddressLine1).first()  
            if businessAddress is None:
                businessAddress = BusinessAddress(AddressLine1=result.Registrant.BusinessAddress.AddressLine1,AddressLine2=result.Registrant.BusinessAddress.AddressLine2,City=result.Registrant.BusinessAddress.City,Province=result.Registrant.BusinessAddress.Province,Country=result.Registrant.BusinessAddress.Country,PostalCode=result.Registrant.BusinessAddress.PostalCode,Phone=result.Registrant.BusinessAddress.Phone)
                session.add(businessAddress)
                session.flush()
            registrant.BusinessAddress_id = businessAddress.id  

            for val in result.Firms:            
                firm = Firm()
                firm.Type_id = session.query(FirmType).filter(FirmType.Type == val.Type).one().id
                firm.Name = val.Name
                firm.TradeName = val.TradeName
                firm.FiscalStart = val.FiscalStart
                firm.FiscalEnd = val.FiscalEnd
                firm.Description = val.Description
                firm.BusinessType_id = session.query(FirmBusinessType).filter(FirmBusinessType.Type == val.BusinessType).one().id
                firm.BusinessAddress = session.query(BusinessAddress).filter(BusinessAddress.AddressLine1 == val.BusinessAddress.AddressLine1).first()
                if firm.BusinessAddress is None:
                    firm.BusinessAddress = BusinessAddress(AddressLine1=val.BusinessAddress.AddressLine1,AddressLine2=val.BusinessAddress.AddressLine2,City=val.BusinessAddress.City,Province=val.BusinessAddress.Province,Country=val.BusinessAddress.Country,PostalCode=val.BusinessAddress.PostalCode,Phone=val.BusinessAddress.Phone)
                    session.add(firm.BusinessAddress)
                    session.flush()
                firm.BusinessAddress_id = firm.BusinessAddress.id

                subjectmatter_to_firm_association = SubjectMatterToFirm(SubjectMatter=subjectMatter, Firm=firm)
                session.add(firm)
                session.add(subjectmatter_to_firm_association)
                session.flush()
                subjectmatter_to_firm_association.firm_id = firm.id
                subjectmatter_to_firm_association.Subject_matter_SMNumber = subjectMatter.SMNumber

            if result.Communications is not None:
                for val in result.Communications:
                    communication = Communication()
                    if clean_PreviousPublicOfficeHolder(val):
                        communication.PreviousPublicOfficeHolder = PreviousPublicOfficeHolder()
                        communication.PreviousPublicOfficeHolder.PreviousPublicOfficeHolder = val.PreviousPublicOfficeHolder
                        communication.PreviousPublicOfficeHolder.PreviousPublicOfficeHoldPosition = val.PreviousPublicOfficeHoldPosition
                        communication.PreviousPublicOfficeHolder.PreviousPublicOfficePositionProgramName = val.PreviousPublicOfficePositionProgramName
                        communication.PreviousPublicOfficeHolder.PreviousPublicOfficeHoldLastDate = val.PreviousPublicOfficeHoldLastDate
                        session.add(communication.PreviousPublicOfficeHolder)
                        session.flush()
                        communication.PreviousPublicOfficeHolder_id = communication.PreviousPublicOfficeHolder.id

                    communication.POH = POH()
                    communication.POH.Office = val.POH_Office
                    communication.POH.Type = val.POH_Type
                    communication.POH.Position = val.POH_Position
                    communication.POH.Name = val.POH_Name
                    session.add(communication.POH)
                    session.flush()
                    communication.POH_id = communication.POH.id

                    communication.CommunicationDate = val.CommunicationDate
                    communication.CommunicationGroupId = val.CommunicationGroupId

                    communication.Lobbyist = Lobbyist()
                    communication.Lobbyist.Number = val.LobbyistNumber
                    communication.Lobbyist.Type = session.query(LobbyistType).filter(LobbyistType.Type == val.LobbyistType).one().id
                    communication.Lobbyist.Prefix = val.LobbyistPrefix
                    communication.Lobbyist.LobbyistFirstName = val.LobbyistFirstName
                    communication.Lobbyist.LobbyistMiddleInitials = val.LobbyistMiddleInitials
                    communication.Lobbyist.LobbyistLastName = val.LobbyistLastName
                    communication.Lobbyist.LobbyistSuffix = val.LobbyistSuffix
                    session.add(communication.Lobbyist)
                    session.flush()
                    communication.Lobbyist_id = communication.Lobbyist.id 

                    if val.LobbyistPublicOfficeHolder is not None or val.LobbyistPreviousPublicOfficeHoldPosition is not None or val.LobbyistPreviousPublicOfficePositionProgramName is not None or val.LobbyistPreviousPublicOfficeHoldLastDate is not None:
                        raise ValueError("Error: LobbyistPublicOfficeHolder, LobbyistPreviousPublicOfficeHoldPosition, LobbyistPreviousPublicOfficePositionProgramName, LobbyistPreviousPublicOfficeHoldLastDate is not None")
                    
                    communication.LobbyistBusinessAddress = BusinessAddress()
                    communication.LobbyistBusinessAddress.AddressLine1 = val.LobbyistBusinessAddress.AddressLine1
                    communication.LobbyistBusinessAddress.AddressLine2 = val.LobbyistBusinessAddress.AddressLine2
                    communication.LobbyistBusinessAddress.City = val.LobbyistBusinessAddress.City
                    communication.LobbyistBusinessAddress.Province = val.LobbyistBusinessAddress.Province
                    communication.LobbyistBusinessAddress.Country = val.LobbyistBusinessAddress.Country
                    communication.LobbyistBusinessAddress.PostalCode = val.LobbyistBusinessAddress.PostalCode
                    communication.LobbyistBusinessAddress.Phone = val.LobbyistBusinessAddress.Phone
                    session.add(communication.LobbyistBusinessAddress)
                    session.flush()
                    communication.LobbyistBusinessAddress_id = communication.LobbyistBusinessAddress.id

                    subjectMatter_to_communication_association = SubjectMatterToCommunication(SubjectMatter=subjectMatter, Communication=communication)
                    session.add(communication)
                    session.add(subjectMatter_to_communication_association)
                    session.flush()
                    subjectMatter_to_communication_association.Communication_id = communication.id
                    subjectMatter_to_communication_association.Subject_matter_SMNumber = subjectMatter.SMNumber

            if result.Grassroots is not None:

                for val in result.Grassroots:
                    grassroot = Grassroot()
                    grassroot.Community = val.Community
                    grassroot.StartDate = val.StartDate
                    grassroot.EndDate = val.EndDate
                    grassroot.Target = val.Target
                    subjectMatter_to_grassroot_association = SubjectMatterToGrassroot(SubjectMatter=subjectMatter, Grassroot=grassroot)
                    session.add(grassroot)
                    session.add(subjectMatter_to_grassroot_association)
                    session.flush()
                    subjectMatter_to_grassroot_association.grassroot_id = grassroot.id
                    subjectMatter_to_grassroot_association.Subject_matter_SMNumber = subjectMatter.SMNumber
            
            if result.Beneficiaries is not None:
                for val in result.Beneficiaries:
                    beneficiary = Beneficiary()
                    beneficiary.Type_id = session.query(BeneficiaryType).filter(BeneficiaryType.Type == val.Type).one().id
                    beneficiary.Name = val.Name
                    beneficiary.TradeName = val.TradeName
                    beneficiary.FiscalStart = val.FiscalStart
                    beneficiary.FiscalEnd = val.FiscalEnd

                    subjectMatter_to_beneficiary_association = SubjectMatterToBeneficiary(SubjectMatter=subjectMatter, Beneficiary=beneficiary)

                    beneficiary.BusinessAddress = BusinessAddress()
                    beneficiary.BusinessAddress.AddressLine1 = val.BusinessAddress.AddressLine1
                    beneficiary.BusinessAddress.AddressLine2 = val.BusinessAddress.AddressLine2
                    beneficiary.BusinessAddress.City = val.BusinessAddress.City
                    beneficiary.BusinessAddress.Province = val.BusinessAddress.Province
                    beneficiary.BusinessAddress.Country = val.BusinessAddress.Country
                    beneficiary.BusinessAddress.PostalCode = val.BusinessAddress.PostalCode
                    beneficiary.BusinessAddress.Phone = val.BusinessAddress.Phone

                    subjectMatter_to_beneficiary_association = SubjectMatterToBeneficiary(SubjectMatter=subjectMatter, Beneficiary=beneficiary)
                    session.add(subjectMatter_to_beneficiary_association)
                    session.add(beneficiary)
                    session.flush()
                    beneficiary.BusinessAddress_id = beneficiary.BusinessAddress.id
                    subjectMatter_to_beneficiary_association.Beneficiary_id = beneficiary.id

            if result.Privatefundings is not None:
                for val in result.Privatefundings:
                    privatefunding = PrivateFunding(Funding=val.Funding,Contact=val.Contact,Agent=val.Agent,AgentContact=val.AgentContact)
                    subjectMatter_to_privatefunding_association = SubjectMatterToPrivateFunding(SubjectMatter=subjectMatter, PrivateFunding=privatefunding)
                    session.add(privatefunding)
                    session.add(subjectMatter_to_privatefunding_association)
                    session.flush()

            if result.Gmtfundings is not None:
                for val in result.Gmtfundings:
                    gmtfunding = GmtFunding(GMTName=val.GMTName, Program=val.Program)
                    subjectMatter_to_gmtfunding_association = SubjectMatterToGmtFunding(SubjectMatter=subjectMatter, GmtFunding=gmtfunding)
                    session.add(gmtfunding)
                    session.add(subjectMatter_to_gmtfunding_association)
                    session.flush()
                    subjectMatter_to_gmtfunding_association.GmtFunding_id = gmtfunding.id
                    subjectMatter_to_gmtfunding_association.Subject_matter_SMNumber = subjectMatter.SMNumber
            
            if result.Meetings is not None:
                for val in result.Meetings:
                    meeting = Meeting()
                    meeting.Committee = val.Committee
                    meeting.Desc = val.Desc
                    meeting.Date = val.Date
                                    
                    if meeting.POHS is not None:
                        for val in meeting.POHS:
                            poh = POH()
                            poh.Name = val.Name
                            poh.Office = val.Office
                            poh.Title = val.Title
                            poh.Type = val.Type
                            meeting_to_POH_association = MeetingToPOH(Meeting=meeting, POH=POH)
                            session.add(poh)
                            session.add(meeting_to_POH_association)
                            session.flush()
                            meeting_to_POH_association.POH_id = poh.id
                            meeting_to_POH_association.Meeting_id = meeting.id        
                    
                    if meeting.Lobbyists is not None:
                        for val in meeting.Lobbyists:
                            lobbyist = Lobbyist()
                            lobbyist.Number = val.Number
                            lobbyist.Prefix = val.Prefix
                            lobbyist.FirstName = val.FirstName
                            lobbyist.MiddleInitials = val.MiddleInitials
                            lobbyist.LastName = val.LastName
                            lobbyist.Suffix = val.Suffix
                            lobbyist.Business = val.Business
                            lobbyist.Type = session.query(LobbyistType).filter(LobbyistType.Type == val.Type).one().id

                            meeting_to_lobbyist_association = MeetingToLobbyist(Meeting=meeting, Lobbyist=lobbyist)
                            session.add(lobbyist)
                            session.add(meeting_to_lobbyist_association)
                            session.flush()
                            meeting_to_lobbyist_association.Lobbyist_id = lobbyist.id
                            meeting_to_lobbyist_association.Meeting_id = meeting.id
                    
                    subjectMatter_to_meeting_association = SubjectMatterToMeeting(SubjectMatter=subjectMatter, Meeting=meeting)
                    session.add(meeting)
                    session.add(subjectMatter_to_meeting_association)
                    session.flush()
                    subjectMatter_to_meeting_association.Subject_matter_SMNumber = subjectMatter.SMNumber
                    subjectMatter_to_meeting_association.Meeting_id = meeting.id
            
            session.add(subjectMatter)
            session.flush()    
        session.commit()

    import json
    from sqlalchemy.orm import class_mapper
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.orm import joinedload, Load

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                fields = {}
                for prop in class_mapper(obj.__class__).iterate_properties:
                    field = prop.key
                    data = obj.__getattribute__(field)
                    try:
                        if hasattr(data, '__iter__') and not isinstance(data, str):
                            data = [self.default(item) for item in data]
                        else:
                            json.dumps(data)
                        fields[field] = data
                    except TypeError:
                        fields[field] = None
                return fields
            return json.JSONEncoder.default(self, obj)



    import yaml
    from sqlalchemy.orm import selectinload
    import json

    def object_to_dict(obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for prop in class_mapper(obj.__class__).iterate_properties:
                field = prop.key
                if field == '_sa_instance_state':  # Ignore the _sa_instance_state field
                    continue
                data = getattr(obj, field)
                if isinstance(data, (int, float, str, bool, type(None))):
                    fields[field] = data
                elif isinstance(data.__class__, DeclarativeMeta):
                    fields[field] = object_to_dict(data)
                elif hasattr(data, '__iter__') and not isinstance(data, str):
                    fields[field] = [object_to_dict(item) for item in data if isinstance(item.__class__, DeclarativeMeta)]
            return fields
        return None


            
    def SubjectMatterPage(subjectmatter:SubjectMatter):
        result = {}
        result['SMNumber'] = subjectmatter.SMNumber
        result['Status'] = subjectmatter.status.Status
        #result['Type'] = subjectmatter.Type.Type
        result['SubjectMatterGroups'] = [group.SubjectMatterGroup.Group for group in subjectmatter.SubjectMatterGroups]
        result['Definition'] = subjectmatter.SubjectMatterDefinition.Definition
        result['Particulars'] = subjectmatter.Particulars
        result['Registrant'] = {}
        result['Registrant']['RegistrationNUmber'] = subjectmatter.Registrant.RegistrationNUmber
        result['Registrant']['Type'] = subjectmatter.Registrant.Type
        result['Registrant']['Prefix'] = subjectmatter.Registrant.Prefix
        result['Registrant']['FirstName'] = subjectmatter.Registrant.FirstName
        result['Registrant']['MiddleInitials'] = subjectmatter.Registrant.MiddleInitials
        result['Registrant']['LastName'] = subjectmatter.Registrant.LastName
        result['Registrant']['Suffix'] = subjectmatter.Registrant.Suffix
        result['Registrant']['PositionTitle'] = subjectmatter.Registrant.PositionTitle
        result['Firms'] = []

        return result