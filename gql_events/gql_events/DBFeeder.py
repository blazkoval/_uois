from doctest import master
from functools import cache
from gql_workflow.DBDefinitions import BaseModel, UserModel, GroupModel, RoleTypeModel

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

data = {
    'events': [
        {'id':'73dda931-1629-4193-963a-c55397b0a706','name':'Slavnostni nastup',
         'start': datetime.datetime(), 'end': datetime.datetime() + datetime.timedelta(hours=1,minutes=30),
         'eventType':'nastup',
         'location':'',
         'lessons':[
                {'id':''}
            ],
         'groups':[
                {'id':''}
            ],
         'participants':[
                {'id':'0cd946af-b840-4b6f-ae4e-2c4029e531a6','nejakyAtribut':'random','user_id':''}  #user_id je z jineho kontejneru
            ]
        },

        {'id':'d3058a19-5234-4f36-a151-395f07c4eb30','name':'Beseda s Dekanem',
         'start': datetime.datetime(), 'end': datetime.datetime() + datetime.timedelta(hours=1,minutes=30),
         'eventType':'beseda',
         'location':'',
         'lessons':[
                {'id':''}
            ],
         'groups':[
                {'id':''}
            ],
         'participants':[
                {'id':'','nejakyAtribut':'random','user_id':''}
            ]
        },

        {'id':'90749da9-9a42-47f6-b4a8-aff8b15f4a27','name':'Sportovni den',
         'start': datetime.datetime(), 'end': datetime.datetime() + datetime.timedelta(hours=1,minutes=30), #do 16:00
         'eventType':'sport',
         'location':'',
         'lessons':[
                {'id':''}
            ],
         'groups':[
                {'id':''}
            ],
         'participants':[
                {'id':'','nejakyAtribut':'random','user_id':''}
            ]
        }
    ]
}