#include <iostream>
#include <grpcpp/grpcpp.h>
#include "pairs.pb.h"
#include "pais.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using std::cout;
using std::endl;
using std::string;

class KeyValueClient {
public:
    KeyValueClient(std::shared_ptr<Channel> channel)
        : stub_(KeyValueService::NewStub(channel)) {}

    void insert(const string& key, const string& value) 
    {
        KeyValue request;
        request.set_key(key);
        request.set_value(value);

        SuccResponse response;

        ClientContext context;
        stub_->insert(&context, request, &response);

        if (response.success() == 0)
            cout << "Inserção bem-sucedida" << endl;
        else 
            std::cerr << "Erro ao inserir: " << status.error_message() << endl;
    }

    void get(const string& key) {
        Key request;
        request.set_key(key);

        Value response;

        ClientContext context;
        Status status = stub_->get(&context, request, &response);

        if (response.value() != "") {
            cout << "Valor obtido: " << response.value() << endl;
        } else {
            std::cerr << "Erro ao obter valor: " << status.error_message() << endl;
        }
    }

private:
    std::unique_ptr<KeyValueService::Stub> stub_;
};

int main() 
{
    KeyValueClient client(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
    client.insert("chave", "valor");
    return 0;
}