
# Design Principles and Goals
## Reliability
One study of large internet services found that configuration errors by operators were the leading cause of outages, whereas hardware faults (servers or network) played a role in only 10–25% of outages.

How do we make our systems reliable, in spite of unreliable humans? The best systems combine several approaches:

- Design systems in a way that minimizes opportunities for error. For example, well-designed abstractions, APIs, and admin interfaces make it easy to do “the right thing” and discourage “the wrong thing.” However, if the interfaces are too restrictive people will work around them, negating their benefit, so this is a tricky balance to get right.
- Decouple the places where people make the most mistakes from the places where they can cause failures. In particular, provide fully featured non-production sandbox environments where people can explore and experiment safely, using real data, without affecting real users. 
- Test thoroughly at all levels, from unit tests to whole-system integration tests and manual tests [3]. Automated testing is widely used, well understood, and especially valuable for covering corner cases that rarely arise in normal operation. 
- Allow quick and easy recovery from human errors, to minimize the impact in the case of a failure. For example, make it fast to roll back configuration changes, roll out new code gradually (so that any unexpected bugs affect only a small subset of users), and provide tools to recompute data (in case it turns out that the old computation was incorrect). 
- Set up detailed and clear monitoring, such as performance metrics and error rates. In other engineering disciplines this is referred to as telemetry. (Once a rocket has left the ground, telemetry is essential for tracking what is happening, and for understanding failures) Monitoring can show us early warning signals and allow us to check whether any assumptions or constraints are being violated. When a problem occurs, metrics can be invaluable in diagnosing the issue. 
- Implement good management practices and training … beyond the scope of this document

## Scalability 
Over the foreseeable lifetime of the application, which aspects are liable to rapid growth and which performance aspects need to stay relatively stable in those situations?  Examples might be:
- The sizes of data sets that need to be batch processed
- The number of simultaneous requests that need to be authenticated and processed with a given response time
- The geographical dispersion of nodes

It is standard practice to define Service Level Agreements (SLAs) to specify legally enforceable standards.  For instance, a company might promise that a service responds in less than 200 ms to 99.9% of requests and is subject to fines by clients if it fails to uphold that.

Amazon describes response time requirements for internal services in terms of the 99.9th percentile, even though it only affects 1 in 1,000 requests. This is because the customers with the slowest requests are often those who have the most data on their accounts because they have made many purchases—that is, they’re the most valuable customers!

Oftentimes, a system needs an architectural overhaul if load increases by an order of magnitude.  

## Maintainability
### Operability
Make it easy for operations teams to keep the system running smoothly.

Good operability means making routine tasks easy, allowing the operations team to focus their efforts on high-value activities. Data systems can do various things to make routine tasks easy, including:
- Providing visibility into the runtime behavior and internals of the system, with good monitoring 
- Providing good support for automation and integration with standard tools 
- Avoiding dependency on individual machines (allowing machines to be taken down for maintenance while the system as a whole continues running uninterrupted) 
- Providing good documentation and an easy-to-understand operational model (“If I do X, Y will happen”) 
- Providing good default behavior, but also giving administrators the freedom to override defaults when needed 
- Self-healing where appropriate, but also giving administrators manual control over the system state when needed 
- Exhibiting predictable behavior, minimizing surprises


### Simplicity 
Make it easy for new engineers to understand the system and for existing engineers to keep a working model of the system in their minds.

Limit accidental complexity, defined as that which is not inherent in the problem that the software solves (as seen by the users) but arises only from the implementation.

One of the best tools we have for removing accidental complexity is abstraction. A good abstraction can hide a great deal of implementation detail behind a clean, simple-to-understand façade. A good abstraction can also be used for a wide range of different applications.
 
### Evolvability
Make it easy for engineers to make changes to the system in the future, adapting it for unanticipated use cases as requirements change. Also known as extensibility, modifiability, or plasticity.


# The Data Model
The data model is probably the most crucial aspect of the design and will have the biggest impact on system performance and usability.

In essence, an application layer is nothing more than a data model and an API for manipulating that data model. Good modular design requires great data modeling

Every data model embodies assumptions about how it is going to be used. Some kinds of usage are easy and some are not supported; some operations are fast and some perform badly; some data transformations feel natural and some are awkward.

It can take a lot of effort to master just one data model (think how many books there are on relational data modeling). Building software is hard enough, even when working with just one data model and without worrying about its inner workings. But since the data model has such a profound effect on what the software layer above it can and can’t do, it’s important to choose one that is appropriate to the application. Custom data models force application developers to think a lot about the internal representation of the data in the database, which has a negative impact on evolvability, simplicity, and maintainability.

A problem that arises with using a generic persistence data model, such as their relational data model, is that there's often a translation that needs to occur between the application data model and the persisted data model. The difference between the two is calmly known as the impedance mismatch. This often arises because your persistence layer is optimizing for on disk storage and generic queries, while your application layer is optimizing for developer and user convenience at the API level. Document stores, like MongoDB, use JSON, which can lower the impedance mismatch, at the cost of redundant data on disk

## Relational Data models
### Heuristics
#### Use IDs and GUIDs for keys
The advantage of using an ID is that because it has no meaning to humans, it never needs to change: the ID can remain the same, even if the information it identifies changes.

Anything that is meaningful to humans may need to change sometime in the future—and if that information is duplicated, all the redundant copies need to be updated. That incurs write overheads, and risks inconsistencies (where some copies of the information are updated but others aren’t). Removing such duplication is the key idea behind normalization in databases.

## Document Data Models
There are several driving forces behind the adoption of NoSQL databases, including:
- A need for greater scalability than relational databases can easily achieve, including very large datasets or very high write throughput 
- A widespread preference for free and open source software over commercial database products 
- Specialized query operations that are not well supported by the relational model 
- Frustration with the restrictiveness of relational schemas, and a desire for a more dynamic and expressive data model
### Strengths
- Higher write throughput
- Typically easier to achieve horizontal scaling of the database
- More dynamic and expressive data model (can minimize impedance mismatch)
- Simplifies one-to-many modelling and gives a locality advantage if you frequently access something like person.address.zip_code (access from JSON vs 3 table join)
	
### Weaknesses
- Eventual consistency
- All of the caveats below
- Typically results in a less evolvable data model

### Caveats
- If joins are needed, application code must be written to do it (negatively affects maintainability, scalability, and evolvability)
- Even if the initial version of an application fits well in a join-free document model, data has a tendency of becoming more interconnected as features are added to applications (evolvability)
- Determining the “access path” for nested data needs to happen in application code, since a lack of schema prevents the use of automatic query optimizers
- The locality advantage only applies if you need large parts of the document at the same time.
  - Loading a single field typically requires loading the entire document
  - Updating a document typically requires rewriting the entire document

## Graph Data Models
### Property graph model
A property graph model is a collection of vertices and edges
Each vertex has a unique id, incoming edges, outgoing edges, and attributes (key-value pairs)
Each edge has a unique ID, start vertex, end vertex, and attributes (key-value pairs)

### Triple stores
In a triple-store, all information is stored in the form of very simple three-part statements: (subject, predicate, object). A triple might be (Jim, likes, bananas), (Jim,is,gay), (gay,type_of, sexual_orientation).

## Summary
Document databases target use cases where data comes in self-contained documents and relationships between one document and another are rare

Graph databases go in the opposite direction, targeting use cases where anything is potentially related to everything

Relationals databases form a middle ground

# Storage and Retrieval
Key problems that a Database must solve
- Efficient storage on disk (Data format)
- Modifying existing records
- Adding new records
- Deleting records
- Retrieving the most accurate view of data
- Crash recovery 
- Partially written records (database may crash)
- Simultaneous users/Concurrency control (scale with # users and # records)

## Example System: Sequential File Write
Imagine a simple database, which consists of get(k) and set(k,v).  The set command appends a key value pair to a file, and the get command fetches the latest record associated with a key.
### Strengths
- Fastest possible writes
- Simple
### Weaknesses
- Extremely slow O(n) reads
- No storage reclamation
- Slow modification
- Potential issues with simultaneous use
## Example System: Hash Indexing (Log Structured Storage)
Create an in-memory hash index for records (key -> byte offset) and segment files (fixed length) instead of a single file.  Keys are stored in chronological order, so that the most recent entry for a key is in the most recent file.
### Strengths
- Fast reads
### Weaknesses
- Slightly slower writes (need to update the index)
- Limited scale since all keys must fit in memory
## LSM Trees (SSTable)
Take our log-structured storage segment, a sequence of key-value pairs appearing in the order that they were written, and *add a sorting requirement*: the sequence of key-value pairs is sorted by key.


We can now make our storage engine work as follows:
- When a write comes in, add it to an in-memory balanced tree data structure (e.g. a red-black tree). This in-memory tree is sometimes called a memtable.
- When the memtable gets bigger than some threshold, write it out to disk as an SSTable file.
  - While the SSTable is being written out to disk, writes can continue to a new memtable instance.
- In order to serve a read request, first try to find the key in the memtable, then in
the most recent on-disk segment, then in the next-older segment, etc
- From time to time, run a merging and compaction process in the background to
combine segment files and to discard overwritten or deleted values.
  - Start reading the SSTable files in parallel, looking at the first key in each file, and copy the lowest key to the output file.  Repeat until all keys are copied over, taking only the most recent instance of a particular key
  - 

### Strengths
- Scales to large datasets
- Easy to perform range queries
- High write throughput since writes are sequential
- LSM-trees can be compressed better, and thus often produce smaller files on disk
than B-trees.  Since LSM-trees are not page-oriented and periodically rewrite SSTables to remove fragmentation, they have lower storage overheads, espe‐
cially when using leveled compaction
- Typically lower write duplication/amplification (for each user write to DB, how many times does the system write that data)
### Weaknesses
- Looking up non-existent keys can be very slow
  - A [bloom-filter](#bloom-filters) can be used to mitigate the costs
- Compaction process can limit write throughput since it competes for write resources
- In configuration is setup incorrectly for use case, databases can grow indefinitely as writes/modifications happen faster than compaction (and duplicate key removal)
- Newer technology, so implementations are not as mature as B-Tree systems
- Reads are typically slower on LSM-trees since they have to check several different data structures and SSTables at different stages of compaction.

## B Trees
Store keys using a B tree
[Btree](../Computer_Science/resources/images/BTree.png)


## Advanced Indexing structures
### Storing values with index
An index can be concieved of as a key/value pair.  In many instances, the key (e.g. index column) is stored with a pointer to the corresponding value (e.g. DB row), which is typically stored in a *heap file*.  This works very well for fixed size records, where values within records can change without changing the block size of that record.

In some situations, the extra step to lookup values by heap file pointer is prohibitive and indexed values are stored alongside the index.  This type of index is known as a **clustered index**.  When only a subset of the record's fields are stored with the index, it is known as a **covering index** and queries that can be answered by using this index alone (without looking up additional values from the row) are said to be *covered*.

### Multi-column indexes
Queries that are a function of multiple attributes cannot always be made efficiently with independent, single key indices.  Additionally, simple solutions like concatenating fields into a single key can be of limited use (e.g. last_name + first_name can be used to query for full names or last names, but not first names).
#### Geospatial Indices
Geospatial indices require a search on 3 values (x,y,z) simultaneously, making traditional single key indices useless.  Some solutions to this problem are:
- Use a [space-filling-curve](#space-filling-curve) to generate a single index value, then a traditional B-tree index
- Use a specialized spatial index, like an [R-tree](#r-trees)

### In memory databases
In memory databases are more performant, when they are feasible for the domain dataset sizes, primarily because they avoid the overhead of encoding in-memory data structures to disk compatible forms.
Examples:
- VoltDB, MemSQL, and Oracle TimesTen are in-memory relational databases
- RAMCloud is an open source, in-memory key-value store with durability 
- Redis and Couchbase provide weak durability with asynchronous disk writes

## Transaction vs Analytics (OLAP vs OLTP)
Originally, databases were used to record single events (e.g. customer transactions) and retrieve those events at a later point in time, typically for display or audit purposes.  In this case, small groups of entire records are retrieved at any given time. This pattern of on-demand access (e.g show all my purchases for May 2022) is known as *online transaction processing* (**OLTP**).  Systems typically interact with the data in a transactional way.
With faster computers and more extensive digital records, databases are increasingly subject to large analytic queries that help drive executive decisions (e.g. total sales by region and demographics).  Such queries require a very different access pattern, typically of the form of accessing a few fields across all records in a database.  This access pattern is known as *online analytic processing* (**OLAP**).  BI analysts typically interact with the data using the OLAP system.

| Property             | Transactions (OLTP)                               | Analytics (OLAP)                          |
| -------------------- | ------------------------------------------------- | ----------------------------------------- |
| Main read pattern    | Small number of records per query, fetched by key | Aggregate over large number of records    |
| Main write pattern   | Random-access, low-latency writes from user input | Bulk import (ETL) or event stream         |
| Primarily used by    | End user/customer, via web application            | Internal analyst, for decision support    |
| What data represents | Latest state of data (current point in time)      | History of events that happened over time |
| Dataset size         | Gigabytes to terabytes                            | Terabytes to petabytes                    |

---

While relational databases can be used for both OLAP and OLTP, many companies use separate database systems for OLAP, termed **data warehouses**.

## Data Warehouses
An enterprise may have dozens of different transaction processing systems: systems
powering the customer-facing website, controlling point of sale (checkout) systems in
physical stores, tracking inventory in warehouses, planning routes for vehicles, man‐
aging suppliers, administering employees, etc. Each of these systems is complex and has its own administrators, who are often not eager to let analysts run arbitrary queries across it during business hours.

To support the OLAP paradigm, a read-only copy of the data (the warehouse) is created from all the various OLTP systems in the company.  The warehouse build process is an example of an ETL:
- (E)xtract the data from OLTP systems, with some combination of periodic data dumps and continuously streamed updates
- (T)ransform the data into an analysis-friendly schema
- Clean the data with OLTP specific logic to remove or complete missing records
- (L)oad the resulting data into the data warehouse.

### Star and Snowflake Schemas
Since the data warehouse is setup for arbitrary queries, its data is stored in a very generic format, a highly normalized relational table form.  The standard schema, in which *events* as stored as rows in a **fact** table, with individual columns containing atomic values (e.g. price or quantity) or foreign key references to complex values (**dimensions**, such as the `product purchased` or `location of sale`), is known as a **star** schema since it has a unifying/central concept (an event/fact) surrounded by a single layer of supporting dimension tables.  If the dimension tables themselves contain complex attributes (i.e. foreign key references to other tables), then the schema is known as a **snowflake** schema.

![Star vs Snowflake](./images/star_vs_snowflake.jpg)

### Column-oriented schemas
Column oriented data storage is popular for data warehouses owing to the facts that:
- Event tables typically have many columns, but only a few are used in any query
- Column data is homogenous
  - Each cell takes up the same space
  - Typically redundancy, which lends itself to better compression
Note that while an arbitrary scheme can be used for ordering rows, that scheme must be applied to all column stores such that element[i] of column[0] must correspond to the same fact/event as element[i] in column[b], $\forall b$.

#### Column compression
![bitmap compression](./images/columnar_compression.png)

#### Sort Order
If certain queries (e.g. group by date) are common, it might make sense to sort the rows by the relevant fields.  Since the data is stored in column format, this typically takes the form of:
1. determine the correct row order by sorting the table containing the field of interest
2. Modifying all other columns stores to use that same row order

Note that have data sorted can help with compression, especially for the values that are sorted.  It might also help with other rows if feature values are similar in a local setting (e.g. Neighboring pixels in a 2D image are often very similar, so compression algorithms can exploit that).

A clever way to allow multiple sort orders without extra duplication is to store replications of the data (which all DBs have already, for recovery) using a different sort order for each replica.

### Data Cubes
 TODO

# Appendix
## Bloom Filters
For set membership testing
## R-trees
Special index for geospatial queries
## Space filling curve
Used to generate a single key value for geospatial data so that a traditional indexing structure (e.g. B-tree) can be used for queries
