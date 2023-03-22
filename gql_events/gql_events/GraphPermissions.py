from sqlalchemy.future import select
import strawberry

from gql_ug.DBDefinitions import BaseModel, UserModel, GroupModel, MembershipModel, RoleModel
from gql_ug.DBDefinitions import GroupTypeModel, RoleTypeModel

def AsyncSessionFromInfo(info):
    """
    It takes the context of the request and returns the session object.
    
    :param info: This is the GraphQLResolveInfo object that contains the information about the query
    :return: The session object
    """
    return info.context['session']

def UserFromInfo(info):
    """
    It returns the user object from the context of the request
    
    :param info: This is the GraphQLResolveInfo object that contains information about the current
    request
    :return: The user object
    """
    return info.context['user']

# `BasePermission` is a class that inherits from `strawberry.permission.BasePermission` and overrides
# the `has_permission` method
class BasePermission(strawberry.permission.BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('BasePermission', source)
        print('BasePermission', self)
        print('BasePermission', kwargs)
        return True

# > The `GroupEditorPermission` class is a subclass of `BasePermission` and it's `has_permission`
# method returns `True` if the user is authenticated and has the `GroupEditor` role in the group
class GroupEditorPermission(BasePermission):
    message = "User is not authenticated"
    
    async def canEditGroup(session, group_id, user_id):
        stmt = select(RoleModel).filter_by(group_id=group_id, user_id=user_id)
        dbRecords = await session.execute(stmt).scalars()
        dbRecords = [*dbRecords] # konverze na list
        if len(dbRecords) > 0 :
            return True
        else:
            return False

    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('GroupEditorPermission', source)
        print('GroupEditorPermission', self)
        print('GroupEditorPermission', kwargs)
        #_ = await self.canEditGroup(AsyncSessionFromInfo(info), source.id, ...)
        print('GroupEditorPermission')
        return True

# `UserEditorPermission` is a class that inherits from `BasePermission` and overrides the
# `has_permission` method
class UserEditorPermission(BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('UserEditorPermission', source)
        print('UserEditorPermission', self)
        print('UserEditorPermission', kwargs)
        return True

# `UserGDPRPermission` is a class that inherits from `BasePermission` and overrides the
# `has_permission` method
class UserGDPRPermission(BasePermission):
    message = "User is not authenticated"
    
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        print('UserGDPRPermission', source)
        print('UserGDPRPermission', self)
        print('UserGDPRPermission', kwargs)
        return True

