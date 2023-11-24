import grpc
import sys
import threading
from concurrent import futures

import pairs_pb2, pairs_pb2_grpc


class CentralServer(pairs_pb2_grpc.CentralServerServicer):
    """
    Class that implements the central server.
    It inherits from the generated class CentralServerServicer as defined by the gRPC library.
    
    Main data structures:
    
    keys_servers: a dictionary that stores the key-server pairs.

    stop_event: used to terminate the server when requested by a client.
    """
    def __init__(self, event):
        self.keys_servers = {}
        self.stop_event = event
    

    def register(self, request, context):
        """
        Registers a pairs server in the central server's dictionary.

        This method add a key-server pair to the central server's dictionary. 
        The value is the server's identifier and the key is a key that server stores.
        It is important to notice that tere can bem multiple keys associated with the same server.

        The message type defined by the proto file is Server, which contains two fields 
        called id and keys. The first represents the server's service identifier and the second
        is a list of keys stored in the server, which is declared as a repeated int32 field.

        This method overwrites the previous value associated with each key and adds the new one.

        Returns: message of type KeyCounter, which contains a single field called count.
            Number of keys registered, which must be equal to the number of keys in the list passed as parameter.
        """
        
        keys_processed = 0
        for key in request.keys:
            self.keys_servers[key] = request.id
            keys_processed += 1
        return pairs_pb2.KeyCounter(count=keys_processed)


    def terminate(self, request, context):
        """
        Terminates the server by setting the stop_event.

        Returns: message of type SuccResponse, which contains a single field called success.
        
        0, if the server was terminated successfully.
        """
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)


    def findOwner(self, request, context):
        """
        Finds the server that stores the key passed as parameter.

        This method searches the central server's dictionary in linear time for the key passed as parameter.
        
        Returns: message of type ServerId, which contains a single field called id.
            If the key is registered, the method returns the server's identifier;
            
            Otherwise, it returns an empty string.

        """
        for key in self.keys_servers:
            if key == request.key:
                return pairs_pb2.ServerId(id=self.keys_servers[key])
        return pairs_pb2.ServerId(id="")


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_CentralServerServicer_to_server(CentralServer(stop_event), server)
    server.add_insecure_port(f"0.0.0.0:{sys.argv[1]}")
    server.start()
    stop_event.wait()  # Program waits for the stop_event to be set
    server.stop(1)  # Server is stopped with a 1 second grace period after the stop_event is set


if __name__ == '__main__':
    serve()
