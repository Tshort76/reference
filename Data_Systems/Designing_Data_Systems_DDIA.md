
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

## Iteratively more complex DB example
### V0
Imagine a simple database, which consists of get(k) and set(k,v).  The set command appends a key value pair to a file, and the get command fetches the latest record associated with a key.
#### Strengths
- Fastest possible writes
- Simple
#### Weaknesses
- Extremely slow O(n) reads
- No storage reclamation
- Slow modification
- Potential issues with simultaneous use
### V1
Create an in-memory hash index for records (key -> byte offset)
Use a series of fixed length files instead of a single file
#### Strengths
- Fast reads
#### Weaknesses
- Slightly slower writes (need to update the index)
- Limited scale since all keys must fit in memory
