clean:
	rm -rf pairs_pb2.py pairs_pb2_grpc.py __pycache__ *.pyc

run_cli_pares: generate_proto client.py
	python3 client.py $(arg)

run_serv_pares_1: generate_proto  
	python3 server.py $(arg)

run_serv_pares_2: generate_proto  
	python3 server.py $(arg) anything

run_serv_central: generate_proto  
	python3 central_server.py $(arg)

run_cli_central: generate_proto  
	python3 central_client.py $(arg)

# Generates interface files from .proto
generate_proto: pairs_pb2.py pairs_pb2_grpc.py

pairs_pb2.py pairs_pb2_grpc.py: pairs.proto
	python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. pairs.proto
