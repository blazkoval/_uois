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


Event_Participant = Table('events_participants', BaseModel.metadata,
    Column('event_id', ForeignKey('event.id'), primary_key=True),
    Column('participant_id', ForeignKey('user.id'), primary_key=True)
    )

Event_Organizer = Table('events_organizers', BaseModel.metadata,
    Column('event_id', ForeignKey('event.id'), primary_key=True),
    Column('organizer_id', ForeignKey('user.id'), primary_key=True)
    )

Event_Group = Table('events_groups', BaseModel.metadata,
    Column('event_id', ForeignKey('event.id'), primary_key=True),
    Column('group_id', ForeignKey('group.id'), primary_key=True)
    )

class EventModel(BaseModel):

    __tablename__ = 'event'

    id = UUIDColumn()
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    capacity = Column(Integer)
    comment = Column(String)
    lastchange = Column(DateTime, default=datetime.datetime.now)
    
    eventtype_id = Column(ForeignKey('eventtype.id'))
    location_id = Column(ForeignKey('location.id'))
    
    eventtype = relationship('EventTypeModel', back_populates='events')
    location = relationship('LocationModel', back_populates='events')
    lessons = relationship('LessonModel', back_populates='event')

    participants = relationship('UserModel', secondary=Event_Participant, back_populates='events_participants')
    organizers = relationship('UserModel', secondary=Event_Organizer, back_populates='events_organizers')
    groups = relationship('GroupModel', secondary=Event_Group, back_populates='events_groups')

class EventTypeModel(BaseModel):
    __tablename__ = 'eventtype'

    id = UUIDColumn()
    name = Column(String)

    events = relationship('EventModel', back_populates='eventtype')

class LocationModel(BaseModel):
    __tablename__ = 'location'

    id = UUIDColumn()
    name = Column(String)

    events = relationship('EventModel', back_populates='location')

class LessonModel(BaseModel):
    __tablename__ = 'lesson'

    id = UUIDColumn()
    name = Column(String)
    
   
    event_id = Column(ForeignKey('event.id')) # ?
    subject_id = Column(ForeignKey('subject.id'))

    event = relationship('EventModel', back_populates='lessons')
    subject = relationship('SubjectModel', back_populates='lessons')

class SubjectModel(BaseModel):
    __tablename__ = 'subject'

    id = UUIDColumn()
    name = Column(String)

    lessons = relationship('LessonModel', back_populates='subject')

class GroupModel(BaseModel):
    __tablename__ = 'group'

    id = UUIDColumn()
    name = Column(String)

    events = relationship('EventModel', secondary=Event_Group, back_populates='events_groups')

class UserModel(BaseModel):
    __tablename__ = 'user'

    id = UUIDColumn()
    name = Column(String)

    events_p = relationship('EventModel', secondary=Event_Participant, back_populates='events_participants')
    events_o = relationship('EventModel', secondary=Event_Organizer, back_populates='events_organizers')

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