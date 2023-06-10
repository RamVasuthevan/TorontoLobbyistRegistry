# TorontoLobbyistRegistry

Do not trust their:
    - Schema
    - Data validation
    - Data Cleaning

- Enum vs lookup table
- Enum should be in a coherent order or alphabetical


How do I handle people?
    - 
    - Clean up Prefix.ERROR

How do I handle address?

LobbyingReport
    - Deal with Subject Matter

Registrant
    - Deal with RegistrationNUmberWithSoNum
    - Registrant Status superseded means that there is a new registrant record. The data I am working with 141 registration_number with mutiple non-SUPERSEDED rows (All active). This is gonna be a pain in the ass
        - SELECT * FROM (SELECT COUNT(registration_number) as count, * FROM (SELECT DISTINCT registration_number, status, effective_date, type, prefix, first_name, middle_initial, last_name, suffix FROM registrant WHERE STATUS != "SUPERSEDED") GROUP BY registration_number) WHERE count>1  ;
    - People can't spell there own name consistently 
        - SELECT DISTINCT registrant.registration_number, prefix, first_name, middle_initial, last_name, suffix FROM registrant INNER JOIN (SELECT registration_number FROM (SELECT DISTINCT registration_number, prefix, first_name, middle_initial, last_name, suffix FROM registrant) GROUP BY registration_number HAVING COUNT(registration_number)>2 ORDER BY COUNT(registration_number),registration_number) t ON registrant.registration_number = t.registration_number;
        - I could be people in a grassroots org using using the same registration_number 
        - REGISTRATION_NUMBERS
        - For now I will be setting puting dummy registrant with registration_number="00000S"
    - Deal with suffix
    



Todo:
    - Clean up Pipfile
    - Update files need for Github Action
    - Clean up .gitignore
    - Deal with devcontainer.json warnings
    - Think about this: [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)


