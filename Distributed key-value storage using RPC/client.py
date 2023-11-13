import grpc
import pairs_pb2, pairs_pb2_grpc

def insert(stub, key, description):
    request = pairs_pb2.KeyValue(key=key, value=description)
    response = stub.insert(request)
    print(response.success, end="\n")

def get(stub, key):
    request = pairs_pb2.Key(key=key)
    response = stub.get(request)
    print(response.value, end="\n")

"""
def activate_service(stub, service_identifier):
    request = pairs_pb2.ActivateRequest(service_identifier=service_identifier)
    response = stub.Activate(request)
    return response.status
"""

def terminate_server(stub):
    request = pairs_pb2.quit()
    response = stub.quit(request)


# 1. Import the necessary gRPC modules and the generated client stub.
def main():
    # 2. Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel('localhost:50051')

    # 3. Create a stub object using the client stub and the channel.
    stub = pairs_pb2_grpc.PairsStub(channel)
    
    # 4. TODO: Read input from the user and call the appropriate RPC.
    


