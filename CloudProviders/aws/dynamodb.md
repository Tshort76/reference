# DynamoDB patterns
Most of these patterns are for noSQL databases in general, although the dynamodb index scheme is mentioned.

## Streams (change notification queue) + AWS_Lambda trigger
Store a running aggregate meta doc for aggregates of interest and update it with changes using a lambda. This will prevent ad hoc aggregate queries, which are expensive.

## Scatter Gather
Create logical partitions to subdivide an item - We have 3 customers (customer name is primary key) but millions of writes per second per customer.  We can create X sub partitions (e.g. customer_x for x in [0,29]) and upon writing a record for customer Y we generate a random number x from [0,29] (or we hash an item attribute) and use that to create the partition key for the item (i.e. customer_x).  That is the scatter.  To gather, we can now run against each sub_partition in order to gather partial aggregates and then perform some other aggregate on top of that.

## GSI-partitioning:
Design pattern to prevent table scans when searching for items that meet a rare condition.
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-indexes-gsi-sharding.html