                            #########################
                               ## SUBJECT TABLE ##
                            #########################

import ProjectLibrary as prj                        
import csv
import re

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# colum_needed: colonne presente nel csv o non di cui ho bisogno per creare sub_table
# csvwriter.writerow(column_needed): vado a scrivere l'header del mio csv
# col_pos: mi recupero la posizione delle colonne necessarie dal csv letto
#------------------------------------------------

with open('subject_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    with open('answerdatacorrect.csv', 'r') as rf:
        header = rf.readline().strip().split(',')
        column_needed = ['SubjectId', 'Description']
        csvwriter.writerow(column_needed)
        col_pos = prj.column_position(header, column_needed)
        
#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# count: sarà la nostra chiave primaria incrementale univoca
# lines: racchiude tutte le line del mio csv ad esclusione della prima che è già stata letta
# meta_lines: si riferisce alle righe lette dal file sub_meta_table creato precedentemente con lo scopo di ordinare
#             in via crescente (per livello) le materie
# no_duplicates: sarà l'insieme dei valori unici dei nostri subjectid (i.e. [3,101,115,342]). Vado dunque prima a lavorare per cercare le combinazioni
#                uniche dei subjectid forniti dalla tabella principale. Questa ridurrà molto i tempi di calcolo.
# for pos, el... : in questo ciclo for si vanno a prendere i valori di cui ho bisogno dal csv in lettura
#                  sfruttando l'indice delle colonne in col_pos. Inoltre vado a fare un match tra i valori dati nel subjectid
#                  della tabella principali (lista di id) con i singoli id della materie nel csv dei metadati. Iterando
#                  vado così a recuperare sia la descrizione testuale delle materie che a riordinare in via crescente di livello gli id.
# alla fine si aumenta il count di uno e si va ad assegnare come id unico creando la variabile new_row.
#-----------------------------------------------
        
        with open('subject_meta_table.csv', 'r') as metadata:
            header_m = metadata.readline().strip().split(',')
            count = 0
            lines = rf.read().splitlines()
            meta_lines = metadata.read().splitlines()
            no_duplicates_id = set()
            for line in lines:
                for pos, el in enumerate(re.split(r',(?=\w|")', line)):
                    if pos == col_pos[0]: # SubjectId es. [3,101,115,342]
                        no_duplicates_id.add(el)
                    else:
                        continue

            for el in no_duplicates_id: # Lo scopo dei due cicli for successivi è di fare il match con la tabella dei metadati e 
                                        # recuperare le informazioni della descrizione mentre riordino per livello. Infatti nel set
                                        # dei non duplicati gli id delle materie non sono ordinati per livello
                subject_id = [] 
                description = []
                
                for meta_line in meta_lines:
                    m_line = meta_line.replace(', ', '; ') # per fare lo split correttamente
                    splitted_line = m_line.split(',')
                    if eval(splitted_line[0]) in set(eval(el.strip('"'))): # vedo se id materia è nel in el (set per fare ricerca più veloce)
                        subject_id.append(eval(splitted_line[0]))
                        description.append(splitted_line[1].replace(';', ',').strip('"')) #appendo descrizione testuale riportando ; = ,
                            
                
                count+=1
                new_row = (count, (subject_id, description)) #scrivo riga con id incrementale e tupla contenente id materia e descrizione testuale
                csvwriter.writerow(new_row)

