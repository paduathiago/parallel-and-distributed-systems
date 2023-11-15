# Makefile para compilar programas C++ e o arquivo .proto

# Compilador
CXX = g++
# Opções de compilação
CXXFLAGS = -std=c++11 -pthread

# Diretório de inclusão para os cabeçalhos gerados pelo proto
PROTO_INC = .

# Diretório de inclusão para as bibliotecas do gRPC
GRPC_INC = /usr/local/lib

# Diretório de inclusão para o arquivo .proto
PROTO_DIR = .

# Nome do executável do servidor
SERVER_EXEC = server

# Nome do executável do cliente
CLIENT_EXEC = client

# Nome do arquivo .proto
PROTO_FILE = pairs.proto

# Nomes dos arquivos fonte
SERVER_SRC = server.cpp
CLIENT_SRC = client.cpp

# Nomes dos arquivos gerados pelo proto
PROTO_CC = $(PROTO_DIR)pairs.pb.cc
PROTO_GRPC_CC = $(PROTO_DIR)pairs.grpc.pb.cc

all: $(SERVER_EXEC) $(CLIENT_EXEC)

$(SERVER_EXEC): $(SERVER_SRC) $(PROTO_CC) $(PROTO_GRPC_CC)
	$(CXX) $(CXXFLAGS) -I$(PROTO_INC) -L$(GRPC_INC) -o $@ $^ -lgrpc++ -lgrpc -lprotobuf

$(CLIENT_EXEC): $(CLIENT_SRC) $(PROTO_CC) $(PROTO_GRPC_CC)
	$(CXX) $(CXXFLAGS) -I$(PROTO_INC) -L$(GRPC_INC) -o $@ $^ -lgrpc++ -lgrpc -lprotobuf

$(PROTO_CC) $(PROTO_GRPC_CC): $(PROTO_FILE)
	protoc -I=$(PROTO_DIR) --cpp_out=$(PROTO_DIR) --grpc_out=$(PROTO_DIR) --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` $<

clean:
	rm -f $(SERVER_EXEC) $(CLIENT_EXEC) $(PROTO_CC) $(PROTO_GRPC_CC)

.PHONY: all clean
