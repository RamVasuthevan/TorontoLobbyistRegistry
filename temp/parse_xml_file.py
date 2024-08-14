import xml.etree.ElementTree as ET
import logging
from models import SubjectMatter, Registrant, RegistrantBusinessAddress, Beneficiary, BeneficiaryBusinessAddress, Firm, FirmBusinessAddress, Communication, LobbyistBusinessAddress, Grassroots, Privatefunding, Gmtfunding, Meeting, POH, MeetingLobbyist

def parse_xml_file(filename, session):
    tree = ET.parse(filename)
    root = tree.getroot()

    for row in root.findall('.//SM'):
        try:
            sm_number = row.find('SMNumber').text
            logging.debug(f"Processing Subject Matter: {sm_number}")

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
                logging.error(f"Error parsing SubjectMatter {sm_number}: {str(e)}")
                continue

            # Registrant parsing
            registrant_elem = row.find('Registrant')
            if registrant_elem is not None:
                try:
                    registrant = Registrant(
                        registration_number=registrant_elem.find('RegistrationNUmber').text,
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

                    sm.registrant = registrant  # Associate the registrant with the subject matter

                    # RegistrantBusinessAddress parsing
                    address_elem = registrant_elem.find('BusinessAddress')
                    if address_elem is not None:
                        try:
                            address = RegistrantBusinessAddress(
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
                            logging.error(f"Error parsing RegistrantBusinessAddress for Registrant {registrant.registration_number}: {str(e)}")
                except Exception as e:
                    logging.error(f"Error parsing Registrant for SubjectMatter {sm_number}: {str(e)}")

            # Beneficiary parsing
            beneficiaries_elem = row.find('Beneficiaries')
            if beneficiaries_elem is not None:
                for beneficiary_elem in beneficiaries_elem.findall('BENEFICIARY'):
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
                        session.flush()  # This ensures beneficiary.id is available

                        # BeneficiaryBusinessAddress parsing
                        address_elem = beneficiary_elem.find('BusinessAddress')
                        if address_elem is not None:
                            try:
                                address = BeneficiaryBusinessAddress(
                                    beneficiary_id=beneficiary.id,
                                    address_line1=address_elem.find('AddressLine1').text,
                                    address_line2=address_elem.find('AddressLine2').text,
                                    city=address_elem.find('City').text,
                                    province=address_elem.find('Province').text,
                                    country=address_elem.find('Country').text,
                                    postal_code=address_elem.find('PostalCode').text
                                )
                                session.add(address)
                            except Exception as e:
                                logging.error(f"Error parsing BeneficiaryBusinessAddress for Beneficiary {beneficiary.name} in SubjectMatter {sm_number}: {str(e)}")
                    except Exception as e:
                        logging.error(f"Error parsing Beneficiary for SubjectMatter {sm_number}: {str(e)}")

            # Firm parsing
            firms_elem = row.find('Firms')
            if firms_elem is not None:
                for firm_elem in firms_elem.findall('Firm'):
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
                        session.flush()  # This ensures firm.id is available

                        # FirmBusinessAddress parsing
                        address_elem = firm_elem.find('BusinessAddress')
                        if address_elem is not None:
                            try:
                                address = FirmBusinessAddress(
                                    firm_id=firm.id,
                                    address_line1=address_elem.find('AddressLine1').text,
                                    address_line2=address_elem.find('AddressLine2').text,
                                    city=address_elem.find('City').text,
                                    province=address_elem.find('Province').text,
                                    country=address_elem.find('Country').text,
                                    postal_code=address_elem.find('PostalCode').text
                                )
                                session.add(address)
                            except Exception as e:
                                logging.error(f"Error parsing FirmBusinessAddress for Firm {firm.name} in SubjectMatter {sm_number}: {str(e)}")
                    except Exception as e:
                        logging.error(f"Error parsing Firm for SubjectMatter {sm_number}: {str(e)}")

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
                            logging.error(f"Error parsing LobbyistBusinessAddress for Communication in SubjectMatter {sm_number}: {str(e)}")
                except Exception as e:
                    logging.error(f"Error parsing Communication for SubjectMatter {sm_number}: {str(e)}")

            # Grassroots parsing
            grassroots_elem = row.find('Grassroots')
            if grassroots_elem is not None:
                for grassroot_elem in grassroots_elem.findall('GRASSROOT'):
                    try:
                        grassroots = Grassroots(
                            sm_number=sm.sm_number,
                            community=grassroot_elem.find('Community').text,
                            start_date=grassroot_elem.find('StartDate').text,
                            end_date=grassroot_elem.find('EndDate').text,
                            target=grassroot_elem.find('Target').text
                        )
                        session.add(grassroots)
                    except Exception as e:
                        logging.error(f"Error parsing Grassroots for SubjectMatter {sm_number}: {str(e)}")

            # Privatefunding parsing
            privatefundings_elem = row.find('Privatefundings')
            if privatefundings_elem is not None:
                for privatefunding_elem in privatefundings_elem.findall('Privatefunding'):
                    try:
                        privatefunding = Privatefunding(
                            sm_number=sm.sm_number,
                            funding=privatefunding_elem.find('Funding').text,
                            contact=privatefunding_elem.find('Contact').text,
                            agent=privatefunding_elem.find('Agent').text,
                            agent_contact=privatefunding_elem.find('AgentContact').text
                        )
                        session.add(privatefunding)
                    except Exception as e:
                        logging.error(f"Error parsing Privatefunding for SubjectMatter {sm_number}: {str(e)}")

            # Gmtfunding parsing
            gmtfundings_elem = row.find('Gmtfundings')
            if gmtfundings_elem is not None:
                for gmtfunding_elem in gmtfundings_elem.findall('Gmtfunding'):
                    try:
                        gmtfunding = Gmtfunding(
                            sm_number=sm.sm_number,
                            gmt_name=gmtfunding_elem.find('GMTName').text,
                            program=gmtfunding_elem.find('Program').text
                        )
                        session.add(gmtfunding)
                    except Exception as e:
                        logging.error(f"Error parsing Gmtfunding for SubjectMatter {sm_number}: {str(e)}")
            
            # Meeting parsing
            meetings_elem = row.find('Meetings')
            if meetings_elem is not None:
                for meeting_elem in meetings_elem.findall('Meeting'):
                    try:
                        meeting = Meeting(
                            sm_number=sm.sm_number,
                            committee=meeting_elem.find('Committee').text,
                            desc=meeting_elem.find('Desc').text,
                            date=meeting_elem.find('Date').text
                        )
                        session.add(meeting)
                        session.flush()  # This ensures meeting.id is available

                        # POH parsing
                        pohs_elem = meeting_elem.find('POHS')
                        if pohs_elem is not None:
                            for poh_elem in pohs_elem.findall('POH'):
                                try:
                                    poh = POH(
                                        meeting_id=meeting.id,
                                        name=poh_elem.find('Name').text,
                                        office=poh_elem.find('Office').text,
                                        title=poh_elem.find('Title').text,
                                        type=poh_elem.find('Type').text
                                    )
                                    session.add(poh)
                                except Exception as e:
                                    logging.error(f"Error parsing POH for Meeting in SubjectMatter {sm_number}: {str(e)}")

                        # Lobbyist parsing
                        lobbyists_elem = meeting_elem.find('Lobbyists')
                        if lobbyists_elem is not None:
                            for lobbyist_elem in lobbyists_elem.findall('Lobbyist'):
                                try:
                                    lobbyist = MeetingLobbyist(
                                        meeting_id=meeting.id,
                                        number=lobbyist_elem.find('Number').text,
                                        prefix=lobbyist_elem.find('Prefix').text,
                                        first_name=lobbyist_elem.find('FirstName').text,
                                        middle_initials=lobbyist_elem.find('MiddleInitials').text,
                                        last_name=lobbyist_elem.find('LastName').text,
                                        suffix=lobbyist_elem.find('Suffix').text,
                                        business=lobbyist_elem.find('Business').text,
                                        type=lobbyist_elem.find('Type').text
                                    )
                                    session.add(lobbyist)
                                except Exception as e:
                                    logging.error(f"Error parsing Lobbyist for Meeting in SubjectMatter {sm_number}: {str(e)}")

                    except Exception as e:
                        logging.error(f"Error parsing Meeting for SubjectMatter {sm_number}: {str(e)}")

            session.commit()
            logging.debug(f"Successfully processed SubjectMatter: {sm_number}")

        except Exception as e:
            logging.error(f"Error processing SubjectMatter: {str(e)}")
            session.rollback()

    logging.info(f"Finished parsing {filename}")
