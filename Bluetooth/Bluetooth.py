import os
import bluetooth
import subprocess

def setup_bluetooth():
    """Turn on Bluetooth and make the Pi discoverable."""
    print("Turning on Bluetooth...")
    # Ensure Bluetooth is powered on
    os.system("sudo bluetoothctl power on")
    # Set discoverable and pairable
    os.system("sudo bluetoothctl discoverable on")
    os.system("sudo bluetoothctl pairable on")
    # Set a default agent to auto-accept pairings
    os.system("sudo bluetoothctl agent NoInputNoOutput")
    os.system("sudo bluetoothctl default-agent")

def start_bluetooth_server():
    """Start the Bluetooth server to accept connections."""
    print("Starting Bluetooth server...")
    # Create a Bluetooth socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Bind the socket to any available port
    port = bluetooth.PORT_ANY
    server_sock.bind(("", port))
    server_sock.listen(1)

    # Advertise the service
    bluetooth.advertise_service(
        server_sock,
        "BluetoothServer",
        service_classes=[bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE],
    )

    print(f"Waiting for connection on RFCOMM channel {port}...")

    # Accept incoming connections
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            client_sock.send("Data received")
    except OSError:
        print("Connection closed.")
    finally:
        client_sock.close()
        server_sock.close()

if __name__ == "__main__":
    setup_bluetooth()
    start_bluetooth_server()