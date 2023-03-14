from typing import List, Union, Optional
import typing
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager
from gql_events.DBFeeder import PutDemodata

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


from gql_events.GraphResolvers import resolveEventById, resolveOrganizersForEvent, resolveParticipantsForEvent, resolveGroupsForEvent, resolveFacilityForEvent 
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
    
    @strawberryA.field(description="""is the membership is still valid""")
    async def valid(self) -> Union[bool, None]:
        return self.valid
    
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

    @strawberryA.field(description="""Participants of the event""")
    async def participants(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        async with withInfo(info) as session:
            links = await resolveParticipantsForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links))
            print('event.prts', result)
            return result

    @strawberryA.field(description="""Organizers of the event""")
    async def organizers(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        async with withInfo(info) as session:
            links = await resolveOrganizersForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links))
            print('event.orgs', result)
            return result

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List['GroupGQLModel']:
        async with withInfo(info) as session:
            links = await resolveGroupsForEvent(session,  self.id)
            result = list(map(lambda item: item.group, links))
            print('event.group', result)
            return result
        
    @strawberryA.field(description="""Returns the project editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['EventEditorGQLModel', None]:
        return self 
    
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

    @strawberryA.field(description="""List of events which have this type""")
    async def events(self, info: strawberryA.types.Info) -> typing.List['EventGQLModel']:
        #result = await resolveGroupForGroupType(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveEventForEventType(session, self.id)
            return result    

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
    
""" /\ 29"""
from gql_events.GraphResolvers import resolveEventsForOrganizer, resolveEventsForParticipant
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Events O""")
    async def events_o(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        async with withInfo(info) as session:
            result = await resolveEventsForOrganizer(session,  self.id, startdate, enddate)
            return result
        
    @strawberryA.field(description="""Events P""")
    async def events_p(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
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


###########################################################################################################################
# 
#                                       GQL EDITORY
#                                       
###################################################################################################################
# 
# gql_ug -> GTD -> 388
# podle gql_ug > GTD
#
# vytvorit editor EventEditorGQLModel, navazat na entitu 
#     resolve_reference zkopirovat i s ID
#     pridat atributy ID a result
#     update zkopirovat krom Modelu a resolverUpdate...
#     pridat metody update, insert atd.
#     jestlize je lastchange, tak...?

#     Editor bude jen jeden
from gql_events.GraphResolvers import resolveUpdateEvent, resolveRemoveEvent
@strawberryA.input(description="""Entity representing a project update""")
class EventUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    capacity: Optional[int] = None
    comment: Optional[str] = None
    #eventtype_id:  Optional[uuid.UUID] = None
    #facility_id: Optional[uuid.UUID] = None
    # participants ? - specificke metody v editoru - add a remove
    # organizers ?

@strawberryA.input
class EventInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    capacity: Optional[int] = None
    comment: Optional[str] = None

from gql_events.GraphResolvers import resolveUpdateEvent, resolveInsertEvent
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable event""")
class EventEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        # result = await resolveGroupById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result
   
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result
    
    @strawberryA.field(description="""Link to the event.""")
    async def event(self, info: strawberryA.types.Info) -> EventGQLModel:
        # result = await resolveEventById(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveEventById(session, self.id)
            return result

    @strawberryA.field(description="""Updates event data""")
    async def update(self, info: strawberryA.types.Info, data: EventUpdateGQLModel) -> 'EventEditorGQLModel':
        lastchange = data.lastchange    
        async with withInfo(info) as session:
            await resolveUpdateEvent(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = EventEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result
    
    @strawberryA.field(description="""Invalidate event""")
    async def invalidate_event(self, info: strawberryA.types.Info) -> 'EventGQLModel':
        async with withInfo(info) as session:
            event = await resolveEventById(session, self.id)
            event.valid = False
            await session.commit()
            return event
        
    @strawberryA.field(description="""Remove event""")
    async def remove_event(self, info: strawberryA.types.Info) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveEvent(session, self.id)
            return result
        
    @strawberryA.field(description="""Create a new event""")
    async def create_event(
        self, info: strawberryA.types.Info, event: EventInsertGQLModel
    ) -> "GroupGQLModel":
        # newGroup = await resolveInsertGroup(session,  group, extraAttributes={'mastergroup_id': self.id})
        async with withInfo(info) as session:
            newEvent = await resolveInsertEvent(
                session, event, extraAttributes={"masterevent_id": self.id}
            )
            print(newEvent)
            return newEvent
        
    

    # # insert ????????????
    # @strawberryA.field(description="""Create a new event""")
    # async def add_eventtype(self, info: strawberryA.types.Info, user_id: strawberryA.ID) -> "EventTypeGQLModel":
    #     # result = await resolveInsertEvent(session,  None,
    #     #    extraAttributes={'user_id': user_id, 'group_id': self.id})
    #     async with withInfo(info) as session:
    #         result = await resolveInsertEvent(session, None, extraAttributes={"user_id": user_id, "group_id": self.id})
    #         return result   
    
    # # remove - pridat resolver
    # @strawberryA.field(description="""Remove eventtype""")
    # async def remove_eventtype(self, info: strawberryA.types.Info, finance_id: uuid.UUID) -> str:
    #     async with withInfo(info) as session:
    #         result = await resolveRemoveEventType(session, self.id, finance_id)
    #         return result

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

    #event_by_facility - nejspis nebude potreba, pokud ano tak dodelat resolver
    
    #zavolat rndm structure
    @strawberryA.field(description="""Finds all events paged""")
    async def load_event_data(self, info: strawberryA.types.Info,) -> str:
        asyncSessionMaker = info.context['asyncSessionMaker']
        result = await PutDemodata(asyncSessionMaker)
        return 'ok'        

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))    
