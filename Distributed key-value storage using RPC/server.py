import grpc
import socket
import sys
import threading
from concurrent import futures

import pairs_pb2
import pairs_pb2_grpc


class Pair(pairs_pb2_grpc.PairsServicer):
    """
    Class that implements the key-value server. It inherits from the generated class PairsServicer
    as defined by the gRPC library.

    Main data structures:

    my_dict: a dictionary that stores the key-value pairs. 

    stop_event: used to terminate the server when requested by a client.
    """

    def __init__(self, event, port):
        self.my_dict = {}
        self.stop_event = event
        self.port = port

    def insert(self, request, context):
        """
        Inserts a key-value pair into the dictionary.

        Returns:
            Return values are defined by the gRPC library. In this case, the function returns an
            object of type SuccResponse, which contains a single field called success. The function
            returns

            0 if the insertion was successful.

            -1 If the key already exists. The insertion fails.
        """
        if request.key not in self.my_dict:
            self.my_dict[request.key] = request.value
            return pairs_pb2.SuccResponse(success=0)

        return pairs_pb2.SuccResponse(success=-1)

    def get(self, request, context):
        """
        Returns the value associated with a key inside the class' dictionary.

        Returns: message of type Value, which contains a single field called value.
            Empty string if the key does not exist, the value associated with the key otherwise.
        """
        return pairs_pb2.Value(value=self.my_dict.get(request.key, ""))

    def activate(self, request, context):
        """
        Activates the server by adding its keys to the central server's dictionary.

        This method creates a connection to the central server through a service identifier
        passed as parameter and calls its register method passing the server's id and the keys stored in my_dict.

        Returns: message of type KeyCounter, which contains a single field called count, representing the number of keys registered, 
        which must be equal to the total passed.

        0, if only one parameter is passed to the program. Number of keys registered otherwise.
        """
        if len(sys.argv) > 2:
            channel = grpc.insecure_channel(request.id)
            stub = pairs_pb2_grpc.CentralServerStub(channel)
            response = stub.register(pairs_pb2.Server(id=f"{socket.getfqdn()}:{self.port}",
                                                      keys=self.my_dict.keys()))
            return pairs_pb2.KeyCounter(count=response.count)

        return pairs_pb2.KeyCounter(count=0)

    def terminate(self, request, context):
        """
        Terminates the server by setting the stop_event.

        Returns: message of type SuccResponse, which contains a single field called success.
        
        0, if the server was terminated successfully.
        """
        
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_PairsServicer_to_server(
        Pair(stop_event, sys.argv[1]), server)
    server.add_insecure_port(f'[::]:{sys.argv[1]}')
    server.start()
    stop_event.wait()  # Programa waits for the stop_event to be set
    server.stop(1)  # Server is stopped with a 1 second grace period after the stop_event is set


if __name__ == '__main__':
    serve()
