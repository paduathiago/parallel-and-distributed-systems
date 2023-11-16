import grpc
import sys
import pairs_pb2, pairs_pb2_grpc

def insert(stub, key, description):
    request = pairs_pb2.KeyValue(key=key, value=description)
    response = stub.insert(request)
    print(response.success, end="\n")


def get(stub, key):
    request = pairs_pb2.Key(key=key)
    response = stub.get(request)
    print(response.value, end="\n")


def activate_service(stub, server_id):
    request = pairs_pb2.ServerId(id=server_id)
    response = stub.activate(request)
    print (response.count, end="\n")


def terminate_server(stub):
    request = pairs_pb2.Empty()
    response = stub.terminate(request)
    print(response.success, end="\n")

# 1. Import the necessary gRPC modules and the generated client stub.
def main():
    # 2. Create a gRPC channel to connect to the server.
    channel = grpc.insecure_channel(sys.argv[1])

    # 3. Create a stub object using the client stub and the channel.
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


if __name__ == '__main__':
    main()
