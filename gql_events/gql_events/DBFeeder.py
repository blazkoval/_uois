from doctest import master
from functools import cache
from gql_events.DBDefinitions import BaseModel, EventTypeModel, EventModel
import random
import itertools
from functools import cache
import datetime
from datetime import time


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

# zkratka a jmeno; Users??; dodělat funkci; eventGroups, eventUsers??

@cache
def DetermineEvents():
    data = [
        {'id':'73dda931-1629-4193-963a-c55397b0a706','name':'Matematika',
            'start': time(8, 0), 'end': time(9, 30),
            'capacity':'40',
            'comment':'Linearni Funkce',
            'lastchange': datetime.date.today(),

            'eventtype_id':'c9a55358-e1c0-4873-abea-43a72516e282',
            'facility_id':'', # ručně, cizí kliče musí existovat
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

import asyncio
async def predefineAllDataStructures(asyncSessionMaker):
     await asyncio.gather(
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventModel, DetermineEvents),
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventTypeModel, DetermineEventTypes),
        
     )

async def PutDemodata(asyncSessionMaker):
    await asyncio.gather(
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventModel, DetermineEvents),
        putPredefinedStructuresIntoTable(asyncSessionMaker, EventTypeModel, DetermineEventTypes),
        
    )

async def putPredefinedStructuresIntoTable(asyncSessionMaker, DBModel, structureFunction):
    """Zabezpeci prvotni inicicalizaci typu externích ids v databazi
       DBModel zprostredkovava tabulku, je to sqlalchemy model
       structureFunction() dava data, ktera maji byt ulozena
    """
    # ocekavane typy 
    externalIdTypes = structureFunction()
    
    #dotaz do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = list(dbSet.scalars())
    
    #extrakce dat z vysledku dotazu
    #vezmeme si jen atributy name a id, id je typu uuid, tak jej zkovertujeme na string
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
        ]

    print(structureFunction, 'external id types found in database')
    print(dbRowsDicts)

    # vytahneme si vektor (list) id, ten pouzijeme pro operator in nize
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # zjistime, ktera id nejsou v databazi
    unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))
    print(structureFunction, 'external id types not found in database')
    print(unsavedRows)

    # pro vsechna neulozena id vytvorime entity
    rowsToAdd = [DBModel(**row) for row in unsavedRows]
    print(rowsToAdd)
    print(len(rowsToAdd))

    # a vytvorene entity jednou operaci vlozime do databaze
    async with asyncSessionMaker() as session:
        async with session.begin():
            session.add_all(rowsToAdd)
        await session.commit()

    # jeste jednou se dotazeme do databaze
    stmt = select(DBModel)
    async with asyncSessionMaker() as session:
        dbSet = await session.execute(stmt)
        dbRows = dbSet.scalars()
    
    #extrakce dat z vysledku dotazu
    dbRowsDicts = [
        {'name': row.name, 'id': f'{row.id}'} for row in dbRows
        ]

    print(structureFunction, 'found in database')
    print(dbRowsDicts)

    # znovu id, ktera jsou uz ulozena
    idsInDatabase = [row['id'] for row in dbRowsDicts]

    # znovu zaznamy, ktere dosud ulozeny nejsou, mely by byt ulozeny vsechny, takze prazdny list
    unsavedRows = list(filter(lambda row: not(row['id'] in idsInDatabase), externalIdTypes))

    # ted by melo byt pole prazdne
    print(structureFunction, 'not found in database')
    print(unsavedRows)
    if not(len(unsavedRows) == 0):
        print('SOMETHING is REALLY WRONG')

    print(structureFunction, 'Defined in database')
    # nyni vsechny entity mame v pameti a v databazi synchronizovane
    print(structureFunction())
    pass