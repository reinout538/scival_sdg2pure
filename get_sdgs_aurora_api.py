import os, sys
import requests
import json
import csv
import xlrd
import math
import datetime
import pandas as pd
from IPython.display import clear_output

file_dir = sys.path[0]
uuid_file = 'uuid_file.xlsx'
url_crud = "https://research.vu.nl/ws/api/"

key_pure_write = input('api key')

index = {"1" : "/dk/atira/pure/sustainabledevelopmentgoals/no_poverty","10" : "/dk/atira/pure/sustainabledevelopmentgoals/reduced_inequalities","11" : "/dk/atira/pure/sustainabledevelopmentgoals/sustainable_cities_and_communities","12" : "/dk/atira/pure/sustainabledevelopmentgoals/responsible_consumption_and_production","13" : "/dk/atira/pure/sustainabledevelopmentgoals/climate_action","14" : "/dk/atira/pure/sustainabledevelopmentgoals/life_below_water","15" : "/dk/atira/pure/sustainabledevelopmentgoals/life_on_land","16" : "/dk/atira/pure/sustainabledevelopmentgoals/peace_justice_and_strong_institutions","17" : "/dk/atira/pure/sustainabledevelopmentgoals/partnerships","2" : "/dk/atira/pure/sustainabledevelopmentgoals/zero_hunger","3" : "/dk/atira/pure/sustainabledevelopmentgoals/good_health_and_well_being","4" : "/dk/atira/pure/sustainabledevelopmentgoals/quality_education","5" : "/dk/atira/pure/sustainabledevelopmentgoals/gender_equality","6" : "/dk/atira/pure/sustainabledevelopmentgoals/clean_water_and_sanitation","7" : "/dk/atira/pure/sustainabledevelopmentgoals/affordable_and_clean_energy","8" : "/dk/atira/pure/sustainabledevelopmentgoals/decent_work_and_economic_growth","9" : "/dk/atira/pure/sustainabledevelopmentgoals/industry_innovation_and_infrastructure"}
publ_uuids = []

#sdg_api_els_multi = 'https://aurora-sdg.labs.vu.nl/classifier/classify/elsevier-sdg-multi?text='
#sdg_api_aur_multi = 'https://aurora-sdg.labs.vu.nl/classifier/classify/aurora-sdg-multi?text='
sdg_api_aur_single = 'https://aurora-sdg.labs.vu.nl/classifier/classify/aurora-sdg?text='

def get_sdg_status(abstract):

    response_sdg_aur_single = requests.get(sdg_api_aur_single+abstract, headers={'Accept': 'application/json'})

    if response_sdg_aur_single.ok:
        get_sdg = 'success'
    else:
        get_sdg = 'failed'

    return response_sdg_aur_single, get_sdg

#main

# read uuid-xlsx
wb = xlrd.open_workbook(os.path.join(file_dir, uuid_file))
sheet = wb.sheet_by_index(0)

for i in range(sheet.nrows)[1:]:
    uuid = str(sheet.cell_value(i, 0))
    publ_uuids.append (uuid)

#publ_uuids = ['95920259-7293-4881-a6d3-7cdc63761aca']

df_log = pd.DataFrame(columns=['uuid','get_pub_pure','get_sdg'])
df_sdg_values = pd.DataFrame(columns=['pure_id', 'sdg_value'])
        
for i, publ_uuid in enumerate(publ_uuids):

    print ('processing:', publ_uuid,' - ',i+1, 'from', len(publ_uuids))
    #clear_output('wait')

    #get pure record log directory
    response_get_pub = requests.get(url_crud+'research-outputs/'+publ_uuid, headers={'Accept': 'application/json', 'Content-Type': 'application/json'},params={'apiKey':key_pure_write})
    
    if response_get_pub.ok:
        json_pure_pub = response_get_pub.json()
        get_pub_log = 'success'
        if 'abstract' in json_pure_pub:
            abstract = json_pure_pub['abstract']['en_GB']
            
            response_sdg_aur_single = get_sdg_status(abstract)[0]
            if get_sdg_status(abstract)[1] == 'success':
                for prediction in (response_sdg_aur_single.json()['predictions']):
                
                    if prediction['prediction'] >= .99:
                        sdg_add = prediction['sdg']['id']
                        sdg_no = sdg_add[sdg_add.find('sdg/')+4:]
                        sdg_class = index[sdg_no]
                        print (sdg_class)
                        df_sdg_values.loc[len(df_sdg_values.index)] = [json_pure_pub['pureId'], sdg_class]
            else:
                print ('failed')
    else:
        get_pub_log = 'failed'

    df_log.loc[len(df_log.index)] = [publ_uuid, get_pub_log, get_sdg_status(abstract)[1]]
    
df_sdg_values.to_csv(os.path.join(file_dir, "sdg_values_log.csv"), encoding='utf-8', index = False)
df_log.to_csv(os.path.join(file_dir, "sdg_log.csv"), encoding='utf-8', index = False)
