import bluetooth

def advertise_service_test():
    try:
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_sock.bind(("", bluetooth.PORT_ANY))
        server_sock.listen(1)

        # Advertise the service
        bluetooth.advertise_service(
            server_sock,
            "TestService",
            service_classes=[bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
        )

        print("Service advertised. Waiting for connection...")
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")

        client_sock.close()
        server_sock.close()
    except bluetooth.BluetoothError as e:
        print(f"BluetoothError: {e}")

if __name__ == "__main__":
    advertise_service_test()