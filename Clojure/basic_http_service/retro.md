# Retrospective
- When I need to build an app on my own, I usually struggle with it for a while, get something to work, and then move on to app development.  As a result, my knowledge base for troubleshooting (e.g. need to decode) is quite limited.  It is definitely a weakness of mine but I have always found that I could leverage someone else for 2 hours to setup networking and then never deal with it again.  Consequently, increasing personal proficiency has never been a priority for me.  I will leave it to you to decide if that is virtue or vice.

- I do have quite a bit of experience in building APIs but mostly dealing with paths, query vs path params, defining reasonable responses but upon reflections someone else has always put the std middleware in place for the services that I have worked on.

- I was unable to get a print statement to work!  I should perhaps have just tried logging with timbre in the off chance that ring was setup to work with it out of the box.  Without the ability to see the format of the request body, I was neutered as a debugger.  This is quite unfortunate as debugging is actually one of my strong suits (assuming that I can get some sort of feedback signal).

- I haven't used Clojure in a year.

Weak debugging instances
- Did not catch that the keys in the request body were strings and not keywords
- Did not catch that the JSON was encoded in the request sent by the reify service
- State should never have been a vector but that was a rushed decision due to the above issues