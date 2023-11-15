import grpc
import pairs_pb2, pairs_pb2_grpc


def findOwner(stub, key):
    request = pairs_pb2.Key(key=key)
    response = stub.findOwner(request)
    
    if(response.server_id != ""):
        print(response.server_id, end=":")
        channel = grpc.insecure_channel(response.server_id)
        stub = pairs_pb2_grpc.PairsStub(channel)
        request = pairs_pb2.Key(key=key)
        response = stub.get(request)
        print(response.value, end="\n")
    
    return


def terminate_server(stub):
    request = pairs_pb2.quit()
    response = stub.quit(request)
    print(response.success, end="\n")

# 1. Import the necessary gRPC modules and the generated client stub.
def main():
    # 2. Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel('localhost:8888')  # TODO: receive ID string from command line

    # 3. Create a stub object using the client stub and the channel.
    stub = pairs_pb2_grpc.PairsStub(channel)
    
    try:
        while True:
            command = input().strip()

            # Check if there is nothing left to read (an empty string)
            if not command:
                break

            if command.startswith("C"):
                _, key = command.split(",", 1)
                findOwner(stub, int(key))

            elif command == "T":
                terminate_server(stub)
                # break Exit the loop when the command is "T"

            
    except Exception as e:
        print(f"Error: {e}")
