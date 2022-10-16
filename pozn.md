kopie do githubu
vlastni projekt-konkretni kontejner
vytvorit vedle gql_ug: gql_ug-kopie-"zkousky" a zde zacit praci
verze alpha 80% projektu: SQL + postgres !!! za 2 tydny !!!

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


Projetkotvy den
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

apl.unob.cz/rozvrh/api/read/rozvrh?id=4 