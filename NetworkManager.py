import socket
import sys
import traceback
from threading import Thread
from HostManager import HostManager
import time
from Client import Client
from DataManager import DataManager


class NetworkManager:
    """
    Handles all network operations in the Proxy Server
    """

    def __init__(self, ip_address, port_number):

        """
        Initialize a Socket for the Proxy Server
        """

        self.__mHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create managers
        self.__mHostManager = HostManager(ip_address, port_number)
        self.__mDataManager = DataManager()

        try:
            self.__mHost.bind((self.__mHostManager.mIpAddress, self.__mHostManager.mPortNumber))
        except:
            print("Bind Failed .. ERROR: " + str(sys.exc_info()))
            sys.exit()

    def start_server(self):
        """
        Listens to new connection requests and accept them according to a password sent to the client (in any form)
        """

        # Define max size of connections
        self.__mHost.listen(200)

        print("WAITING")

        # Accept Connections
        while True:
            client, socket_pair = self.__mHost.accept()

            print("New Connection at ", socket_pair)
            try:
                new_thread = Thread(target=self.__handle_connection, args=(client, socket_pair))
                new_thread.start()
            except:
                print("Thread did not start.")
                traceback.print_exc()

    def __handle_connection(self, client, socket_pair):

        """
        Handles communication after connection is established

        :param socket_pair: IP Address and Port Number of the client
        :param client: connection to the client
        """

        _BUFFER_SIZE = 5
        _MAX_WAIT_TIME = 25

        recv = client.recv(1024)
        recv = recv.decode("UTF-8").split("\n")[0]

        # Send the data that will be used in the verification of the client
        client_id = self.__validate_data(recv, socket_pair)
        if client_id is None:
            client.close()
            return

        # Send all info about online clients formatted as [ID,Passwd,IP,Port] line by line
        msg = ""
        for client in self.__mDataManager.mClient:
            if client.mIsOnline & (client.mUid != client_id):
                msg += client.mUid + ","
                msg += client.mIpAddress + ","
                msg += client.mPortNumber + "\n"

        client.send(msg.encode())

        start_time = time.time()
        while True:
            recv = client.recv(_BUFFER_SIZE)
            recv_size = sys.getsizeof(recv)
            recv = recv.decode("UTF-8").split("\r\n")[0]
            print(recv)

            if (recv_size == 5) & (recv == "ALIVE"):
                print(recv)
                start_time = time.time()
            elif time.time() - start_time > _MAX_WAIT_TIME:
                print("Connection Time Out")
                break

        client.close()

    def __validate_data(self, data, socket_pair):

        """
        Validates the data then save it

        :param data: msg received from the client
        :param socket_pair: IP Address and Port Number of the client

        :return: if data is valid: Client UUID -- else: None
        """

        info = data.split(",")

        if (self.__mHostManager.mUid == info[2]) & (self.__mHostManager.mPassword == info[3]):
            c = Client()
            c.mUid = info[0]
            if c not in self.__mDataManager.mClient:
                self.__mDataManager.add_client(c)

            index = self.__mDataManager.mClient.index(c)
            self.__mDataManager.mClient[index].mIpAddress = socket_pair[0]
            self.__mDataManager.mClient[index].mPortNumber = int(info[1])
            self.__mDataManager.mClient[index].mIsOnline = True
            return info[0]
        return None
