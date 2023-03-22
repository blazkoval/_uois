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


from gql_events.GraphResolvers import resolveEventById, resolveOrganizersForEvent, resolveParticipantsForEvent, resolveGroupsForEvent
@strawberryA.federation.type(keys=["id"], description="")
# It's a GraphQL model for the Event class
class EventGQLModel:
    #gql_ug - GraphTypeDefinitions - 15
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        """
        It takes a class and an id, and returns an object of that class with the given id
        
        :param cls: The class that is being resolved
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: The result of the query is a list of Event objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventById(session,  id)
            #result._type_definition = UserGQLModel()._type_definition # little hack :)
            result._type_definition = cls._type_definition # little hack :)
            return result
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        """
        It returns the id of the object.
        :return: The id of the user
        """
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        """
        This function returns the name of the person
        :return: The name of the person
        """
        return self.name

    @strawberryA.field(description="""start""")
    def start(self) -> Union[datetime.datetime, None]:
        """
        It returns the start time of the event.
        :return: The start time of the event.
        """
        return self.start

    @strawberryA.field(description="""end""")
    def end(self) -> Union[datetime.datetime,None]:
        """
        It returns the end date of the event.
        :return: The end date of the event.
        """
        return self.end

    @strawberryA.field(description="""capacity""")
    def capacity(self) -> Union[int,None]:
        """
        It returns the capacity of the array.
        :return: The capacity of the vehicle.
        """
        return self.capacity

    @strawberryA.field(description="""comment""")
    def comment(self) -> Union[str,None]:
        """
        This function returns the comment of the current object
        :return: The comment
        """
        return self.comment
   
    @strawberryA.field(description="""lastchange""") # ?? default=datetime.datetime.now
    def lastchange(self) -> Union[datetime.datetime,None]:
        """
        It returns the lastchange value of the object.
        :return: The lastchange attribute of the object.
        """
        return self.lastchange
    
    @strawberryA.field(description="""is the membership is still valid""")
    async def valid(self) -> Union[bool, None]:
        """
        It returns a boolean value.
        :return: The valid attribute of the class.
        """
        return self.valid
    
    @strawberryA.field(description="""Event's type (like Zkouška)""")
    async def eventtype(self, info: strawberryA.types.Info) -> Union['EventTypeGQLModel', None]:
        """
        If the eventtype_id is None, return None, otherwise, return the result of the
        resolveEventTypeById function.
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: The result of the query is being returned.
        """
        async with withInfo(info) as session:
            if self.eventtype_id is None:
                return None
            else:
                #result = resolveEventTypeById(session,  self.grouptype_id)
                result = await resolveEventTypeById(session, self.eventtype_id)
                return result   
   
    @strawberryA.field(description="""facility, related to a event""")
    async def facility(self) -> 'FacilityGQLModel':
        return FacilityGQLModel(id=self.facility_id)

    # @strawberryA.field(description="""Facility (like K44/175)""")
    # async def facility(self, info: strawberryA.types.Info) -> Union['FacilityGQLModel', None]:
    #     """
    #     It returns a list of FacilityGQLModel objects
        
    #     :param info: strawberryA.types.Info
    #     :type info: strawberryA.types.Info
    #     :return: A list of FacilityGQLModel objects.
    #     """
    #     async with withInfo(info) as session:            
    #         links = await resolveFacilityForEvent(session,  self.id)
    #         result = list(map(lambda item: item.group, links))
    #         print('event.facility', result)
    #         return result

    @strawberryA.field(description="""Participants of the event""")
    async def participants(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        """
        It returns a list of UserGQLModel objects, which are the participants of the event
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: A list of UserGQLModel objects.
        """
        async with withInfo(info) as session:
            links = await resolveParticipantsForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links))
            print('event.prts', result)
            return result

    @strawberryA.field(description="""Organizers of the event""")
    async def organizers(self, info: strawberryA.types.Info) -> List['UserGQLModel']:
        """
        It returns a list of UserGQLModel objects, which are the organizers of the event
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: A list of UserGQLModel objects.
        """
        async with withInfo(info) as session:
            links = await resolveOrganizersForEvent(session,  self.id)
            result = list(map(lambda item: item.user, links)) 
            #result = list(map(lambda item: UserGQLModel.resolve_reference(info, item.user_id))) #nelze číst
            print('event.orgs', result)
            return result

    @strawberryA.field(description="""Groups of users linked to the event""")
    async def groups(self, info: strawberryA.types.Info) -> List['GroupGQLModel']:
        """
        It returns a list of GroupGQLModel objects, which are the groups associated with the event
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: A list of GroupGQLModel objects.
        """
        async with withInfo(info) as session:
            links = await resolveGroupsForEvent(session,  self.id)
            result = list(map(lambda item: item.group, links))
            print('event.group', result)
            return result
        
    @strawberryA.field(description="""Returns the event's editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['EventEditorGQLModel', None]:
        """
        It returns the object itself.
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: The return type is a Union of two types.
        """
        return self 
    
from gql_events.GraphResolvers import resolveEventTypeById, resolveEventForEventType
@strawberryA.federation.type(keys=["id"], description="")
# It's a GraphQL model for a SQLAlchemy model
class EventTypeGQLModel:
    
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        """
        It takes a class and an id, and returns an object of that class with the given id
        
        :param cls: The class that is being resolved
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: The result of the query.
        """
        #result = await resolveGroupTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventTypeById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result    
    
    @strawberryA.field(description="""primary key""")
    def id(self) -> strawberryA.ID:
        """
        It returns the id of the object.
        :return: The id of the user
        """
        return self.id
    
    @strawberryA.field(description="""name""")
    def name(self) -> Union[str, None]:
        """
        This function returns the name of the person
        :return: The name of the person
        """
        return self.name

    @strawberryA.field(description="""List of events which have this type""")
    async def events(self, info: strawberryA.types.Info) -> typing.List['EventGQLModel']:
        """
        This function is called by the GraphQL server when a client requests the events field of an
        EventType object. It uses the info object to get the current session, then calls the
        resolveEventForEventType function to get the list of Event objects, and returns that list.
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: A list of EventGQLModel objects
        """
        #result = await resolveGroupForGroupType(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveEventForEventType(session, self.id)
            return result    

@strawberryA.federation.type(keys=["id"], description="")
# `FacilityGQLModel` is a class that has a `resolve_reference` method that returns a
# `FacilityGQLModel` instance with an `id` attribute
class FacilityGQLModel:
    # Creating a field called ID in the strawberryA table.
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        """
        It takes a class and an ID, and returns an instance of that class with the given ID
        
        :param cls: The class of the object you want to resolve
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: A FacilityGQLModel object
        """
        return FacilityGQLModel(id=id)
        
    # @strawberryA.field(description="""primary key""")
    # def id(self) -> strawberryA.ID:
    #     """
    #     It returns the id of the object.
    #     :return: The id of the user
    #     """
    #     return self.id

from gql_events.GraphResolvers import resolveEventsForOrganizer, resolveEventsForParticipant
@strawberryA.federation.type(extend=True, keys=["id"])
# The class is a GQL model for a user. It has two fields, events_o and events_p, which return lists of
# events.
class UserGQLModel:
    # Creating a field called ID in the strawberryA table.
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        """
        It takes a class and an ID, and returns an instance of that class with the given ID
        
        :param cls: The class of the object you want to resolve
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: A UserGQLModel object
        """
        print("Jsem tu")
        return UserGQLModel(id=id)

    @strawberryA.field(description="""Events O""")
    async def events_o(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        """
        It takes in a startdate and enddate, and returns a list of events that are between those dates
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param startdate: datetime.datetime = None, enddate: datetime.datetime = None
        :type startdate: datetime.datetime
        :param enddate: datetime.datetime = None
        :type enddate: datetime.datetime
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForOrganizer(session,  self.id, startdate, enddate)
            return result
        
    @strawberryA.field(description="""Events P""")
    async def events_p(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        """
        It takes a participant id, and returns a list of events that the participant is associated with
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param startdate: datetime.datetime = None, enddate: datetime.datetime = None
        :type startdate: datetime.datetime
        :param enddate: datetime.datetime = None, startdate: datetime.datetime = None
        :type enddate: datetime.datetime
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForParticipant(session,  self.id, startdate, enddate)
            return result


from gql_events.GraphResolvers import resolveEventsForGroup
@strawberryA.federation.type(extend=True, keys=["id"])
# The `events` method returns a list of `EventGQLModel` objects
class GroupGQLModel:
    # Creating a field called ID in the strawberryA table.
    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        """
        It takes a class and an ID, and returns an instance of that class with the given ID
        
        :param cls: The class that is being resolved
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: A GroupGQLModel object
        """
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""Events""")
    async def events(self, info: strawberryA.types.Info, startdate: datetime.datetime = None, enddate: datetime.datetime = None) -> List['EventGQLModel']:
        """
        It takes in a group id, startdate, and enddate, and returns a list of events that are associated
        with that group
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param startdate: datetime.datetime = None, enddate: datetime.datetime = None
        :type startdate: datetime.datetime
        :param enddate: datetime.datetime = None, startdate: datetime.datetime = None
        :type enddate: datetime.datetime
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session,  self.id, startdate, enddate)
            return result


###########################################################################################################################
# 
#                                       GQL EDITORY
#                                       
###################################################################################################################

from gql_events.GraphResolvers import resolveUpdateEvent, resolveRemoveEvent, resolveRemoveParticipant
@strawberryA.input(description="""Entity representing a project update""")
# > This class is used to update an event
class EventUpdateGQLModel:
    lastchange: datetime.datetime
    name: Optional[str] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    capacity: Optional[int] = None
    comment: Optional[str] = None
    eventtype_id:  Optional[uuid.UUID] = None
    facility_id: Optional[uuid.UUID] = None

@strawberryA.input
# This class is used to create a new event
class EventInsertGQLModel:
    id: Optional[strawberryA.ID] = None
    name: Optional[str] = None
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    capacity: Optional[int] = None
    comment: Optional[str] = None
    eventtype_id:  Optional[uuid.UUID] = None
    facility_id: Optional[uuid.UUID] = None

from gql_events.GraphResolvers import resolveUpdateEvent, resolveInsertEvent, resolveInsertOrganizer, resolveInsertParticipant, resolveRemoveOrganizer
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable event""")
# The class is a wrapper around the event model. It provides a set of methods to manipulate the event
# model
class EventEditorGQLModel:
    # Assigning the value None to the variable strawberryA.ID.
    id: strawberryA.ID = None
    # Declaring a variable called result and assigning it the value of None.
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        """
        It takes a class and an id, and returns an object of that class
        
        :param cls: The class that is being resolved
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: strawberryA.ID
        :type id: strawberryA.ID
        :return: The result of the query.
        """
        # result = await resolveGroupById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventById(session, id)
            result._type_definition = cls._type_definition  # little hack :)
            return result
   
    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        """
        It returns the id of the object.
        :return: The id of the user.
        """
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        """
        It returns the result of the function.
        :return: The result of the calculation.
        """
        return self.result
    
    @strawberryA.field(description="""Link to the event.""")
    async def event(self, info: strawberryA.types.Info) -> EventGQLModel:
        """
        The function is an async function that takes in a self and info object and returns an
        EventGQLModel object
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: The result of the query.
        """
        # result = await resolveEventById(session,  self.id)
        async with withInfo(info) as session:
            result = await resolveEventById(session, self.id)
            return result

    @strawberryA.field(description="""Updates event data""")
    async def update(self, info: strawberryA.types.Info, data: EventUpdateGQLModel) -> 'EventEditorGQLModel':
        """
        If the lastchange value in the data object is the same as the lastchange value in the database,
        then return a resultMsg of "fail", otherwise return a resultMsg of "ok".
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param data: EventUpdateGQLModel
        :type data: EventUpdateGQLModel
        :return: The return type is EventEditorGQLModel.
        """
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
        """
        It takes in an event id, finds the event in the database, sets the valid flag to false, and
        returns the event
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: The return type is the EventGQLModel.
        """
        async with withInfo(info) as session:
            event = await resolveEventById(session, self.id)
            event.valid = False
            await session.commit()
            return event
        
    @strawberryA.field(description="""Remove event""")
    async def remove_event(self, info: strawberryA.types.Info) -> str:
        """
        It takes in a GraphQL query, and returns a string
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :return: The result of the mutation.
        """
        async with withInfo(info) as session:
            result = await resolveRemoveEvent(session, self.id)
            return result
        
    @strawberryA.field(description="""Create a new event""")
    async def create_event(
        self, info: strawberryA.types.Info, event: EventInsertGQLModel
    ) -> "GroupGQLModel":
        """
        I'm trying to create a new event and return it
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param event: EventInsertGQLModel
        :type event: EventInsertGQLModel
        :return: The new event that was created.
        """
        # newGroup = await resolveInsertGroup(session,  group, extraAttributes={'mastergroup_id': self.id})
        # Creating a new event and returning it.
        async with withInfo(info) as session:
            newEvent = await resolveInsertEvent(
                session, event, extraAttributes={"masterevent_id": self.id}
            )
            print(newEvent)
            return newEvent
        
    @strawberryA.field(description="""Create new organizer""")
    async def add_organizer(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'UserGQLModel':
        """
        It takes a user_id and an event_id, and inserts a row into the organizers table with those
        values
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param user_id: uuid.UUID
        :type user_id: uuid.UUID
        :return: The return value is a UserGQLModel object.
        """
        async with withInfo(info) as session:
            await resolveInsertOrganizer(session, None, extraAttributes={'user_id': user_id, 'event_id': self.id})
            return UserGQLModel.resolve_reference(id=user_id)
    
    @strawberryA.field(description="""Remove organizer""")
    async def remove_organizer(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'UserGQLModel':
        """
        It removes the organizer from the database and returns the user object
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param user_id: uuid.UUID
        :type user_id: uuid.UUID
        :return: The return value is a UserGQLModel object.
        """
        async with withInfo(info) as session:
            await resolveRemoveOrganizer(session, user_id)
            return UserGQLModel.resolve_reference(id=user_id)  
            # result = await resolveRemoveOrganizer(session, user_id)
            # return result

    @strawberryA.field(description="""Create new participant""")
    async def add_participant(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'UserGQLModel':
        """
        It takes a user_id and an event_id, and inserts a row into the database with those values
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param user_id: uuid.UUID
        :type user_id: uuid.UUID
        :return: The return type is a UserGQLModel.
        """
        async with withInfo(info) as session:
            await resolveInsertParticipant(session, None, extraAttributes={'user_id': user_id, 'event_id': self.id})
            return UserGQLModel.resolve_reference(id=user_id)

    @strawberryA.field(description="""Remove participant""")
    async def remove_participant(self, info: strawberryA.types.Info, user_id: uuid.UUID) -> 'UserGQLModel':
        """
        It removes a participant from an event, and returns the user that was removed
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param user_id: uuid.UUID
        :type user_id: uuid.UUID
        :return: The return value is a UserGQLModel object.
        """
        async with withInfo(info) as session:
            await resolveRemoveParticipant(session, user_id)
            return UserGQLModel.resolve_reference(id=user_id)  
            # result = await resolveRemoveOrganizer(session, user_id)
            # return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from gql_events.GraphResolvers import resolveEventPage, resolveEventTypePage
from typing import Optional
@strawberryA.type(description="""Type for query root""")
# It's a class that contains a bunch of methods that return data.
class Query:
   
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello_events(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        """
        It takes a UUID as an argument and returns a string
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID
        :type id: uuid.UUID
        :return: The return type is a Union of str and None.
        """
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[EventGQLModel]:
        """
        It takes in a skip and limit, and returns a list of EventGQLModel objects
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param skip: int = 0, limit: int = 10, defaults to 0
        :type skip: int (optional)
        :param limit: int = 10, defaults to 10
        :type limit: int (optional)
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventPage(session,  skip, limit)
            return result

    @strawberryA.field(description="""Finds a particulat event""")
    async def event_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventGQLModel, None]:
        """
        "This function takes in a GraphQL info object and an id, and returns an EventGQLModel or None."
        
        The info object is a GraphQL object that contains information about the current GraphQL request
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID
        :type id: uuid.UUID
        :return: The return type is a Union of EventGQLModel and None.
        """
        async with withInfo(info) as session:
            result = await resolveEventById(session,  id)
            return result

    @strawberryA.field(description="""Finds all events for an organizer""")
    async def event_by_organizer(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        """
        > This function returns a list of events for a given organizer
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID
        :type id: uuid.UUID
        :param startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] =
        None
        :type startdate: Optional[datetime.datetime]
        :param enddate: Optional[datetime.datetime] = None
        :type enddate: Optional[datetime.datetime]
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForOrganizer(session, id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for an participant""")
    async def event_by_participant(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        """
        `resolveEventsForParticipant` is a function that takes a session, a participant id, and two
        dates, and returns a list of events
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate:
        Optional[datetime.datetime] = None
        :type id: uuid.UUID
        :param startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] =
        None
        :type startdate: Optional[datetime.datetime]
        :param enddate: Optional[datetime.datetime] = None
        :type enddate: Optional[datetime.datetime]
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForParticipant(session,  id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds all events for a group""")
    async def event_by_group(self, info: strawberryA.types.Info, id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] = None) -> List[EventGQLModel]:
        """
        It takes in a group id, and a start and end date, and returns a list of events that are
        associated with that group
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID, startdate: Optional[datetime.datetime] = None, enddate:
        Optional[datetime.datetime] = None
        :type id: uuid.UUID
        :param startdate: Optional[datetime.datetime] = None, enddate: Optional[datetime.datetime] =
        None
        :type startdate: Optional[datetime.datetime]
        :param enddate: Optional[datetime.datetime] = None
        :type enddate: Optional[datetime.datetime]
        :return: A list of EventGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventsForGroup(session,  id, startdate, enddate)
            return result

    @strawberryA.field(description="""Finds a event type by its id""")
    async def event_type_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[EventTypeGQLModel, None]:
        """
        This function takes a session object and an id and returns an EventTypeGQLModel object or None
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param id: uuid.UUID
        :type id: uuid.UUID
        :return: The return type is a Union of EventTypeGQLModel and None.
        """
        #result = await resolveEventTypeById(session,  id)
        async with withInfo(info) as session:
            result = await resolveEventTypeById(session, id)
            return result

    @strawberryA.field(description="""Finds all events paged""")
    async def event_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[EventTypeGQLModel]:
        """
        It takes in a skip and limit, and returns a list of EventTypeGQLModel objects
        
        :param info: strawberryA.types.Info
        :type info: strawberryA.types.Info
        :param skip: int = 0, limit: int = 10, defaults to 0
        :type skip: int (optional)
        :param limit: int = 10, defaults to 10
        :type limit: int (optional)
        :return: A list of EventTypeGQLModel objects.
        """
        async with withInfo(info) as session:
            result = await resolveEventTypePage(session,  skip, limit)
            return result

    #event_by_facility - nejspis nebude potreba, pokud ano tak dodelat resolver
    
    #zavolat rndm structure
    @strawberryA.field(description="""Finds all events paged""")
    async def load_event_data(self, info: strawberryA.types.Info,) -> str:
        """
        It takes a graphql info object, and uses the asyncSessionMaker object from the info object to
        create a new asyncSessionMaker object, and then uses that to call the PutDemodata function
        
        :param info: strawberryA.types.Info,
        :type info: strawberryA.types.Info
        :return: The return value is a string.
        """
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

# Creating a schema for the Query class and the UserGQLModel class.
schema = strawberryA.federation.Schema(Query, types=(UserGQLModel, ))    
