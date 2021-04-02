
0. Please write down the full names and netids of all your team members.
ahr58 Aarif Razak
jt896 Jonathan Tai

1. Briefly discuss how you implemented the LS functionality of
   tracking which TS responded to the query and timing out if neither
   TS responded.
   Using the select.select method we could intialize a timeout that would be both nonblocking as well 
   as return an empty value within the variable 'readable' which would then either respond to a query from TS1 or TS2 or, in the case of a timeout, respond with an error message that would be routed to the client.

2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
   As of now, everything SHOULD work :)

3. What problems did you face developing code for this project?
At one point, the formatting of select.select was returning null values, along with python attempting to send an empty socket as a message, this proved to be trivial as we understood that a resulting LIST was returned, and we were attemping to put it into a single list, not three seperate ones based on the conditions of the method.

4. What did you learn by working on this project?
    Plenty, especially more about how to deal with multiple sockets within a single server, and how blocking recv can cause issues for multiple servers. Additonally, it really showed how network hardware and software should be built to scale easily.