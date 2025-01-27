import json
import pandas as pd
import os
import glob
import sys
from dotenv import load_dotenv 

# column names one function
def get_column_names(schemas, ds_name, sorting_key='column_position'):
    column_details = schemas[ds_name]
    columns = sorted(column_details, key=lambda col: col[sorting_key])
    return [col['column_name'] for col in columns]

def read_csv(file, schemas):
    file_path_list = file.split('/')
    ds_name = file_path_list[-2]
    column_names = get_column_names(schemas, ds_name)
    df = pd.read_csv(file,names=column_names)
    return df
    
def to_json(df, tgt_base_dir, ds_name, file_name):
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    os.makedirs(f'{tgt_base_dir}/{ds_name}',exist_ok=True)
    df.to_json(
        json_file_path, 
        orient='records',
        lines=True
    )

def file_converter(src_base_dir, tgt_base_dir, ds_name):
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*')
        
    for file in files:
        df = read_csv(file, schemas)
        file_name = file.split('/')[-1]
        to_json(df, tgt_base_dir, ds_name, file_name)
        
def process_files(ds_names=None):
    load_dotenv("file_formater.env")
    src_base_dir = os.environ.get('SRC_BASE_DIR')
    tgt_base_dir = os.environ.get('TGT_BASE_DIR')
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        print(f"processing {ds_name}")
        file_converter(src_base_dir, tgt_base_dir, ds_name)
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        ds_names =json.loads(sys.argv[1])
        process_files(ds_names)
    else:
        process_files()