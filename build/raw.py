from typing import List


from app import db as app_db
from app.models.processor_models import (
    RawAddress,
    RawRegistrant,
    RawCommunication,
    RawGrassroot,
    RawBeneficiary,
    RawFirm,
    RawPrivateFunding,
    RawGmtFunding,
    RawMeeting,
    RawPOH,
    RawLobbyist,
    RawPrivateFunding,
    RawGmtFunding,
    RawLobbyingReport,
)
from app.models.enums import DataSource


from dataclasses import dataclass

@dataclass
class Data:
    data_value: str
    source: DataSource


def create_raw_tables(db, data_rows: List[Data]):
    for idx, data_row in enumerate(data_rows):
        data_value = data_row.data_value
        print(f"({idx+1}/{len(data_rows)}): {data_value['SMNumber']}")

        raw_lobbying_report = RawLobbyingReport(
            DataSource=data_row.source,
            SMNumber=data_value["SMNumber"],
            Status=data_value["Status"],
            Type=data_value["Type"],
            SubjectMatter=data_value["SubjectMatter"],
            Particulars=data_value["Particulars"],
            InitialApprovalDate=data_value["InitialApprovalDate"],
            EffectiveDate=data_value["EffectiveDate"],
            ProposedStartDate=data_value["ProposedStartDate"],
            ProposedEndDate=data_value["ProposedEndDate"],
        )

        db.session.add(raw_lobbying_report)
        db.session.flush()

        registrant_data = data_value["Registrant"]
        registrant_address_data = registrant_data["BusinessAddress"]

        registrant_address = RawAddress(
            DataSource=data_row.source,
            address_line_1=registrant_address_data["AddressLine1"],
            address_line_2=registrant_address_data.get("AddressLine2"),
            city=registrant_address_data["City"],
            country=registrant_address_data["Country"],
            phone=registrant_address_data["Phone"],
            postal_code=registrant_address_data["PostalCode"],
            province=registrant_address_data["Province"],
        )

        db.session.add(registrant_address)
        db.session.flush()

        raw_registrant = RawRegistrant(
            DataSource=data_row.source,
            RegistrationNUmber=registrant_data["RegistrationNUmber"],
            RegistrationNUmberWithSoNum=registrant_data["RegistrationNUmberWithSoNum"],
            Status=registrant_data["Status"],
            EffectiveDate=registrant_data["EffectiveDate"],
            Type=registrant_data["Type"],
            Prefix=registrant_data["Prefix"],
            FirstName=registrant_data["FirstName"],
            MiddleInitials=registrant_data["MiddleInitials"],
            LastName=registrant_data["LastName"],
            Suffix=registrant_data["Suffix"],
            PositionTitle=registrant_data["PositionTitle"],
            PreviousPublicOfficeHolder=registrant_data["PreviousPublicOfficeHolder"],
            PreviousPublicOfficeHoldPosition=registrant_data[
                "PreviousPublicOfficeHoldPosition"
            ],
            PreviousPublicOfficePositionProgramName=registrant_data[
                "PreviousPublicOfficePositionProgramName"
            ],
            PreviousPublicOfficeHoldLastDate=registrant_data[
                "PreviousPublicOfficeHoldLastDate"
            ],
            address=registrant_address,
        )

        db.session.add(raw_registrant)
        db.session.flush()

        if "Communications" in data_value:
            if isinstance(data_value["Communications"]["Communication"], dict):
                raw_communications = [data_value["Communications"]["Communication"]]
            else:
                raw_communications = data_value["Communications"]["Communication"]

            for communication_data in raw_communications:
                communication_address_data = communication_data[
                    "LobbyistBusinessAddress"
                ]

                raw_communication_address = RawAddress(
                    DataSource=data_row.source,
                    address_line_1=communication_address_data["AddressLine1"],
                    address_line_2=communication_address_data.get("AddressLine2"),
                    city=communication_address_data["City"],
                    country=communication_address_data["Country"],
                    phone=communication_address_data["Phone"],
                    postal_code=communication_address_data["PostalCode"],
                    province=communication_address_data["Province"],
                )

                db.session.add(raw_communication_address)
                db.session.flush()

                raw_communication = RawCommunication(
                    DataSource=data_row.source,
                    POH_Office=communication_data["POH_Office"],
                    POH_Type=communication_data["POH_Type"],
                    POH_Position=communication_data["POH_Position"],
                    POH_Name=communication_data["POH_Name"],
                    CommunicationsMethod=communication_data["CommunicationMethod"],
                    CommunicationDate=communication_data["CommunicationDate"],
                    CommunicationGroupId=communication_data["CommunicationGroupId"],
                    LobbyistNumber=communication_data["LobbyistNumber"],
                    LobbyistType=communication_data["LobbyistType"],
                    LobbyistPrefix=communication_data["LobbyistPrefix"],
                    LobbyistFirstName=communication_data["LobbyistFirstName"],
                    LobbyistMiddleInitials=communication_data["LobbyistMiddleInitials"],
                    LobbyistLastName=communication_data["LobbyistLastName"],
                    LobbyistSuffix=communication_data["LobbyistSuffix"],
                    LobbyistBusiness=communication_data["LobbyistBusiness"],
                    LobbyistPositionTitle=communication_data["LobbyistPositionTitle"],
                    PreviousPublicOfficeHolder=communication_data[
                        "PreviousPublicOfficeHolder"
                    ],
                    PreviousPublicOfficePositionProgramName=communication_data[
                        "PreviousPublicOfficePositionProgramName"
                    ],
                    PreviousPublicOfficeHoldLastDate=communication_data[
                        "PreviousPublicOfficeHoldLastDate"
                    ],
                    address=raw_communication_address,
                    report_id=raw_lobbying_report.id,
                )
                db.session.add(raw_communication)

        if "Grassroots" in data_value:
            if isinstance(data_value["Grassroots"]["GRASSROOT"], dict):
                raw_grassroots = [data_value["Grassroots"]["GRASSROOT"]]
            else:
                raw_grassroots = data_value["Grassroots"]["GRASSROOT"]

            for grassroot_data in raw_grassroots:
                raw_grassroot = RawGrassroot(
                    Community=grassroot_data["Community"],
                    StartDate=grassroot_data["StartDate"],
                    EndDate=grassroot_data["EndDate"],
                    Target=grassroot_data["Target"],
                    report_id=raw_lobbying_report.id,
                )

                db.session.add(raw_grassroot)
                db.session.flush()

        if "Beneficiaries" in data_value:
            if isinstance((data_value["Beneficiaries"]["BENEFICIARY"]), dict):
                raw_beneficiaries = [data_value["Beneficiaries"]["BENEFICIARY"]]
            else:
                raw_beneficiaries = data_value["Beneficiaries"]["BENEFICIARY"]

            for beneficiary_data in raw_beneficiaries:
                raw_beneficiary_address = RawAddress(
                    DataSource=data_row.source,
                    address_line_1=beneficiary_data["BusinessAddress"]["AddressLine1"],
                    address_line_2=beneficiary_data["BusinessAddress"].get(
                        "AddressLine2"
                    ),
                    city=beneficiary_data["BusinessAddress"]["City"],
                    country=beneficiary_data["BusinessAddress"]["Country"],
                    phone=beneficiary_data["BusinessAddress"].get("Phone", None),
                    postal_code=beneficiary_data["BusinessAddress"]["PostalCode"],
                    province=beneficiary_data["BusinessAddress"]["Province"],
                )

                db.session.add(raw_beneficiary_address)
                db.session.flush()

                raw_beneficiary = RawBeneficiary(
                    DataSource=data_row.source,
                    Type=beneficiary_data["Type"],
                    Name=beneficiary_data["Name"],
                    TradeName=beneficiary_data["TradeName"],
                    FiscalStart=beneficiary_data["FiscalStart"],
                    FiscalEnd=beneficiary_data["FiscalEnd"],
                    address_id=raw_beneficiary_address.id,
                    report_id=raw_lobbying_report.id,
                )

                db.session.add(raw_beneficiary)
                db.session.flush()

        if "Firms" in data_value:
            if isinstance((data_value["Firms"]["Firm"]), dict):
                raw_firms = [data_value["Firms"]["Firm"]]
            else:
                raw_firms = data_value["Firms"]["Firm"]

            for firm_data in raw_firms:
                raw_firm_address = RawAddress(
                    DataSource=data_row.source,
                    address_line_1=firm_data["BusinessAddress"]["AddressLine1"],
                    address_line_2=firm_data["BusinessAddress"].get("AddressLine2"),
                    city=firm_data["BusinessAddress"]["City"],
                    country=firm_data["BusinessAddress"]["Country"],
                    phone=firm_data["BusinessAddress"].get("Phone"),
                    postal_code=firm_data["BusinessAddress"]["PostalCode"],
                    province=firm_data["BusinessAddress"]["Province"],
                )

                db.session.add(raw_firm_address)
                db.session.flush()

                raw_firm = RawFirm(
                    DataSource=data_row.source,
                    Type=firm_data["Type"],
                    Name=firm_data["Name"],
                    TradeName=firm_data["TradeName"],
                    FiscalStart=firm_data["FiscalStart"],
                    FiscalEnd=firm_data["FiscalEnd"],
                    Description=firm_data["Description"],
                    BusinessType=firm_data["BusinessType"],
                    address_id=raw_firm_address.id,
                    address=raw_firm_address,
                    report_id=raw_lobbying_report.id,
                )

                db.session.add(raw_firm)
                db.session.flush()

        if "Privatefundings" in data_value:
            if isinstance(data_value["Privatefundings"]["Privatefunding"], dict):
                raw_privatefundings = [data_value["Privatefundings"]["Privatefunding"]]
            else:
                raw_privatefundings = data_value["Privatefundings"]["Privatefunding"]

            for privatefunding_data in raw_privatefundings:
                raw_privatefunding = RawPrivateFunding(
                    DataSource=data_row.source,
                    Funding=privatefunding_data["Funding"],
                    Contact=privatefunding_data["Contact"],
                    Agent=privatefunding_data["Agent"],
                    AgentContact=privatefunding_data["AgentContact"],
                    report_id=raw_lobbying_report.id,
                )
                db.session.add(raw_privatefunding)
                db.session.flush()

        if "GMTFUNDINGS" in data_value:
            if isinstance((data_value["GMTFUNDINGS"]["GMTFUNDING"]), dict):
                raw_gmtfundings = [data_value["GMTFUNDINGS"]["GMTFUNDING"]]
            else:
                raw_gmtfundings = data_value["GMTFUNDINGS"]["GMTFUNDING"]

            for gmtfunding_data in raw_gmtfundings:
                raw_gmtfunding = RawGmtFunding(
                    DataSource=data_row.source,
                    GMTName=gmtfunding_data["GMTName"],
                    Program=gmtfunding_data["Program"],
                    report_id=raw_lobbying_report.id,
                )
                db.session.add(raw_gmtfunding)
                db.session.flush()

        if "Meetings" in data_value:
            if isinstance((data_value["Meetings"]["Meeting"]), dict):
                meetings_data = [data_value["Meetings"]["Meeting"]]
            else:
                meetings_data = data_value["Meetings"]["Meeting"]
            for meeting_data in meetings_data:
                raw_meeting = RawMeeting(
                    DataSource=data_row.source,
                    Committee=meeting_data["Committee"],
                    Desc=meeting_data["Desc"],
                    Date=meeting_data["Date"],
                    report_id=raw_lobbying_report.id,
                )
                db.session.add(raw_meeting)
                db.session.flush()

                if "POHS" in meeting_data:
                    if isinstance((meeting_data["POHS"]["POH"]), dict):
                        pohs_data = [meeting_data["POHS"]["POH"]]
                    else:
                        pohs_data = meeting_data["POHS"]["POH"]
                    for poh_data in pohs_data:
                        raw_poh = RawPOH(
                            DataSource=data_row.source,
                            Name=poh_data["Name"],
                            Office=poh_data["Office"],
                            Title=poh_data["Title"],
                            Type=poh_data["Type"],
                            meeting_id=raw_meeting.id,
                        )
                        db.session.add(raw_poh)

            if "Lobbyists" in meeting_data:
                if isinstance(meeting_data["Lobbyists"]["Lobbyist"], dict):
                    lobbyists_data = [meeting_data["Lobbyists"]["Lobbyist"]]
                else:
                    lobbyists_data = meeting_data["Lobbyists"]["Lobbyist"]
                for lobbyist_data in lobbyists_data:
                    raw_lobbyist = RawLobbyist(
                        DataSource=data_row.source,
                        Number=lobbyist_data["Number"],
                        Prefix=lobbyist_data["Prefix"],
                        FirstName=lobbyist_data["FirstName"],
                        MiddleInitials=lobbyist_data["MiddleInitials"],
                        LastName=lobbyist_data["LastName"],
                        Suffix=lobbyist_data["Suffix"],
                        Business=lobbyist_data["Business"],
                        Type=lobbyist_data["Type"],
                        meeting_id=raw_meeting.id,
                    )
                    db.session.add(raw_lobbyist)

        raw_lobbying_report.registrant_id = raw_registrant.id
        db.session.add(raw_lobbying_report)
    db.session.flush()


