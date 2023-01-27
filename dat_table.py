                             ####################
                               ## DATE TABLE ##
                             ####################

import csv
import ProjectLibrary as prj
import re
from datetime import datetime as dt

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# colum_needed: colonne presente nel csv o non di cui ho bisogno per creare dat_table
# csvwriter.writerow(columns): vado a scrivere l'header del mio csv
# col_pos: mi recupero la posizione delle colonne necessarie dal csv letto
#------------------------------------------------

with open('date_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    with open('answerdatacorrect.csv', 'r') as rf:
        header = rf.readline().strip().split(',')
        column_needed = ['DateId', 'DateOfBirth', 'DateAnswered', 'Date', 'Day', 'Month', 'Year', 'Quarter']
        csvwriter.writerow(['DateId', 'Date', 'Day', 'Month', 'Year', 'Quarter'])
        col_pos = prj.column_position(header, column_needed)
                
#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# count: sarà la nostra chiave primaria incrementale univoca
# lines: racchiude tutte le line del mio csv ad esclusione della prima che è già stata letta
# no_duplicates: sarà l'insieme delle tuple di valori che rappresentano una combinazione unica
# for pos, el... : in questo ciclo for si vanno a prendere i valori di cui ho bisogno dal csv in lettura
#                  sfruttando l'indice delle colonne in col_pos. Inoltre vengono creati day, month, year sfruttando datetime
#                  e quarter utilizzando invece una funzione scritta ee riportata in ProjectLibrary
# alla fine si crea la nostra row, si guarda se già non è stata scritta e nel caso si aumenta il count di uno e
# si va ad assegnare il suo id unico creando la variabile new_row. L'id a differenza delle altre volte deve tenere conto
# della differenza natura delle date. Per questo si va a distinguere con #-a le date di risposta e #-b quelle di nascita
#-----------------------------------------------

        count = 0
        lines = rf.read().splitlines()
        no_duplicates = set()
        for line in lines:
            for pos, el in enumerate(re.split(r',(?=\w|")', line)):
                if pos == col_pos[0]: #DateOfBirth
                    date_birth = dt.strptime(el, '%Y-%m-%d').date() #trasformo in date per sfruttarne i metodi
                    day = date_birth.day
                    month = date_birth.month
                    year = date_birth.year
                    quarter = prj.quarter(date_birth)
                else:
                    continue
            row = (date_birth, day, month, year, quarter) # riga preliminare da ontrollare se doppione
            if row not in no_duplicates:
                no_duplicates.add(row)
                count+=1 # se non doppione aggiungo al set e aggiorno indice incrementale
                index = '{}-b'.format(count) #indice specifico per DateOfBirth
                new_row = (index, date_birth, day, month, year, quarter) #riga da scrivere
                csvwriter.writerow(new_row)
        # speculare a quanto fatto sopra ma per DateAnswered
        count = 0
        for line in lines:
            for pos, el in enumerate(re.split(r',(?=\w|")', line)):
                if pos == col_pos[1]: # DateAnswered
                    date_ans = dt.strptime(el[0:10], '%Y-%m-%d').date() #escludo orario
                    day = date_ans.day
                    month = date_ans.month
                    year = date_ans.year
                    quarter = prj.quarter(date_ans)
                else:
                    continue
            row = (date_ans, day, month, year, quarter)
            if row not in no_duplicates:
                no_duplicates.add(row)
                count+=1
                index = '{}-a'.format(count) # indice specifico per DateAnswered
                new_row = (index, date_ans, day, month, year, quarter)
                csvwriter.writerow(new_row)

