import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
questions = [
    " What is the Italian word for PIE? \n a. Mozarella\n b. Pasty\n c. Patty\n d. Pizza",
    " Which sea creature has three hearts? \n a. Dolphin\n b. Octopus\n c. Walrus\n d. Seal",
    " How many bones does an adult human have? \n a. 206\n b. 208\n c. 201\n d. 196",
    " Who is Loki? \n a. God of Thunder\n b. God of Dwarves\n c. God of Mischief\n d. God of Gods",
    " Who gifted the Statue of Liberty to the US? \n a. Brazil\n b. France\n c. Wales\n d. Germany"
]
nicknames = []
answers = ['d', 'b', 'a', 'c', 'b']
print("Server has started...")
def get_random_question_answer(conn):
    random_index = random.randit(0, len(questions) -1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer
def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn):
    score=0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c, or d.".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better kuck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)
while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + "connected!")
    new_thread = Thread(target = clientthread, args = (conn, nickname))
    new_thread.start() 
