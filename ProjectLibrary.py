                ##############################################
                     ### GROUP_21 LDS PROJRCT LIBRARY ###
                ##############################################

                            #######################
                            ## General Functions ##
                            #######################

# importing libraries
import csv
import pycountry_convert as pc

# Tale funzione mi ritorna la posizione delle colonne a me necessarie

def column_position(Header, ColumnNeeded):
    col_pos = []
    for pos, el in enumerate(Header):
        if el in ColumnNeeded:
            col_pos.append(pos)
    return col_pos

# Tale funzione mi legge i csv passati e mi riorna una lista di dizionari con ognuno all'interno come chiavi le colonne 
# e come valori il valore delle colonne

def csv_dict_reader(CsvPath):
    with open(CsvPath, 'r') as file:
        rows = []
        data = csv.DictReader(file, delimiter=',')
        for row in data:
            rows.append(row)
    return rows


                        ############################
                          ## Specific Functions ##
                        ############################

# Implementata in geography_table.csv
# Dato il country code mi ritorna il country code ed il continente. Uk è necessario mapparlo in Gb perchè
# essendo riservato non è utilizzabile da pycountry_convert

def country_to_continent(CountryCode):
    if CountryCode == 'uk':
        country_code = 'gb'
    else:
        country_code = CountryCode
    c = country_code.upper()
    continent = pc.country_alpha2_to_continent_code(c)
    return CountryCode, continent

# Implementata in date_table.csv
# Mi calcolo il quadrimestre

def quarter(DateTime):
    month = DateTime.month
    quarter = ((month-1)//3)+1
    return quarter

# Implementata in answer_table.csv
# Mi creo un valore binario che ritorna 1 se la risposta è corretta, 0 altrimenti

def IsCorrect(AnswerValue, CorrectValue):
    if AnswerValue == CorrectValue:
        is_correct = 1
    else:
        is_correct = 0
    return is_correct
