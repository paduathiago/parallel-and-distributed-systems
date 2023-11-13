import grpc
from concurrent import futures

import pairs_pb2, pairs_pb2_grpc

class Pair(pairs_pb2_grpc.PairsServicer):
    def __init__(self):
        self.my_dict = {}
    
    def insert(self, context, request):
        if request.key not in self.my_dict:
            self.my_dict[request.key] = request.value
            return pairs_pb2.SuccResponse(success=0)
        else:
            return pairs_pb2.SuccResponse(success=-1)
    
    def get(self, context, request): 
        return pairs_pb2.Value(value=self.my_dict.get(request.key, ""))
    
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pairs_pb2_grpc.add_PairsServicer_to_server(Pair(), server)
    server.add_insecure_port('localhost:8888')
    server.start()
    server.wait_for_termination()
