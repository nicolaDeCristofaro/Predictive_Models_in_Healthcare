import pandas as pd

mimic3_path = '../../mimic-iii-clinical-database-1.4/'

def dataframe_from_csv(path, header=0, index_col=0):
    return pd.read_csv(path, header=header, index_col=index_col)

# read patients table
def read_patients_table(mimic3_path):
    pats = dataframe_from_csv(mimic3_path + 'PATIENTS.csv')
    pats = pats[['SUBJECT_ID', 'GENDER', 'DOB', 'DOD']]
    pats.DOB = pd.to_datetime(pats.DOB)
    pats.DOD = pd.to_datetime(pats.DOD)
    return pats

# read admissions table
def read_admissions_table(mimic3_path):
    admits = dataframe_from_csv(mimic3_path + 'ADMISSIONS.csv')
    admits = admits[['SUBJECT_ID', 'HADM_ID', 'ADMITTIME', 'DISCHTIME', 'DEATHTIME', 'ADMISSION_TYPE', 'ETHNICITY', 'DIAGNOSIS']]
    admits.ADMITTIME = pd.to_datetime(admits.ADMITTIME)
    admits.DISCHTIME = pd.to_datetime(admits.DISCHTIME)
    admits.DEATHTIME = pd.to_datetime(admits.DEATHTIME)
    return admits

# Partiamo leggendo le 3 tabelle principali linkate tra loro ignorando per ciascuna di loro alcuni attributi che non rilvenza ai fini dei nostri obiettivi
# Ad esempio nella tabella PATIENTS l'attributo DOD merged together DOD_HOSP and DOD_SSN, giving priority to DOD_HOSP if both were recorded quindi non c'è bisogno di avere valori anche per gli ultimi due attributi citati
# Ancora in ADMISSIONS table non sono necessari gli attributi RELIGION, LANGUAGE, MARITAL STATUS ecc.
patients = read_patients_table(mimic3_path)
admits = read_admissions_table(mimic3_path)

def merge_on_subject(table1, table2):
    return table1.merge(table2, how='inner', left_on=['SUBJECT_ID'], right_on=['SUBJECT_ID'])

patients_admits = merge_on_subject(patients, admits)

print(patients_admits.head())