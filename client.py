from pymodbus.client import ModbusTcpClient
import time

def simuler_bouton_compresseur():
    while True:
        client = ModbusTcpClient('127.0.0.1', port=502)
        try:
            if not client.connect():
                raise ConnectionError

            # Lecture de la pression actuelle
            result = client.read_holding_registers(address=0)
            if result.isError():
                raise ConnectionError
            pression_bar = result.registers[0] / 100
            print(f"Pression actuelle: {pression_bar:.2f} bar")

            choix = input("Appuyez sur Entrée pour allumer le compresseur, ou q pour quitter : ")
            if choix.lower() == "q":
                print("Fermeture du client.")
                client.close()
                break
            client.write_register(address=1, value=1)
            print("Compresseur allumé ! (registre 1 = 1)")

            # Lecture de la pression après activation
            time.sleep(1)
            result = client.read_holding_registers(address=0)
            if not result.isError():
                pression_bar = result.registers[0] / 100
                print(f"Nouvelle pression: {pression_bar:.2f} bar")
        except Exception:
            print("Erreur de connexion au serveur Modbus. Vérifiez que le serveur est allumé et accessible sur le port 502.")
            time.sleep(2)
            continue
        finally:
            client.close()

if __name__ == "__main__":
    simuler_bouton_compresseur()