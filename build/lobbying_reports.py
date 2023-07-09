from typing import List
from app.models.models import (
    LobbyingReport,
    LobbyingReportStatus,
    LobbyingReportType,
)
from app.models.processor_models import RawLobbyingReport
from sqlalchemy import insert
from datetime import datetime
from sqlalchemy.orm import Session


def get_data_row(raw_lobbying_report: RawLobbyingReport) -> dict:
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

    return {
        "smnumber": raw_lobbying_report.SMNumber,
        "status": LobbyingReportStatus(raw_lobbying_report.Status),
        "type": LobbyingReportType(raw_lobbying_report.Type),
        "subject_matter": raw_lobbying_report.SubjectMatter,
        "particulars": raw_lobbying_report.Particulars,
        "proposed_start_date": proposed_start_date,
        "proposed_end_date": proposed_end_date,
        "initial_approval_date": initial_approval_date,
        "effective_date": effective_date,
    }


def create_lobbying_report_table(session: Session, raw_lobbying_reports: List[RawLobbyingReport]) -> List[LobbyingReport]:
    data = []

    for raw_lobbying_report in raw_lobbying_reports:
        data.append(get_data_row(raw_lobbying_report))

    session.execute(insert(LobbyingReport), data)
    session.commit()
    return session.query(LobbyingReport).all()
