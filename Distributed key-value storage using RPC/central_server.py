import socket
import threading
from concurrent import futures
import grpc

import pairs_pb2, pairs_pb2_grpc

class CentralServer:
    def __init__(self, event):
        self.my_servers = {}
        self.stop_event = event
    

    def register(self, request, context):
        self.my_server.add(request.server_id, request.server_keys)
        return pairs_pb2.KeyCounter(count=len(self.my_servers[request.server_id]))
    

    def terminate(self, request, context):
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)
    

    def findOwner(self, request, context):
        for server_id in self.my_servers:
            if request.key in self.my_servers[server_id]:
                return pairs_pb2.OwnerResponse(owner_id=server_id)
        return pairs_pb2.OwnerResponse(owner_id="")


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_CentralServerServicer_to_server(CentralServer(stop_event), server)
    server.add_insecure_port('localhost:8888')
    server.start()
    stop_event.wait()
    server.stop(1)

if __name__ == '__main__':
    serve()
