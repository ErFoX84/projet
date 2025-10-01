
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from threading import Thread

# Adresse du registre où la pression sera stockée
PRESSION_REGISTER = 0


def perte_pression_horaire(pression, perte_mensuelle_pourcent=15.0):
    """
    Calcule la pression restante après 1 heure, selon une perte mensuelle réaliste.
    La pression est en centibar (ex: 200 = 2 bars).
    """
    perte_horaire = perte_mensuelle_pourcent / 100 / 720
    return pression * (1 - perte_horaire)

def pression_simulation(context, slave_id=0x00):
    """Simule une perte de pression réaliste toutes les heures."""
    pression = 200  # Pression initiale (2 bars, en centibar)
    heures = 0
    while True:
        pression = perte_pression_horaire(pression)
        pression = max(100, min(pression, 300))  # Entre 1 et 3 bars
        context[slave_id].setValues(3, PRESSION_REGISTER, [int(pression)])
        heures += 1
        print(f"Heure {heures}: pression = {pression/100:.2f} bar")
        time.sleep(3600)  # 1 heure

if __name__ == "__main__":
    # Création du datastore Modbus avec un registre de 10 mots
    device = ModbusDeviceContext(
        hr=ModbusSequentialDataBlock(0, [200]*10)  # 20.0°C initial
    )
    context = ModbusServerContext(devices=device, single=True)

    # Lancement du thread de simulation de température
    sim_thread = Thread(target=pression_simulation, args=(context,))
    sim_thread.daemon = True
    sim_thread.start()

    # Démarrage du serveur Modbus TCP sur le port 502
    print("Serveur Modbus TCP démarré sur le port 502...")
    StartTcpServer(context, address=("0.0.0.0", 502))