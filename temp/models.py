from sqlalchemy import Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table for the many-to-many relationship between Registrant and SubjectMatter
registrant_subject_matter = Table('registrant_subject_matter', Base.metadata,
    Column('registrant_id', Integer, ForeignKey('registrants.id')),
    Column('sm_number', String(10), ForeignKey('subject_matters.sm_number'))
)

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

    registrants = relationship("Registrant", secondary=registrant_subject_matter, back_populates="subject_matters")
    beneficiaries = relationship("Beneficiary", back_populates="subject_matter")
    firms = relationship("Firm", back_populates="subject_matter")
    communications = relationship("Communication", back_populates="subject_matter")
    grassroots = relationship("Grassroots", back_populates="subject_matter")

class Registrant(Base):
    __tablename__ = 'registrants'

    id = Column(Integer, primary_key=True)
    registration_number = Column(String(20), unique=True)
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

    subject_matters = relationship("SubjectMatter", secondary=registrant_subject_matter, back_populates="registrants")
    business_address = relationship("BusinessAddress", uselist=False, back_populates="registrant")
    communications = relationship("Communication", back_populates="registrant")

class BusinessAddress(Base):
    __tablename__ = 'business_addresses'

    id = Column(Integer, primary_key=True)
    registrant_id = Column(Integer, ForeignKey('registrants.id'), unique=True)
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    postal_code = Column(String(20))
    phone = Column(String(20))

    registrant = relationship("Registrant", back_populates="business_address")

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