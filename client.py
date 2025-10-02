
from pymodbus.client import ModbusTcpClient

def simuler_bouton_compresseur():
    client = ModbusTcpClient('127.0.0.1', port=502)
    client.connect()

    # Lecture de la pression actuelle
    result = client.read_holding_registers(address=0)
    if not result.isError():
        print("Pression actuelle:", result.registers[0], "centibar")

    input("Appuyez sur Entrée pour allumer le compresseur...")
    # On simule l'activation du compresseur en écrivant 1 dans le coil 0
    client.write_coil(address=0, value=True)
    print("Compresseur allumé ! (coil 0 = True)")

    client.close()

if __name__ == "__main__":
    simuler_bouton_compresseur()    