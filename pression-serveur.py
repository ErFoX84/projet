
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusDeviceContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from threading import Thread

# Adresse du registre où la pression sera stockée
PRESSION_REGISTER = 0



def pression_simulation(context, slave_id=0x00, pression_initiale=200, perte_mensuelle=15):
    """
    Simule la perte de pression et met à jour le registre Modbus chaque jour.
    La pression est en centibar (ex: 200 = 2 bars).
    """
    perte_journaliere = perte_mensuelle / 100 / 30
    pression = pression_initiale
    jours = 0
    while True:
        # Vérifie si le compresseur est activé (registre 1)
        compresseur = context[slave_id].getValues(3, 1, count=1)[0]
        if compresseur == 1:
            pression = pression_initiale
            context[slave_id].setValues(3, 1, [0])  # Réinitialise le bouton
            print(f"Compresseur activé : pression remise à {pression} centibar(s)")
        else:
            pression *= (1 - perte_journaliere)
            pression = max(0, min(pression, 300))  # Entre 0 et 3 bars
        jours += 1
        context[slave_id].setValues(3, PRESSION_REGISTER, [int(pression)])
        print(f"Jour {jours}: pression = {int(pression)} centibar(s)")
        time.sleep(1)  # 1 seconde = 1 jour simulé


# --- Bloc serveur Modbus ---


if __name__ == "__main__":
    # Création du datastore Modbus avec un registre de 10 mots
    device = ModbusDeviceContext(
        hr=ModbusSequentialDataBlock(0, [200]*10),
        co=ModbusSequentialDataBlock(0, [True]*10)
    )
    context = ModbusServerContext(devices=device, single=True)

    # Lancement du thread de simulation de la pression
    sim_thread = Thread(target=pression_simulation, args=(context,))
    sim_thread.daemon = True
    sim_thread.start()

    # Démarrage du serveur Modbus TCP sur le port 502
    print("Serveur Modbus TCP démarré sur le port 502...")
    StartTcpServer(context, address=("0.0.0.0", 502))