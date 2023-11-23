# Parallel and Distributed Systemas
Exercises Developed as part of The Parallel and Distributed Systems course in Computer Science @UFMG

## Multiple Atomic Locks
This code implements a thread synconization system that controls the access to multiple locks simultaneously, in a model that locks nothing or everything. 
The syncroniztion is based on mutex and condition variables, using pthreads.


## Distributed key-value storage using RPC
This project aims to implement a distributed storage system that allows users to query keys and receive the corresponding stored values in response. The service is designed using Google Remote Procedure Call (gRPC) and comprises four main entities: central or local server and clients - following the same logic - responsible for making requests.
The entity responsible for storing the key-value pairs and handling user requests is the server, which can be local or central. The former is implemented to maintain a dictionary with the data provided by users. It is capable of triggering an RPC to register with the centralizer and provide its values when requested by the client.
The latter is a server of servers, whose role is to store the registered keys assigned to its origin. It serves to direct its clients to the source of the information requested by them, that is, the original server.
Each type of server has its specific category of associated client. They must connect and then can request the implemented RPCs. From this, they should receive what was given as a response and then display the corresponding output in a compatible manner