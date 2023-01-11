from typing import List, Union
import typing
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager

"""/\ 9"""
@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

"""\/ """

def AsyncSessionFromInfo(info):
    return info.context['session']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

""" /\ 29"""
from gql_events.GraphResolvers import resolveEventsForUser
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        async with withInfo(info) as session:
            result = await resolveEventsForUser(session,  self.id, startdate, enddate)
            return result


from gql_events.GraphResolvers import resolveEventsForGroup
@strawberryA.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session,  self.id, startdate, enddate)
            return result
            
""" \/ 60"""

from gql_events.GraphResolvers import resolveEventById, resolveUsersForEvent, resolveGroupsForEvent
@strawberryA.federation.type(keys=["id"], description="")
class EventGQLModel:
    #gql_ug - GraphTypeDefinitions - 15
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveEventById(session,  id)
            #result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition # little hack :)
            return result
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        return self.name

    @strawberryA.field(description="""start""")
    def start(self) -> datetime.datetime:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> datetime.datetime:
        return self.end

    @strawberryA.field(description="""capacity""")
    def capacity(self) -> int:
        return self.capacity

    @strawberryA.field(description="""comment""")
    def comment(self) -> str:
        return self.comment

from gql_events.GraphResolvers import resolveEventById

    #resolver pro EventType ??
    #propojeni federace 


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver

@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result


    @strawberryA.field
    def hello(self) -> str:
        return "Hello World"
    """
    @strawberry.field
    def event_by_id(self, info:strawberry.types.info, id: uuid.UUID) -> EventGQLModel:
        return EventGQLModel(id=1)
    """
 
    #gql_ug - GraphTypeDefinitions - 424
    @strawberryA.field(description="""Finds an event by their id""")
    async def event_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union['EventGQLModel', None]:
        result = await resolveEventById(AsyncSessionFromInfo(info), id)
        return result  

#event_by_location - bude potreba resolver

    
