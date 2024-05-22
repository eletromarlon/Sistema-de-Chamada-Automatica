package main

import (
    "context"
    "fmt"
    "log"

    "github.com/golang/protobuf/proto"
    "google.golang.org/grpc"

    pb "mensagem"
)

func main() {
    conn, err := grpc.Dial(":50051", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Erro ao conectar com o servidor: %v", err)
    }
    defer conn.Close()

    cliente := pb.NewImagemServiceClient(conn)

    imagem := []byte{0, 1, 2, 3, 4, 5}

    stream, err := cliente.UploadImagem(context.Background())
    if err != nil {
        log.Fatalf("Erro ao iniciar stream: %v", err)
    }
    defer stream.Close()

    // Enviar imagem para o servidor
    req := &pb.ImagemRequest{Imagem: imagem}
    if err := stream.Send(req); err != nil {
        log.Printf("Erro ao enviar imagem: %v", err)
        return
    }

    // Receber mensagem do servidor
    res, err := stream.Recv