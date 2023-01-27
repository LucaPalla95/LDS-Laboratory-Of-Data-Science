##########################
## ANSWER TABLE ##
##########################

import ProjectLibrary as prj
import csv

FilePath = "answerdatacorrect.csv"
FilePathOrg = 'organization_table.csv'
FilePathDate = 'date_table.csv'
FilePathSub = 'subject_table.csv'

#------------------------------------------------
# FASE PRELIMINARE
# wf: file da scrivere
# rf: file da leggere
# rows: lista di dizionari che contengono colonne e valori di ogni singola riga di answerdatacorrect
# colum_needed: colonne presente nel csv e non di cui ho bisogno per creare ans_table
# csvwriter.writerow(column_needed): vado a scrivere l'header del mio csv
#------------------------------------------------

with open('answer_table.csv', 'w', newline='') as wf:
    csvwriter = csv.writer(wf)
    rows = prj.csv_dict_reader(FilePath)
    column_needed = ['QuestionId', 'UserId', 'AnswerId', 'AnswerValue', 'CorrectAnswer', 'DateOfBirth', 'DateAnswered',
                         'Confidence', 'GroupId', 'QuizId', 'SchemeOfWorkId', 'SubjectId']
    csvwriter.writerow(['AnswerId', 'QuestionId', 'UserId', 'OrganizationId', 'DateId', 'SubjectId',
                         'AnswerValue', 'CorrectAnswer', 'IsCorrect', 'Confidence'])
        
#-----------------------------------------------
# FASE DI COSTRUZIONE DEL CSV FILE
# o_rows/d_rows/s_rows: Apro i 3 csv di organization_table, date_table e subject_table come lista di dizionari utilizzando la funzione csv_dict_reader
# implementata nel file py ProjectLibrary. Praticamente ogni riga del csv viene immagazzinata dentro una lista sotto forma di dizionario
# con chiave il nome della colonna e come valore il valore dell'attributo in tale riga.

# reverse_dict_org/reverse_dict_date/reverse_dict_sub sono 3 dizionari reversi (scambio chiave con valore) che sono stati
# creati per rendere il lookup dei valori molto più veloce (creazione tabella circa 10 secondi). La chiave per reverse_dict_org è data dalla
# concatenzaione con underscore degli attributi GroupId, QuizId e SchemeOfWorkId. La chiave per reverse_dict_date è data da date
# mentre per reverse_dict_subject è data da solo la parte numerica di description (es. [3, 101, 342, 1650])

# Una volta costruiti tali dizionari si va a scorrere ogni linea di rows e se i dati a noi necessari sono già disponibili
# si va a creare una variabile che li contenga, altrimnenti si vanno a recuperare nei dizionari reversi delle tabelle create o si usano
# funzioni specifiche (i.e. is_correct).
# Alla fine, quando tutti i dati della singola riga della fact table sono stati recupearti si vanno a scrivere nel file con csvwriter
#-----------------------------------------------

    o_rows = prj.csv_dict_reader(FilePathOrg)
        
    reverse_dict_org = {}
    for row in o_rows:
        val = list(row.values())
        key = '{}_{}_{}'.format(val[1], val[2], val[3]) #GroupId, QuizId, SchemeOfWorkId
        reverse_dict_org[key] = eval(val[0])            #OrganizationId
            
    d_rows = prj.csv_dict_reader(FilePathDate)
    reverse_dict_date = {}
    for row in d_rows:
        val = list(row.values())[0:2]
        key = val[1] #Date
        reverse_dict_date[key] = val[0] #DateId
                
    s_rows = prj.csv_dict_reader(FilePathSub)
    reverse_dict_sub = {}
    for row in s_rows:
        val = list(row.values())[0:2]
        x = val[1].find('],')
        key = tuple(sorted(eval(val[1][1:x+1]))) # escludo parte non numerica. eval necessario per il sorted (altrimenti ordino uno stringa e non una lista)
                                                #  tuple necessario per rendere la key immutabile
        reverse_dict_sub[key] = val[0] #SubjectId
                
    for line in rows:
        answer_id = line['AnswerId']
        question_id = line['QuestionId']
        user_id = line['UserId']
                        
        group_id = line['GroupId']
        quiz_id = line['QuizId']
        schemeofwork_id = line['SchemeOfWorkId'].replace('.0', '')
        union = '{}_{}_{}'.format(group_id, quiz_id, schemeofwork_id)
        organization_id = reverse_dict_org[union]
        
        dateanswered = line['DateAnswered'][0:10] #escludo orario
        date_id = reverse_dict_date[dateanswered]
                        
        sub_id = tuple(eval(line['SubjectId']))
        subject_id = reverse_dict_sub[sub_id]
                        
        answer_value = line['AnswerValue']
        correct_value = line['CorrectAnswer']
        is_correct = prj.IsCorrect(answer_value, correct_value) # ritorna 1 se vero, 0 altrimenti
        confidence = line['Confidence'].replace('.0', '')
                        
        row = (answer_id, question_id, user_id, organization_id, date_id, subject_id, answer_value,
               correct_value, is_correct, confidence)
                        
        csvwriter.writerow(row)
