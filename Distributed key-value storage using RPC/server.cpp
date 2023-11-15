#include <iostream>
#include <unordered_map>
#include <grpcpp/grpcpp.h>
#include "storage.pb.h"
#include "storage.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using std::cout;
using std::endl;
using std::string;

class KeyValueServiceImpl final : public KeyValueService::Service {
private: 
    std::unordered_map<int, std::string> dict;

public:
    int insert(ServerContext* context, const KeyValue* request, SuccResponse* response) override 
    {
        // Lógica de inserção aqui
        if(dict.insert({request->key(), request->value()}).second)
        {
            cout << "Inserindo: " << request->key() << ", " << request->value() << endl;
            response->set_success(0);
            return 0;
        }
        else
        {
            cout << "Chave já existe: " << request->key() << ", " << request->value() << endl;
            response->set_success(-1);
            return -1;
        }
    }

    Status get(ServerContext* context, const Key* request, Value* response) override 
    {
        // Lógica de consulta aqui
        cout << "Consultando chave: " << request->key() << endl;
        if (dict.find(request->key) != dict.end()) 
            response->set_value(dict[request->key]);

        else 
            // A chave não existe
            response->set_value("");

        return Status::OK;
    }
    /*Status activate(ServerContext* context, const Key* request, Value* response) override {
        // Lógica de consulta aqui
        cout << "Ativando chave: " << request->key() << endl;
        response->set_value("Valor correspondente à chave");
        return Status::OK;
    }*/
};

void RunServer() {
    string server_address("0.0.0.0:50051");
    KeyValueServiceImpl service;

    ServerBuilder builder;
    builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
    builder.RegisterService(&service);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    cout << "Servidor gRPC aguardando em " << server_address << endl;
    server->Wait();
}

int main() {
    RunServer();
    return 0;
}