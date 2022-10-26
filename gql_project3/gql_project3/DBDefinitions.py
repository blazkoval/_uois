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
class EventModel(BaseModel):

    __tablename__ = 'Event'

    id = UUIDColumn()
    name = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)
    capacity = Column(Integer)
    comment = Column(String)

    EventType = relationship('EventType', back_populates='Event')
    Location = relationship('Location', back_populates='Event')
    Lesson = relationship('Lesson', back_populates='Event')
    Subject = relationship('Subject', back_populates='Event')
    #Group = relationship('Group', back_populates='Event')
    #User = relationship('User', back_populates='Event')

class EventType(BaseModel):
    __tablename__ = 'EventType'

    id = UUIDColumn()
    name = Column(String)

    Event = relationship('EventModel', back_populates='EventType')

class Location(BaseModel):
    __tablename__ = 'Location'

    id = UUIDColumn()
    name = Column(String)

    Event = relationship('EventModel', back_populates='Location')

class Lesson(BaseModel):
    __tablename__ = 'Lesson'

    id = UUIDColumn()
    name = Column(String)
    subject_id = UUIDColumn()

    Event = relationship('EventModel', back_populates='Lesson')
    Subject = relationship('Subject', back_populates='Lesson')

class Subject(BaseModel):
    __tablename__ = 'Subject'

    id = UUIDColumn()
    name = Column(String)

    Event = relationship('EventModel', back_populates='Subject')
    Lesson = relationship('Lesson', back_populates='Subject')

class Group(BaseModel):
    __tablename__ = 'Group'

    id = UUIDColumn()
    name = Column(String)

    Event = relationship('EventModel', back_populates='Group')

class User(BaseModel):
    __tablename__ = 'User'

    id = UUIDColumn()
    name = Column(String)

    Event = relationship('EventModel', back_populates='User')




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