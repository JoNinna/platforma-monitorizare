#! /bin/bash
# Script bash pentru monitorizarea resurselor sistemului.

logfile="system-state.log"
export timeinterval="${timeinterval:-5}"

if [[ ! -f "$logfile" ]]; then
    touch "$logfile"
fi

while true; do
    echo "$(date)" >> "$logfile"
    echo "CPU Info" >> "$logfile"
    cat /proc/cpuinfo >> "$logfile"

    echo "Memory Info" >> "$logfile"
    free -h >> "$logfile"

    echo "Numarul de procese in starea de Running este: " >> "$logfile"
    ps r | wc -l >> "$logfile"

    echo "Utilizarea diskului este: " >> "$logfile"
    df -h >> "$logfile"

    echo "Numele sistemului este: " >> "$logfile"
    hostname >> "$logfile"

    echo "Interfete, adrese IP si conexiuni deschise:" >> "$logfile"
    ip a  >> "$logfile"
    ss -tulpn >> "$logfile"

    echo "Fisierul cu informatiile de sistem urmeaza sa fie suprascris"
    sleep "$timeinterval"
    > "$logfile"
done