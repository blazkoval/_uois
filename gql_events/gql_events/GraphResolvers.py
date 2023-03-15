
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

#from gql_workflow.DBDefinitions import BaseModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################
from gql_events.DBDefinitions import EventModel, EventTypeModel
from gql_events.DBDefinitions import UserModel, GroupModel, FacilityModel
from gql_events.DBDefinitions import EventGroupModel, EventOrganizerModel, EventParticipantModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

# event resolvers
resolveEventById = createEntityByIdGetter(EventModel)
resolveEventPage = createEntityGetter(EventModel)
resolveEventAll = createEntityGetter(EventModel)
resolveUpdateEvent = createUpdateResolver(EventModel)
resolveInsertEvent = createInsertResolver(EventModel)

async def resolveRemoveEvent(session, event_id):
    """
    It deletes a row from the EventModel table where the id matches the event_id passed in
    
    :param session: the session object
    :param event_id: the id of the event to be deleted
    :return: The result of the query.
    """
    stmt = delete(EventModel).where(EventModel.id==event_id)
    resultMsg= ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if(response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
        
    except:
        resultMsg="error"
  
    return resultMsg

# Creating a resolver for the event model.
resolveOrganizersForEvent = create1NGetter(EventOrganizerModel, foreignKeyName='event_id', options=joinedload(EventOrganizerModel.user))
resolveParticipantsForEvent = create1NGetter(EventParticipantModel, foreignKeyName='event_id', options=joinedload(EventParticipantModel.user))
resolveGroupsForEvent = create1NGetter(EventGroupModel, foreignKeyName='event_id', options=joinedload(EventGroupModel.group))

# eventtype resolvers
# Creating a resolver for the event type model.
resolveEventTypeById = createEntityByIdGetter(EventTypeModel)
resolveEventTypePage = createEntityGetter(EventTypeModel)
resolveUpdateEventType = createUpdateResolver(EventTypeModel)
resolveInsertEventType = createInsertResolver(EventTypeModel)
resolveEventForEventType = create1NGetter(EventModel, foreignKeyName = 'eventtype_id')

# lesson resolvers - odpovednost projekt c. 7 ... vypuštěno

# facility resolvers - nebude potreba, pokud se budu v Query ptat na event_by_facility tak ano

# group resolvers
resolveEventsForGroup_ = create1NGetter(EventGroupModel, foreignKeyName='group_id', options=joinedload(EventGroupModel.event))

from sqlalchemy.future import select
async def resolveEventsForGroup(session, id, startdate=None, enddate=None):
    """
    It returns a list of events that are associated with a group, and optionally filtered by a start and
    end date
    
    :param session: the session object
    :param id: the id of the group
    :param startdate: datetime.datetime
    :param enddate: datetime.datetime(2020, 1, 1, 0, 0)
    :return: A list of EventModel objects.
    """
    statement = select(EventModel).join(EventGroupModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventGroupModel.group_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result

# user reslovers
resolveEventsForUser_ = create1NGetter(EventOrganizerModel, foreignKeyName='user_id', options=joinedload(EventOrganizerModel.event))

async def resolveEventsForOrganizer(session, id, startdate=None, enddate=None):
    """
    It returns a list of events that are organized by a user with a given id, and that are between a
    given start and end date
    
    :param session: the session object
    :param id: the id of the organizer
    :param startdate: datetime.datetime
    :param enddate: datetime.datetime
    :return: A list of EventModel objects
    """
    statement = select(EventModel).join(EventOrganizerModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventOrganizerModel.user_id == id)
    response = await session.execute(statement)
    result = response.scalars()
    return result

async def resolveEventsForParticipant(session, id, startdate=None, enddate=None):
    """
    It returns a list of events that a user is participating in, given a start and end date
    
    :param session: the session object
    :param id: The id of the user
    :param startdate: datetime.datetime
    :param enddate: datetime.datetime
    :return: A list of EventModel objects.
    """
    statement = select(EventModel).join(EventParticipantModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventParticipantModel.user_id == id)
    response = await session.execute(statement)
    result = response.scalars()
    return result
            
resolveInsertOrganizer = createInsertResolver(EventOrganizerModel)
resolveInsertParticipant = createInsertResolver(EventParticipantModel)