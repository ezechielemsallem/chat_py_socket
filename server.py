import socket
import threading


HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_client = [] #list of currently users 



#fonctyiom to listen for upcoming messages 
def listen_for__messages(client, username):
    while 1: 
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"the message send from client {username} is empty")

#function to send message to all the client that 
#are currently connected 
def send_messages_to_all( message):
    for user in active_client: 
        send_message_to_client(user[1], message)

# fonction to send message to a single client 
def send_message_to_client(client, messsage): 
    client.sendall(messsage.encode())


#function to handle client 
def client_handler(client):
    #server will listen for client message that will 
    #contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_client.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("client username is empty")
    threading.Thread(target=listen_for__messages, args=(client, username, )).start()



def main():
    #creating the socket class object
    #AF_INET we are going to unse ipv4 qdress
    #sock_strem going to use dcp packet from comunications
    server =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Running the server on {HOST}- {PORT}")

    try:
        #provide the server wiith an addres in the form 
        # of host IP and PORT 
        server.bind((HOST, PORT))
    except:
        print(f"unable to bind to host {HOST} and port {PORT}")



    #set server limit 
    server.listen(LISTENER_LIMIT)


    #this while loop will keep listening to client connection 
    while 1:
        client, address = server.accept()
        print(f"Succeesfuly connected to client {address[0]}- {address[1]} ")
        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()