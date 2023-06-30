from typing import List, Dict
import os
import shutil
import xmltodict
import time
import zipfile
import pprint

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
    CanadianAddress,
    CanadianProvincesTerritories
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
from util.sqlalchemy_helpers import get_one_or_create, get_one_or_create_all
from util.address_helper import is_postal_code


from datetime import datetime, date
from dataclasses import dataclass
from sqlalchemy import delete

def create_addresses(db, raw_addresses: List[RawAddress]) -> List[Address]:
    CANADA_SPELLING = {
        s.lower()
        for s in [
            "Canada",
            "canada",
            "CANADA",
            "candada",
            "can.",
            "can",
            "ca",
            "cANADA",
            "VCanada",
            "Toronto",
            "Cnd",
            "Cdn",
            "Candad",
            "Canda",
            "Canaxa",
            "Cananda",
            "Canadá",
            "CanadÃÂÃÂÃÂÃÂ¡",
            "Canadsa",
            "Canads",
            "Canadda",
            "Canadaq",
            "Canadaa",
            "Canada`",
            "Canad",
            "cad",
            "Ca",
            "CAN",
            "C",
            "CA",
            "CAnada",
            "CDA",
            "Caanada",
            "Caanda",
            "Camada",
            "Can",
        ]
    }
    CANADIAN_PROVINCES_TERRITORIES_MAPPING = {
        "AB": CanadianProvincesTerritories.AB,
        "Albert": CanadianProvincesTerritories.AB,
        "Alberta": CanadianProvincesTerritories.AB,
        "Albrerta": CanadianProvincesTerritories.AB,
        "B.C.": CanadianProvincesTerritories.BC,
        "BC": CanadianProvincesTerritories.BC,
        "BRITISH COLUMBIA": CanadianProvincesTerritories.BC,
        "British  Columbia": CanadianProvincesTerritories.BC,
        "British Colmbia": CanadianProvincesTerritories.BC,
        "British Colombia": CanadianProvincesTerritories.BC,
        "British Coloumbia": CanadianProvincesTerritories.BC,
        "British Columbia": CanadianProvincesTerritories.BC,
        "British Columbia / Colombie-Britannique": CanadianProvincesTerritories.BC,
        "MB": CanadianProvincesTerritories.MB,
        "Manitoba": CanadianProvincesTerritories.MB,
        "NB": CanadianProvincesTerritories.NB,
        "NS": CanadianProvincesTerritories.NS,
        "New Brunswick": CanadianProvincesTerritories.NB,
        "New Bruswick": CanadianProvincesTerritories.NB,
        "Newfoundland": CanadianProvincesTerritories.NL,
        "Nova Scotia": CanadianProvincesTerritories.NS,
        "ON": CanadianProvincesTerritories.ON,
        "ON - Ontario": CanadianProvincesTerritories.ON,
        "ON-Ontario": CanadianProvincesTerritories.ON,
        "ON.": CanadianProvincesTerritories.ON,
        "ONT": CanadianProvincesTerritories.ON,
        "ONTARIO": CanadianProvincesTerritories.ON,
        "ONt": CanadianProvincesTerritories.ON,
        "ONtario": CanadianProvincesTerritories.ON,
        "On": CanadianProvincesTerritories.ON,
        "Onatrio": CanadianProvincesTerritories.ON,
        "Onrario": CanadianProvincesTerritories.ON,
        "Onrtario": CanadianProvincesTerritories.ON,
        "Ont": CanadianProvincesTerritories.ON,
        "Ont.": CanadianProvincesTerritories.ON,
        "Ontaio": CanadianProvincesTerritories.ON,
        "Ontairo": CanadianProvincesTerritories.ON,
        "Ontar": CanadianProvincesTerritories.ON,
        "Ontari": CanadianProvincesTerritories.ON,
        "Ontaria": CanadianProvincesTerritories.ON,
        "Ontariio": CanadianProvincesTerritories.ON,
        "Ontario": CanadianProvincesTerritories.ON,
        "Ontario (ON)": CanadianProvincesTerritories.ON,
        "Ontario0": CanadianProvincesTerritories.ON,
        "Ontario`": CanadianProvincesTerritories.ON,
        "Ontaro": CanadianProvincesTerritories.ON,
        "Ontatio": CanadianProvincesTerritories.ON,
        "Ontatrio": CanadianProvincesTerritories.ON,
        "Ontrario": CanadianProvincesTerritories.ON,
        "Ontrio": CanadianProvincesTerritories.ON,
        "Onttario": CanadianProvincesTerritories.ON,
        "PE": CanadianProvincesTerritories.PE,
        "PEI": CanadianProvincesTerritories.PE,
        "QC": CanadianProvincesTerritories.QC,
        "QU": CanadianProvincesTerritories.QC,
        "QUEBEC": CanadianProvincesTerritories.QC,
        "Qc": CanadianProvincesTerritories.QC,
        "Qc=C": CanadianProvincesTerritories.QC,
        "Qubec": CanadianProvincesTerritories.QC,
        "Quebec": CanadianProvincesTerritories.QC,
        "Quebec - CA": CanadianProvincesTerritories.QC,
        "Québec": CanadianProvincesTerritories.QC,
        "SK": CanadianProvincesTerritories.SK,
        "Sk": CanadianProvincesTerritories.SK,
        "Saskachewan": CanadianProvincesTerritories.SK,
        "Saskatchewan": CanadianProvincesTerritories.SK,
        "Yukon": CanadianProvincesTerritories.YT,
        "alberta": CanadianProvincesTerritories.AB,
        "oNTARIO": CanadianProvincesTerritories.ON,
        "on": CanadianProvincesTerritories.ON,
        "ont": CanadianProvincesTerritories.ON,
        "ont.": CanadianProvincesTerritories.ON,
        "ontaio": CanadianProvincesTerritories.ON,
        "ontairo": CanadianProvincesTerritories.ON,
        "ontariio": CanadianProvincesTerritories.ON,
        "ontario": CanadianProvincesTerritories.ON,
        "qc": CanadianProvincesTerritories.QC,
        "quebec": CanadianProvincesTerritories.QC,
    }

    address_mappings = {}
    canadian_addresses_data = []
    addresses_data = []

    for idx, raw_address in enumerate(raw_addresses):
        postal_code = None
        raw_fields = {
            "address_line1": raw_address.address_line_1,
            "address_line2": raw_address.address_line_2,
            "city": raw_address.city,
            "province": raw_address.province,
            "country": raw_address.country,
            "postal_code": raw_address.postal_code,
            "phone": raw_address.phone,
        }

        if raw_address.province == "AL" and raw_address.city == "Calgary":
            raw_address.province = "Alberta"

        if raw_address.province == "ALBERTA, CANADA" and raw_address.city == "Calgary":
            raw_address.province = "Alberta"

        if raw_address.province == "AC" and raw_address.city == "Montreal":
            raw_address.province = "Quebec"

        if raw_address.province == "Bentley  Canada Inc.":
            raw_address.province = "Ontario"
        
        if raw_address.province == "CA" and raw_address.city == "San Francisco" and raw_address.country == "CA":
            raw_address.province = "California"
            raw_address.country = "United States"
        
        if  raw_address.province == "CA" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "California" and raw_address.country == "Canada":
            raw_address.country = "United States"

        if raw_address.province == "ON MSN1X4":
            raw_address.province = "Ontario"
            raw_address.postal_code = "M5N 1X4"

        if raw_address.province == "New Jersey" and raw_address.country == "Canada":
            raw_address.country = "United States"
        
        if raw_address.province == "TX" and raw_address.country == "Canada":
            raw_address.country = "United States"
        
        if raw_address.province == "Winnepeg,":
            raw_address.province = "Manitoba"

        if raw_address.province == "Wisconsin" and raw_address.country == "Canada":
            raw_address.country = "United States"        

        if raw_address.province == "State" and raw_address.city == "East York":
            raw_address.province = "Ontario"
        
        if raw_address.province == "Texas" and raw_address.country == "Canada":
            raw_address.country = "United States"
        
        if raw_address.province == "Washington" and raw_address.country == "Canada":
            raw_address.country = "United States"
        
        if raw_address.province == "o" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "o" and raw_address.city == "Markham":
            raw_address.province = "Ontario"
        
        if raw_address.province == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "O" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "O" and raw_address.city == "TORONTO":
            raw_address.province = "Ontario"
        
        if raw_address.province == "N/A" and raw_address.country == "Canada": # Look into me
            raw_address.province = None
            raw_address.country = None
        
        if raw_address.province == "Nevada" and raw_address.country == "Canada":
            raw_address.country = "United States"
        
        if raw_address.province == "Canada" and raw_address.city == "Vaughan":
            raw_address.province = "Ontario"

        if raw_address.province == "Canada" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "Select" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "Province" and raw_address.city == "Toronto":
            raw_address.province = "Ontario"
        
        if raw_address.province == "Yes" and raw_address.city == "toronto":
            raw_address.province = "Ontario"
            
        if raw_address.country is not None and raw_address.country.lower() in CANADA_SPELLING:
            country = "Canada"
            postal_code = (
                "".join(char for char in raw_address.postal_code if char.isalnum())
                .upper()
                .replace("O", "0")
            )
            postal_code = postal_code[:3] + " " + postal_code[3:]

            if not is_postal_code(postal_code):
                postal_code = None

            if raw_address.province not in CANADIAN_PROVINCES_TERRITORIES_MAPPING:
                print(raw_fields)
            province = CANADIAN_PROVINCES_TERRITORIES_MAPPING[raw_address.province]

            fields = {
                "address_line1": raw_address.address_line_1,
                "address_line2": raw_address.address_line_2,
                "city": raw_address.city,
                "province": province,
                "country": country,
                "postal_code": postal_code,
                "raw_fields": raw_fields,
            }
            canadian_addresses_data.append((idx, fields))

        else:
            fields = {"raw_fields": raw_fields}
            addresses_data.append((idx, fields))

    canadian_addresses_tuples = get_one_or_create_all(
        db.session, CanadianAddress, [data for _, data in canadian_addresses_data]
    )
    addresses_tuples = get_one_or_create_all(
        db.session, Address, [data for _, data in addresses_data]
    )

    for (index, _), (created_address, _) in zip(
        canadian_addresses_data, canadian_addresses_tuples
    ):
        address_mappings[index] = created_address
    for (index, _), (created_address, _) in zip(addresses_data, addresses_tuples):
        address_mappings[index] = created_address

    db.session.flush()

    # Sort the created addresses based on their original order
    sorted_addresses = [address_mappings[i] for i in sorted(address_mappings.keys())]

    return sorted_addresses

