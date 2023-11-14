import socket
import grpc

import pairs_pb2, pairs_pb2_grpc

class CentralServer:
    def __init__(self):
        self.my_servers = {}
    
    def register(self, request, context):
        self.my_server.add(request.server_id, request.server_keys)
        return pairs_pb2.KeyCounter(count=len(self.my_servers[request.server_id]))
    
    def terminate(self, request, context):
        pass