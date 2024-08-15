from sqlalchemy.orm import Session
from models import Registrant, RegistrantBusinessAddress
import logging
from collections import defaultdict

def clean_country_name(country):
    if not country:
        return None
    
    country = country.strip().lower()
    
    country_mapping = {
        'canada': 'Canada',
        'united states': 'United States',
        'usa': 'United States',
        'u.s.a.': 'United States',
        'us': 'United States',
        'united states of america': 'United States',
        'united state america': 'United States',
        'united states ': 'United States',
        'united-states': 'United States',
        'united states': 'United States',
        'u.s.': 'United States',
        'singapore': 'Singapore',
        'italy': 'Italy',
        'united kingdom': 'United Kingdom',
        'uk': 'United Kingdom',
        'england': 'United Kingdom',
        'france': 'France',
        'toronto': 'Canada',
        'ontario': 'Canada',
        'quebec': 'Canada',
        'switzerland': 'Switzerland',
        'suisse': 'Switzerland',
        'nigeria': 'Nigeria',
        'slovakia': 'Slovakia',
        'australia': 'Australia',
        'india': 'India',
        'brazil': 'Brazil',
        'brasil': 'Brazil',
        'germany': 'Germany',
        'nederland': 'Netherlands',
        'netherlands': 'Netherlands',
        'the netherlands': 'Netherlands',
        'united arab emirates': 'United Arab Emirates',
        'austria': 'Austria',
        'spain': 'Spain',
        'prc': 'China',
        'china': 'China',
        'sweden': 'Sweden',
        'belgium': 'Belgium',
        'south korea': 'South Korea',
        'etats-unis': 'United States',
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
    }
    
    # Handle special cases
    if country in ['can', 'cad', 'cdn', 'cda', 'ca', 'c', 'canad', 'cananda', 'canda', 'caanda']:
        return 'Canada'
    
    if country in ['canadá', 'canadÃ¡']:
        return 'Canada'
    
    # Check if the country is in our mapping
    if country in country_mapping:
        return country_mapping[country]
    
    # If not found in mapping, capitalize the first letter of each word
    return country.title()

def clean_province_name(province):
    if not province:
        return None
    
    province = province.strip().upper()
    
    province_mapping = {
        'ON': 'Ontario',
        'ONTARIO': 'Ontario',
        'ONT': 'Ontario',
        'ONT.': 'Ontario',
        'ONTAIO': 'Ontario',
        'ONTAIRO': 'Ontario',
        'ONTARI': 'Ontario',
        'ONTARIA': 'Ontario',
        'ONTARO': 'Ontario',
        'ONTATIO': 'Ontario',
        'ONTATRIO': 'Ontario',
        'ONTRARIO': 'Ontario',
        'ONTRIO': 'Ontario',
        'QC': 'Quebec',
        'QUEBEC': 'Quebec',
        'QUÉBEC': 'Quebec',
        'BC': 'British Columbia',
        'B.C.': 'British Columbia',
        'BRITISH COLUMBIA': 'British Columbia',
        'BRITISH COLOUMBIA': 'British Columbia',
        'BRITISH COLMBIA': 'British Columbia',
        'AB': 'Alberta',
        'ALBERTA': 'Alberta',
        'MB': 'Manitoba',
        'MANITOBA': 'Manitoba',
        'MANTIOBA': 'Manitoba',
        'SK': 'Saskatchewan',
        'NB': 'New Brunswick',
        'NS': 'Nova Scotia',
        'PE': 'Prince Edward Island',
        'PEI': 'Prince Edward Island',
        'NL': 'Newfoundland and Labrador',
        'YT': 'Yukon',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        
        # US States
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
        'DC': 'District of Columbia',
    }
    
    # Check if the province is in our mapping
    if province in province_mapping:
        return province_mapping[province]
    
    # If not found in mapping, return the original value
    return province.title()

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

def run_data_cleaning(session: Session):
    logging.info("Starting data cleaning operations")
    clean_registrants_previous_public_office_holder(session)
    clean_registrant_business_addresses_country(session)
    clean_registrant_business_addresses_province(session)
    logging.info("Completed data cleaning operations")