from scrapper import Scrapping as scrap
import pandas as pd
import os


# '''Current file location'''
# current_file_path = os.path.join(os.path.dirname(__file__))
# os.chdir(current_file_path)
# # print(current_file_path)


'''Directory where scrapped data will be saved.'''
os.mkdir('./Scrapped_Data')


"""To extract data from World Bank Evaluation And Ratings."""
df_wbear = scrap.world_bank_evaluation_and_ratings()
df_wbear.to_excel('./Scrapped_Data/WorldBankEvaluationAndRatings_Dataset.xlsx')  # Saving dataframe as excel file in Scrapped_Data folder. 


"""To extract data from China Bidding."""
project_title, content, date = scrap.china_bidding_com()
com_china_bidding = {
    "Project Title": project_title,
    "Content": content,
    "Date & Time": date
}
df_china_bidding_com = pd.DataFrame(com_china_bidding)
df_china_bidding_com.to_excel('./Scrapped_Data/ChinaBiddingCom_Dataset.xlsx')    # Saving dataframe as excel file in Scrapped_Data folder. The 'r' character is placed before the path to remove unicode error.


"""To extract data from China Bidding Mofcom"""
overview, bidding_no, project_name, date = scrap.china_bidding_mofcom()
mofcom_china_bidding = {
    "Overview": overview,
    "Bidding Number": bidding_no,
    "Project Title": project_name,
    "Date": date
}
df_china_bidding_mofcom = pd.DataFrame(mofcom_china_bidding)
df_china_bidding_mofcom.to_excel('./Scrapped_Data/ChinaBiddingMofcom_Dataset.xlsx')


"""To extract data from CPPPC organisation."""
title, date = scrap.cpppc_org_data()
cpppc_org = {
    "Title": title,
    "Date": date
}
df_cpppc_org = pd.DataFrame(cpppc_org)
df_cpppc_org.to_excel('./Scrapped_Data/CPPPC_Dataset.xlsx')

