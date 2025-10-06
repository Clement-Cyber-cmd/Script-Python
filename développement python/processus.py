import psutil
if "chrome.exe" in (p.name() for p in psutil.process_iter()):
    print("Le processus chrome est en cours d'exécution.")