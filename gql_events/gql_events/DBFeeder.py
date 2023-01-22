from doctest import master
from functools import cache
from gql_workflow.DBDefinitions import BaseModel, EventTypeModel, EventModel, UserModel, GroupModel, FacilityModel

import random
import itertools
from functools import cache
import datetime


from sqlalchemy.future import select

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

# zkratka a jmeno; dodělat funkci; eventGroups, eventUsers??
# import nefunkční

@cache
def DetermineEvents():
    data = [
        {'id':'73dda931-1629-4193-963a-c55397b0a706','name':'',
            'start': datetime.datetime(), 'end': datetime.datetime() + datetime.timedelta(hours=1,minutes=30),
            'capacity':'',
            'comment':'',
            'lastchange':'',

            'eventtype_id':'',
            'location_id':'',
        }
    ]
    return data

@cache
def DetermineEventTypes():
    data = [
        {'id': '794b4c17-6fde-4a84-bea0-bddbb0632ec4', 'name': 'Cviceni'},
        {'id': 'c9a55358-e1c0-4873-abea-43a72516e282', 'name': 'Prednaska'},
        {'id': 'ecd54144-ba57-4292-abc7-502d64c209a0', 'name': 'Seminar'},
        {'id': '14f68158-aeab-4e76-862e-fd2079892a59', 'name': 'Slavnostni nastup'},
        {'id': '9387085c-bca1-4470-88b4-2e72241e7de6', 'name': 'Sportovni den'},
        {'id': '29f1c23b-c74a-4070-ac54-658672129699', 'name': 'Beseda'},
        {'id': 'a707696e-a051-4876-a995-899f1f27d4d9', 'name': 'Zkouska'},
        {'id': '8e599414-99d8-43fd-bfa6-51ca9a6a2426', 'name': 'Zapoctovy tes'},
        {'id': '61e7d4e4-2bb4-4ce0-8065-7ce2fa61abb4', 'name': 'Jina udalost'},
        {'id': 'b71bac7a-536e-4bac-8aff-687a65127eaa', 'name': 'Samostudium'}, 
    ]
    return data

@cache
def DetermineFacilitys():
    data = [
        {'id': '812d1598-4771-4d38-a52b-4cfeff075488', 'name': 'KJB'},
        {'id': '090d7268-9661-4594-99db-e70c3a187e2d', 'name': 'Sumavska'},
        {'id': '0a5ce699-0763-4e6f-8278-9f19b73d50fd', 'name': 'Kounicova'},
    ]

@cache
def DetermineGroups():
    data = [
        {'id': '4d71b800-d74c-4f02-9d4f-ef01ece884c5', 'name': '23-KB1'}, # zkratka, jmeno?
        {'id': 'aa1b4f1e-42c2-48f9-a5ec-68aec05e529b', 'name': '23-KB-C'},
        {'id': 'cb37641f-27df-46a9-800f-f7057260733a', 'name': '23-5BSV'},
        {'id': '8becd27a-2793-455b-960e-e4964672e9f9', 'name': '23-5LTZ'},
        {'id': '67bb9e0d-1b28-45ef-be19-05f6a10c320d', 'name': '23-5RLP'},
        {'id': '649420bf-8dc1-4154-8055-688f1e696b05', 'name': '23-5ZM'},
    ]

@cache
def DetermineUsers():
    data = [

    ]



import asyncio
async def predefineAllDataStructures(asyncSessionMaker):
     asyncio.gather(
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventModel, DetermineEvents),
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventTypeModel, DetermineEventTypes),
        putPredefinedStructuresIntoTable(asyncSessionMaker, FacilityModel, DetermineFacilitys),
        putPredefinedStructuresIntoTable(asyncSessionMaker, GroupModel, DetermineGroups),
        putPredefinedStructuresIntoTable(asyncSessionMaker, UserModel, DetermineUsers),
        
     )

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction): # dodělat funkci

    externalIdTypes = structureFunction()