# Data Munging

Code is licensed under the MIT Licence and data is licensed under the Open Government Licence

Do not trust existing data:
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
    - Deal with PositionTitle
    
Address 
    - Deal with person who put there country as toronto
Person
    - Some people spill their name with all uppercase 
    - One looks like this Terence (Terry)
    - More dedup is needed
    - process_person clean up O(N) operation

Grassroot
    - Target can be made more structured

beneficiary
    - Should 'Controlling Interest','Controlling interest holder' be megered
    
TRUST
    - We need to trust that RegistrationNumber is unique

My promblem last time was that I introduced too much bad data. I won't proceed past  Registrant until I get it work as expected

Schema
- Not POH_Ty it's POH_Type
- Not CommunicationsMethod it's CommunicationMethod
- Not CommunicationGroupid it's CommunicationGroupId
- Not LobbyistPublicOfficeHolder it's PreviousPublicOfficeHolder
- Not LobbyistPreviousPublicOfficeHoldPosition it's PreviousPublicOfficeHoldPosition
- Not LobbyistPreviousPublicOfficeHoldPosition it's PreviousPublicOfficePositionProgramName
- Not LobbyistPreviousPublicOfficePositionProgramName it's PreviousPublicOfficeHoldLastDate
- Not LobbyistPreviousPublicOfficeHoldLastDate it's PreviousPublicOfficeHoldLastDate
- Beneficiaries.BusinessAddress doesn't always have phone?

- Meeting.Desc is always empty
- Lobbyist.Business is always empty

Lessons learnt
- Commits are expensive

Todo:
- Clean up Pipfile
- Update files need for Github Action
- Clean up .gitignore
- Deal with devcontainer.json warnings
- Think about this: [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html)
- SQL is default nullable
- Update get_enum_error_message for null values
- More code reuse in build
- Remove back_ref [Using the legacy ‘backref’ relationship parameter¶](https://docs.sqlalchemy.org/en/20/orm/backref.html)
- Make template names consistent 
- Create Person Pages (Public Officer Holder)

