# Sistema de Chamada Automática de Sala de Aula

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📚 Sobre o Projeto

Este sistema foi desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) em Ciência da Computação na Universidade Federal do Ceará. O objetivo é automatizar a chamada em sala de aula utilizando reconhecimento facial.

## 🖥️ Arquitetura do Sistema

### Componentes Principais:

1. **Cliente (Raspberry Pi)**

   - Captura imagens dos alunos.
   - Envia imagens para o servidor via gRPC.
2. **Servidor**

   - Recebe imagens do cliente.
   - Realiza o reconhecimento facial utilizando o framework [DeepFace](https://github.com/serengil/deepface).
   - Devolve informações do aluno reconhecido.
   - Envia pacotes de multicast com informações de endereço para que o Raspberry possa se conectar automaticamente.

### Fluxo de Funcionamento:

1. **Inicialização:**

   - O servidor inicia e envia pacotes de multicast com seu endereço IP.
   - O Raspberry Pi detecta esses pacotes e se conecta ao servidor via gRPC.
2. **Reconhecimento Facial:**

   - O Raspberry Pi captura imagens dos alunos.
   - As imagens são enviadas ao servidor.
   - O servidor utiliza o DeepFace para identificar os alunos e retorna as informações.

## 🚀 Tecnologias Utilizadas

- **gRPC**: Comunicação entre cliente e servidor.
- **Python**: Linguagem de programação principal.
- **Raspberry Pi**: Dispositivo cliente.
- **DeepFace**: Framework de reconhecimento facial.
- **Sockets**: Implementação do multicast.

## 🛠️ Como Executar o Projeto

### Pré-requisitos

- Python 3.8+
- Raspberry Pi com câmera
- Instalação das bibliotecas necessárias:
  ```bash
  pip install grpcio grpcio-tools opencv-python deepface requests numpy pandas gdown tqdm Pillow opencv-python tensorflow keras Flask mtcnn retina-face fire gunicorn
  ```


### Passo a Passo

1. **Clonar o Repositório**
   ```bash
   git clone https://github.com/eletromarlon/Sistema-de-Chamada-Automatica.git
   cd Sistema-de-Chamada-Automatica
   ```

## 📄 Estrutura do Projeto

<pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>plaintext</span><div class="flex items-center"><span class="" data-state="closed"></span></div></div><div class="overflow-y-auto p-4 text-left undefined" dir="ltr"><code class="!whitespace-pre hljs language-plaintext">.
├── server-client_v2
│   ├── cam_auto_take.py
│   ├── sca_discover_client.py
│   ├── sca_discover_server.py
│   ├── sca_main.py
│   ├── sca_recognizer.py
│   ├── sca_server.py
│   └── server_grpc_JSON.py
├── protos
│   ├── grpc_image2.proto
├── README.md
└── requirements.txt
</code></div></div></pre>

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues.

## 📞 Contato

Para mais informações, entre em contato com:

* **Nome:** Marlon Duarte
* **Email:** [eletromarlon@gmail.com](mail.google.com)

---

Feito com ❤️ na [Universidade Federal do Ceará](http://www.ufc.br/) - Campus de Crateús.
