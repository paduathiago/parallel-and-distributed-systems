# Limpa todos os arquivos intermediários
clean:
	rm -rf pairs_pb2.py pairs_pb2_grpc.py __pycache__ *.pyc

# Executa o programa cliente da primeira parte
run_cli_pares: generate_proto client.py
	python3 client.py $(arg)

# Executa o programa servidor de pares com o comportamento da primeira parte
run_serv_pares_1: generate_proto  
	python3 server.py $(arg)

# Executa o programa servidor de pares com o comportamento da segunda parte
run_serv_pares_2: generate_proto  
	python3 server.py $(arg) qqcoisa

# Executa o programa servidor da segunda parte
run_serv_central: generate_proto  
	python3 central_server.py $(arg)

# Executa o programa cliente da segunda parte
run_cli_central: generate_proto  
	python3 central_client.py $(arg)

generate_proto: pairs_pb2.py pairs_pb2_grpc.py

pairs_pb2.py pairs_pb2_grpc.py: pairs.proto
	python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. pairs.proto
