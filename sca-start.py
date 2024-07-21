import threading, os

def run_flask():
    os.system('python app.py')

def run_grpc():
    os.system('python server-client_v2/sca_server.py')

if __name__ == '__main__':
    grpc_thread = threading.Thread(target=run_grpc)
    flask_thread = threading.Thread(target=run_flask)

    flask_thread.start()
    grpc_thread.start()

    flask_thread.join()
    grpc_thread.join()