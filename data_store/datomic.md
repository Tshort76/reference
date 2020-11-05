<div align="center">Datomic</div>
===
# Datalog
## Query Basics
Copied nearly verbatim from [http://www.learndatalogtoday.org/chapter/1](http://www.learndatalogtoday.org/chapter/1) <br>

The data model in Datomic is based around atomic facts called *datoms*. A *datom* is a 4-tuple of form:

`[<Entity ID>  <Attribute>  <Value>  <Transaction ID>]`

You can think of the database as a flat set of datoms of the form:
```
[<EID>  <attribute>      <value>          <tx-id>]
[ 167    :person/name     "James Cameron"    102  ]
[ 234    :movie/title     "Die Hard"         102  ]
[ 234    :movie/year      1987               102  ]
[ 235    :movie/title     "Terminator"       102  ]
[ 235    :movie/director  167                102  ]
```
Note that the last two datoms share the same entity ID (EID), which means they are facts about the same movie. Note also that the last datom's value is the same as the first datom's EID, i.e. the value of the :movie/director attribute is itself an entity. All the datoms in the above set were added to the database in the same transaction, so they share the same transaction ID.

A query is represented as a vector starting with the keyword :find followed by one or more pattern variables *(symbols starting with ?, e.g. ?title)*. After the find clause comes the :where clause which restricts the query to datoms that match the given data patterns.

For example, this query finds all EIDs that have the attribute :person/name with a value of "Ridley Scott":

```
[:find ?e
 :where
 [?e :person/name "Ridley Scott"]]
```
A **data pattern** is a datom with some parts replaced with pattern variables. It is the job of the query engine to figure out every possible value of each of the pattern variables and return the ones that are specified in the :find clause.

The symbol _ can be used as a wildcard for the parts of the data pattern that you wish to ignore. You can also elide trailing values in a data pattern.

## Important ideas
* Variables can serve either as a constraint (when they have already been initialized to a value) or as a target for a binding (unitialized).
* A single bound variable must be the same across queries, which is why an initialized variable acts as a constraint.


# Example queries

#### Find the name of all directors whom have directed Arnold Schwarzenegger
```
[:find ?name
 :where
 [?arn :person/name "Arnold Schwarzenegger"]  ; ?arn <- the EID corresponding to Arnold
 [?m :movie/cast ?arn]                        ; ?m  <- EID of movies with Arnold in cast
 [?m :movie/director ?dir]                    ; ?dir <- EID of directors of movies with Arnold in cast
 [?dir :person/name ?name]]					  ; ?name <- name of persons corresponding to EIDs ?dir
```

#### 
```
[:find ?filename ?timestamp ?md5  ; eq. to project fields in relational algebra
 :in $ ?o ?ft    ;position-based aliases for inputs to q function
 :where   
  [?e :owner ?o]    ;bind to ?e the EIDs of all records with :owner attribute = ?o
  [?e :file-type ?ft]   ;match all records with EID 'in' ?e AND :file-type = ?ft ("voya")
  [?e :md5 ?md5]    ;match all records with entity id 'in' ?e, bind the :md5 attribute of corresponding records to ?md5
  [?e :upload ?up]  ;match all records with entity id 'in' ?e, bind the :upload attribute (apparently an entity id) of corresponding records to ?up
  [?up :filename ?filename]  ;match all records with entity id 'in' ?up, bind the :filename attribute of the corresponding records to ?filename
  [?up :timestamp ?timestamp]]        ;match all records with entity id 'in' ?up, bind the :timestamp attribute of the corresponding records to ?timestamp
```



## Resources
- [http://www.learndatalogtoday.org/](http://www.learndatalogtoday.org/)