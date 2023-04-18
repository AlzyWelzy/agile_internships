import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

# Authentication with Google Sheets API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet and select the sheets
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mxMzHy-F2kFrjZVJyQojasCCBdKISp8Wft4_kDhKzNU/edit#gid=866894181"
sh = client.open_by_url(spreadsheet_url)
user_ids_sheet = sh.worksheet("Input User IDs")
rigorbuilder_raw_sheet = sh.worksheet("Input Rigorbuilder RAW")
teamwise_output_sheet = sh.worksheet("LeaderBoard TeamWise (Output)")
individual_output_sheet = sh.worksheet("LeaderBoard Individual (Output)")

# Read the input data into dataframes
user_ids = pd.DataFrame(user_ids_sheet.get_all_records())
rigorbuilder_raw = pd.DataFrame(rigorbuilder_raw_sheet.get_all_records())

# Drop empty rows in the user_ids sheet
user_ids = user_ids.dropna()

# Merge the user_ids and rigorbuilder_raw dataframes
merged_data = pd.merge(rigorbuilder_raw, user_ids, on="UID", how="left")

# Fill the missing names with 'NA'
merged_data["Name"] = merged_data["Name"].fillna("NA")

# Calculate the average statements and reasons for each team
teamwise_data = (
    merged_data.groupby("Team")
    .agg({"Statements": np.mean, "Reasons": np.mean})
    .reset_index()
)

# Sort the teams by their total score
teamwise_data["Total"] = teamwise_data["Statements"] + teamwise_data["Reasons"]
teamwise_data = teamwise_data.sort_values("Total", ascending=False).reset_index(
    drop=True
)

# Rank the teams and add the rank column to the teamwise_data dataframe
teamwise_data["Rank"] = teamwise_data.index + 1

# Format the teamwise_data dataframe and write it to the output sheet
teamwise_data_formatted = teamwise_data[["Rank", "Team", "Statements", "Reasons"]]
teamwise_data_formatted.columns = [
    "Team Rank",
    "Thinking Teams Leaderboard",
    "Average Statements",
    "Average Reasons",
]
set_with_dataframe(teamwise_output_sheet, teamwise_data_formatted, include_index=False)

# Calculate the total number of statements and reasons for each user
individual_data = (
    merged_data.groupby(["Name", "UID"])
    .agg({"Statements": sum, "Reasons": sum})
    .reset_index()
)

# Sort the users by their total score
individual_data["Total"] = individual_data["Statements"] + individual_data["Reasons"]
individual_data = individual_data.sort_values(
    ["Total", "Name", "UID"], ascending=[False, True, True]
).reset_index(drop=True)

# Rank the users and add the rank column to the individual_data dataframe
individual_data["Rank"] = individual_data.index + 1

# Format the individual_data dataframe and write it to the output sheet
individual_data_formatted = individual_data[
    ["Rank", "Name", "UID", "Statements", "Reasons"]
]
individual_data_formatted.columns = [
    "Rank",
    "Name",
    "UID",
    "No. of Statements",
    "No. of Reasons",
]
set_with_dataframe(
    individual_output_sheet, individual_data_formatted, include_index=False
)
