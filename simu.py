
def pression_apres_jours(pression_initiale: int, jours: int, perte_mensuelle: int = 15) -> int:
    perte_journaliere = perte_mensuelle / 100 / 30
    pression = pression_initiale
    for j in range(1, jours + 1):
        pression *= (1 - perte_journaliere)
        print(f"Jour {j}: pression = {int(pression)} bar")
    return int(pression)

if __name__ == "__main__":
    pression_initiale = 200  # pression initiale en bar
    jours = 1000  # nombre de jours à simuler
    perte_mensuelle = 15  # perte mensuelle en %
    pression_finale = pression_apres_jours(pression_initiale, jours, perte_mensuelle)
    print(f"\nAprès {jours} jours, la pression est de {pression_finale} bar.")

