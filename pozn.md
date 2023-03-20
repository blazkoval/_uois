kopie do githubu
vlastni projekt-konkretni kontejner
vytvorit vedle gql_ug: gql_ug-kopie-"zkousky" a zde zacit praci

docker compose - pro spusteni
docker image - vyvtarime, zverejnime cele komunite
connectionstring

UUID pouzivat
    ma vyhody ale i nevyhody (nekompabilita s jinymi databazemi)

vazby mezi projekty (viz 1, 2, 6) - federace (odpoved z dilcich kontejneru) - umoznovat vazby - foreignkey - odkaz na "UUID"

definice pojmu:
    kontejner reprezentuje "zabalenou" aplikaci, je posazen vedle dalsich kontejneru, spolecne vytvari aplikaci
    localhost - muj pc

naplnit vzorovymi daty - daji se ulozit do jasonu a mit je porad stejna
    v DBFeeder radky 40, 311,....
    GraphTypeDefinitions - kdy se DBFeeder spousti (naplnuji se data)? funkce se vola pres GQL

gql_events - je "fake" doplnkovy - ukazuje federaci
    events2, vychazet ze vzoroveho projektu

strukturalizovat projekt do vice soubru: DBDef, DBFeed., GraphResolver - zkopírovat, GraphTypeDef. - gql modely, resolvery
v mainu se vytvari aplikace - řádek 73

pg admin:
    hostname, postgres všude


# 1. Projetkotvy den - cile
kde je adresar, ukazat commit

Struktura graphql slozena z vice vsrtev
    databaze nad tim graphql + vsrtva apollo - prekryva endpointy, "lezi nad vsemi"

Scaling = škálovatelnost - 

uživatelské prostředí:
    localhost:port/gql

mutace = schopnost menit data v databazi
    create
    update (write)
    delete - zneplatneni
mutace relaci - ??

nakopírovat si modely v gql_events > main.py

smazat subject, prohodit vztah lesson */1 event

# Projektak
17 kontejneru

spoluprace s richterem
    musime se shodnout na nazvech EventGQL

# Alfa verze - 29.11.
Struktury databaze, modely, cteni z databaze (ne generovani nahodnych dat) 20 %

# 20.10.
gql_empty

# 26.10.
Proč nám nejde v pg adminu po compose up naše modely: Event, EventType
Jak zprovoznit jupyter? - Event, EventType - už se zobrazují, ale neaktualizují se
Nečitelné https://github.com/hrbolek/learning/blob/master/notebooks/inf/05B_sqlalchemy.ipynb

# projektový den 29.11.
localhost:31180/ui/api - API celého systému
               /api/nogql/utils/umlschema - schema celeho systemu

model který není zodpovědný vypadá jinak (extarnal)

# Beta verze - 12.01.
vyuzivat tu novou verzi na hrbolek github - GraphResolvers

v README.md jsou rady 

podle gql_ug > GTD
vytvorit editor EventEditorGQLModel, navazat na entitu 
    resolve_reference zkopirovat i s ID
    pridat atributy ID a result
    update zkopirovat krom Modelu a resolverUpdate...
    pridat metody update, insert atd.
    jestlize je lastchange, tak...?

    Editor bude jen jeden

# konzultace 19.01.

smazat lessonModel i v resolverech

frontend kontejner - stahnout a pridat do dockercompose
stahnout nginx.config z hrbolek

localhost:80/ui/api 

v jupyteru http request - na konci 05D:

import requests

query = """query {
    user(id: 1) {
        id
        name
        surname
        email
    }

    group(id: 1) {
        id
        name
    }
}"""
payload = {'query': query}
r = requests.post("http://localhost:9994/gql", json=payload)
result = r.json()

print(result)


http://apollo:3000/gql poslat request, da odpoved v jsonu

# po konzultaci
![GraphiQL - proč je tam group_id?](gql_events/gql_events/Graphiql.png)
dosavadní postup ověřen přes pgadmin a GraphiQL - vše funkční

# TO DO:

gql editory (mutace)
external_id
-	K primary key (ID) vždy přidružte external_id (indexed)
-	Primary key je typu UUID, external_id je string
docker image (na docker hub)
vygenerovaná dokumantace
příběh, deník
prezentace:
- integrace do uois?
- jupyter

# 4.3.
v DBFeeder - řádek 42 -> odkomentovat facility

podle gql_ug > GTD
vytvorit editor EventEditorGQLModel, navazat na entitu 
    resolve_reference zkopirovat i s ID
    pridat atributy ID a result
    update zkopirovat krom Modelu a resolverUpdate...
    pridat metody update, insert atd.
    jestlize je lastchange, tak...?

    Editor bude jen jeden


# v GraphTypeDefinitions:

EventGQLModel
+ resolve_references
+ atributy z SQL
+ editor ...z EventEditorGQLModel - spusti editor v rozhrani

EventTypeGQLModel
+ resolvereferences
+ atributy z SQL

UserGQLModel
+ id ...z UserGQLModel
+ resolve_references
+ events a events

FacilityGQLModel ??

# jak na editory

EventUpdateGQLModel - zakladni polozky v tabulce
+ atributy:
    name: Optional[str] = None
    ...
    participant, organizer - specificke metody v EditorGQL - add a invalidate

EventEditorGQLModel ??
+ atributy:
    id X
    result X
+ metody:
    resolve_refenrece X
    event ...z EventGQLModel X
    update ...z EventUpdateGQLModel - prijima dat. strukturu, ktera meni event
    invalidate - misto remove - zneplatni polozku

    add_organizer
        user_id - jediny parametr
    add_participant
        user_id

    remove - musi byt ke kazdemu add (sql alchemy delete row - pro resolver) pouziva se misto nej invalidate

    invalidate - musi se pridat atribut valid do modelu



EventTypeUpdateGQLModel - ne

EventTypeEditorGQLModel - ne


delete:
session.query(EventModel).filter(EventModel.id).delete()
session.commit()

async def putSingleEntityToDb(session, entity):
    async with session.begin():
        session.add(entity)
    await session.commit()
    return entity


# co ted?
pridat add a remove (popr invalidate) pro organizer a participant

# po konzultaci 15.03.
resolveInsertOrganizer = createInsertResolver(UserModel)
- nahradit za resolveInsertOrganizer = createInsertResolver(EventOrganizerModel)
- pri pridavani organizer musi uuid existovat v tabulce "users"

mozna bude potreba zmena v async def organizers -> result = ...
- > po teto zmene nelze cist uzivatele


# a dal
facility v gql nefunguje
"Entity namespace for \"facilities\" has no property \"event_id\""
- spatne definovany v EventGQLModel ?
-> opraveno v EventGQL, smazano id z FacilityGQL

add_organizer, add_participants:
- po upravach po konzultaci, vše funguje jak má, do pg adminu se změny propíší, ale z nějakého důvodu to háže error v graphiql
-> opraveno: problem v UserGQLModel: resolve_reference
    - chyba odstraněna metodou pokus omyl, už ani nevím jak, přidávala jsem tam parametr info, pak zase odstraňovala až to začalo fungovat

