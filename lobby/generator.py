
import json
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import joinedload, Load

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import Mapped
from sqlalchemy import Table

import pprint as pp
import json
from typing import List, Dict, Any, Union, Optional
from lobby import LobbyParser, downloader
from itertools import chain

from lobby.uploader import *

import os

engine = create_engine("sqlite:///TorontoLobbyistRegistry.db", echo=False, future=True)

import yaml
from sqlalchemy.orm import selectinload
import json

from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import DeclarativeMeta

import zipfile
import yaml
import os
from sqlalchemy.orm import selectinload

class Generator:

    def __init__(self):
        pass

    @staticmethod
    def generate_markdown():
        print('start')

        # Create a new zip file to store the YAML documents
        with zipfile.ZipFile('yaml_documents.zip', 'w') as zipf:
            with Session(engine) as session:
                results = session.query(SubjectMatter).options(selectinload('*')).all()
                for idx,val in enumerate(results):
                    print(f"{idx+1}/{len(results)}: {val.SMNumber}")
                    
                    # Convert the object to a dictionary including related objects
                    data_dict = val.as_dict()
                    
                    # Save the YAML content in a variable
                    yaml_content = yaml.dump(data_dict, sort_keys=False, default_flow_style=False)
                    
                    # Write the YAML content to a file
                    with open(val.SMNumber + '.markdown', 'w') as outfile:
                        outfile.write("---\n")
                        outfile.write("layout: subjectmatter")
                        outfile.write("\n---")
                        outfile.write(yaml_content)

                    # Add the YAML file to the zip file
                    zipf.write(val.SMNumber + '.markdown')

                    # Remove the YAML file after adding it to the zip file
                    os.remove(val.SMNumber + '.markdown')

        print('end')