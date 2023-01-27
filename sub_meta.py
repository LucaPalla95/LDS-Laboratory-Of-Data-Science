                           ############################
                           ## SUBJECT METADATA TABLE ##
                           ############################
         
import ProjectLibrary as prj
import csv

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# colum_needed: colonne presente nel csv o non di cui ho bisogno per creare sub_meta_table
# csvwriter.writerow(column_needed): vado a scrivere l'header del mio csv
# col_pos: mi recupero la posizione delle colonne necessarie dal csv letto
#------------------------------------------------

with open('subject_meta_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    with open('subject_metadata.csv', 'r') as rf:
        header = rf.readline().strip().replace('ï»¿', '').split(',')
        column_needed = ['SubjectId', 'Name', 'ParentId', 'Level']
        csvwriter.writerow(column_needed)
        col_pos = prj.column_position(header, column_needed)

#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# count: sarà la nostra chiave primaria incrementale univoca
# lines: racchiude tutte le line del mio csv ad esclusione della prima che è già stata letta
# no_duplicates: sarà l'insieme delle tuple di valori che rappresentano una combinazione unica
# for pos, el... : in questo ciclo for si vanno a prendere i valori di cui ho bisogno dal csv in lettura
#                  sfruttando l'indice delle colonne in col_pos. Il replace per name va a sostituire nuovamente il ;
#                  con la virgola per ritornare alla "versione base". Il .0 viene invece rimosso per portare il valore da float
#                  a int (anche se sotto forma di stringa)
# alla fine di crea la nostra row, si guarda se già non è stata scritta. Dopo aver iterato su tutto il csv principale, si va 
# ad ordinare il set tenendo di conto della variabile livello. Alla fine si porta tutto a nuovo csv.
#-----------------------------------------------

        lines = rf.read().splitlines()
        no_duplicates = set()
        for line in lines:
            line = line.replace('"', '')
            line = line.replace(', ', '; ') # utile per fare lo split correttamente 
            
            for pos, el in enumerate(line.split(',')):
                if pos == col_pos[0]: # SubjectId
                    subject_id = el
                elif pos == col_pos[1]: # Name
                    name = el.replace('; ', ', ') #riporto la lista delle materie alla forma originale
                elif pos == col_pos[2]: # ParentId
                    parent_id = el.replace('.0', '')
                else: #Level
                    level = el
            row = (subject_id, name, parent_id, level)
            if row not in no_duplicates:
                no_duplicates.add(row)
        ordered_set = sorted(no_duplicates, key = lambda x: x[3]) #Ordino in via crescente in base al livello
        
        for elem in ordered_set:
            csvwriter.writerow(elem) #scrivo csv ordinato per livello. Sarà utile successivamente.

