import pandas as pd
import sys
import time

# Data Path
ADSERVER_FILE_PATH, ADOBE_FILE_PATH = sys.argv[1:]

# Read data into pandas
df_adserver = pd.read_excel(ADSERVER_FILE_PATH, header=15, sheet_name=0)
df_adobe = pd.read_excel(ADOBE_FILE_PATH, header=12, sheet_name=1)

# Clean Match column by removing AID
df_adobe['Unnamed: 0'] = df_adobe['Unnamed: 0'].apply(lambda x: x.upper().replace('AID',''))

# Rename Columns
df_adobe.columns  = ['MatchKey','Unique Visitors','Bounce Rate','Leads','Remove']

# Remove last row
df_adserver = df_adserver.iloc[:-1,:]

# Merge data
df = pd.merge(df_adserver, 
				df_adobe, 
				left_on='OLA / PSOC Link',
				right_on='MatchKey',
				how='left'
				)

# Remove NaN rows		
df = df[~df['MatchKey'].isna()]

# Remove column MatchKey
df = df.drop(['MatchKey',
			  'Activity ID',
			  'Creative ID',
			  'Campaign ID',
			  'Placement ID',
			  'Remove'], axis=1)

# Organize columns
df = df[['OLA / PSOC Link',
		'Campaign',
		'Site (CM360)',
		'Placement',
		'Impressions',
		'Clicks',
		'Unique Visitors', 
		'Bounce Rate', 
		'Leads'
		]]

# Export data
fname = f'output_{int(time.time())}.xlsx'
df.to_excel(f'webapp/static/output/{fname}', index=False)
sys.stdout.write(fname)