# scival_sdg2pure
create Pure SDG-keyword import file from SciVal export

step 1: make SciVal export: https://github.com/reinout538/scival_sdg2pure/blob/main/Manual_export_publication_SDGs_SciVal.docx to create a csv-export from SciVal containing EID, DOI and SDG-label

step 2: rename Scival csv-file to 'scival_export.csv' and place it in the same folder as the python script

step 3: run python script: https://github.com/reinout538/scival_sdg2pure/blob/main/sdg2pure_SciVal_export.py The script will check via the Pure-API if the EID is listed in Pure and - if so - will add the Pure-ID + SDG-uri to the import file for Pure

step 4: open the generated import2pure.csv and split the values to columns - copy the data to the dedicated import file: https://github.com/reinout538/scival_sdg2pure/blob/main/bulk-change-keywords-on-content-sample.xls

step 5: import the Excel file via Administrator > Jobs > Bulk-change keywords on content

settings: content type = ResearchOutput / logical name = sustainabledevelopmentgoals
