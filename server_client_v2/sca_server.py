from concurrent import futures
from sca_recognizer import face_compare, pkl_generator
from sca_discover_server import run_server
from db_operations import DatabaseManager
from datetime import datetime

import numpy as np
import cv2, grpc, time, threading, os, pytz
import grpc_image2_pb2
import grpc_image2_pb2_grpc

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_PORT = 50051
MESSAGE = b'Servidor gRPC disponivel na porta 50051'
LISTA_ALUNOS = []

class EnvioDeMensagensServicer(grpc_image2_pb2_grpc.EnvioDeMensagensServicer):
    def parse_string_to_tuple(self, s: str) -> tuple:
        """_summary_

        Args:
            s (str): _description_

        Returns:
            tuple: _description_
        """
        # Remove os parênteses
        s = s.strip('()')
        # Divide a string em partes
        parts = s.split(', ')
        # Converte cada parte para inteiro e cria uma tupla
        return tuple(map(int, parts))

    
    def db_ops(self, name: str = 'sca_db'):
        return DatabaseManager(name)
    
    def sys_path(self):
        return os.getcwd()
    
    def time_today(self):
        dd_mm = self.get_time_components(time.time())
        return (dd_mm['dia'], dd_mm['mes'])
    
    def status_frequencia(self, banco, matricula, aula):
        db = self.db_ops(banco)
        print(matricula)
        saida = db.read("Frequencia", {'matricula_aluno': matricula, 'codigo_aula': aula}) # Verifica se há registro da matricula para esta aula
        db.close()
        try:
            if saida[0][1] == matricula: # 
                print(f'Entrou no if - saida[1] = {saida[1]}')
                return True
        except:
            return False
    
    def gerar_frequencia(self, banco, matricula, disciplina, data):
        db = self.db_ops(banco)

        today = self.time_today() # saida dd mm para comparar dia de hoje com a aula

        for i in db.read('Aula'): # Olha as aulas cadastradas no banco
            data_aula = self.get_time_components(float(i[2])) # Transforma timestump em discionario de data
            if data_aula['dia'] == today[0] and data_aula['mes'] == today[1] and i[1] == disciplina: # Caso haja aula previstas para a turma no dia e mÊs que o reguistro 
                aula = i[0] # Caso verdade aula recebe o código da aula prevista para hoje
                print(f"Aula {aula}")
                print(f"Saida de status_frequencia {self.status_frequencia(banco, matricula, aula)}")
                if not self.status_frequencia(banco, matricula, aula): # Verificar se já há registro desse aluno na frequencia para hoje
                    db.create('Frequencia', {'matricula_aluno': matricula, # Gera a frequencia para aquele aluno
                                            'codigo_aula': aula,
                                            'presente': '1',
                                            'data': data})
                else:
                    print(f"Não haverá aula {data_aula} ou registro já feito!")
        
        db.close()
    
    def reshape_img(self, shape, image):
        try:
            image = np.frombuffer(image, dtype=np.uint8).reshape(int(shape[1]),int(shape[0]),3)
        except:
            try:
                image = np.frombuffer(image, dtype=np.uint8).reshape(int(shape[1]),int(shape[0]),4)
            except:
                print("Erro no shape da imagem - informe o shape correto da camera")
        return image
    
    def get_time_components(self, timestamp: float, timezone: str='America/Sao_Paulo') -> dict:
        """
        Converte um timestamp para um dicionário com os componentes de data e hora no formato brasileiro.
        
        Args:
            timestamp (float): O timestamp Unix a ser convertido.
            timezone (str): O fuso horário desejado (ex: 'America/Sao_Paulo').
        
        Returns:
            dict: Dicionário com os componentes de data e hora {'dia', 'mes', 'ano', 'hora', 'minuto', 'segundo'}.
        """
        local_tz = pytz.timezone(timezone)
        local_time = datetime.fromtimestamp(timestamp, local_tz)
        return {
            'dia': local_time.day,
            'mes': local_time.month,
            'ano': local_time.year,
            'hora': local_time.hour,
            'minuto': local_time.minute,
            'segundo': local_time.second
        }

    def get_img_db(self, id_turma):
        '''Compacta as pastas de cada aluno e envia cada arquivo .zip de forma que quando descompactar do outro lado eles estaram organizados'''
        # A ideia agora é a seguinte, tem uma constante chama LISTA_ALUNOS em que serão colocado a lista de pastas da turma
        # enquanto a lista não estiver esvaziada, o cliente requisita ao servidor novos alunos compactados
        # 
        comando = f'zip -r {id_turma} img_db/{id_turma}' 
        folder_path = 'img_db/' + id_turma
        if not LISTA_ALUNOS:
            print(f'Compactando imagens')
            for aluno_folder in os.listdir(folder_path):
                if aluno_folder.find('.pkl') == -1:
                    comando = f'zip -r {aluno_folder} {folder_path}/{aluno_folder}'
                    LISTA_ALUNOS.append(aluno_folder)
                    os.system(comando)
        if LISTA_ALUNOS:
            print(f'Realizando o envio das imagens em bytes')
            matricula = LISTA_ALUNOS.pop()
            with open(matricula + '.zip', 'rb') as file:
                arq = file.read()
                print(f'Numero de alunos na LISTA_ALUNOS {len(LISTA_ALUNOS)}')
                if not LISTA_ALUNOS:
                    os.system(f'rm {matricula + '.zip'}')
                    return arq, True
                else:
                    os.system(f'rm {matricula + '.zip'}')
                    return arq, False
        return b'vazio', True
        
        '''
        for aluno_folder in os.listdir(folder_path):
            if aluno_folder.find('.pkl') == -1:
                images = os.path.join(folder_path, aluno_folder)
                for img_file in os.listdir(images):
                    print(img_file)
            
            image_path = os.path.join(folder_path, image_name)
            if os.path.isfile(image_path) :
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    image = image_transfer_pb2.Image(name=image_name, data=image_data)
                    images.append(image)'''

    def EnviarMensagem(self, request, context):
        '''
        Esta função tem a tarefa de receber mensagens dos clintes e as devolver

        A mensagem do clinte inclui os seguintes dados:
            type int32;
            id_turma string;
            id_disciplina string;
            id_aluno = string;
            time int64;  // Timestamp geralmente é representado como int64
            image bytes;
            name string;
        '''

        # Decodificando a mensagem e transformando em nparray - os valores em reshape devem ser alterados de acordo com a camera
        # Quando utilizado o método opencv, esses valores devem ser cuidadosamente alterados
        #image = np.frombuffer(request.image, dtype=np.uint8).reshape(720,1080,4)
        
        if request.type == 0:
            response = grpc_image2_pb2.ServidorParaCliente()
            response.type = request.type
            response.id_turma = '_'
            response.id_disciplina = '_'
            response.id_aluno = '_'
            response.time = 0.0
            response.name = str('_')
            response.num_faltas = 0
            response.repositorio = b'_'
            return response

        elif request.type == 1:
            repositorio = self.get_img_db(request.id_turma)
            response = grpc_image2_pb2.ServidorParaCliente()
            response.type = request.type
            response.id_turma = ''
            response.id_disciplina = ''
            response.id_aluno = ''
            response.time = time.time()
            with open('image.jpg', 'rb') as file:
                file = file.read()
                response.image = file
            response.name = str(repositorio[1])
            response.num_faltas = 0
            response.repositorio = repositorio[0]
            print(f'Repositorio == {(repositorio[0])[:25]}')
            return response
        else:
        

            db = self.db_ops('sca_db')

            print(request.shape)

            #shape = self.reshape_adj(request.shape)

            #image = self.reshape_img(shape, request.image)

            image = np.frombuffer(request.image, dtype=np.uint8).reshape(self.parse_string_to_tuple(request.shape))

            # Salvando a imagem recebida. Essa linha poderá ser apagada caso se possa utilizar o ndarray na lib deepface
            cv2.imwrite('image.jpg', image)
        
        # Realizando o reconhecimento a partir da imagem salva na linha anterior
            result = face_compare('image.jpg', self.sys_path() + '/img_db/' + request.id_turma, 3)

            try:
                matricula = os.path.basename(result[0])
                matricula = matricula[:matricula.find('-')]
            except:
                matricula = result[0]

            print(matricula)

            self.gerar_frequencia('teste.db', matricula, request.id_disciplina, request.time)

            # Preenchendo os valores da resposta do servidor para o cliente
            response = grpc_image2_pb2.ServidorParaCliente()
            response.type = request.type
            response.id_turma = request.id_turma
            response.id_disciplina = request.id_disciplina
            response.id_aluno = matricula
            response.time = request.time
            response.image = request.image
            response.name = (db.read('Aluno', {'matricula_aluno': matricula}))[0][1]
            response.num_faltas = 0
            response.repositorio = b''

            db.close()
            
            return response

def serve():
    # Padrão em uso de servidores gRPC apenas com aumento de tamanho máximo de resposta
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
					   options=[('grpc.max_send_message_length', 19*1024*1024),
				 				('grpc.max_receive_message_length', 19*1024*1024),
								]
					   )
    grpc_image2_pb2_grpc.add_EnvioDeMensagensServicer_to_server(EnvioDeMensagensServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor iniciado na porta 50051")

    # Inicia a thread de anúncio multicast
    threading.Thread(run_server(), daemon=True).start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        exit()

if __name__ == '__main__':
    serve()
