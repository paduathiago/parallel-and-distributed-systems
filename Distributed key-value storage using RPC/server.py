import grpc
import socket
import sys
import threading
from concurrent import futures

import pairs_pb2, pairs_pb2_grpc

class Pair(pairs_pb2_grpc.PairsServicer):
    def __init__(self, event, port):
        self.my_dict = {}
        self.stop_event = event
        self.port = port
    
    
    def insert(self, request, context):
        if request.key not in self.my_dict:
            self.my_dict[request.key] = request.value
            return pairs_pb2.SuccResponse(success=0)

        return pairs_pb2.SuccResponse(success=-1)
    

    def get(self, request, context): 
        return pairs_pb2.Value(value=self.my_dict.get(request.key, ""))
    

    def activate(self, request, context):
        if len(sys.argv) > 2:
            channel = grpc.insecure_channel(request.id)
            stub = pairs_pb2_grpc.CentralServerStub(channel)
            response = stub.register(pairs_pb2.Server(id=f"{socket.getfqdn()}:{self.port}",
                                                       keys=self.my_dict.keys()))
            return pairs_pb2.KeyCounter(count=response.count)

        return pairs_pb2.KeyCounter(count=0)
    
    
    def terminate(self, request, context):
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_PairsServicer_to_server(Pair(stop_event, sys.argv[1]), server)
    server.add_insecure_port(f'[::]:{sys.argv[1]}')  # Check
    server.start()
    stop_event.wait()
    server.stop(1)
    # server.wait_for_termination()


if __name__ == '__main__':
    serve()
