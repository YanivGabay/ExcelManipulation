def contains_hebrew(text):
    # Hebrew Unicode block ranges from 0590 to 05FF
    return any("\u0590" <= c <= "\u05FF" for c in text)

def reverse_hebrew_strings(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x[::-1] if isinstance(x, str) and contains_hebrew(x) else x)
    return df

def concatenate_columns(df, column1, column2, new_column_name):
    
    if column1 in df.columns and column2 in df.columns:
        df[new_column_name] = df[column1].astype(str) + ' ' + df[column2].astype(str)
    else:
        print(f"One or both columns: '{column1}' and '{column2}' do not exist in the DataFrame.")
    
    return df