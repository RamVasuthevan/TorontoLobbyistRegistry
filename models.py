from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SubjectMatter(Base):
    __tablename__ = 'subject_matters'

    sm_number = Column(String(10), primary_key=True)
    status = Column(String(20))
    type = Column(String(50))
    subject_matter = Column(String)
    particulars = Column(String)
    subject_matter_definition = Column(String)
    initial_approval_date = Column(String)
    effective_date = Column(String)
    proposed_start_date = Column(String)
    proposed_end_date = Column(String)

    registrant_id = Column(Integer, ForeignKey('registrants.id'), unique=True)  # Adding the foreign key
    registrant = relationship("Registrant", back_populates="subject_matters")  # One-to-many relationship

    beneficiaries = relationship("Beneficiary", back_populates="subject_matter")
    firms = relationship("Firm", back_populates="subject_matter")
    communications = relationship("Communication", back_populates="subject_matter")
    grassroots = relationship("Grassroots", back_populates="subject_matter")
    privatefundings = relationship("Privatefunding", back_populates="subject_matter")
    gmtfundings = relationship("Gmtfunding", back_populates="subject_matter")
    meetings = relationship("Meeting", back_populates="subject_matter")


class Registrant(Base):
    __tablename__ = 'registrants'

    id = Column(Integer, primary_key=True)
    registration_number = Column(String(20))
    status = Column(String(20))
    effective_date = Column(String)
    type = Column(String(50))
    prefix = Column(String(10))
    first_name = Column(String(100))
    middle_initials = Column(String(10))
    last_name = Column(String(100))
    suffix = Column(String(10))
    position_title = Column(String(100))
    previous_public_office_holder = Column(String(3))
    previous_public_office_hold_position = Column(String(100))
    previous_public_office_position_program_name = Column(String(100))
    previous_public_office_hold_last_date = Column(String)

    subject_matters = relationship("SubjectMatter", back_populates="registrant")  # Updated relationship
    registrant_business_address = relationship("RegistrantBusinessAddress", uselist=False, back_populates="registrant")
    communications = relationship("Communication", back_populates="registrant")


class RegistrantBusinessAddress(Base):
    __tablename__ = 'registrant_business_addresses'

    id = Column(Integer, primary_key=True)
    registrant_id = Column(Integer, ForeignKey('registrants.id'), unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    phone = Column(String(20))

    registrant = relationship("Registrant", back_populates="registrant_business_address")

class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    type = Column(String(50))
    name = Column(String(100))
    trade_name = Column(String(100))
    fiscal_start = Column(String)
    fiscal_end = Column(String)

    subject_matter = relationship("SubjectMatter", back_populates="beneficiaries")
    beneficiary_business_address = relationship("BeneficiaryBusinessAddress", uselist=False, back_populates="beneficiary")

class BeneficiaryBusinessAddress(Base):
    __tablename__ = 'beneficiary_business_addresses'

    id = Column(Integer, primary_key=True)
    beneficiary_id = Column(Integer, ForeignKey('beneficiaries.id'), unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))

    beneficiary = relationship("Beneficiary", back_populates="beneficiary_business_address")

class Firm(Base):
    __tablename__ = 'firms'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    type = Column(String(50))
    name = Column(String(100))
    trade_name = Column(String(100))
    fiscal_start = Column(String)
    fiscal_end = Column(String)
    description = Column(String)
    business_type = Column(String(50))

    subject_matter = relationship("SubjectMatter", back_populates="firms")
    firm_business_address = relationship("FirmBusinessAddress", uselist=False, back_populates="firm")

class FirmBusinessAddress(Base):
    __tablename__ = 'firm_business_addresses'

    id = Column(Integer, primary_key=True)
    firm_id = Column(Integer, ForeignKey('firms.id'), unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))

    firm = relationship("Firm", back_populates="firm_business_address")

class Communication(Base):
    __tablename__ = 'communications'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    registrant_id = Column(Integer, ForeignKey('registrants.id'))
    poh_office = Column(String(100))
    poh_type = Column(String(50))
    poh_position = Column(String(100))
    poh_name = Column(String(100))
    communication_method = Column(String(50))
    communication_date = Column(String)
    communication_group_id = Column(String(50))
    lobbyist_number = Column(String(20))
    lobbyist_type = Column(String(50))
    lobbyist_prefix = Column(String(10))
    lobbyist_first_name = Column(String(100))
    lobbyist_middle_initials = Column(String(10))
    lobbyist_last_name = Column(String(100))
    lobbyist_suffix = Column(String(10))
    lobbyist_business = Column(String(100))
    lobbyist_position_title = Column(String(100))
    lobbyist_previous_public_office_holder = Column(String(3))
    lobbyist_previous_public_office_hold_position = Column(String(100))
    lobbyist_previous_public_office_position_program_name = Column(String(100))
    lobbyist_previous_public_office_hold_last_date = Column(String)

    subject_matter = relationship("SubjectMatter", back_populates="communications")
    registrant = relationship("Registrant", back_populates="communications")
    lobbyist_business_address = relationship("LobbyistBusinessAddress", uselist=False, back_populates="communication")

class LobbyistBusinessAddress(Base):
    __tablename__ = 'lobbyist_business_addresses'

    id = Column(Integer, primary_key=True)
    communication_id = Column(Integer, ForeignKey('communications.id'), unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    phone = Column(String(20))

    communication = relationship("Communication", back_populates="lobbyist_business_address")

class Grassroots(Base):
    __tablename__ = 'grassroots'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    community = Column(String(100))
    start_date = Column(String)
    end_date = Column(String)
    target = Column(String(100))

    subject_matter = relationship("SubjectMatter", back_populates="grassroots")

class Privatefunding(Base):
    __tablename__ = 'privatefundings'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    funding = Column(String(100))
    contact = Column(String(100))
    agent = Column(String(100))
    agent_contact = Column(String(100))

    subject_matter = relationship("SubjectMatter", back_populates="privatefundings")

class Gmtfunding(Base):
    __tablename__ = 'gmtfundings'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    gmt_name = Column(String(100))
    program = Column(String(100))

    subject_matter = relationship("SubjectMatter", back_populates="gmtfundings")

class Meeting(Base):
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    sm_number = Column(String(10), ForeignKey('subject_matters.sm_number'))
    committee = Column(String(100))
    desc = Column(String)
    date = Column(String)

    subject_matter = relationship("SubjectMatter", back_populates="meetings")
    pohs = relationship("POH", back_populates="meeting")
    lobbyists = relationship("MeetingLobbyist", back_populates="meeting")

class POH(Base):
    __tablename__ = 'pohs'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'))
    name = Column(String(100))
    office = Column(String(100))
    title = Column(String(100))
    type = Column(String(50))

    meeting = relationship("Meeting", back_populates="pohs")

class MeetingLobbyist(Base):
    __tablename__ = 'meeting_lobbyists'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'))
    number = Column(String(20))
    prefix = Column(String(10))
    first_name = Column(String(100))
    middle_initials = Column(String(10))
    last_name = Column(String(100))
    suffix = Column(String(10))
    business = Column(String(100))
    type = Column(String(50))

    meeting = relationship("Meeting", back_populates="lobbyists")