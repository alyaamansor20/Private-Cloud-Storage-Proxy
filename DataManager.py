import os.path

from Client import Client


class DataManager:
    """
    Manages the data about verified/acceptable clients
    """

    def __init__(self):
        self.mClient = []
        self.__load_data()

    def __load_data(self):
        if not os.path.exists("data.txt"):
            open("data.txt", "x")

        file = open("data.txt", "rt")
        c = Client()

        for line in file:
            c.mUid = line

            self.mClient.append(c)
        file.close()

    def __save_data(self):
        file = open("data.txt", "w")

        for client in self.mClient:
            file.write(client.mUid + "\n")

        file.close()

    def add_client(self, c):
        """
        Adds new client and save the new array
        :param c: new client
        """
        self.mClient.append(c)
        self.__save_data()

    def remove_client(self, c):
        """
        Removes a client and save the new array
        :param c: old client
        """
        self.mClient.remove(c)
        self.__save_data()
