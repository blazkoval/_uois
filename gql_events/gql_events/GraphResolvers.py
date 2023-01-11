
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
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
from gql_events.DBDefinitions import UserModel, GroupModel, LocationModel, LessonModel, SubjectModel
from gql_events.DBDefinitions import EventGroupModel, EventOrganizerModel, EventParticipantModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

# event resolvers
resolveEventById = createEntityByIdGetter(EventModel)
resolveEventPage = createEntityGetter(EventModel) # ?? k cemu to je?
resolveEventAll = createEntityGetter(EventModel) # ?? k cemu to je?
resolveUpdateEvent = createUpdateResolver(EventModel)
resolveInsertEvent = createInsertResolver(EventModel)

resolveLessonsForEvent = create1NGetter(LessonModel, foreignKeyName='event_id')

#resolveUsersForEvent = create1NGetter(Event_Organizer, foreignKeyName='event_id', options=joinedload(Event_Organizer.user))
resolveUsersForEvent = create1NGetter(EventOrganizerModel, foreignKeyName='event_id', options=joinedload(EventOrganizerModel.user))
# ??? pro participants
#resolveGroupsForEvent = create1NGetter(EventGroupModel, foreignKeyName='event_id', options=joinedload(EventGroupModel.group))

# eventtype resolvers
resolveEventTypeById = createEntityByIdGetter(EventTypeModel)
resolveEventForEventType = create1NGetter(EventModel, foreignKeyName = 'eventtype_id')
resolveUpdateEventType = createUpdateResolver(EventTypeModel)
resolveInsertEventType = createInsertResolver(EventTypeModel)


# group resolvers ??
resolveEventsForGroup_ = create1NGetter(EventGroupModel, foreignKeyName='group_id', options=joinedload(EventGroupModel.event))

from sqlalchemy.future import select
async def resolveEventsForGroup(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventGroupModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventGroupModel.group_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result

# lesson resolvers ??

# location resolvers ?? nebude potreba, pokud se budu v QUery taza

# subject resolvers ??

# user reslovers
resolveEventsForUser_ = create1NGetter(EventOrganizerModel, foreignKeyName='user_id', options=joinedload(EventOrganizerModel.event))

async def resolveEventsForUser(session, id, startdate=None, enddate=None):
    statement = select(EventModel).join(EventOrganizerModel)
    if startdate is not None:
        statement = statement.filter(EventModel.start >= startdate)
    if enddate is not None:
        statement = statement.filter(EventModel.end <= enddate)
    statement = statement.filter(EventOrganizerModel.user_id == id)

    response = await session.execute(statement)
    result = response.scalars()
    return result
    
