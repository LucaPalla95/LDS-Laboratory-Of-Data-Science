                             ######################
                                ## USER TABLE ##
                             ######################

import ProjectLibrary as prj
import csv
import re
from datetime import datetime as dt

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# colum_needed: colonne presente nel csv o non di cui ho bisogno per creare us_table
# csvwriter.writerow(column_needed): vado a scrivere l'header del mio csv
# col_pos: mi recupero la posizione delle colonne necessarie dal csv letto
#------------------------------------------------

with open('user_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    with open('answerdatacorrect.csv', 'r') as rf:
        header = rf.readline().strip().split(',')
        lines = rf.read().splitlines()
        column_needed = ['UserId', 'Gender', 'DateOfBirth', 'Region', 'CountryCode']
        csvwriter.writerow(['UserId', 'DateOfBirthId', 'GeoId', 'Gender'])
        col_pos = prj.column_position(header, column_needed)

#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# prima di tutto vado a leggere i csv di date e geography per poi mettere in liste i loro dati.
# lines: racchiude tutte le line del mio csv ad esclusione della prima che è già stata letta
# no_duplicates: sarà l'insieme dei valori unici dei nostri user_id (e successivamente le row, anche se evitabile).
# content: qui vado ad appendere liste che contengono gli attributi di interesse per creare user e per recuperare le chiavi esterne dalle altre tabelle
# for elem in content: questo ciclo for serve dunque per definire una volta per tutte gli elementi necessari neòòa tabella user
# alla fine si va a scrivere la nuova riga
#-----------------------------------------------
        
        with open('geography_table.csv', 'r') as gf:
            header_g = gf.readline().strip().split(',')
            geo_lines = gf.read().splitlines()
            
            with open('date_table.csv', 'r') as df:
                header_d = df.readline().strip().split(',')
                date_lines = df.read().splitlines()
                
                no_duplicates = set()
                content = [] #qui avrò userId, Gender, DateOfBirthId, Region, CountryCode
                for line in lines:
                    splittled_line = re.split(r',(?=\w|")', line)
                    waiting_list = [] # mi serve per creare la lista di valori da appendere a content
                    if splittled_line[1] not in no_duplicates: # mi è sufficiente controllare user_id
                        no_duplicates.add(splittled_line[1])
                        waiting_list.append(splittled_line[1]) #user_id
                        waiting_list.append(splittled_line[5]) #gender
                        waiting_list.append(splittled_line[6]) #dateofbirth
                        waiting_list.append(splittled_line[15]) #region
                        waiting_list.append(splittled_line[16]) #country_code
                        content.append(waiting_list)
                        
                for elem in content:
                    user_id = elem[0] 
                    gender = elem[1]
                    date = dt.strptime(elem[2], '%Y-%m-%d').date()
                    for d_line in date_lines:
                        split_d_line = d_line.split(',')
                        if date == dt.strptime(split_d_line[1], '%Y-%m-%d').date():
                            dateBid = split_d_line[0] #DateOfBirth
                            break
                    region = elem[3]
                    country_code = elem[4]
                    for g_line in geo_lines:
                        split_g_line = g_line.split(',')
                        if region == split_g_line[1] and country_code == split_g_line[2]:
                            geoid = split_g_line[0] #GeoId
                            break
                    
                    row = (user_id, dateBid, geoid, gender)
                    if row not in no_duplicates:
                        no_duplicates.add(row)
                        new_row = (user_id, dateBid, geoid, gender) #riga da scrivere
                        csvwriter.writerow(new_row)
                        