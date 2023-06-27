from typing import List, Dict
import os
import shutil
import xmltodict
import time
import zipfile
import pprint
from collections import defaultdict
from app import db as app_db
from app.models.models import (
    LobbyingReport,
    LobbyingReportStatus,
    LobbyingReportType,
    Address,
    Grassroot,
    Beneficiary,
    BeneficiaryType,
    Firm,
    FirmType,
    FirmBusinessType,
    GovernmentFunding,
    PrivateFunding,
)
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
from util.sqlalchemy_helpers import get_one_or_create

from datetime import datetime, date
from dataclasses import dataclass
from sqlalchemy import delete


DATA_PATH = "data"


@dataclass
class Data:
    data_value: str
    source: DataSource


def xml_to_dict(data_source: DataSource) -> Dict:
    with open(os.path.join(DATA_PATH, data_source.value)) as fd:
        return xmltodict.parse(fd.read())


def setup_db(db):
    db.drop_all()
    db.create_all()
    return db


def get_data_rows(file_dict: Dict, data_source: DataSource) -> List[Data]:
    data_rows = []
    for val in file_dict["ROWSET"]["ROW"]:
        row = val["SMXML"]["SM"]
        data_rows.append(Data(data_value=row, source=data_source))

    return data_rows


def create_raw_tables(data_rows: List[Data]):
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


def create_lobbying_reports(
    raw_lobbying_reports: List[RawLobbyingReport],
) -> List[LobbyingReport]:
    lobbying_reports = []

    for raw_lobbying_report in raw_lobbying_reports:
        proposed_start_date = (
            datetime.strptime(raw_lobbying_report.ProposedStartDate, "%Y-%m-%d").date()
            if raw_lobbying_report.ProposedStartDate
            else None
        )
        proposed_end_date = (
            datetime.strptime(raw_lobbying_report.ProposedEndDate, "%Y-%m-%d").date()
            if raw_lobbying_report.ProposedEndDate
            else None
        )
        initial_approval_date = datetime.strptime(
            raw_lobbying_report.InitialApprovalDate, "%Y-%m-%d"
        ).date()
        effective_date = datetime.strptime(
            raw_lobbying_report.EffectiveDate, "%Y-%m-%d"
        ).date()

        lobbying_report = LobbyingReport(
            smnumber=raw_lobbying_report.SMNumber,
            status=LobbyingReportStatus(raw_lobbying_report.Status),
            type=LobbyingReportType(raw_lobbying_report.Type),
            subject_matter=raw_lobbying_report.SubjectMatter,
            particulars=raw_lobbying_report.Particulars,
            proposed_start_date=proposed_start_date,
            proposed_end_date=proposed_end_date,
            initial_approval_date=initial_approval_date,
            effective_date=effective_date,
        )
        lobbying_reports.append(lobbying_report)

    db.session.bulk_save_objects(lobbying_reports)
    db.session.flush()
    return lobbying_reports


def create_grassroots(raw_grassroots: List[RawGrassroot]) -> List[Grassroot]:
    grassroots = []

    for raw_grassroot in raw_grassroots:
        start_date = datetime.strptime(raw_grassroot.StartDate, "%Y-%m-%d").date()
        end_date = datetime.strptime(raw_grassroot.EndDate, "%Y-%m-%d").date()

        grassroots_entry = Grassroot(
            community=raw_grassroot.Community,
            start_date=start_date,
            end_date=end_date,
            target=raw_grassroot.Target,
            report_id=raw_grassroot.report_id,
        )
        grassroots.append(grassroots_entry)

    db.session.bulk_save_objects(grassroots)
    db.session.flush()
    return grassroots


def create_beneficiaries(raw_beneficiaries: List[RawBeneficiary]) -> List[Beneficiary]:
    address_dict = {
        raw_beneficiary.address: address
        for raw_beneficiary, address in zip(
            raw_beneficiaries,
            create_addresses(
                raw_beneficiary.address for raw_beneficiary in raw_beneficiaries
            ),
        )
    }

    raw_beneficiaries_dict = defaultdict(list)
    for raw_beneficiary in raw_beneficiaries:
        raw_beneficiaries_dict[
            (
                raw_beneficiary.Type,
                raw_beneficiary.Name,
                raw_beneficiary.TradeName,
                raw_beneficiary.FiscalStart,
                raw_beneficiary.FiscalEnd,
                raw_beneficiary.address_id,
            )
        ].append(raw_beneficiary)

    beneficiaries_dict = defaultdict(list)
    for raw_beneficiary_key, raw_beneficiary_group in raw_beneficiaries_dict.values():
        raw_beneficiary = raw_beneficiary_group[0]
        beneficiary_type = BeneficiaryType(raw_beneficiary.Type)
        fiscal_start = (
            None
            if raw_beneficiary.FiscalStart is None
            else datetime.strptime(raw_beneficiary.FiscalStart, "%Y-%m-%d").date()
        )
        fiscal_end = (
            None
            if raw_beneficiary.FiscalEnd is None
            else datetime.strptime(raw_beneficiary.FiscalEnd, "%Y-%m-%d").date()
        )
        address = address_dict[raw_beneficiary.address]

        beneficiary = Beneficiary.query.filter(
            Beneficiary.type == beneficiary_type,
            Beneficiary.name == raw_beneficiary.Name,
            Beneficiary.trade_name == raw_beneficiary.TradeName,
            Beneficiary.fiscal_start == fiscal_start,
            Beneficiary.fiscal_end == fiscal_end,
            Beneficiary.address_id == address.id,
        ).one_or_none()

        if beneficiary is not None:
            beneficiary.resports.append(
                LobbyingReport.query.get(raw_beneficiary.report_id)
            )
        else:
            beneficiary = Beneficiary(
                type=beneficiary_type,
                name=raw_beneficiary.Name,
                trade_name=raw_beneficiary.TradeName,
                fiscal_start=fiscal_start,
                fiscal_end=fiscal_end,
                address_id=address.id,
                address=address,
                reports=[
                    db.session.get(LobbyingReport, raw_beneficiary.report_id)
                    for raw_beneficiary in raw_beneficiary_group
                ],
            )

        beneficiaries_dict[raw_beneficiary_key].append(beneficiary)
        db.session.add(beneficiary)
        db.session.flush()

    beneficiaries = [
        beneficiaries_dict[
            (
                raw_beneficiary.Type,
                raw_beneficiary.Name,
                raw_beneficiary.TradeName,
                raw_beneficiary.FiscalStart,
                raw_beneficiary.FiscalEnd,
                raw_beneficiary.address_id,
            )
        ]
        for raw_beneficiary in raw_beneficiaries
    ]
    # db.session.bulk_save_objects(beneficiaries)
    db.session.flush()

    return beneficiaries


def create_addresses_old(raw_addresses: List[RawAddress]) -> List[Address]:
    addresses = []
    for raw_address in raw_addresses:
        address = Address(
            address_line1=raw_address.address_line_1,
            address_line2=raw_address.address_line_2,
            city=raw_address.city,
            province=raw_address.province,
            country=raw_address.country,
            postal_code=raw_address.postal_code,
            phone=raw_address.phone,
        )
        addresses.append(address)

    db.session.add_all(addresses)
    db.session.flush()
    return addresses


def create_addresses(raw_addresses: List[RawAddress]) -> List[Address]:
    addresses = []
    for raw_address in raw_addresses:
        address, created = get_one_or_create(
            db.session,
            Address,
            address_line1=raw_address.address_line_1,
            address_line2=raw_address.address_line_2,
            city=raw_address.city,
            province=raw_address.province,
            country=raw_address.country,
            postal_code=raw_address.postal_code,
            phone=raw_address.phone,
        )
        addresses.append(address)

    # db.session.add_all(addresses)
    db.session.flush()
    return addresses


def create_firms(raw_firms: List[RawFirm]) -> List[Firm]:
    firms = []
    address_dict = {
        raw_firm.address: address
        for raw_firm, address in zip(
            raw_firms, create_addresses(raw_firm.address for raw_firm in raw_firms)
        )
    }

    for raw_firm in raw_firms:
        firm_type = FirmType(raw_firm.Type)
        fiscal_start = (
            None
            if raw_firm.FiscalStart is None
            else datetime.strptime(raw_firm.FiscalStart, "%Y-%m-%d").date()
        )
        fiscal_end = (
            None
            if raw_firm.FiscalEnd is None
            else datetime.strptime(raw_firm.FiscalEnd, "%Y-%m-%d").date()
        )
        business_type = (
            None
            if raw_firm.BusinessType is None
            else FirmBusinessType(raw_firm.BusinessType)
        )
        address = address_dict[raw_firm.address]
        firm = Firm(
            type=firm_type,
            name=raw_firm.Name,
            trade_name=raw_firm.TradeName,
            fiscal_start=fiscal_start,
            fiscal_end=fiscal_end,
            description=raw_firm.Description,
            business_type=business_type,
            address_id=address.id,
            address=address,
            report_id=raw_firm.report_id,
        )
        firms.append(firm)

    db.session.bulk_save_objects(firms)
    db.session.flush()

    return firms


def create_government_funding(
    raw_fundings: List[RawGmtFunding],
) -> List[GovernmentFunding]:
    fundings = []

    for raw_funding in raw_fundings:
        funding = GovernmentFunding(
            government_name=raw_funding.GMTName,
            program=raw_funding.Program,
            report_id=raw_funding.report_id,
        )
        fundings.append(funding)

    db.session.bulk_save_objects(fundings)
    db.session.flush()

    return fundings


def create_private_funding(
    raw_fundings: List[RawPrivateFunding],
) -> List[PrivateFunding]:
    fundings = []

    for raw_funding in raw_fundings:
        funding = PrivateFunding(
            funding=raw_funding.Funding,
            contact=raw_funding.Contact,
            agent=raw_funding.Agent,
            agent_contact=raw_funding.AgentContact,
            report_id=raw_funding.report_id,
        )
        fundings.append(funding)

    db.session.bulk_save_objects(fundings)
    db.session.flush()

    return fundings


from app import app, db


def run():
    with app.app_context():
        zip_file = os.path.join(DATA_PATH, "lobbyactivity.zip")
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            for member in zip_ref.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue
                source = zip_ref.open(member)
                target = open(os.path.join(DATA_PATH, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

        db = setup_db(app_db)
        data_rows = []
        for data_source in DataSource:
            start_time = time.time()
            data_rows += get_data_rows(xml_to_dict(data_source), data_source)
            end_time = time.time()
            print(f"Parse {data_source.value}: {end_time - start_time} seconds")

        start_time = time.time()
        create_raw_tables(data_rows)
        end_time = time.time()
        print(f"Create all Raw Tables: {end_time - start_time} seconds")

        for model in [
            LobbyingReport,
            Grassroot,
            Beneficiary,
            Address,
            Firm,
            PrivateFunding,
            GovernmentFunding,
        ]:
            db.session.execute(delete(model))

        start_time = time.time()
        create_lobbying_reports(RawLobbyingReport.query.all())
        end_time = time.time()
        print(f"Create all Lobbying Reports: {end_time - start_time} seconds")

        start_time = time.time()
        create_grassroots(RawGrassroot.query.all())
        end_time = time.time()
        print(f"Create all Grassroot: {end_time - start_time} seconds")

        start_time = time.time()
        create_beneficiaries(RawBeneficiary.query.all())
        end_time = time.time()
        print(f"Create all Beneficiary: {end_time - start_time} seconds")

        start_time = time.time()
        create_firms(RawFirm.query.all())
        end_time = time.time()
        print(f"Create all Firm: {end_time - start_time} seconds")

        start_time = time.time()
        create_government_funding(RawGmtFunding.query.all())
        end_time = time.time()
        print(f"Create all Government Funding: {end_time - start_time} seconds")

        start_time = time.time()
        create_private_funding(RawPrivateFunding.query.all())
        end_time = time.time()
        print(f"Create all Private Funding: {end_time - start_time} seconds")

        db.session.commit()


if __name__ == "__main__":
    run()
