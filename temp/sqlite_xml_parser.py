import os
import xml.etree.ElementTree as ET
import logging
from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database setup
Base = declarative_base()
db_file = 'lobbyist_registry.db'
engine = create_engine(f'sqlite:///{db_file}')
Session = sessionmaker(bind=engine)

# Association table for the many-to-many relationship between Registrant and SubjectMatter
registrant_subject_matter = Table('registrant_subject_matter', Base.metadata,
    Column('registrant_id', Integer, ForeignKey('registrants.id')),
    Column('sm_number', String(10), ForeignKey('subject_matters.sm_number'))
)

# Define models
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

def delete_existing_db():
    if os.path.exists(db_file):
        os.remove(db_file)
        logging.info(f"Deleted existing database file: {db_file}")

def create_tables():
    Base.metadata.create_all(engine)
    logging.info("Created new database tables")

def parse_xml_file(filename):
    logging.info(f"Starting to parse {filename}")
    tree = ET.parse(filename)
    root = tree.getroot()
    
    session = Session()

    # Create error log file
    error_filename = f"error_log_{os.path.splitext(os.path.basename(filename))[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(error_filename, 'w') as error_file:
        error_file.write(f"Error log for {filename}\n")
        error_file.write(f"Parsing started at: {datetime.now()}\n\n")

        for row in root.findall('.//SM'):
            try:
                sm_number = row.find('SMNumber').text
                logging.info(f"Processing Subject Matter: {sm_number}")

                # SubjectMatter parsing
                try:
                    sm = SubjectMatter(
                        sm_number=sm_number,
                        status=row.find('Status').text,
                        type=row.find('Type').text,
                        subject_matter=row.find('SubjectMatter').text,
                        particulars=row.find('Particulars').text,
                        subject_matter_definition=row.find('SubjectMatterDefinition').text if row.find('SubjectMatterDefinition') is not None else None,
                        initial_approval_date=row.find('InitialApprovalDate').text,
                        effective_date=row.find('EffectiveDate').text,
                        proposed_start_date=row.find('ProposedStartDate').text,
                        proposed_end_date=row.find('ProposedEndDate').text
                    )
                    session.add(sm)
                except Exception as e:
                    error_message = f"Error parsing SubjectMatter {sm_number}: {str(e)}\n"
                    logging.error(error_message)
                    error_file.write(error_message)
                    continue

                # Registrant parsing
                registrant_elem = row.find('Registrant')
                if registrant_elem is not None:
                    try:
                        registration_number = registrant_elem.find('RegistrationNUmber').text
                        registrant = session.query(Registrant).filter_by(registration_number=registration_number).first()
                        
                        if registrant is None:
                            registrant = Registrant(
                                registration_number=registration_number,
                                status=registrant_elem.find('Status').text,
                                effective_date=registrant_elem.find('EffectiveDate').text,
                                type=registrant_elem.find('Type').text,
                                prefix=registrant_elem.find('Prefix').text,
                                first_name=registrant_elem.find('FirstName').text,
                                middle_initials=registrant_elem.find('MiddleInitials').text,
                                last_name=registrant_elem.find('LastName').text,
                                suffix=registrant_elem.find('Suffix').text,
                                position_title=registrant_elem.find('PositionTitle').text,
                                previous_public_office_holder=registrant_elem.find('PreviousPublicOfficeHolder').text,
                                previous_public_office_hold_position=registrant_elem.find('PreviousPublicOfficeHoldPosition').text,
                                previous_public_office_position_program_name=registrant_elem.find('PreviousPublicOfficePositionProgramName').text,
                                previous_public_office_hold_last_date=registrant_elem.find('PreviousPublicOfficeHoldLastDate').text
                            )
                            session.add(registrant)
                            session.flush()

                            # BusinessAddress parsing
                            address_elem = registrant_elem.find('BusinessAddress')
                            if address_elem is not None:
                                try:
                                    address = BusinessAddress(
                                        registrant_id=registrant.id,
                                        address_line1=address_elem.find('AddressLine1').text,
                                        address_line2=address_elem.find('AddressLine2').text,
                                        city=address_elem.find('City').text,
                                        province=address_elem.find('Province').text,
                                        country=address_elem.find('Country').text,
                                        postal_code=address_elem.find('PostalCode').text,
                                        phone=address_elem.find('Phone').text
                                    )
                                    session.add(address)
                                except Exception as e:
                                    error_message = f"Error parsing BusinessAddress for Registrant {registration_number}: {str(e)}\n"
                                    logging.error(error_message)
                                    error_file.write(error_message)

                        registrant.subject_matters.append(sm)
                    except Exception as e:
                        error_message = f"Error parsing Registrant for SubjectMatter {sm_number}: {str(e)}\n"
                        logging.error(error_message)
                        error_file.write(error_message)

                # Beneficiary parsing
                for beneficiary_elem in row.findall('.//BENEFICIARY'):
                    try:
                        beneficiary = Beneficiary(
                            sm_number=sm.sm_number,
                            type=beneficiary_elem.find('Type').text,
                            name=beneficiary_elem.find('Name').text,
                            trade_name=beneficiary_elem.find('TradeName').text,
                            fiscal_start=beneficiary_elem.find('FiscalStart').text,
                            fiscal_end=beneficiary_elem.find('FiscalEnd').text
                        )
                        session.add(beneficiary)
                    except Exception as e:
                        error_message = f"Error parsing Beneficiary for SubjectMatter {sm_number}: {str(e)}\n"
                        logging.error(error_message)
                        error_file.write(error_message)

                # Firm parsing
                for firm_elem in row.findall('.//Firm'):
                    try:
                        firm = Firm(
                            sm_number=sm.sm_number,
                            type=firm_elem.find('Type').text,
                            name=firm_elem.find('Name').text,
                            trade_name=firm_elem.find('TradeName').text,
                            fiscal_start=firm_elem.find('FiscalStart').text,
                            fiscal_end=firm_elem.find('FiscalEnd').text,
                            description=firm_elem.find('Description').text,
                            business_type=firm_elem.find('BusinessType').text
                        )
                        session.add(firm)
                    except Exception as e:
                        error_message = f"Error parsing Firm for SubjectMatter {sm_number}: {str(e)}\n"
                        logging.error(error_message)
                        error_file.write(error_message)

                # Communication parsing
                for comm_elem in row.findall('.//Communication'):
                    try:
                        communication = Communication(
                            sm_number=sm.sm_number,
                            registrant_id=registrant.id if registrant else None,
                            poh_office=comm_elem.find('POH_Office').text,
                            poh_type=comm_elem.find('POH_Type').text,
                            poh_position=comm_elem.find('POH_Position').text,
                            poh_name=comm_elem.find('POH_Name').text,
                            communication_method=comm_elem.find('CommunicationMethod').text,
                            communication_date=comm_elem.find('CommunicationDate').text,
                            communication_group_id=comm_elem.find('CommunicationGroupId').text,
                            lobbyist_number=comm_elem.find('LobbyistNumber').text,
                            lobbyist_type=comm_elem.find('LobbyistType').text,
                            lobbyist_prefix=comm_elem.find('LobbyistPrefix').text,
                            lobbyist_first_name=comm_elem.find('LobbyistFirstName').text,
                            lobbyist_middle_initials=comm_elem.find('LobbyistMiddleInitials').text,
                            lobbyist_last_name=comm_elem.find('LobbyistLastName').text,
                            lobbyist_suffix=comm_elem.find('LobbyistSuffix').text,
                            lobbyist_business=comm_elem.find('LobbyistBusiness').text,
                            lobbyist_position_title=comm_elem.find('LobbyistPositionTitle').text,
                            lobbyist_previous_public_office_holder=comm_elem.find('PreviousPublicOfficeHolder').text,
                            lobbyist_previous_public_office_hold_position=comm_elem.find('PreviousPublicOfficeHoldPosition').text,
                            lobbyist_previous_public_office_position_program_name=comm_elem.find('PreviousPublicOfficePositionProgramName').text,
                            lobbyist_previous_public_office_hold_last_date=comm_elem.find('PreviousPublicOfficeHoldLastDate').text
                        )
                        session.add(communication)
                        session.flush()

                        # LobbyistBusinessAddress parsing
                        lobbyist_address_elem = comm_elem.find('LobbyistBusinessAddress')
                        if lobbyist_address_elem is not None:
                            try:
                                lobbyist_address = LobbyistBusinessAddress(
                                    communication_id=communication.id,
                                    address_line1=lobbyist_address_elem.find('AddressLine1').text,
                                    address_line2=lobbyist_address_elem.find('AddressLine2').text,
                                    city=lobbyist_address_elem.find('City').text,
                                    province=lobbyist_address_elem.find('Province').text,
                                    country=lobbyist_address_elem.find('Country').text,
                                    postal_code=lobbyist_address_elem.find('PostalCode').text,
                                    phone=lobbyist_address_elem.find('Phone').text
                                )
                                session.add(lobbyist_address)
                            except Exception as e:
                                error_message = f"Error parsing LobbyistBusinessAddress for Communication in SubjectMatter {sm_number}: {str(e)}\n"
                                logging.error(error_message)
                                error_file.write(error_message)
                    except Exception as e:
                        error_message = f"Error parsing Communication for SubjectMatter {sm_number}: {str(e)}\n"
                        logging.error(error_message)
                        error_file.write(error_message)

                # Grassroots parsing
                grassroots_elem = row.find('Grassroots')
                if grassroots_elem is not None:
                    try:
                        grassroots = Grassroots(
                            sm_number=sm.sm_number,
                            community=grassroots_elem.find('Community').text,
                            start_date=grassroots_elem.find('StartDate').text,
                            end_date=grassroots_elem.find('EndDate').text,
                            target=grassroots_elem.find('Target').text
                        )
                        session.add(grassroots)
                    except Exception as e:
                        error_message = f"Error parsing Grassroots for SubjectMatter {sm_number}: {str(e)}\n"
                        logging.error(error_message)
                        error_file.write(error_message)

                session.commit()
                logging.info(f"Successfully processed SubjectMatter: {sm_number}")

            except Exception as e:
                error_message = f"Error processing SubjectMatter: {str(e)}\n"
                logging.error(error_message)
                error_file.write(error_message)
                session.rollback()

        error_file.write(f"\nParsing finished at: {datetime.now()}\n")

    session.close()
    logging.info(f"Finished parsing {filename}")
    logging.info(f"Error log written to {error_filename}")

if __name__ == "__main__":
    delete_existing_db()
    create_tables()
    
    parse_xml_file('lobbyactivity-active.xml')
    parse_xml_file('lobbyactivity-closed.xml')