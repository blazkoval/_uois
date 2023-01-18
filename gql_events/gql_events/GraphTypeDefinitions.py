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




from gql_events.GraphResolvers import resolveEventById, resolveOrganizersForEvent, resolveParticipantsForEvent, resolveGroupsForEvent, resolveLessonsForEvent, resolveFacilityForEvent 
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
    def start(self) -> Union[datetime.datetime, None]:
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> Union[datetime.datetime,None]:
        return self.end

    @strawberryA.field(description="""capacity""")
    def capacity(self) -> Union[int,None]:
        return self.capacity

    @strawberryA.field(description="""comment""")
    def comment(self) -> Union[str,None]:
        return self.comment
   
    @strawberryA.field(description="""lastchange""") # ?? default=datetime.datetime.now
    def lastchange(self) -> Union[datetime.datetime,None]:
        return self.lastchange
    

    @strawberryA.field(description="""Organizers of the event""")
    async def organizers(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        async with withInfo(info) as session:
            links = await resolveOrganizersForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links))
            print('event.orgs', result)
            return result
   
    @strawberryA.field(description="""Participants of the event""")
    async def participants(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        async with withInfo(info) as session:
            links = await resolveParticipantsForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links))
            print('event.prts', result)
            return result

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List['GroupGQLModel']:
        async with withInfo(info) as session:
            links = await resolveGroupsForEvent(session,  self.id)
            result = list(map(lambda item: item.group, links))
            print('event.group', result)
            return result
    
    @strawberryA.field(description="""Event's type (like Zkouška)""")
    async def eventtype(self, info: strawberryA.types.Info) -> Union['EventTypeGQLModel', None]:
        async with withInfo(info) as session:
            if self.eventtype_id is None:
                return None
            else:
                #result = resolveEventTypeById(session,  self.grouptype_id)
                result = await resolveEventTypeById(session, self.eventtype_id)
                return result

    @strawberryA.field(description="""Facility (like K44/175)""")
    async def facility(self, info: strawberryA.types.Info) -> Union['FacilityGQLModel', None]:
        async with withInfo(info) as session:
            links = await resolveFacilityForEvent(session,  self.id)
            result = list(map(lambda item: item.group, links))
            print('event.facility', result)
            return result
    
    
    @strawberryA.field(description="""""")
    async def lessons(self, info: strawberryA.types.Info) -> List['LessonGQLModel']:
        async with withInfo(info) as session:
            links = await resolveLessonsForEvent(session,  self.id)
            result = list(map(lambda item: item.group, links))
            print('event.lessons', result)
            return result


from gql_events.GraphResolvers import resolveEventTypeById, resolveEventForEventType
@strawberryA.federation.type(keys=["id"], description="")
class EventTypeGQLModel:
    
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        #result = await resolveGroupTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventTypeById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result    
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        return self.name

    @strawberryA.field(description="""List of groups which have this type""")
    async def groups(self, info: strawberryA.types.Info) -> typing.List['EventGQLModel']:
        #result = await resolveGroupForGroupType(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveEventForEventType(session, self.id)
            return result    

""" /\ 29"""
from gql_events.GraphResolvers import resolveEventsForOrganizer, resolveEventsForParticipant
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Events O""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        async with withInfo(info) as session:
            result = await resolveEventsForOrganizer(session,  self.id, startdate, enddate)
            return result
    @strawberryA.field(description="""Events P""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        async with withInfo(info) as session:
            result = await resolveEventsForParticipant(session,  self.id, startdate, enddate)
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

@strawberryA.federation.type(keys=["id"], description="")
class LessonGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return LessonGQLModel(id=id)
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        return self.name

@strawberryA.federation.type(keys=["id"], description="")
class FacilityGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return FacilityGQLModel(id=id)
        
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        return self.name

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from gql_events.GraphResolvers import resolveEventPage, resolveEventTypePage
from typing import Optional
@strawberryA.type(description="""Type for query root""")
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_events(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventPage(session,  skip, limit)
            return result

    @strawberryA.field(description="""Finds a particulat event""")
    async def event_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveEventById(session,  id)
            return result

    @strawberryA.field(description="""Finds all events for an organizer""")
    async def event_by_organizer(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForOrganizer(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for an participant""")
    async def event_by_participant(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForParticipant(session,  id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for a group""")
    async def event_by_group(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session,  id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds a event type by its id""")
    async def event_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventTypeGQLModel, None]:
        #result = await resolveEventTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventTypeById(session, id)
            return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[EventTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveEventTypePage(session,  skip, limit)
            return result



    #gql_ug - GraphTypeDefinitions - 424


#event_by_facility - bude potreba resolver

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))    
