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
    - Look likes RegistrationNUmberWithSoNum is per person
    - Should be though of as the RegistrationNUmberWithSoNum same
    - This is Rakr
        - https://www.linkedin.com/in/moyaghi/
    
Address 
    - Deal with person who put there country as toronto
Person
    - Some people spill their name with all uppercase 
    - One looks like this Terence (Terry)
    - More dedup is needed
    - process_person clean up O(N) operation

TRUST
    - We need to trust that RegistrationNumber is unique

My promblem last time was that I introduced too much bad data. I won't proceed past  Registrant until I get it work as expected

Todo:
    - Clean up Pipfile
    - Update files need for Github Action
    - Clean up .gitignore
    - Deal with devcontainer.json warnings
    - Think about this: [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
    - SQL is default nullable
    - Update get_enum_error_message for null values


