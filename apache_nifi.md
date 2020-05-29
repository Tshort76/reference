# Apache NiFi
## Overview




## Core Components
### FlowFile
Encapsulated data that is moved through and acted upon by the system.  Similar to HTTP responses in that FlowFiles have 2 components: a (meta data) header and content (binary data).

### FlowFile Processor


### Connection
### Flow Controller
### Process Group


#### Pros
- Opensource
  - Free
  - Power to customize
- Versioning of flows
  - https://nifi.apache.org/registry.html
- Data Provenance
- Support for push and pull models of ingestion

#### Cons




## Quickstart guide:
Use docker to get nifi running locally, without authentication enabled:

$ docker run --name nifi -p 8080:8080 -d apache/nifi:latest
Bring up your favorite web browser and navigate to: localhost:8080/nifi



## Additional Resources
- Apache NiFi Crash Course - https://www.youtube.com/watch?v=fblkgr1PJ0o
- Best practices from running NiFi at Renault - https://www.youtube.com/watch?v=rF7FV8cCYIc
- https://www.udemy.com/course/apache-nifi/
