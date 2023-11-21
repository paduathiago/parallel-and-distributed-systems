.PHONY: clean run_cli_pares run_serv_pares_1 run_serv_pares_2 run_serv_central run_cli_central generate_proto

# Regra para limpar arquivos intermediários
clean: generate_proto
    rm -f pairs_pb2.py pairs_pb2_grpc.py

# Regra para executar o cliente da primeira parte
run_cli_pares: generate_proto
    python client.py $(arg)

# Regra para executar o servidor de pares com comportamento da primeira parte
run_serv_pares_1: generate_proto
    python server.py $(arg)

# Regra para executar o servidor de pares com comportamento da segunda parte
run_serv_pares_2: generate_proto
    python server.py $(arg) qqcoisa

# Regra para executar o servidor central da segunda parte
run_serv_central: generate_proto
    python central_server.py $(arg)

# Regra para executar o cliente da segunda parte
run_cli_central: generate_proto
    python central_client.py $(arg)

# Regra para gerar arquivos intermediários a partir do arquivo proto
generate_proto: pairs_pb2.py pairs_pb2_grpc.py

pairs_pb2.py pairs_pb2_grpc.py: pairs.proto
    python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. pairs.proto
