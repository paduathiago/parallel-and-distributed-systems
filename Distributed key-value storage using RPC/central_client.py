import grpc
import sys
import pairs_pb2, pairs_pb2_grpc


def findOwner(stub, key):
    """
    RPC to get the value associated with a key inside a corresponding server in the central server's dictionary.

    This function queries the central server in order to find the pairs server that owns the key passed as argument.
    If the key is registered, the client creates a connection with the corresponding pairs server using its identifier
    obtained as the response for the first RPC (findOwner). From this point, it creates a stub to be able to call the
    get RPC on the pairs server and prints the result.

    Prints: response.id, which is defined by ServerId message type in the proto file.
        Empty string if the key does not exist;

        The identifier of the server that owns the key followed by the value associated with it, which can be an empty string.
    """
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
    """
    RPC to terminate the central server which the client is connected to.

    Prints: response.success, which is defined by Sucess message type in the proto file.
        0 if the termination was successful.
    """
    request = pairs_pb2.Empty()
    response = stub.terminate(request)
    print(response.success, end="\n")


def main():
    # Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel(sys.argv[1])

    # Create a stub object using the client stub and the channel.
    stub = pairs_pb2_grpc.CentralServerStub(channel)
    
    try:
        while True:
            command = input().strip()

            if command.startswith("C"):
                _, key = command.split(",", 1)
                findOwner(stub, int(key))

            elif command == "T":
                terminate_server(stub)
                break 
  
    except EOFError:
        sys.exit(0)
    """
    Catching EOFError exception is necessary because the client is reading from stdin.
    This exception is raised when the client reaches the end of the file (EOF) and it is
    used to terminate the program. In this way the client can be terminated safely without 
    affecting the server.
    """

if __name__ == '__main__':
    main()
