from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect as sqlalchemy_inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import Table

import pprint as pp
import json
from typing import List, Dict, Any, Union, Optional
from .downloader import *
from .lobbyParser import *
from itertools import chain
import os

class Base(DeclarativeBase):
    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in sqlalchemy_inspect(obj).mapper.column_attrs}
    
    def as_dict(self):
        data = {c.key: getattr(self, c.key) for c in sqlalchemy_inspect(self).mapper.column_attrs}

        # Include related objects
        for name, relation in sqlalchemy_inspect(self).mapper.relationships.items():
            related_objects = getattr(self, name)
            if relation.uselist:
                data[name] = [self.object_as_dict(o) for o in related_objects] if related_objects else []
            else:
                data[name] = self.object_as_dict(related_objects) if related_objects else None

        return data


class PreviousPublicOfficeHolder(Base):
    __tablename__ = 'previous_public_office_holder'
    id: Mapped[int] = mapped_column(primary_key=True)
    Position: Mapped[str] = mapped_column()
    PositionProgramName: Mapped[str] = mapped_column()
    HoldLastDate: Mapped[str] = mapped_column()

class BusinessAddress(Base): # Find where the null address is coming from
    __tablename__ = 'business_address'
    id: Mapped[int] = mapped_column(primary_key=True)
    AddressLine1: Mapped[str] = mapped_column(nullable=True)
    AddressLine2: Mapped[str] = mapped_column(nullable=True)
    City: Mapped[str] = mapped_column(nullable=True)
    Province: Mapped[str] = mapped_column(nullable=True)
    Country: Mapped[str] = mapped_column(nullable=True)
    PostalCode: Mapped[str] = mapped_column(nullable=True)
    Phone: Mapped[str] = mapped_column(nullable=True)

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
    id: Mapped[int] = mapped_column(primary_key=True)
    RegistrationNUmber: Mapped[String] = mapped_column(String)
    RegistrationNumberWithSoNum: Mapped[String] = mapped_column(String, nullable=True)

    Status_id : Mapped[int] = mapped_column(ForeignKey('registrant_status.id'), nullable=True)
    Status: Mapped["RegistrantStatus"] = relationship()
    
    EffectiveDate = mapped_column(String, nullable=True)

    Type_id: Mapped[int] = mapped_column(ForeignKey('registrant_type.id'), nullable=True)
    Type: Mapped["RegistrantType"] = relationship()

    Prefix_id: Mapped[int] = mapped_column(ForeignKey('registrant_prefix.id'), nullable=True)
    Prefix: Mapped["RegistrantPrefix"] = relationship()

    FirstName = mapped_column(String, nullable=True)
    MiddleInitials = mapped_column(String, nullable=True)
    LastName = mapped_column(String, nullable=True)
    Suffix = mapped_column(String, nullable=True)
    PositionTitle = mapped_column(String, nullable=True)

    PreviousPublicOfficeHolder_id: Mapped[int] = mapped_column(ForeignKey('previous_public_office_holder.id'), nullable=True) 
    PreviousPublicOfficeHolder: Mapped["PreviousPublicOfficeHolder"] = relationship()

    BusinessAddress_id: Mapped[int] = mapped_column(ForeignKey('business_address.id'), nullable=True)
    BusinessAddress: Mapped["BusinessAddress"] = relationship()

class CommunicationMethod(Base):
    __tablename__ = 'communication_method'
    id = Column(Integer, primary_key=True)
    Method = Column(String)

class Communication(Base):
    __tablename__ = 'communication'
    id: Mapped[int] = mapped_column(primary_key=True)

    PreviousPublicOfficeHolder_id : Mapped[int] = mapped_column(ForeignKey('previous_public_office_holder.id'), nullable=True)
    PreviousPublicOfficeHolder: Mapped["PreviousPublicOfficeHolder"] = relationship()

    POH_id: Mapped[int] = mapped_column(ForeignKey('poh.id'), nullable=True)
    POH: Mapped["POH"] = relationship()

    CommunicationDate = mapped_column(String, nullable=True)
    CommunicationGroupId = mapped_column(String, nullable=True)

    Lobbyist_id: Mapped[int] = mapped_column(ForeignKey('lobbyist.id'), nullable=True)
    Lobbyist: Mapped["Lobbyist"] = relationship()

    communicationMethod_id: Mapped[int] = mapped_column(ForeignKey('communication_method.id'), nullable=True)
    communicationMethod: Mapped["CommunicationMethod"] = relationship()

    LobbyistBussinessAddress_id: Mapped[int] = mapped_column(ForeignKey('business_address.id'), nullable=True)
    LobbyistBussinessAddress: Mapped["BusinessAddress"] = relationship()

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
    id: Mapped[int] = mapped_column(primary_key=True)

    Type_id: Mapped[int] = mapped_column(ForeignKey('beneficiary_type.id'))
    Type: Mapped["BeneficiaryType"] = relationship()

    Name: Mapped[str] = mapped_column(String, nullable=True)
    TradeName: Mapped[str] = mapped_column(String, nullable=True)
    FiscalStart: Mapped[str] = mapped_column(String, nullable=True)
    FiscalEnd: Mapped[str] = mapped_column(String, nullable=True)

    BusinessAddress_id: Mapped[int] = mapped_column(ForeignKey('business_address.id'))
    BusinessAddress: Mapped["BusinessAddress"] = relationship()

class PrivateFunding(Base):
    __tablename__ = 'private_funding'
    id: Mapped[int] = mapped_column(primary_key=True)
    Funding: Mapped[str] = mapped_column(String, nullable=True)
    Contact: Mapped[str] = mapped_column(String, nullable=True)
    Agent: Mapped[str] = mapped_column(String, nullable=True)
    AgentContact: Mapped[str] = mapped_column(String, nullable=True)

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

    Type_id: Mapped[int] = mapped_column(ForeignKey('lobbyist_type.id'))
    Type: Mapped["LobbyistType"] = relationship()

meeting_poh_association_table = Table('meeting_poh_association', Base.metadata,
    Column('meeting_id', Integer, ForeignKey('meeting.id')),
    Column('poh_id', Integer, ForeignKey('poh.id'))
)
meeting_lobbyist_association_table = Table('meeting_lobbyist_association', Base.metadata,
    Column('meeting_id', Integer, ForeignKey('meeting.id')),
    Column('lobbyist_id', Integer, ForeignKey('lobbyist.id'))
)
class Meeting(Base):
    __tablename__ = 'meeting'
    id: Mapped[int] = mapped_column(primary_key=True)
    Committee: Mapped[str] = mapped_column(String)
    Desc: Mapped[str] = mapped_column(String, nullable=True)
    Date: Mapped[str] = mapped_column(String)

    POHS: Mapped[List[POH]] = relationship(secondary=meeting_poh_association_table)

    Lobbyists: Mapped[List[Lobbyist]] = relationship(secondary=meeting_lobbyist_association_table)

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
    id: Mapped[int] = mapped_column(primary_key=True)
    Definition: Mapped[str] = mapped_column(String, nullable=True)

subjectmatter_group_association_table = Table('subject_matter_to_group', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('subject_matter_group_id', Integer, ForeignKey('subject_matter_group.id'))
)

subjectMatter_firm_association_table = Table('subject_matter_to_firm', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('firm_id', Integer, ForeignKey('firm.id'))
)

subjectMatter_communication_association_table = Table('subject_matter_to_communication', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('communication_id', Integer, ForeignKey('communication.id'))
)

subjectMatter_grassroot_association_table = Table('subject_matter_to_grassroot', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('grassroot_id', Integer, ForeignKey('grassroot.id'))
)

subjectMatter_beneficiary_association_table = Table('subject_matter_to_beneficiary', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('beneficiary_id', Integer, ForeignKey('beneficiary.id'))
)

subjectMatter_private_funding_association_table = Table('subject_matter_to_private_funding', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('private_funding_id', Integer, ForeignKey('private_funding.id'))
)

subjectMatter_gmt_funding_association_table = Table('subject_matter_to_gmt_funding', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('gmt_funding_id', Integer, ForeignKey('gmt_funding.id'))
)

subjectmatter_meeting_association_table = Table('subject_matter_to_meeting', Base.metadata,
    Column('subject_matter_smnumber', Integer, ForeignKey('subject_matter.SMNumber')),
    Column('meeting_id', Integer, ForeignKey('meeting.id'))
)

class SubjectMatter(Base):
    __tablename__ = 'subject_matter'
    SMNumber: Mapped[String] =  mapped_column(String,primary_key=True)

    Status_id: Mapped[int] = mapped_column(ForeignKey('subject_matter_statuses.id'))
    Status: Mapped["SubjectMatterStatuses"]  = relationship()

    Type_id: Mapped[int] = mapped_column(ForeignKey('subject_matter_types.id'))
    Type: Mapped["SubjectMatterTypes"] = relationship()

    Groups: Mapped[List[SubjectMatterGroup]] = relationship(secondary=subjectmatter_group_association_table)
    
    Definition_id: Mapped[int] = mapped_column(ForeignKey('subject_matter_definition.id'))
    Definition : Mapped["SubjectMatterDefinition"] = relationship()
    
    Particulars: Mapped[String] = Column(String)
    InitialApprovalDate: Mapped[String] = Column(String)
    EffectiveDate: Mapped[String] = Column(String)
    ProposedStartDate: Mapped[String] = Column(String)
    ProposedEndDate: Mapped[String] = Column(String)

    Registrant_id:Mapped[int]  = mapped_column(ForeignKey('registrant.id'))
    Registrant: Mapped["Registrant"] = relationship()
                                               
    Firms : Mapped[List[Firm]] = relationship(secondary=subjectMatter_firm_association_table)

    Communications: Mapped[List[Communication]] = relationship(secondary=subjectMatter_communication_association_table)

    Grassroots: Mapped[List[Grassroot]] = relationship(secondary=subjectMatter_grassroot_association_table)

    Beneficiaries: Mapped[List[Beneficiary]] = relationship(secondary=subjectMatter_beneficiary_association_table)

    PrivateFundings: Mapped[List[PrivateFunding]] = relationship(secondary=subjectMatter_private_funding_association_table)

    GmtFundings: Mapped[List[GmtFunding]] = relationship(secondary=subjectMatter_gmt_funding_association_table)

    Meetings: Mapped[List[Meeting]] = relationship(secondary=subjectmatter_meeting_association_table)
   

class Uploader:

    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_db_file(use_existing_data=True):
        print("Deletes TorontoLobbyistRegistry.db if it exists ...")
        Uploader.delete_db()

        print("Setup db ...")
        engine = Uploader.setup_db()

        if use_existing_data:
            print("Geting existing data ...")
            results = Uploader.get_existing_data()
        else:
            print("Geting new data ...")
            results = Uploader.get_data()

        print("Generate key value tables ...")
        Uploader.add_key_value_tables(engine,results)

        print("Add data to db ...")
        Uploader.add_data_to_db(engine,results)

        print("Created db ...")

    @staticmethod
    def delete_db():
        if os.path.exists("TorontoLobbyistRegistry.db"): 
            os.remove("TorontoLobbyistRegistry.db")

    @staticmethod 
    def setup_db():
        engine = create_engine("sqlite:///TorontoLobbyistRegistry.db", echo=False, future=True)
        Base.metadata.create_all(engine)
        return engine
    
    @staticmethod 
    def get_data():
        downloader = Downloader()
        lobbyactivity_xml = downloader.lobbyactivity_xml()
        downloader.extract_files()
        results = LobbyParser(lobbyactivity_xml).get_results_dataclasses()
        return results

    @staticmethod 
    def get_existing_data():
        FILE_NAMES = ["lobbyactivity-active.xml","lobbyactivity-closed.xml"]
        lobbyactivity_xml = {}
        for file_name in FILE_NAMES:
            lobbyactivity_xml[file_name] = open(file_name, "rb")
        results = LobbyParser(lobbyactivity_xml).get_results_dataclasses()
        return results

    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
    def clean_PreviousPublicOfficeHolder(val):
        if val.PreviousPublicOfficeHolder in  [None,"No","no"]: 
            #TODO Look into this
            #if val.PreviousPublicOfficeHoldPosition is not  None and val.PreviousPublicOfficeHoldLastDate is not None:
            #    raise ValueError(f"PreviousPublicOfficeHolder is falsey but PreviousPublicOfficeHoldPosition and PreviousPublicOfficeHoldLastDate are not None: {communication.PreviousPublicOfficeHoldPosition} {communication.PreviousPublicOfficeHoldLastDate}")
            return False
        elif val.PreviousPublicOfficeHolder in ["Yes","yes"]:
            return True
        raise ValueError(f"Unexpected value for PreviousPublicOfficeHolder: {val.PreviousPublicOfficeHolder}")

    @staticmethod
    def add_key_value_tables(engine, results):
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
            
            for firmType in Uploader.get_firm_types(results):
                session.add(FirmType(Type=firmType))
            
            for firm_bussiness_type in Uploader.get_firm_bussiness_type(results):
                session.add(FirmBusinessType(Type=firm_bussiness_type))

            for lobbyistType in Uploader.get_lobbist_types(results):
                session.add(LobbyistType(Type=lobbyistType))
            
            for beneficiaryType in Uploader.get_beneficiary_types(results):
                session.add(BeneficiaryType(Type=beneficiaryType))
            
            session.commit()
        
    @staticmethod 
    def add_data_to_db(engine,results):
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
                    group = session.query(SubjectMatterGroup).filter(SubjectMatterGroup.Group == group).one()
                    session.add(group)
                    subjectMatter.Groups.append(group)
                
                subjectMatter.Definition = session.query(SubjectMatterDefinition).filter(SubjectMatterDefinition.Definition == result.SubjectMatterDefinition).one()
                subjectMatter.Definition_id = subjectMatter.Definition.id
                
                subjectMatter.Particulars = result.Particulars
                subjectMatter.InitialApprovalDate = result.InitialApprovalDate
                subjectMatter.EffectiveDate = result.EffectiveDate
                subjectMatter.ProposedStartDate = result.ProposedStartDate
                subjectMatter.ProposedEndDate = result.ProposedEndDate
                
                registrant = Registrant()
                registrant.RegistrationNUmber = result.Registrant.RegistrationNUmber
                registrant.RegistrationNUmberWithSoNum = result.Registrant.RegistrationNUmberWithSoNum

                registrant.Status = session.query(RegistrantStatus).filter(RegistrantStatus.Status == result.Registrant.Status).one()
                registrant.Status_id = registrant.Status.id

                registrant.EffectiveDate = result.Registrant.EffectiveDate

                registrant.Type = session.query(RegistrantType).filter(RegistrantType.Type == result.Registrant.Type).one()
                registrant.Type_id = registrant.Type.id

                registrant.Prefix = session.query(RegistrantPrefix).filter(RegistrantPrefix.Prefix == result.Registrant.Prefix).one()
                registrant.Prefix_id = registrant.Prefix.id

                registrant.FirstName = result.Registrant.FirstName
                registrant.MiddleInitials = result.Registrant.MiddleInitials
                registrant.LastName = result.Registrant.LastName
                registrant.Suffix = result.Registrant.Suffix
                registrant.PositionTitle = result.Registrant.PositionTitle
                
                if Uploader.clean_PreviousPublicOfficeHolder(result.Registrant):
                            registrant.PreviousPublicOfficeHolder = PreviousPublicOfficeHolder()
                            registrant.PreviousPublicOfficeHolder.Position = result.Registrant.PreviousPublicOfficeHoldPosition
                            registrant.PreviousPublicOfficeHolder.PositionProgramName = result.Registrant.PreviousPublicOfficePositionProgramName
                            registrant.PreviousPublicOfficeHolder.HoldLastDate = result.Registrant.PreviousPublicOfficeHoldLastDate
                            session.add(registrant.PreviousPublicOfficeHolder)
                            session.flush()
                            registrant.PreviousPublicOfficeHolder_id = registrant.PreviousPublicOfficeHolder.id
                
                registrant.BusinessAddress = session.query(BusinessAddress).filter(BusinessAddress.AddressLine1 == result.Registrant.BusinessAddress.AddressLine1).first() # TODO I need a stronger match here
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
                    firm.Type = session.query(FirmType).filter(FirmType.Type == val.Type).one()
                    firm.Type_id = firm.Type.id
                    firm.Name = val.Name
                    firm.TradeName = val.TradeName
                    firm.FiscalStart = val.FiscalStart
                    firm.FiscalEnd = val.FiscalEnd
                    firm.Description = val.Description
                    firm.BusinessType = session.query(FirmBusinessType).filter(FirmBusinessType.Type == val.BusinessType).one()
                    firm.BusinessType_id = firm.BusinessType.id
                    firm.BusinessAddress = session.query(BusinessAddress).filter(BusinessAddress.AddressLine1 == val.BusinessAddress.AddressLine1).first()
                    if firm.BusinessAddress is None:
                        firm.BusinessAddress = BusinessAddress(AddressLine1=val.BusinessAddress.AddressLine1,AddressLine2=val.BusinessAddress.AddressLine2,City=val.BusinessAddress.City,Province=val.BusinessAddress.Province,Country=val.BusinessAddress.Country,PostalCode=val.BusinessAddress.PostalCode,Phone=val.BusinessAddress.Phone)
                        session.add(firm.BusinessAddress)
                        session.flush()
                    firm.BusinessAddress_id = firm.BusinessAddress.id
                    session.add(firm)
                    subjectMatter.Firms.append(firm)

                if result.Communications is not None:
                    for val in result.Communications:
                        communication = Communication()
                        if Uploader.clean_PreviousPublicOfficeHolder(val):
                            communication.PreviousPublicOfficeHolder = PreviousPublicOfficeHolder()
                            communication.PreviousPublicOfficeHolder.Holder = val.PreviousPublicOfficeHolder
                            communication.PreviousPublicOfficeHolder.Position = val.PreviousPublicOfficeHoldPosition
                            communication.PreviousPublicOfficeHolder.PositionProgramName = val.PreviousPublicOfficePositionProgramName
                            communication.PreviousPublicOfficeHolder.HoldLastDate = val.PreviousPublicOfficeHoldLastDate
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
                        communication.Lobbyist.Type = session.query(LobbyistType).filter(LobbyistType.Type == val.LobbyistType).one()
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

                        session.add(communication)
                        subjectMatter.Communications.append(communication)

                if result.Grassroots is not None:
                    for val in result.Grassroots:
                        grassroot = Grassroot()
                        grassroot.Community = val.Community
                        grassroot.StartDate = val.StartDate
                        grassroot.EndDate = val.EndDate
                        grassroot.Target = val.Target
                        session.add(grassroot)
                        subjectMatter.Grassroots.append(grassroot)

                if result.Beneficiaries is not None:
                    for val in result.Beneficiaries:
                        beneficiary = Beneficiary()
                        beneficiary.Type = session.query(BeneficiaryType).filter(BeneficiaryType.Type == val.Type).one()
                        beneficiary.Type.id = beneficiary.Type.id
                        beneficiary.Name = val.Name
                        beneficiary.TradeName = val.TradeName
                        beneficiary.FiscalStart = val.FiscalStart
                        beneficiary.FiscalEnd = val.FiscalEnd

                        beneficiary.BusinessAddress = BusinessAddress()
                        beneficiary.BusinessAddress.AddressLine1 = val.BusinessAddress.AddressLine1
                        beneficiary.BusinessAddress.AddressLine2 = val.BusinessAddress.AddressLine2
                        beneficiary.BusinessAddress.City = val.BusinessAddress.City
                        beneficiary.BusinessAddress.Province = val.BusinessAddress.Province
                        beneficiary.BusinessAddress.Country = val.BusinessAddress.Country
                        beneficiary.BusinessAddress.PostalCode = val.BusinessAddress.PostalCode
                        beneficiary.BusinessAddress.Phone = val.BusinessAddress.Phone

                        session.add(beneficiary)
                        subjectMatter.Beneficiaries.append(beneficiary)

                if result.Privatefundings is not None:
                    for val in result.Privatefundings:
                        privatefunding = PrivateFunding(Funding=val.Funding,Contact=val.Contact,Agent=val.Agent,AgentContact=val.AgentContact)
                        session.add(privatefunding)
                        subjectMatter.PrivateFundings.append(privatefunding)

                if result.Gmtfundings is not None:
                    for val in result.Gmtfundings:
                        gmtfunding = GmtFunding(GMTName=val.GMTName, Program=val.Program)
                        session.add(gmtfunding)
                        subjectMatter.GmtFundings.append(gmtfunding)

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
                                session.add(poh)
                                meeting.POHS.append(poh)
                        
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
                                lobbyist.Type = session.query(LobbyistType).filter(LobbyistType.Type == val.Type).one()
                                lobbyist.Type_id = lobbyist.Type.id

                                session.add(lobbyist)
                                meeting.Lobbyists.append(lobbyist)                    
                        session.add(meeting)
                        subjectMatter.Meetings.append(meeting)            
                session.add(subjectMatter)
                session.flush()    
            session.commit()