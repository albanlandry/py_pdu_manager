import socket
import threading
import utils.string_utils as strUtils
from patterns.observer import PDUSubject, PDUListener
from typing import List

class PduController(PDUSubject):
    _instance = None

    _isConnected = False
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        
        return cls._instance
    
    # @staticmethod
    def findPdu(self, message, broadcast_ip, broadcast_port: int = 5001, timeout: float = 20):
        """
        Parameters:
        - message (string): Message to broadcast on the network to the PDU
        - broadcast_ip (string): Broadcast address
        - broadcast_port: Broadcast port
        - timeout (int): socket timeout in seconds
        """
        msg_hex = message.encode('utf-8').hex()
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Creates a UDP socket for the given message and bind it to all existing addresses
            server.bind(('0.0.0.0', 5001))

            # Enable broadcast on the server
            server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # server.settimeout(timeout)

            # Pack the message and send it to the broadcast ip and port
            server.sendto(bytes.fromhex(msg_hex), (broadcast_ip, broadcast_port))

            # Listening to incoming repliess
            while True:
                data, (cli_addr, cli_port) = server.recvfrom(1024)

                print(data, (cli_addr, cli_port))

                header = strUtils.extract_bytes(data, 0, 4)
                mac = strUtils.extract_bytes(data, 4, 6)
                flag = strUtils.extract_bytes(data, 10, 1)
                ip = strUtils.extract_bytes(data, 11, 4)
                subnet = strUtils.extract_bytes(data, 15, 4)
                gateway = strUtils.extract_bytes(data, 19, 4)
                port = strUtils.extract_bytes(data, 23, 4)
                message = strUtils.extract_bytes(data, 25, 11)
                sets = strUtils.extract_bytes(data, 36, len(data) - 36 - 1)

                # Broadcast the received reply to the listeners
                for observer in self._observers:
                    observer.onPduFound(
                        {
                            "header": header.decode("ascii"),
                            "mac": mac.hex(),
                            "flag": int.from_bytes(flag),
                            "ip": ip.hex(),
                            "subnet": subnet.hex(),
                            "gateway": gateway.hex(),
                            "port": int.from_bytes(port),
                            "message": message,
                            "other": sets
                        }
                    )
        except Exception as err:
            print(err)

        finally:
            server.close()
