import grpc
import os
import socket
import sys
import threading
from concurrent import futures

import pairs_pb2, pairs_pb2_grpc

class Pair(pairs_pb2_grpc.PairsServicer):
    def __init__(self, event):
        self.my_dict = {}
        self.stop_event = event
        self.port = os.environ.get("PORT", "8888")  # TODO: receive port from command line
    
    def insert(self, context, request):
        if request.key not in self.my_dict:
            self.my_dict[request.key] = request.value
            return pairs_pb2.SuccResponse(success=0)
        else:
            return pairs_pb2.SuccResponse(success=-1)
    
    def get(self, context, request): 
        return pairs_pb2.Value(value=self.my_dict.get(request.key, ""))
    

    def activate(self, request, context):
        if len(sys.argv) > 1:
            channel = grpc.insecure_channel(request.server_id)
            stub = pairs_pb2_grpc.CentralServerStub(channel)
            response = stub.register(pairs_pb2.Server(server_id=f"{socket.getfqdn()}:{self.port}",
                                                       server_keys=self.my_dict.keys()))
            return pairs_pb2.KeyCounter(count=response.count)

        return pairs_pb2.KeyCounter(count=0)
    
    
    def terminate(self, context, request):
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_PairsServicer_to_server(Pair(stop_event), server)
    server.add_insecure_port('localhost:8888')
    server.start()
    stop_event.wait()
    server.stop(1)
    # server.wait_for_termination()


if __name__ == '__main__':
    serve()
