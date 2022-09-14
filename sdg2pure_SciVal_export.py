#Process SciVal-export of SDGs labels (csv with DOI, EID, SDGs) to create import-file for Pure (bulk import keywords)

import os, sys
import csv
import requests
import math
from IPython.display import clear_output

file_dir = sys.path[0]
scival_file = 'scival_export.csv'
import2pure_file = 'import2pure.csv'

pure_root = input('enter root url of pure instance (eg "research.vu.nl"):')
api_pure_pub = f"https://{pure_root}/ws/api/523/research-outputs/"
key_pure = input('enter api-key:')

index = {"SDG 1" : "/dk/atira/pure/sustainabledevelopmentgoals/no_poverty","SDG 10" : "/dk/atira/pure/sustainabledevelopmentgoals/reduced_inequalities","SDG 11" : "/dk/atira/pure/sustainabledevelopmentgoals/sustainable_cities_and_communities","SDG 12" : "/dk/atira/pure/sustainabledevelopmentgoals/responsible_consumption_and_production","SDG 13" : "/dk/atira/pure/sustainabledevelopmentgoals/climate_action","SDG 14" : "/dk/atira/pure/sustainabledevelopmentgoals/life_below_water","SDG 15" : "/dk/atira/pure/sustainabledevelopmentgoals/life_on_land","SDG 16" : "/dk/atira/pure/sustainabledevelopmentgoals/peace_justice_and_strong_institutions","SDG 17" : "/dk/atira/pure/sustainabledevelopmentgoals/partnerships","SDG 2" : "/dk/atira/pure/sustainabledevelopmentgoals/zero_hunger","SDG 3" : "/dk/atira/pure/sustainabledevelopmentgoals/good_health_and_well_being","SDG 4" : "/dk/atira/pure/sustainabledevelopmentgoals/quality_education","SDG 5" : "/dk/atira/pure/sustainabledevelopmentgoals/gender_equality","SDG 6" : "/dk/atira/pure/sustainabledevelopmentgoals/clean_water_and_sanitation","SDG 7" : "/dk/atira/pure/sustainabledevelopmentgoals/affordable_and_clean_energy","SDG 8" : "/dk/atira/pure/sustainabledevelopmentgoals/decent_work_and_economic_growth","SDG 9" : "/dk/atira/pure/sustainabledevelopmentgoals/industry_innovation_and_infrastructure"}
eid2sdg_dict = {}
failed = []

#process SciVal csv-file
with open(os.path.join(file_dir,scival_file)) as sciv_file:
    csv_reader = csv.reader(sciv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        
        line_count += 1
        #if line_count == 100: break
        if len(row) >2 and '2-s2.0-' in row[1]:
            doi = row[0]
            eid = row [1]
            eid_clean = eid[eid.rfind('-')+1:].rstrip()
            
            #get SDGs - loop if more than one (pipe is present)
            if row[2] != '-':
                if '|' in row[2]:
                    sdg_list = row[2].split('|')
                    for sdg in sdg_list:
                        sdg_uri = index[sdg.strip()]
                        eid2sdg_dict[eid_clean] = sdg_uri
                        
                else:
                    sdg = row[2]
                    sdg_uri = index[sdg.strip()]
                    eid2sdg_dict[eid_clean] = sdg_uri


#check if EID in Pure and get PureID from Pure-API
with open (os.path.join(file_dir,import2pure_file), "w", newline='') as import2pure:
    wr_import2pure = csv.writer(import2pure, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE, lineterminator='\r\n')
    for n, eid in enumerate(eid2sdg_dict):
        clear_output ('wait')                
        print(f"pure check - record {n+1} of {len(eid2sdg_dict)} with SDG-label(s)")
                
        try:
            response = requests.get(api_pure_pub+eid+'?idsource=scopus', headers={'Accept': 'application/json'}, params={'apiKey':key_pure})

            if response.status_code != 404:
                json_record = response.json()
                wr_import2pure.writerow([json_record['pureId'],eid2sdg_dict[eid]])
        
        except:
            failed.append(eid)

print ('done')
if failed != []: print (f"failed api call for EID: {failed}")
