# Script Python pentru efectuarea backup-ului logurilor de sistem din fisierul system-state.log  dacă fișierul s-a modificat.

import os
import shutil
import hashlib
from datetime import datetime

# Perioada la care se face backup este primită ca variabilă de mediu cu valoarea implicită 5 secunde.
checkforbackup = os.getenv('CHECKFORBACKUP', 1)

# Directorul în care se fac backup-urile este primit ca variabilă de mediu cu valoare implicită backup.
backupdir= os.getenv('BACKUPDIR', 'backup')

def check_initial_hash(file_to_check):
    with open(file_to_check, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash

def check_for_modifications(filetocheck):
    initial_hash = check_initial_hash(filetocheck)

    while checkforbackup:
        updated_hash = check_initial_hash(filetocheck)

        if initial_hash != updated_hash:

            print("Fisierul a fost modificat, urmeaza sa fie backed up!")
            # Fișierul de backup trebuie să conțină în nume și data la care a fost efectuat backup-ul.
            now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            filebackup = f"{os.path.basename(filetocheck.split('.')[0])}-{str(now)}.log"
            print(f"Fisierul {filebackup} a fost backed up!")

            if os.path.exists(backupdir):
                shutil.copy2(filetocheck, backupdir)
                os.rename("backupdir/filetocheck",filebackup)
            else:
                os.mkdir(backupdir)
        else:
            print("Niciun update momentan!")

try:
    if os.path.exists('system-state.log'):
        filetocheck = os.path.basename('scripts/system-state.log')
except:
    print("Fisierul pentru backup nu a fost gasit!")

check_for_modifications(filetocheck)


