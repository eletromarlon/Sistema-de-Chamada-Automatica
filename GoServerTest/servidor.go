package main

import (
    "context"
    "fmt"
    "log"
    "net"

    "github.com/golang/protobuf/proto"
    "google.golang.org/grpc"
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"

    pb "mensagem"
)

type servidor struct{}

func (s *servidor) UploadImagem(stream pb.ImagemService_UploadImagemServer) error {
    var imagem []byte
    var mensagem string

    for {
        req, err := stream.Recv()
        if err == io.EOF {
            break
        }
        if err != nil {
            log.Printf("Erro ao receber imagem: %v", err)
            return status.Error(codes.Internal, "Erro interno do servidor")
        }

        imagem = req.Imagem

        // Processar a imagem (por exemplo, salvar em disco)

        mensagem = "Imagem recebida com sucesso!"

        res := &pb.ImagemResposta{Mensagem: mensagem}
        if err := stream.Send(res); err != nil {
            log.Printf("Erro ao enviar mensagem: %v", err)
            return status.Error(codes.Internal, "Erro interno do servidor")
        }
    }

    return nil
}

func main() {
    lis, err := net.Listen("tcp", ":50051")
    if err != nil {
        log.Fatalf("Erro ao criar listener: %v", err)
    }
    defer lis.Close()

    s := grpc.NewServer()
    pb.RegisterImagemServiceServer(s, &servidor{})

    log.Printf("Servidor iniciado na porta 50051")
    if err := s.Serve(lis); err != nil {
        log.Fatalf("Erro ao iniciar servidor: %v", err)
    }
}