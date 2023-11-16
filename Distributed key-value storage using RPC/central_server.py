import grpc
import socket
import sys
import threading

from concurrent import futures

import pairs_pb2, pairs_pb2_grpc

class CentralServer:
    def __init__(self, event):
        self.keys_servers = {}
        self.stop_event = event
    

    def register(self, request, context):
        keys_processed = 0
        for key in request.server_keys:
            self.keys_servers[key] = request.server_id
            keys_processed += 1
        return pairs_pb2.KeyCounter(count=keys_processed)


    def terminate(self, request, context):
        self.stop_event.set()
        return pairs_pb2.SuccResponse(success=0)


    def findOwner(self, request, context):
        for key in self.keys_servers:
            if key == request.key:
                return pairs_pb2.ServerId(id=self.keys_servers[key])
        return pairs_pb2.ServerId(id="")


def serve():
    stop_event = threading.Event()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_CentralServerServicer_to_server(CentralServer(stop_event), server)
    server.add_insecure_port(f"[::]:{sys.argv[1]}")
    server.start()
    stop_event.wait()
    server.stop(1)

if __name__ == '__main__':
    serve()
