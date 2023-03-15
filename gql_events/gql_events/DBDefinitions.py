from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    """
    It creates a column with a UUID data type, and sets it as the primary key, and sets the default
    value to a random UUID
    
    :param name: The name of the column
    :return: A Column object with the following properties:
    """
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Creating a base class for all of your models.
BaseModel = declarative_base()

def UUIDColumn(name=None):
    """
    It creates a column with a UUID data type, and sets it as the primary key, and sets the default
    value to a random UUID
    
    :param name: The name of the column
    :return: A Column object with the following properties:
    """
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)

#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)    
class EventParticipantModel(BaseModel):
    # Defining the name of the table in the database.
    __tablename__ = "events_participants"
    # A function that returns a Column object.
    id = UUIDColumn()
    # Creating a foreign key relationship between the two tables.
    event_id = Column(ForeignKey('events.id'))
    user_id = Column(ForeignKey('users.id'))

    # Creating a relationship between the two tables.
    event = relationship('EventModel', back_populates = 'participants')
    user = relationship('UserModel', back_populates = 'events_p')

# The EventOrganizerModel class is a model that represents the events_organizers table in the database
class EventOrganizerModel(BaseModel):
    # Defining the name of the table in the database.
    __tablename__ = "events_organizers"
    # A function that returns a Column object.
    id = UUIDColumn()
    # Creating a foreign key relationship between the two tables.
    event_id = Column(ForeignKey('events.id'))
    user_id = Column(ForeignKey('users.id'))

    # Creating a relationship between the two tables.
    event = relationship('EventModel', back_populates = 'organizers')
    user = relationship('UserModel', back_populates = 'events_o')

# The EventGroupModel class is a table that has a foreign key to the EventModel and GroupModel tables
class EventGroupModel(BaseModel):
    # Defining the name of the table in the database.
    __tablename__ = "events_groups"
    # A function that returns a Column object.
    id = UUIDColumn()
    # Creating a foreign key relationship between the two tables.
    event_id = Column(ForeignKey('events.id'))
    group_id = Column(ForeignKey('groups.id'))

    # Creating a relationship between the two tables.
    event = relationship('EventModel', back_populates = 'groups')
    group = relationship('GroupModel', back_populates = 'events')

# The EventModel class is a SQLAlchemy model that represents an event
class EventModel(BaseModel):
    # Defining the name of the table in the database.
    __tablename__ = 'events'
    # A function that returns a Column object.
    id = UUIDColumn()
    # Creating a column in the database with the name of the variable and the type of the variable.
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    capacity = Column(Integer)
    comment = Column(String)
    # Setting the default value of the column to the current time.
    lastchange = Column(DateTime, default=datetime.datetime.now)
    # Creating a column in the database with the name of the variable and the type of the variable.
    valid = Column(Boolean, default=True)
    ######lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.mow())
    # Creating a foreign key relationship between the two tables.
    eventtype_id = Column(ForeignKey('eventtypes.id'))
    facility_id = Column(ForeignKey('facilities.id'))

    
    # Creating a relationship between the two tables.
    eventtype = relationship('EventTypeModel', back_populates='events')
    facility = relationship('FacilityModel', back_populates='events')
    participants = relationship('EventParticipantModel', back_populates = 'event')
    organizers = relationship('EventOrganizerModel', back_populates = 'event')
    groups = relationship('EventGroupModel', back_populates='event')

# The EventTypeModel class is a Python class that inherits from the BaseModel class. It has a table
# name of eventtypes, an id column of type UUIDColumn, a name column of type String, and a valid
# column of type Boolean
class EventTypeModel(BaseModel):
    # Defining the name of the table in the database.
    __tablename__ = 'eventtypes'
    # A function that returns a Column object.
    id = UUIDColumn()
    # Creating a column in the database with the name of the variable and the type of the variable.
    name = Column(String)
    valid = Column(Boolean, default=True)

    # Creating a relationship between the EventModel and EventTypeModel classes.
    events = relationship('EventModel', back_populates='eventtype')

# The FacilityModel class inherits from the BaseModel class, which is a class that inherits from the
# declarative_base class
class FacilityModel(BaseModel):
    __tablename__ = 'facilities'
    # A function that returns a Column object.
    id = UUIDColumn()

    # Creating a one-to-many relationship between the EventModel and FacilityModel classes.
    events = relationship('EventModel', back_populates='facility')

# "The GroupModel class is a SQLAlchemy model that represents a group.
# 
# The first line of the class definition is the class name. The second line is the name of the table
# that the class represents. The third line is the primary key of the table. 
class GroupModel(BaseModel):
    __tablename__ = 'groups'
    id = UUIDColumn()

    # Creating a one-to-many relationship between the GroupModel and EventGroupModel classes.
    events = relationship('EventGroupModel', back_populates='group')

# The UserModel class is a SQLAlchemy model that represents a user
class UserModel(BaseModel):
    __tablename__ = 'users'
    # A function that returns a Column object.
    id = UUIDColumn()

    # Creating a one-to-many relationship between the UserModel and EventParticipantModel classes.
    events_p = relationship('EventParticipantModel', back_populates='user')
    events_o = relationship('EventOrganizerModel', back_populates='user')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """
    It creates an async engine, then creates a sessionmaker that uses that engine, and returns the
    sessionmaker
    
    :param connectionstring: The connection string to the database
    :param makeDrop: If True, the database will be dropped before creating the tables, defaults to False
    (optional)
    :param makeUp: If True, the database will be created, defaults to True (optional)
    :return: async_sessionMaker
    """

    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring