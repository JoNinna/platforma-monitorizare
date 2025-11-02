# Script Python pentru efectuarea backup-ului logurilor de sistem din fisierul system-state.log  dacă fișierul s-a modificat.

import os
import shutil
import hashlib
from time import sleep
from datetime import datetime

filetocheck = 'system-state.log'

# Perioada la care se face backup este primită ca variabilă de mediu cu valoarea implicită 5 secunde.
checkforbackup = int(os.getenv('CHECKFORBACKUP', 5))

# Directorul în care se fac backup-urile este primit ca variabilă de mediu cu valoare implicită backup.
backupdir= os.getenv('BACKUPDIR', 'backup')

def check_initial_hash(file_to_check):
    try:
        with open(file_to_check, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return file_hash
    except FileNotFoundError:
        print(f"[EROARE] Fișierul {file_to_check} nu a fost găsit!")
        return None
    except Exception as e:
        print(f"[EROARE] Nu s-a putut citi fișierul {file_to_check}: {e}")
        return None


def check_for_modifications(filetocheck):
    initial_hash = check_initial_hash(filetocheck)

    while True:
        updated_hash = check_initial_hash(filetocheck)

        if initial_hash != updated_hash:

            print(f"Fisierul {filetocheck} a fost modificat, urmeaza sa fie backed up!")
            # Fișierul de backup trebuie să conțină în nume și data la care a fost efectuat backup-ul.
            now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            if not os.path.exists(backupdir):
                os.mkdir(backupdir)

            filebackup = f"{os.path.basename(filetocheck.split('.')[0])}-{str(now)}.log"
            pathbackup = os.path.join(backupdir,filebackup) 

            try:
                shutil.copy2(filetocheck, pathbackup)
                print(f"Fisierul {filebackup} a fost backed up!")
            except Exception as e:
                print(f"[EROARE] Backup-ul nu a putut fi realizat: {e}")

            initial_hash = updated_hash
        else:
            print(f"[INFO] {datetime.now()} Niciun update momentan!")

        sleep(checkforbackup)

def main():
    if not os.path.exists(filetocheck):
        print(f"[WARNING] Fisierul {filetocheck} pentru backup nu a fost gasit!")
        while not os.path.exists(filetocheck):
            print(f"[INFO] Astept ca fisierul de loguri {filetocheck} pentru backup sa fie generat!")
            sleep(checkforbackup)
    check_for_modifications(filetocheck)

if __name__ == "__main__":
    print(f"[INFO] Pornire monitorizare fișier {filetocheck} la {datetime.now()}")
    main()


