import grpc
import sys
import pairs_pb2, pairs_pb2_grpc


def findOwner(stub, key):
    request = pairs_pb2.Key(key=key)
    response = stub.findOwner(request)
    
    if(response.id != ""):
        print(response.id, end=":")
        channel = grpc.insecure_channel(response.id)
        stub = pairs_pb2_grpc.PairsStub(channel)
        request = pairs_pb2.Key(key=key)
        response = stub.get(request)
        print(response.value, end="\n")
    
    return


def terminate_server(stub):
    request = pairs_pb2.Empty()
    response = stub.terminate(request)
    print(response.success, end="\n")


def main():
    # 2. Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel(sys.argv[1])

    # 3. Create a stub object using the client stub and the channel.
    stub = pairs_pb2_grpc.CentralServerStub(channel)
    
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
                break 
  
    except Exception as e:
        print(f"Error: {e}")

    
if __name__ == '__main__':
    main()
