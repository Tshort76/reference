## HTTP
### URI
\<protocol\>://\<service-name\>/\<resource-path\>

### Methods
- GET: This is used for fetching details from the server and is basically a read-only operation.
- POST: This method is used to **create** new resources on the server.  Has a payload (data)
- PUT: This method is used to **update or replace** the existing resources on the server
- DELETE: This method is used to delete the resource on the server.
- PATCH: This is used for modifying the resource on the server.
- OPTIONS: This fetches the list of supported options of resources present on the server.
- HEAD: Basically GET but requests the headers ONLY


GET, HEAD, OPTIONS are safe and idempotent methods, PUT and DELETE methods are only idempotent, and POST and PATCH methods are neither.

### Status codes
- 1xx - represents informational responses
- 2xx - represents successful responses
- 3xx - represents redirects
- 4xx - represents client errors
- 5xx - represents server errors

#### Common codes
- 200 - success/OK
- 201 - CREATED - used in POST or PUT methods.
- 304 - NOT MODIFIED - used in conditional GET requests to reduce the bandwidth use of the network
- 400 - BAD REQUEST - This can be due to validation errors or missing input data.
- 401 - UNAUTHORIZED - No valid authentication credentials sent along with the request.
- 403 - FORBIDDEN - sent when the user does not have access (or is forbidden) to the resource.
- 404 - NOT FOUND - Resource method is not available.
- 500 - INTERNAL SERVER ERROR - server threw some exceptions while running the method.
- 502 - BAD GATEWAY - Server was not able to get the response from another upstream server.

### HTTP Request components
- Method : i.e. GET, PUT, POST, DELETE, etc
- URI : Uniquely identifies the resources on the server
- HTTP Version : Version of HTTP protocol you are using (e.g. HTTP v1.1)
- Request Header : Details of the request metadata such as client type, the content format supported, message format, cache settings, etc.
- Request Body: The actual message content to be sent to the server.

### HTTP Response components
- Response Status Code : Server response status code
- HTTP Version: The HTTP protocol version
- Response Header: Metadata of the response message. Data can describe what is the content length, content type, response date, what is server type, etc.
- Response Body: The actual resource/message returned from the server.

## REST
- REST stands for Representational State Transfer
- Uses client/server model, where client state is NOT stored on the server
  - It is NOT possible to maintain sessions unless the client-side manages a session id
- Uses HTTP for implementation
  - request headers, request body, response body, status codes
- Lightweight, provide maintainability, scalability, support communication among multiple applications that are developed using different programming languages
- They provide means of accessing resources present at server required for the client via the web browser
- Data transfer format is typically JSON or XML, but also supports MIME and Text
- REST does not impose security restrictions inherently. It inherits the security measures of the protocols implementing it.

### API Best Practices
- Accept and respond with JSON data format whenever possible (since javascript will likely parse it)
  - response and request headers should have Content-Type set to as application/JSON
- Naming
  - Use lowercase, underscores, and plural nouns and not verbs (HTTP method is the verb). An appropriate 
- Return a standard HTTP status code that best expresses the return status (e.g. Not Found vs Forbidden)
- Include filtering and pagination for large resources.
- Secure your endpoints
  - Use HTTPS
  - Use SSL (certificates are easier to get/use) and load on the server
  - Incorporate authorization with roles/services
- Version your API, typically with /vX at the beginning of the API path
  - When the URI is updated, the older URI must be redirected to the new one using the HTTP status code 300.


### Alternatives
- SOAP - Bloat but can be used for enhanced security and reliability
- Web Sockets - establish connection and then maintain a stateful session (needed for streaming)

:::::::::::::::::::::::::::::::::::::::::::::
HERE
:::::::::::::::::::::::::::::::::::::::::
https://www.youtube.com/watch?v=U6OAdQqWegQ




## Middleware
Middleware can be used as an adaptor that fits between the browser and your application, converting HTTP requests from the browser into language specific data structures and converting language specific data structures into HTTP responses.
![Middleware](resources/images/web_middleware.png)

I will use the Clojure web service stack to demonstrate.

### Compojure
[Compojure Wiki](https://github.com/weavejester/compojure/wiki)

Lightweight package for defining routes, leveraging the Ring library.
```clojure
(def my-routes
  (routes
   (GET "/foo" [] "Hello Foo")
   (GET "/bar" [] "Hello Bar")))

(defroutes user-routes
  (context "/user/current" []  ; define routes that share a common prefix
    (GET "/" [] ...) ; the route that exists at "/user/current"
    (GET "/profile" [] ...)
    (GET "/posts" [] ...)))
```
### Ring
[Concepts Wiki](https://github.com/ring-clojure/ring/wiki/Concepts)

