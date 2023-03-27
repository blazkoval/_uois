# Průběhový deník
čet. Lenka Blažková, čet. Filip Zindler
## Projekt č. 3 - zadání:
Vytvořte datové struktury pro definici:
- události
- typ události (výuka, zkouška, apod.)
- místa jejího konání (viz 2.)
- organizátorů (učitelé)
- účastníků (skupiny i jednotlivci) (viz 1.)<br/>
neopomeňte vztah k předmětu, k lekci v předmětu (viz 7.).

## 10. 10. 2022
Zvěřejnění harmonogramu projektu, upřesnění zadání a společných podmínek. Vytvořili jsme si fork z https://github.com/hrbolek/_uois/tree/v2.1, kde je náš pracovní prostor.

## 16. 10.
Vytvořili jsme si schéma, abychom si ujasnili strukturu naší databáze.</br>
schema_vAlpha.pdf

## 17. 10.
Přidali jsme si základní SQLAlchemy modely a jejich atributy v DBDefinition podle schéma. 

## 18. 10. - projektový den
Prezentovali jsme naše schéma a dosud vytvořené modely v DBDefinition. Ujasnili jsme si jaké modely se týkají našeho projektu a jaký vztah mezi nimi budou. Např. vztah Lesson:Event je N:1, vypustili jsme SubjectModel z naší databáze.

## 25. 10. 
Modely jsme programovali v prostředí jupyteru v experimental.ipynb, abychom nemuseli pokaždé celý náš projekt spouštět přes docker-compose. Vyrázně se se urychlí celá činnost při úpravách a kontrole chyb v naší databázi. V experimental.ipynb máme stručný postup, jak vytvářet databáze v SQLAlchemy.

## 29. 11. 2022 - projektový den (verze alfa)
Prezentovali jsme naši databázi v pgAdminu, kterou jsme vytvářeli v DBDefinition.

## 29. 11. 2022 
Začali jsme vytvářet GQL modely a resolvery v GraphTypeDefinition a GraphResolvers, zatím jen pro EventModel. Zde jsme pracovali přímo v souborech gql_event v prostředí VS code, protože v prostředí jupyteru nám nešlo spustit http://localhost:31102/gql/, kde jsme chtěli ověřovat funkčnost GQL modelů.
## 11. 01. 2023 - projektový den (verze beta)
Prezentovali jsme první GQL modely a řešlili jsme nefunkčnost GraphiQL spuštěného z jupyteru.

## 11. 01. 2023
Změnili jsme mezilehlé tabulky pro relace Event-Participant a Event-Organizer z Table() na class, abychom mohli využít předdefinované resolvery.</br>
První demo data v DBFeeder.

## 12. 01.
Upravili jsme schéma, tak aby odpovídalo názvům tabulek a vztahům z databází kolegů.</br>
schema_vBeta.pdf

## 19. 01.
Přidali jsme frontend kontejner. Po konzultaci jsme vypustili i LessonModel, protože odpovědnost a tedy rozšíření pro EventModel spadá pod projekt č. 7.</br>
Do pgAdminu jsme vložili základní demo data a ověřili jsme funkčnost GQL modelů v prostředí GraphiQL (http://localhost:31128/gql/).<br>
schema_final.pdf

## 22. 01. - 21. 02.
Úpravy v DBFeederu. Demo data se zapsali do naší databáze a zobrazují se v pgAdminu.

## 04. 03.
Začali jsme vytvářet editor pro Event.

## 14. 03.
Vytvořili jsme metody update a insert pro úpravu základních dat v Eventu (ne cizí klíče). Přidali jsme metody create a invalidate pro vytvoření a zneplatnění (nahrazuje smazání) Eventu.

## 15. 03.
Přidali jsme metody pro přiřazení organizer a participant k eventu (add_organizer, add_participant)

## 20. 03.
Opravili jsme veškeré chyby, tak aby bylo možné všechny metody realizovat v GraphiQL.

## 27. 03. - prezentace finální verze

## Docker Image
https://hub.docker.com/layers/megalekk/gql_events/latest/images/sha256-ae1d4987d78a82caf2fee500119632bf196e9dac17acc939224d5df5d2e9efed?context=explore&fbclid=IwAR2O0bD2V4zLGzyFojLLYJMpISu-bUbFsasqYhYzqit99Y_VrAT27AFV5sM