from email.policy import default
import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
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

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)    
class EventParticipantModel(BaseModel):
    __tablename__ = "events_participants"
    id = UUIDColumn()
    event_id = Column(ForeignKey('events.id'))
    user_id = Column(ForeignKey('users.id'))

    event = relationship('EventModel', back_populates = 'participants')
    user = relationship('UserModel', back_populates = 'events_p')

class EventOrganizerModel(BaseModel):
    __tablename__ = "events_organizers"
    id = UUIDColumn()
    event_id = Column(ForeignKey('events.id'))
    user_id = Column(ForeignKey('users.id'))

    event = relationship('EventModel', back_populates = 'organizers')
    user = relationship('UserModel', back_populates = 'events_o')

class EventGroupModel(BaseModel):
    __tablename__ = "events_groups"
    id = UUIDColumn()
    event_id = Column(ForeignKey('events.id'))
    group_id = Column(ForeignKey('groups.id'))

    event = relationship('EventModel', back_populates = 'groups')
    group = relationship('GroupModel', back_populates = 'events')

class EventModel(BaseModel):
    __tablename__ = 'events'
    id = UUIDColumn()
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    capacity = Column(Integer)
    comment = Column(String)
    lastchange = Column(DateTime, default=datetime.datetime.now)
    #lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.mow())
    eventtype_id = Column(ForeignKey('eventtypes.id'))
    facility_id = Column(ForeignKey('facilities.id'))
    
    eventtype = relationship('EventTypeModel', back_populates='events')
    facility = relationship('FacilityModel', back_populates='events')
    participants = relationship('EventParticipantModel', back_populates = 'event')
    organizers = relationship('EventOrganizerModel', back_populates = 'event')
    groups = relationship('EventGroupModel', back_populates='event')
class EventTypeModel(BaseModel):
    __tablename__ = 'eventtypes'
    id = UUIDColumn()
    name = Column(String)

    events = relationship('EventModel', back_populates='eventtype')

class FacilityModel(BaseModel):
    __tablename__ = 'facilities'
    id = UUIDColumn()

    events = relationship('EventModel', back_populates='facility')

class GroupModel(BaseModel):
    __tablename__ = 'groups'
    id = UUIDColumn()

    events = relationship('EventGroupModel', back_populates='group')
class UserModel(BaseModel):
    __tablename__ = 'users'
    id = UUIDColumn()

    events_p = relationship('EventParticipantModel', back_populates='user')
    events_o = relationship('EventOrganizerModel', back_populates='user')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
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