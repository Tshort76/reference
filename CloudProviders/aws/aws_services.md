# Relational Datastores and ElastiCache
## RDS
RDS stands for Relational Database Service.  It is a managed service on which you can run relational databases such as Postgres and MySQL.
It has the following advantages over just running a containerized DB instance in EC2:
- Automated patching and provisioning
- Continuous backup allowing for Point in Time restoration
- Monitoring dashboards
- Read replicas
- Multiple availability zones, maintenance windows, horizontal and vertical scaling, storage backup (EBS)

## Aurora
Aurora is an AWS-optimized Relational Database that implements the same protocols as (and is therefore compatible with the drivers of) MySql and PostGres.  It comes in a standard version (very similar to other RDS databases), a serverless version (no capacity planning), and a global version (auto allocation across availability zones).

## ElastiCache
ElastiCache is a managed cache service that implemented either the Redis or Memcached cluster engine.  In other words, it is an in-memory database that is used for storing a copy of frequently accessed data, relieving the load on the DB while also increasing your application's response times.
<!-- ![Elasticache](./images/elasticache.png | width=100) -->
<img src="./images/elasticache.png" alt="Elasticache" width="50%">

# Amazon S3
S3 is conceptualized as a group of *buckets*, where each bucket contains *objects*.  S3 is a global service but buckets are linked to regions.
## Buckets
A bucket has the following properties:
- globally unique name (mostly lowercase alphanumeric)
- are defined at the region level
- NO directories
  - confusing since paths contain '/' characters, long names, and are treated as if folders in the UI

## Objects
An object is a file with a *key*, where the *key* is the full path to the object.  Each *key* consists of a prefix and an object name, where the object name is the last entry in the '/' delimited *key*.  For example, the following object URL `s3://my-bucket/my-folder/a-sub-folder/my-file.csv` can be partitioned into:
- `s3://`: protocol
- `my-bucket/`: bucket name + slash
- `my-folder/a-sub-folder/my-file.csv`: object *key*
- `my-folder/a-sub-folder/`: object prefix
- `my-file.csv`: object name

Objects are comprised of 4 components:
- values: the content/data (5 TB limit)
- metadata: key/value pairs that describe the data (added by system or user)
- tags: key/value pairs (added by user)
- version ID

### Versioning
When versioning is enabled, uploading multiple files to the same bucket with the same filename will duplicate the item but assign version #.  Only the latest version of an object is shown in the overview page.  Deleting a versioned file does NOT delete the file; instead, it adds a *delete* version of the file that hides the file in the overview screen.  This allows for recovering old versions of a file. If desired, you can delete specific versions of a file.

### Encryption
- SSE-S3: AWS handles all aspects of encryption and does it server-side
- SSE-KMS: AWS handles encryption but provides keys and audit trail (allowing granular access)
- SSE-C: Client provides encryption key, AWS uses (but doesn't store) key to encrypt objects

## Security
In addition to the standard user-based access (via IAM policies), S3 has resource (bucket) based policies which apply to particular buckets and allow cross account access.  An IAM principal can access an S3 object if:
- the user IAM has permission or the resource policy allows access 
- AND there is no explicit DENY policy

## Static website hosting
You can host a static webpage directly from a bucket by configuring a few things in the bucket properties tab and then ensuring that the bucket is accessible via policies.

# Queues and Messages
AWS offers a Simple Queue Service (SQS) for queues, Simple Notification Service (SNS) for the publish and subscribe pattern, and Kinesis for streaming.

<!-- ![Queues and Messages services](./images/queues_messages.png) -->
<img src="./images/queues_messages.png" alt="Queues and Messages services" width="50%">

Note that Redis offers data durability and can be used as a conventional database, whereas Memcached can only serve as a cache.

### Security
#### Encryption
In-flight, at-rest, and client-side encryption are all supported.
#### Access
- IAM policies to regulate access to the SQS API
- SQS access policy similar to the S3 bucket policies
  - Useful for cross-account access to the queues

## SQS
- Unlimited throughput and message capacity
- Limited retention, 1 minute < X < 14 days
- Limited message size of 256 KB
- At least once delivery
- Best Effort ordering
- Delayed processing (per queue or per message)

When a message is polled from a consumer, it becomes invisible for 30 seconds to ensure that the consumer can process the data.  If the consumer does not delete the message (or make an API call to increase the invisibility window duration) by the end of the invisibility window then the message will become visible and another consumer will process the message.  If this happens often enough (configurable) for a message, that message will go to the Dead Letter Queue.  This allows logic and workflows to be built around the frequently failing jobs/message.

## SNS
SNS is a managed notification system for the Publish / Subscribe model.  An SNS instance contains many topics.  An event producer (e.g. publisher) writes a single message to a topic while all subscribers to that topic receive that message.  Subscribers can be SQS, HTTP/HTTPS, Lambda, Emails, SMS messages, and Mobile Notifications.  A common pattern is combining SNS and SQS to write to multiple queues from a single service (fan out).

## Kinesis
Kinesis handles real-time big data such as application logs, IoT, and clickstreams.

## Amazon MQ
AWS provides Amazon MQ, a managed message broker service for Apache ActiveMQ, to assist with migrating on-premise (queue utilizing) architectures to the cloud.