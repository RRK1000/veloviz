import os
import csv
import zipfile
import pandas as pd


#iterate through file names starting with 'bike-ridership'
# for file in os.listdir():
#     if file.startswith('bikeshare-ridership') and file.endswith('.zip'):
#         zip_file = file
#         # unzip the file
#         with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#             name = './'+zip_file.split('.')[0]
#             print(name)
#             zip_ref.extractall(name)

for i,file in enumerate(os.listdir()):
    if file.startswith('bikeshare-ridership') and os.path.isdir(file):
        dir_name = file
        # concat rowwise the csvs in the folder
        new_csv = dir_name + '.csv'
        csv_files = sorted([f for f in os.listdir(dir_name) if f.endswith('.csv')])
        
        df_list = []
        
        for j, csv_file in enumerate(csv_files):
            file_path = os.path.join(dir_name, csv_file)
            
            if j == 0 and i == 0:
                df = pd.read_csv(file_path, on_bad_lines='skip',encoding='cp1252')
            else:
                df = pd.read_csv(file_path, header=None, on_bad_lines='skip',encoding='cp1252')
            
            df_list.append(df)
        
        combined_df = pd.concat(df_list, ignore_index=True)
    
        combined_df.to_csv(new_csv, index=False, header=(i == 0))
        print('done')
        