import grpc
import pairs_pb2, pairs_pb2_grpc

# 1. Import the necessary gRPC modules and the generated client stub.
def run():
    # 2. Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel('localhost:50051')

    # 3. Create a stub object using the client stub and the channel.
    stub = pairs_pb2_grpc.PairsStub(channel)

    # 4. Call the methods exposed by the server through the stub object.
    
