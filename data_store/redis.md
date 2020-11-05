<div align="center">Redis</div>
===

## Features
- In-memory database
  - Extremely fast
- Horizontally scalable
  - Master:slave model
- **Key-value store**
  - supports data-structures as values, including objects (hashes), lists, sets, and streams
- Optional save to disc **persistence**
- Supports transactions


## Common use cases
- User session management
- Caching
- Pub/Sub (using a List)

## Conventions
- Use : for separating words in a key (e.g. user:1000 -> user with id = 1000)

# [Data types](https://redis.io/topics/data-types-intro)
### [String](https://redis.io/commands#string)
  - append, set (value), decrement, increment, length
```
set cache_hits 12
incr cache_hits
get cache_hits   # 13 
set user_id:is_active true EX 20 NX  # expire in 20 seconds (EX), set only if key does Not Exist (NX)
```
- [List](https://redis.io/commands#list)
  - insert at (left|right), pop, push, length, get at index, set at index
- [Set](https://redis.io/commands#set)
  - add, membership check, set difference|intersection|union 
- [Sorted Set](https://redis.io/commands#sorted_set)
  - combo of set and list commands
- [Hash (maps)](https://redis.io/commands#hash)
  - Represent objects (field-value pairs)
```
> hmset user:1000 username antirez birthyear 1977 verified 1
OK
> hget user:1000 username
"antirez"
> hget user:1000 birthyear
"1977"
> hgetall user:1000
1) "username"
2) "antirez"
3) "birthyear"
4) "1977"
5) "verified"
6) "1"
```
- [Streams](https://redis.io/commands#stream)
  - [Intro to streams](https://redis.io/topics/streams-intro)


# System-level Features
## Persistence and Backup
### Redis Database File (RDB)
RDB makes a snapshot of the database at a specified frequency by forking a child process to write the database to a file.  It is simple and easy but there is the possibility of heavy resource usage and losing data that has been added since the last snapshot.
### Append Only File (AOF)
With AOF, each write operation is stored in a file which can then be replayed to restore the database.  This can be a resource drain since the AOF file is larger than the database AND a file is appended to for each operation.

## Availability
### Redis Sentinel
Sentinel acts as a load balancer and monitoring service for the Redis cluster, sitting between the client and the master node.  It performs the following functions:
- Monitoring the master and slave nodes
- Exposing an API for determining cluster state
- Promoting a Worker to the Master role when the Master goes down


# Useful commands
```
keys <pattern>   # eg use * to list all, thomas* to list all keys starting with thomas
```


## References
[Official Documentation](https://redis.io/documentation)