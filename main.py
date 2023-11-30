from HostManager import HostManager
from NetworkManager import NetworkManager

# TODO: Should read from user input
ip_address = "10.10.10.14"
port_number = 4444

network_manager = NetworkManager(ip_address, port_number)
network_manager.start_server()
