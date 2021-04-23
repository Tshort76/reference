# Usage

This app is intended for use with the dialogflow interview app, which is available at https://dialogflow-interview-20201211.herokuapp.com/ and specifies sample requests.

## Start up
If you are using v2 (redis persistence), you will need to have docker installed.  Once it is installed, you should start up your redis instance before starting your http server.  Start the redis instance by running the following command from the project's root directory:
`docker run --rm -v $PWD:/usr/local/etc/redis -p 6379:6379 --name myredis redis redis-server /usr/local/etc/redis/redis.conf &`

## Starting the HTTP server
Use `lein ring server` to start up your HTTP server.  You can configure which version of the app to use by modifying the version number in the groceries-http-service.app/app function (line 9 at the time of this writing).

# Handler versions
## v0
This is the work that completed in the ~ hour that was allotted.  Roughly 90 % of the time was spent getting a basic echo service to work and (sadly) even that took quite a bit of assistance.  I have posted a retrospective at the bottom of this file. 

## v1
With the basic service in place, I was able to make some quick improvements to the app.  I figured that the list (and thus state) would be best served up as an item:count map.  When an item's count is less than 1 then the item is removed from the list.

## v2
A Redis instance was created inside of a Docker container.  For better durability (I would hate for someone to forget to purchase that special ingredient that makes the dish), it was configured to be append only so that it persists state after each write.  Redis fit the use case quite naturally, as can be seen by the size of the required code.
