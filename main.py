import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API credentials
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# Read input data from first input sheet
input_sheet1 = client.open('InputSheet1').worksheet('Sheet1')
input_data1 = input_sheet1.get_all_values()

# Read input data from second input sheet
input_sheet2 = client.open('InputSheet2').worksheet('Sheet1')
input_data2 = input_sheet2.get_all_values()

# Process input data to generate output data
# Replace this with your own data processing code

# Write output data to first output sheet
output_sheet1 = client.open('OutputSheet1').worksheet('Sheet1')
output_sheet1.clear()
output_sheet1.append_rows(output_data1)

# Write output data to second output sheet
output_sheet2 = client.open('OutputSheet2').worksheet('Sheet1')
output_sheet2.clear()
output_sheet2.append_rows(output_data2)
