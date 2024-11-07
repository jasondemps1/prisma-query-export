import polars as pl

# Asset Name | Service | Account | Region Name | Last Modified | Deleted | Custom Tags | All Tags

def dict_to_str(d: dict, filter_chars=["'",'"']) -> str:
    completed = []
    for x in d:
        strs=[]
        if isinstance(x, dict):
            for k, val in x.items():
                strs.append(f"{k}={val}")
            completed.append('{' + f"{', '.join(strs)}" + '}')
        elif isinstance(x, list):
            completed.append(str(x))
        elif isinstance(x, str):
            completed.append(x)

    completed_formatted = str(completed)
    
    for c in filter_chars:
        completed_formatted = completed_formatted.replace(c,"")

    return str(completed_formatted)

def process(response_data: dict):
    processed = {
        "asset_name": [],
        "service": [],
        "account": [],
        "region_name": [],
        "deleted": [],
    }

    extra_columns = []

    for col in response_data['data']['dynamicColumns']:
        extra_columns.append(col)
        processed[col] = []

    for item in response_data['data']['items']:
        processed["asset_name"].append(item['name'])
        processed["service"].append(item['service'])
        processed["account"].append(item['accountName'])
        processed["region_name"].append(item['regionName'])
        processed["deleted"].append(item['deleted'])

        for col in extra_columns:
            if not item['dynamicData'].get(col):
                processed[col].append(None)
                continue
                
            processed[col].append(dict_to_str(item['dynamicData'][col]))

    # Create a DataFrame
    df = pl.DataFrame(processed)

    # Write DataFrame to CSV file
    df.write_csv("data.csv", separator=',')