# Data Science: project

The goal of the project is to develop a software that enables one to process data stored in different formats and to upload them into two distinct databases to query these databases simultaneously according to predefined operations. 

## Data

Exemplar data for testing the project have been made available. In particular:

* for creating the graph database, there is one [CSV file](data/doaj.csv) containing metadata about the journals contained in the [Directory of Open Access Journals (DOAJ)](https://doaj.org). Please note that multiple languages of the same journal will be contained in just one string and split by `, `. 

* for creating the relational database, there is one [JSON file](data/scimago.json) containing information of scholarly journals (referenced by their ISSN as identifiers) in terms of their categories and areas of interest as extracted from [Scimago Journal Rank](https://www.scimagojr.com). The name of the categories and the areas acts as their identifier.

It is important to stress that the two files above are just exemplars. It is possible that, during the use of the code developed, a user can use different CSV and JSON files. However, all these files must follow the convention (i.e. the structure) of those provided as exemplars.


## Workflow

![Workflow of the project](img/workflow.png)

## Data model

![Data model](img/datamodel.png)

## UML of data model classes

![Data model classes](img/datamodel-uml.png)

All the methods of each class must return the appropriate value that have been specified in the object of that class when it has been created. It is up to the implementer to decide how to enable someone to add this information to the object of each class, e.g. by defining a specific constructor. While one can add additional methods to each class if needed, it is crucial that the *get* and *has* methods introduced in the UML diagram are all defined.

## UML of additional classes

![Data model classes](img/classes-uml.png)

All the attributes methods of each class are defined as follows. All the constructors of each of the class introduced in the UML diagram do not take in input any parameter. While one can add additional methods to each class if needed, it is crucial that all the methods introduced in the UML diagram are defined.


### Class `Handler`

#### Attributes
`dbPathOrUrl`: the variable containing the path or the URL of the database, initially set as an empty string, that will be updated with the method `setDbPathOrUrl`.

#### Methods
`getDbPathOrUrl`: it returns the path or URL of the database.

`setDbPathOrUrl`: it enables to set a new path or URL for the database to handle.


### Class `UploadHandler`

#### Methods
`pushDataToDb`: it takes in input the path of a file containing annotations and uploads them in the database. This method can be called everytime there is a need to upload annotations in the database. The actual implementation of this method is left to its subclasses.


### Classes `JournalUploadHandler` and `CategoryUploadHandler`

These two classes implements the method of the superclass to handle the specific scenario, i.e. `JournalUploadHandler` to handle CSV files in input and to store their data in a graph database and `CategoryUploadHandler` to handle JSON files in input and to store their data in a relational database.


### Class `QueryHandler`

#### Methods
`getById`: it returns a data frame with all the identifiable entities (i.e. journals, categories, and areas) matching the input identifier (i.e. maximum one entity if there exists one with the input id).


### Class `JournalQueryHandler`

#### Methods
`getAllJournals`: it returns a data frame containing all the journals included in the database.

`getJournalsWithTitle`: it returns a data frame containing all the journals that have, as a title, any that matches (even partially) with the input string.

`getJournalsPublishedBy`: it returns a data frame containing all the journals that have, as a publisher, any that matches (even partially) with the input string.

`getJournalsWithLicense`: it returns a data frame containing all the journals that have the license specified in input.

`getJournalsWithAPC`: it returns a data frame containing all the journals that do specify an Article Processing Charge (APC).

`getJournalsWithDOAJSeal`: it returns a data frame containing all the journals that do specify a DOAJ Seal.


### Class `CategoryQueryHandler`

#### Methods
`getAllCategories`: it returns a data frame containing all the categories included in the database, with no repetitions.

`getAllAreas`: it returns a data frame containing all the areas included in the database, with no repetitions.

`getCategoriesWithQuartile`: it returns a data frame containing all the categories having specified, as input, particular quartiles, with no repetitions. In case the input collection of quartiles is empty, it is like all quartiles are actually specified.

`getCategoriesAssignedToAreas`: it returns a data frame containing all the categories assigned to particular areas specified as input, with no repetitions. In case the input collection of areas is empty, it is like all areas are actually specified.

`getAreasAssignedToCategories`: it returns a data frame containing all the areas assigned to particular categories specified as input, with no repetitions. In case the input collection of categories is empty, it is like all categories are actually specified.


### Class `BasicQueryEngine`

#### Attributes
`journalQuery`: the variable containing the list of `JournalQueryHandler` objects to involve when one of the *get* methods below (needing metadata) is executed. In practice, every time a *get* method is executed, the method will call the related method on all the `JournalQueryHandler` objects included in the variable `journalQuery`, before combining the results with those of other `QueryHandler`(s) and returning the requested object.

`categoryQuery`: the variable containing the list of `CategoryQueryHandler` objects to involve when one of the *get* methods below (needing acquisition and digitisation information) is executed. In practice, every time a *get* method is executed, the method will call the related method on all the `CategoryQueryHandler` objects included in the variable `categoryQuery`, before combining the results with those of other `QueryHandler`(s) and returning the requested object.


#### Methods
`cleanJournalHandlers`: it cleans the list `journalQuery` from all the `JournalQueryHandler` objects it includes.

`cleanCategoryHandlers`: it cleans the list `categoryQuery` from all the `CategoryQueryHandler` objects it includes.

`addJournalHandler`: it appends the input `JournalHandler` object to the list `journalQuery`.

`addCategoryHandler`: it appends the input `CategoryQueryHandler` object to the list `categoryQuery`.

`getEntityById`: it returns an object having class `IdentifiableEntity` identifying the entity available in the databases accessible via the query handlers matching the input identifier (i.e. maximum one entity). In case no entity is identified by the input identifier, `None` must be returned. The object returned must belong to the appropriate class – e.g. if the `IdentifiableEntity` to return is actually a journal, an instance of the class `Journal` (being it a subclass of `IdentifiableEntity`) must be returned.

`getAllJournals`: it returns a list of objects having class `Journal` containing all the journals included in DOAJ.

`getJournalsWithTitle`: it returns a list of objects having class `Journal` containing all the journals in DOAJ that have, as a title, any that matches (even partially) with the input string.

`getJournalsPublishedBy`: it returns a list of objects having class `Journal` containing all the journals in DOAJ that have, as a publisher, any that matches (even partially) with the input string.

`getJournalsWithLicense`: it returns a list of objects having class `Journal` containing all the journals in DOAJ that have the license specified in input.

`getJournalsWithAPC`: it returns a list of objects having class `Journal` containing all the journals in DOAJ that do specify an Article Processing Charge (APC).

`getJournalsWithDOAJSeal`: it returns a list of objects having class `Journal` containing all the journals in DOAJ that do specify a DOAJ Seal.

`getAllCategories`: it returns a list of objects having class `Category` containing all the categories included in Scimago Journal Rank, with no repetitions.

`getAllAreas`: it returns a list of objects having class `Area` containing all the areas included in Scimago Journal Rank, with no repetitions.

`getCategoriesWithQuartile`: it returns a list of objects having class `Category` containing all the categories in Scimago Journal Rank having specified, as input, particular quartiles, with no repetitions. In case the input collection of quartiles is empty, it is like all quartiles are actually specified.

`getCategoriesAssignedToAreas`: it returns a list of objects having class `Category` containing all the categories in Scimago Journal Rank assigned to particular areas specified as input, with no repetitions. In case the input collection of areas is empty, it is like all areas are actually specified.

`getAreasAssignedToCategories`: it returns a list of objects having class `Area` containing all the areas in Scimago Journal Rank assigned to particular categories specified as input, with no repetitions. In case the input collection of categories is empty, it is like all categories are actually specified.


### Class `FullQueyEngine`


#### Methods
`getJournalsInCategoriesWithQuartile`: it returns a list of objects having class `Journal` containing all the journals *in DOAJ* that have, at least one of the input categories specified with the related quartile in *Scimago Journal Rank*, with no repetitions. In case the input collections of categories/quartiles are empty, it is like all categories/quartiles are actually specified.

`getJournalsInAreasWithLicense`: it returns a list of objects having class `Journal` containing all the journals *in DOAJ* with at least one of the licenses specific as input, and that have at least one of the input areas specified in *Scimago Journal Rank*, with no repetitions. In case the input collection of areas/licenses are empty, it is like all areas/licenses are actually specified.

`getDiamondJournalsInAreasAndCategoriesWithQuartile`: it returns a list of objects having class `Journal` containing all the journals *in DOAJ* that have at least one of the input categories (with the related quartiles) specified and at least one of the areas specified in *Scimago Journal Rank*, with no repetitions. In addition, only journals that do not have an Article Processing Charge should be considered in the result. In case the input collection of categories/quartiles/areas are empty, it is like all categories/quartiles/areas are actually specified.



## Uses of the classes

```
# Supposing that all the classes developed for the project
# are contained in the file 'impl.py', then:

# 1) Importing all the classes for handling the relational database
from impl import CategoryUploadHandler, CategoryQueryHandler

# 2) Importing all the classes for handling graph database
from impl import JournalUploadHandler, JournalQueryHandler

# 3) Importing the class for dealing with mashup queries
from impl import FullQueryEngine

# Once all the classes are imported, first create the relational
# database using the related source data
rel_path = "relational.db"
cat = CategoryUploadHandler()
cat.setDbPathOrUrl(rel_path)
cat.pushDataToDb("data/scimago.json")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# Then, create the graph database (remember first to run the
# Blazegraph instance) using the related source data
grp_endpoint = "http://127.0.0.1:9999/blazegraph/sparql"
jou = JournalUploadHandler()
jou.setDbPathOrUrl(grp_endpoint)
jou.pushDataToDb("data/doaj.csv")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# In the next passage, create the query handlers for both
# the databases, using the related classes
cat_qh = CategoryQueryHandler()
cat_qh.setDbPathOrUrl(rel_path)

jou_qh = JournalQueryHandler()
jou_qh.setDbPathOrUrl(grp_endpoint)

# Finally, create a advanced mashup object for asking
# about data
que = FullQueryEngine()
que.addCategoryHandler(cat_qh)
que.addJournalHandler(jou_qh)

result_q1 = que.getAllJournals()
result_q2 = que.getJournalsInCategoriesWithQuartile({"Artificial Intelligence", "Oncology"}, {"Q1"})
result_q3 = que.getEntityById("Artificial Intelligence")
result_q4 = que.getEntityById("2532-8816")
# etc...
```

## Submission of the project

You have to provide all Python files implementing your project, by sharing them in some way (e.g. via OneDrive). You have to send all the files **two days before** the exam session you want to take. Before submitting the project, you must be sure that your code passes a [the basic test](test.py) which aims at checking if the code is runnable and compliant with the specification of the UML. The test has been developed using [`unittest`](https://docs.python.org/3/library/unittest.html), which is one of Python libraries dedicated to tests. 

To run the test, you should:

1. put the file `test.py` in the folder containing the other files with the code you wrote;
2. modify the lines 18-21 in `test.py` if needed, i.e. to import correctly your classes from the files you have created;
3. modify the lines 32-35 in `test.py` if needed, i.e. the paths pointing to the exemplar data used in the test (`doaj.csv`, `scimago.json`), the path of your relational database file and the URL of the SPARQL endpoint of your Blazegraph instance;
4. run your Blazegraph instance as explained in the related hands-on lecture (`java -server -Xmx1g -jar blazegraph.jar`).

Once everything above is set, open the terminal, go to the directory containing the file `test.py`, and run the following command:

```
python -m unittest test
```

It will print on screen status of the execution, reporting on possible errors and mistakes, to allow you to correct them in advance, before the submission. Be aware that this test checks only the compliancy of the methods and the object returned by them, but does not check for additional stuff. You are free, of course, to extend it as you prefer. However, it is **mandatory** that your code passes the test provided without any additional modification (besides the imports mentioned in point (2) and the paths mentioned in point (3)) **before** submitting it.

The same test will be run on all the project provided after their submission. If the project will not pass this basic test, no project evaluation will be performed.

If you notice some mistakes in the test file, please do not hesitate to highlight it.

## F.A.Q.

1. Is the ID of the method getByID the attribute of the class `IdentifiableEntity`?
   
   **Answer:** The ID parameter for `getById` does correspond to the `id` attribute of the `IdentifiableEntity` class.

2. What information should be contained in the `DataFrame` returned by the method `getById`? 
   
   **Answer:** It strongly depends on how you address the implementation of the code. As a basic starting point, the data frame returned should contain all the attributes about the entity connected to the given `id` input parameter. However, it may also contain or point to (in some way) all the information related to all the other entities pointed by the one returned. For instance, if `getById` returns attributes about a journal, also the attributes of the categories and areas associated to it may be returned as well. This is an important aspect to highlight since, when a user run a method of the class `FullQueryEngine`, e.g. `getEntityById` passing as input an identifier of an journal, I expect to have back a python object having class `Journal` and, if I run its method `getCategories()` on it, I receive a `list` of items, each of it is an object having class `Category`, with all its attribute set appropriately.

3. In the classes `JournalQueryHandler` and `CategoryQueryHandler` the methods `getAll[something]` (like `getAllJournals()`), should return a `DataFrame` containing all the entities with the related attributes or just the entities themselves (e.g. the URIs for the graph database and the id we created for the relational database)?
   
   **Answer**: It strongly depends on how you address the implementation of the code. The `DataFrame` returned could include all the entities with their related attributes. Returning just the entities themselves, such as URIs for the graph database or IDs for the relational database, might be useful for certain types of queries but generally provides less context than a full set of attributes.

4. We do not understand while there should be multiple `QueryHandlers` in the attribute of the class `BasicQueryEngine`. Are they there in case the user wants to use multiple database of the same kind (es. multiple relational database about categories, multiple graph database about journals)?
   
   **Answer**: The inclusion of multiple `QueryHandlers` for both metadata and process queries in the `BasicQueryEngine` class enables the possibility of querying multiple databases. Here are a few reasons and scenarios where having multiple `QueryHandlers` could be beneficial:
   
   * Integration of diverse data sources: in a real-world scenario, journal metadata could be stored across various sources, each maintaining its own database.
   * Scalability: as the project or the amount of data grows, you may need to distribute the data across multiple databases to manage load. 
   * Data redundancy and reliability: using multiple databases can also enhance the reliability of your application. By storing and accessing data from multiple sources, your application can remain functional even if one of the databases is temporarily unavailable.
   * Specialized databases for different needs: different databases might be optimized for different kinds of queries or data.
   * Development and testing: multiple handlers can be useful in development and testing environments, where you might have separate databases for testing, development, and production.
   
   Moreover, even if in this project journal metadata is stored in graph databases and category data in relational databases, in real-world scenarios, metadata might be distributed across heterogeneous databases, including graph, relational, and other types of databases not covered in this course.

5. In case more languages are present in the field *LanguagesLanguages in which the journal accepts manuscripts* of the input CSV, which string is used to separate them?

   **Answer**: the string used is `", "` - e.g. `"Portuguese, English"`.
