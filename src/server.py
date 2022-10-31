import socketserver
import threading
import platform
import os
import sys
import subprocess
import numpy as np
import cv2
import pyautogui
import base64
import random

from subprocess import Popen
from typing import Any, Literal
from typing_extensions import Self


# It receives data from the client, processes it, and sends it back
class ServerInstace(socketserver.BaseRequestHandler):
    def handle(self: object) -> None:
        """
        It receives data from the client, processes it, and sends it back
        """
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

# It's a TCP server that uses threads to handle multiple clients
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Commands:
    def __init__(self: object) -> None:
        pass
    
    def getOs(self: object) -> str:
        """
        It returns a string containing the system, release, and name of the operating system
        :return: The operating system, release, and name.
        """
        system = platform.system()
        rel = platform.release()
        name = os.name
        return "{}, {}, {}".format(system, rel, name)

    def executeCommandInCmd(self: object, command: str) -> (bytes | Literal[0]):
        """
        It executes a command in the command line and returns the output of the command

        :param self: object - This is the object that is being passed to the function
        :type self: object
        :param command: The command to be executed in the command prompt
        :type command: str
        :return: The output of the command is being returned.
        """
        self.command = command
        p = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = p.communicate()
        if (output):
                p.kill()
                return output
        if (errors):
            p.kill()
            return errors
        p.kill()
        return 0

    def Screenshot(self: object) -> str:
        """
        It takes a screenshot of the screen, converts it to a numpy array, converts it to a
        BGR image, and saves it as a .png file
        :return: The name of the image.
        """
        image = pyautogui.screenshot()

        image = cv2.cvtColor(np.array(image),
                             cv2.COLOR_RGB2BGR)
        
        self.nameImage = "image1.png"
        cv2.imwrite(self.nameImage, image)
        return self.nameImage
    
    def convertImageToString(self: object, nameImage: str) -> tuple[str, bytes]:
        """
        It takes an image file, converts it to a string, and then writes that string to a
        binary file
        
        :param self: object
        :type self: object
        :param nameImage: The name of the image to be converted to string
        :type nameImage: str
        :return: The name of the file and the string converted.
        """
        with open(nameImage, 'rb') as image2string:
            stringConverted = base64.b64encode(image2string.read())
        
        self.fileBin = f'encoded{random.random()}.bin'
        
        with open(self.fileBin, "wb") as file:
            file.write(stringConverted)
        
        return (self.fileBin, stringConverted)
    
    def convertStringToImage(self: object, nameBinFile: str) -> str:
        """
        It opens the binary file, reads the bytes, closes the file, then opens a new file with
        the same name but with a different extension, writes the decoded bytes to the new
        file, and closes the new file
        
        :param self: object
        :type self: object
        :param nameBinFile: The name of the binary file that you want to convert to an image
        :type nameBinFile: str
        :return: The name of the decoded image.
        """
        file = open(nameBinFile, 'rb')
        byte = file.read()
        file.close()
        
        self.imageNameDecoded = nameBinFile.replace('bin', 'jpeg')
        
        decodeit = open(self.imageNameDecoded, 'wb')
        decodeit.write(base64.b64decode(byte))
        decodeit.close()
        return self.imageNameDecoded
        

class Server:
    def __init__(self: object, PORT: int, HOST: str, ThreadedTCPInstace: Any | ThreadedTCPServer) -> None:
        """
        A constructor for the class.

        :param PORT: The port you want to use for the server
        :type PORT: int
        :param HOST: The IP address of the server
        :type HOST: str
        :param ThreadedTCPInstace: This is the class that will handle the client connections
        :type ThreadedTCPInstace: ThreadedTCPServer
        """
        self.PORT = PORT
        self.HOST = HOST
        self.ThreadedTCPInstace = ThreadedTCPInstace
        self.server = ThreadedTCPServer((self.HOST, self.PORT), self.ThreadedTCPInstace)
        self.Commands = Commands()

    def run(self: object) -> None:
        """
        The function starts a server thread that runs in the background and listens for
        requests
        """
        with self.server:
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

    def getIpAndHost(self: object) -> tuple[str, int]:
        """
        It returns the IP address and hostname of the server
        :return: The ip and host of the server.
        """
        with self.server:
            """
            It shuts down the server
            """
            ip, host = self.server.server_address
            return (ip, host)

    def shutdown(self: object) -> None:
        """
        It shuts down the server
        """
        self.server.shutdown()
