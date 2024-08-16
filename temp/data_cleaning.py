from sqlalchemy.orm import Session
from models import Registrant, RegistrantBusinessAddress, Communication
import logging
from collections import defaultdict

def clean_country_name(country):
    if not country or country.strip().lower() in ['', 'country']:
        return None
    
    country = country.strip().lower()
    
    country_mapping = {
        'canada': 'Canada',
        'can': 'Canada',
        'cad': 'Canada',
        'cdn': 'Canada',
        'cda': 'Canada',
        'ca': 'Canada',
        'c': 'Canada',
        'canad': 'Canada',
        'cananda': 'Canada',
        'canda': 'Canada',
        'caanda': 'Canada',
        'canadá': 'Canada',
        'canadÃ¡': 'Canada',
        'can.': 'Canada',
        'canada ': 'Canada',
        'l4w 5k4': 'Canada',  # Corrected to map to Canada
        'usa': 'United States',
        'u.s.a.': 'United States',
        'us': 'United States',
        'united states': 'United States',
        'united states of america': 'United States',
        'united state america': 'United States',
        'united states ': 'United States',
        'united-states': 'United States',
        'u.s.': 'United States',
        'etats-unis': 'United States',
        '55343': 'United States',  # Assuming this is a U.S. ZIP code
        'brazil': 'Brazil',
        'brasil': 'Brazil',
        'england': 'United Kingdom',
        'uk': 'United Kingdom',
        'united kingdom': 'United Kingdom',
        'singapore': 'Singapore',
        'italy': 'Italy',
        'france': 'France',
        'germany': 'Germany',
        'nederland': 'Netherlands',
        'netherlands': 'Netherlands',
        'the netherlands': 'Netherlands',
        'united arab emirates': 'United Arab Emirates',
        'austria': 'Austria',
        'spain': 'Spain',
        'china': 'China',
        'prc': 'China',
        'sweden': 'Sweden',
        'belgium': 'Belgium',
        'south korea': 'South Korea',
        'south africa': 'South Africa',
        'ireland': 'Ireland',
        'portugal': 'Portugal',
        'new zealand': 'New Zealand',
        'hungary': 'Hungary',
        'norway': 'Norway',
        'israel': 'Israel',
        'croatia': 'Croatia',
        'cameroon': 'Cameroon',
        'denmark': 'Denmark',
        'finland': 'Finland',
        'suisse': 'Switzerland',
        'switzerland': 'Switzerland',
        'nigeria': 'Nigeria',
        'slovakia': 'Slovakia',
        'hong kong': 'Hong Kong',
        'australia': 'Australia',
        'india': 'India',
        'p r china': 'China',
    }
    
    # Handle special cases for Canada and United States variations
    if country in country_mapping:
        return country_mapping[country]
    
    # If not found in mapping, capitalize the first letter of each word
    return country.title()

def clean_province_name(province):
    if not province or province.strip().lower() in ['n/a', 'none', '-', 'non']:
        return None
    
    province = province.strip().upper()
    
    province_mapping = {
        'AB': 'Alberta',
        'AB - ALBERTA': 'Alberta',
        'ALBERTA': 'Alberta',
        'BC': 'British Columbia',
        'B.C.': 'British Columbia',
        'BRITISH COLUMBIA': 'British Columbia',
        'BRITICH COLUMBIA': 'British Columbia',
        'BRITISH COLUMBIA / COLOMBIE-BRITANNIQUE': 'British Columbia',
        'BRITISH COLUMBIA,': 'British Columbia',
        'ON': 'Ontario',
        'ON - ONTARIO': 'Ontario',
        'ON -- ONTARIO': 'Ontario',
        'ONTARIO': 'Ontario',
        'ONT': 'Ontario',
        'ONT.': 'Ontario',
        'ONTAIO': 'Ontario',
        'ONTAIRO': 'Ontario',
        'ONTARI': 'Ontario',
        'ONTARIA': 'Ontario',
        'ONTARO': 'Ontario',
        'ONTATIO': 'Ontario',
        'ONTRARIO': 'Ontario',
        'ONTRIO': 'Ontario',
        'ON ONTARIO': 'Ontario',
        'ON,': 'Ontario',
        'ONTARIO (ON)': 'Ontario',
        'ONTARIO - ON': 'Ontario',
        'ONTARIO`': 'Ontario',
        'QC': 'Quebec',
        'QUEBEC': 'Quebec',
        'QC - QUEBEC': 'Quebec',
        'QUÉBEC': 'Quebec',
        'QUÉBEC)': 'Quebec',
        'PE': 'Prince Edward Island',
        'PEI': 'Prince Edward Island',
        'NS': 'Nova Scotia',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'MB': 'Manitoba',
        'SK': 'Saskatchewan',
        'YT': 'Yukon',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        'CA': 'California',
        'CA - CALIFORNIA': 'California',
        'CALIFORNIA': 'California',
        'TX': 'Texas',
        'TEXAS': 'Texas',
        'NY': 'New York',
        'NEW YORK': 'New York',
        'FL': 'Florida',
        'FLORIDA': 'Florida',
        'GA': 'Georgia',
        'GEORGIA': 'Georgia',
        'IL': 'Illinois',
        'ILLINOIS': 'Illinois',
        'WA': 'Washington',
        'WASHINGTON': 'Washington',
        'MA': 'Massachusetts',
        'MASSACHUSETTS': 'Massachusetts',
        'MI': 'Michigan',
        'MICHIGAN': 'Michigan',
        'PA': 'Pennsylvania',
        'PENNSYLVANIA': 'Pennsylvania',
        'CO': 'Colorado',
        'COLORADO': 'Colorado',
        'NC': 'North Carolina',
        'NORTH CAROLINA': 'North Carolina',
        'OH': 'Ohio',
        'OHIO': 'Ohio',
        'VA': 'Virginia',
        'VIRGINIA': 'Virginia',
        'MO': 'Missouri',
        'MISSOURI': 'Missouri',
        'MN': 'Minnesota',
        'MINNESOTA': 'Minnesota',
        'NV': 'Nevada',
        'NEVADA': 'Nevada',
        'AZ': 'Arizona',
        'ARIZONA': 'Arizona',
        'OR': 'Oregon',
        'OREGON': 'Oregon',
        'NJ': 'New Jersey',
        'NEW JERSEY': 'New Jersey',
        'LA': 'Louisiana',
        'LOUISIANA': 'Louisiana',
        'UT': 'Utah',
        'UTAH': 'Utah',
        'ID': 'Idaho',
        'IDAHO': 'Idaho',
        'MD': 'Maryland',
        'MARYLAND': 'Maryland',
        'SC': 'South Carolina',
        'SOUTH CAROLINA': 'South Carolina',
        'IA': 'Iowa',
        'IOWA': 'Iowa',
        'KY': 'Kentucky',
        'KENTUCKY': 'Kentucky',
        'TN': 'Tennessee',
        'TENNESSEE': 'Tennessee',
        'ME': 'Maine',
        'MAINE': 'Maine',
        'CT': 'Connecticut',
        'CONNECTICUT': 'Connecticut',
        'DC': 'District of Columbia',
        'DISTRICT OF COLUMBIA': 'District of Columbia',
        'IN': 'Indiana',
        'INDIANA': 'Indiana',
        'AL': 'Alabama',
        'ALABAMA': 'Alabama',
        'KS': 'Kansas',
        'KANSAS': 'Kansas',
        'OK': 'Oklahoma',
        'OKLAHOMA': 'Oklahoma',
        'NE': 'Nebraska',
        'NEBRASKA': 'Nebraska',
        'WI': 'Wisconsin',
        'WISCONSIN': 'Wisconsin',
        'MT': 'Montana',
        'MONTANA': 'Montana',
        'ND': 'North Dakota',
        'NORTH DAKOTA': 'North Dakota',
        'SD': 'South Dakota',
        'SOUTH DAKOTA': 'South Dakota',
        'WV': 'West Virginia',
        'WEST VIRGINIA': 'West Virginia',
        'WY': 'Wyoming',
        'WYOMING': 'Wyoming',
        'VT': 'Vermont',
        'VERMONT': 'Vermont',
        'NH': 'New Hampshire',
        'NEW HAMPSHIRE': 'New Hampshire',
        'NM': 'New Mexico',
        'NEW MEXICO': 'New Mexico',
        'RI': 'Rhode Island',
        'RHODE ISLAND': 'Rhode Island',
        'DE': 'Delaware',
        'DELAWARE': 'Delaware',
        'AK': 'Alaska',
        'ALASKA': 'Alaska',
        'HI': 'Hawaii',
        'HAWAII': 'Hawaii',
        'England': 'England',
        'France': 'France',
        'Germany': 'Germany',
        'Italy': 'Italy',
        'Spain': 'Spain',
        'Japan': 'Japan',
        'China': 'China',
        'Brazil': 'Brazil',
        'Australia': 'Australia',
        'India': 'India',
        'Israel': 'Israel',
        'Singapore': 'Singapore',
        'Netherlands': 'Netherlands',
        'Norway': 'Norway',
        'Sweden': 'Sweden',
        'Switzerland': 'Switzerland',
        'United Kingdom': 'United Kingdom',
        'South Korea': 'South Korea',
        'Mexico': 'Mexico',
        'Hong Kong': 'Hong Kong',
        'South Africa': 'South Africa',
        'Belgium': 'Belgium',
        'Russia': 'Russia',
        'Thailand': 'Thailand',
        'Philippines': 'Philippines',
        'Malaysia': 'Malaysia',
        'Indonesia': 'Indonesia',
        'Poland': 'Poland',
        'Austria': 'Austria',
        'Denmark': 'Denmark',
        'Ireland': 'Ireland',
        'Greece': 'Greece',
        'Finland': 'Finland',
        'Portugal': 'Portugal',
        'Argentina': 'Argentina',
        'Chile': 'Chile',
        'Czech Republic': 'Czech Republic',
        'Hungary': 'Hungary',
        'Turkey': 'Turkey',
        'Saudi Arabia': 'Saudi Arabia',
        'United Arab Emirates': 'United Arab Emirates',
        'Luxembourg': 'Luxembourg',
        'Slovakia': 'Slovakia',
        'Croatia': 'Croatia',
        'Slovenia': 'Slovenia',
        'Lithuania': 'Lithuania',
        'Latvia': 'Latvia',
        'Estonia': 'Estonia',
        'Iceland': 'Iceland',
        'New Zealand': 'New Zealand',
        'Monaco': 'Monaco',
        'San Marino': 'San Marino',
        'Malta': 'Malta',
        'Liechtenstein': 'Liechtenstein',
    }
    
    # Check if the province is in our mapping
    if province in province_mapping:
        return province_mapping[province]
    
    # If not found in mapping, return the original value
    return province.title()

def clean_city_name(city):
    if not city:
        return None
    
    city = city.strip().lower()
    
    city_mapping = {
        ".mississauga": "Mississauga",
        "aurora": "Aurora",
        "austell": "Austell",
        "burlington,": "Burlington",
        "brampton": "Brampton",
        "brossard": "Brossard",
        "burlington, on": "Burlington",
        "etobicoke,": "Etobicoke",
        "king city,": "King City",
        "mississauga": "Mississauga",
        "montréal": "Montreal",
        "scarborough": "Scarborough",
        "toronto,": "Toronto",
        "mississauga,": "Mississauga",
        "thornhill": "Thornhill",
        "toronto on": "Toronto",
        "toronto,": "Toronto",
        "toronto": "Toronto",
        "vaughan,": "Vaughan",
        "vaughan": "Vaughan",
        "york,": "York",
        "calgary": "Calgary",
        "denver": "Denver",
        "etobicoke": "Etobicoke",
        "hamilton": "Hamilton",
        "houston": "Houston",
        "mississauga": "Mississauga",
        "montreal": "Montreal",
        "oakville": "Oakville",
        "oshawa": "Oshawa",
        "san francisco": "San Francisco",
        "scarborough": "Scarborough",
        "vaughan": "Vaughan",
        "woodbridge": "Woodbridge",
        "york": "York",
        "'s-hertogenbosch": "'s-Hertogenbosch",
    }
    
    # Handle specific common city name cases
    if city in city_mapping:
        return city_mapping[city]
    
    # Capitalize each word in the city name
    return city.title()

def clean_registrants_previous_public_office_holder(session: Session):
    logging.info("Starting clean_registrants_previous_public_office_holder")
    try:
        registrants = session.query(Registrant).filter(Registrant.previous_public_office_holder.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for registrant in registrants:
            old_value = registrant.previous_public_office_holder
            new_value = old_value.capitalize()
            if old_value != new_value:
                registrant.previous_public_office_holder = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrants.previous_public_office_holder:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrants.previous_public_office_holder")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrants.previous_public_office_holder: {str(e)}")
    
    logging.info("Completed clean_registrants_previous_public_office_holder")

def clean_registrant_business_addresses_country(session: Session):
    logging.info("Starting clean_registrant_business_addresses_country")
    try:
        addresses = session.query(RegistrantBusinessAddress).filter(RegistrantBusinessAddress.country.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for address in addresses:
            old_value = address.country
            new_value = clean_country_name(old_value)
            if old_value != new_value:
                address.country = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrant_business_addresses.country:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrant_business_addresses.country")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrant_business_addresses.country: {str(e)}")
    
    logging.info("Completed clean_registrant_business_addresses_country")

def clean_registrant_business_addresses_province(session: Session):
    logging.info("Starting clean_registrant_business_addresses_province")
    try:
        addresses = session.query(RegistrantBusinessAddress).filter(RegistrantBusinessAddress.province.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for address in addresses:
            old_value = address.province
            new_value = clean_province_name(old_value)
            if old_value != new_value:
                address.province = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrant_business_addresses.province:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrant_business_addresses.province")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrant_business_addresses.province: {str(e)}")
    
    logging.info("Completed clean_registrant_business_addresses_province")

def clean_communications_lobbyist_previous_public_office_holder(session: Session):
    logging.info("Starting clean_communications_lobbyist_previous_public_office_holder")
    try:
        communications = session.query(Communication).filter(Communication.lobbyist_previous_public_office_holder.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for communication in communications:
            old_value = communication.lobbyist_previous_public_office_holder
            new_value = old_value.capitalize() if old_value.islower() else old_value
            if old_value != new_value:
                communication.lobbyist_previous_public_office_holder = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in communications.lobbyist_previous_public_office_holder:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in communications.lobbyist_previous_public_office_holder")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating communications.lobbyist_previous_public_office_holder: {str(e)}")
    
    logging.info("Completed clean_communications_lobbyist_previous_public_office_holder")

def clean_lobbyist_business_addresses_city(session: Session):
    logging.info("Starting clean_lobbyist_business_addresses_city")
    try:
        addresses = session.query(RegistrantBusinessAddress).filter(RegistrantBusinessAddress.city.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for address in addresses:
            old_value = address.city
            new_value = clean_city_name(old_value)
            if old_value != new_value:
                address.city = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrant_business_addresses.city:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrant_business_addresses.city")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrant_business_addresses.city: {str(e)}")
    
    logging.info("Completed clean_lobbyist_business_addresses_city")

def clean_lobbyist_business_addresses_province(session: Session):
    logging.info("Starting clean_lobbyist_business_addresses_province")
    try:
        addresses = session.query(RegistrantBusinessAddress).filter(RegistrantBusinessAddress.province.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for address in addresses:
            old_value = address.province
            new_value = clean_province_name(old_value)
            if old_value != new_value:
                address.province = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrant_business_addresses.province:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrant_business_addresses.province")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrant_business_addresses.province: {str(e)}")
    
    logging.info("Completed clean_lobbyist_business_addresses_province")

def clean_lobbyist_business_addresses_country(session: Session):
    logging.info("Starting clean_lobbyist_business_addresses_country")
    try:
        addresses = session.query(RegistrantBusinessAddress).filter(RegistrantBusinessAddress.country.isnot(None))
        update_count = 0
        changes = defaultdict(int)
        
        for address in addresses:
            old_value = address.country
            new_value = clean_country_name(old_value)
            if old_value != new_value:
                address.country = new_value
                update_count += 1
                changes[f"'{old_value}' -> '{new_value}'"] += 1
        
        session.commit()
        
        if update_count > 0:
            logging.info(f"Updated {update_count} rows in registrant_business_addresses.country:")
            for change, count in changes.items():
                logging.info(f"  {change}: {count} occurrences")
        else:
            logging.info("No updates were necessary in registrant_business_addresses.country")
    
    except Exception as e:
        session.rollback()
        logging.error(f"Error updating registrant_business_addresses.country: {str(e)}")
    
    logging.info("Completed clean_lobbyist_business_addresses_country")

def run_data_cleaning(session: Session):
    logging.info("Starting data cleaning operations")
    clean_registrants_previous_public_office_holder(session)
    clean_registrant_business_addresses_province(session)
    clean_registrant_business_addresses_country(session)

    clean_communications_lobbyist_previous_public_office_holder(session)

    clean_lobbyist_business_addresses_city(session)
    clean_lobbyist_business_addresses_province(session)
    clean_lobbyist_business_addresses_country(session)

    logging.info("Completed data cleaning operations")