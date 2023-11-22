import grpc
import sys
import pairs_pb2, pairs_pb2_grpc


def insert(stub, key, description):
    """
    RPC to insert a key-value pair into the server's dictionary.

    Prints: response.success, which is defined by Sucess message type in the proto file.
        0 if the insertion was successful.

        -1 if the key already exists. The insertion fails.
    """
    request = pairs_pb2.KeyValue(key=key, value=description)
    response = stub.insert(request)
    print(response.success, end="\n")


def get(stub, key):
    """
    RPC to get the value associated with a key in the server's dictionary.

    Prints: response.value, which is defined by Value message type in the proto file.
        Empty string if the key does not exist, the value associated with the key otherwise.
    """
    request = pairs_pb2.Key(key=key)
    response = stub.get(request)
    print(response.value, end="\n")


def activate_service(stub, server_id):
    """
    RPC to activate the connected server by adding its keys to the central server's dictionary.

    Prints: response.count, which is defined by KeyCounter message type in the proto file.
        0, if only one parameter is passed to the program, meaning that the server is no activable. 
        
        Number of keys registered otherwise.
    """
    request = pairs_pb2.ServerId(id=server_id)
    response = stub.activate(request)
    print (response.count, end="\n")


def terminate_server(stub):
    """
    RPC to terminate the server which the client is connected to.

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
    stub = pairs_pb2_grpc.PairsStub(channel)
    try:
        while True:
            command = input().strip()

            if command.startswith("I"):
                _, key, description = command.split(",", 2)
                insert(stub, int(key), description)

            elif command.startswith("C"):
                _, key = command.split(",", 1)
                get(stub, int(key))

            elif command == "T":
                terminate_server(stub)
                break

            elif command.startswith("A"):
                _, service_identifier = command.split(",", 1)
                activate_service(stub, service_identifier) 
            
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
