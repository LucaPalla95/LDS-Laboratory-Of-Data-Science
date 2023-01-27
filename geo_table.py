                            #########################
                              ## GEOGRAPHY TABLE ##
                            #########################
   
import ProjectLibrary as prj
import csv
import re

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# colum_needed: colonne presente nel csv o non di cui ho bisogno per creare geo_table
# csvwriter.writerow(column_needed): vado a scrivere l'header del mio csv
# col_pos: mi recupero la posizione delle colonne necessarie dal csv letto
#------------------------------------------------

with open('geography_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    with open('answerdatacorrect.csv', 'r') as rf:
        header = rf.readline().strip().split(',')
        column_needed = ['GeoId', 'Region', 'CountryCode', 'Continent']
        csvwriter.writerow(column_needed)
        col_pos = prj.column_position(header, column_needed)

#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# count: sarà la nostra chiave primaria incrementale univoca
# lines: racchiude tutte le line del mio csv ad esclusione della prima che è già stata letta
# no_duplicates: sarà l'insieme delle tuple di valori che rappresentano una combinazione unica
# for pos, el... : in questo ciclo for si vanno a prendere i valori di cui ho bisogno dal csv in lettura
#                  sfruttando l'indice delle colonne in col_pos. Inoltre viene creata 'continent' sfruttando pycountry
# alla fine di crea la nostra row, si guarda se già non è stata scritta e nel caso si aumenta il count di uno e
# si va ad assegnare il suo id unico creando la variabile new_row.
#-----------------------------------------------

        count = 0
        lines = rf.read().splitlines()
        no_duplicates = set()
        for line in lines:
            for pos, el in enumerate(re.split(r',(?=\w|")', line)):
                if pos == col_pos[0]: #Region
                    region = el
                elif pos == col_pos[1]: #CountryCode
                    country_code, continent = prj.country_to_continent(el)
                else:
                    continue
            row = (region, country_code, continent)
            if row not in no_duplicates:
                no_duplicates.add(row)
                count+=1 # se non doppione vado ad aggiornare indice
                new_row = (count, region, country_code, continent) #riga da scrivere
                csvwriter.writerow(new_row)
