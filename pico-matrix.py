import max7219
from machine import Pin, SPI
from time import sleep
import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # Use any available port
server_socket.listen(1)

while True:
    print("Waiting for a connection...")
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    data = client_socket.recv(1024).decode()
    if data == "start":
        print("Received start_program signal. Running the program...")
        spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
        ss = Pin(5, Pin.OUT)

        msg = 'NYR GOAL!!'
        length = len(msg)
        length = (length*8)
        display = max7219.Matrix8x8(spi, ss, 4)
        display.brightness(15)   # adjust brightness 1 to 15
        display.fill(0)
        display.show()
        sleep(0.5)

        while True:
            for x in range(32, -length, -1):
                display.text(msg ,x,0,1)
                display.show()
                sleep(0.03)
                display.fill(0)
        
    client_socket.close()

