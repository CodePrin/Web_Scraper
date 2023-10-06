'''Import packages'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
from io import BytesIO
import os


class Scrapping:
    
    '''Function to extract project data from World Bank Evaluation And Ratings  website (https://ieg.worldbankgroup.org/data).'''
    def world_bank_evaluation_and_ratings():

        # Setup chrome driver.
        driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))

        # Getting the webpage of mentioned url.
        url = "https://ieg.worldbankgroup.org/data"
        driver.get(url)  # A chrome windows will open with the particular url. 
        WebDriverWait(driver, 20)  # To make the windows wait for 20sec.

        parent_handle = driver.current_window_handle  # Make the first opened windows as a parent handle.

        driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div/section/div/section[1]/div/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[3]/h4/a").click()  # To find and click the 'View Dashboard' button of 'WB Project Ratings and Lessons' present on the webpage.

        all_handles = driver.window_handles  # Stored all the handles that are currently opened.
        
        for handle in all_handles:
            if handle != parent_handle:
                driver.switch_to.window(handle)
                download_tag = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div/section/div/section/div/div/div/div/div/div/div/p[3]/a")

        download_url = download_tag.get_attribute("href")  # To get the 'href' attribute from the download tag of the element.
        response = requests.get(download_url)  # To get the url data to be donloaded.

        if response.status_code == 200:
            file_content = response.content
        # <Response [200]> means that it collected the data.
            
        content = BytesIO(file_content)  # For converting data into bytes as assumed by me.
        data_table = pd.read_excel(content)

        driver.quit()  # Used to close the current working chrome handlers opened having webdriver session remaining opened.
        return data_table


    '''Function to extract tender data from china bidding website (https://www.chinabidding.com/en)'''
    def china_bidding_com():

        # Setup chrome driver.
        driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))

        url = "https://www.chinabidding.com/en"
        driver.get(url)  # A chrome windows will open with the particular url. 

        # To make the chrome windows wait for 30sec.
        wait = WebDriverWait(driver, 60)

        driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[3]/div/div[1]/div[1]/div/div/span[2]/a").click()
        wait.until(EC.number_of_windows_to_be(2))

        all_handles = driver.window_handles  # Stored all the handles that are currently opened.
        new_handle = all_handles[-1]
        driver.switch_to.window(new_handle)

        project_title = []
        content = []
        date = []
        page_number = 1

        while page_number != 430000:

            if page_number != 1:
                driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/div[4]/div/div/ul/form/li[10]/a").click()
                wait = WebDriverWait(driver, 60)

            page_number += 1

            # Extract the Title from the elements.
            title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-title-text")))
            extracted_title = [element.text for element in title_elements]
            project_title += extracted_title

            # Extract the Content from the elements
            content_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-content")))
            extracted_content = [element.text for element in content_elements]
            content += extracted_content

            # Extract the Date from the elements.
            date_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "item-title-data")))
            extracted_date = [element.text for element in date_elements]
            date += extracted_date

        driver.quit()
        return project_title, content, date


    '''Function to extract tender data from china bidding mofcom (http://en.chinabidding.mofcom.gov.cn/)'''
    def china_bidding_mofcom():

        # Setup chrome driver.
        driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))

        url = "http://en.chinabidding.mofcom.gov.cn/"
        driver.get(url)  # A chrome windows will open with the particular url.
        wait = WebDriverWait(driver, 60)  # To make the chrome windows wait for 60sec.

        driver.find_element(By.XPATH, "/html/body/section/div/div[3]/div[1]/div/p/a").click()
        wait.until(EC.number_of_windows_to_be(2))

        all_handles = driver.window_handles  # Stored all the handles that are currently opened.
        new_handle = all_handles[-1]
        driver.switch_to.window(new_handle)
            
        overview = []
        bidding_no = []
        project_name = []
        date = []
        page_number = 1

        while page_number != 313000:

            if page_number != 1:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div/div[2]/div[3]/div[2]/div/a[10]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)  # Scroll to the element
                driver.execute_script("arguments[0].click();", next_button)
                
            page_number += 1

            # Extract the Title from the elements.
            title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "w645")))
            extracted_title = [element.text for element in title_elements]
            overview += extracted_title

            # Extract the Content from the elements
            content_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-sum")))
            extracted_content = [element.text for element in content_elements]

            bidding_numbers = [element.split(',', 1)[0].strip() for element in extracted_content]
            bidding_no += bidding_numbers     
            
            project_names_list = [element.split(',', 1)[1].strip() for element in extracted_content]
            project_name += project_names_list

            # Extract the Date from the elements.
            date_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "result-time")))
            extracted_date = [element.text for element in date_elements]
            date_part_only = [element.split(':', 1)[1].strip() for element in extracted_date]
            date += date_part_only
        
        driver.quit()
        return overview, bidding_no, project_name, date


    '''Function to extract tender data from cpppc_org_data (https://www.cpppc.org/en/PPPyd.jhtml)'''
    def cpppc_org_data():

        # Setup chrome driver.
        driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))

        url = "https://www.cpppc.org/en/PPPyd.jhtml"
        driver.get(url)  # A chrome windows will open with the particular url.

        driver.implicitly_wait(100)  # Wait up to given seconds for elements to appear.

        # To make the chrome windows wait for 100sec.
        wait = WebDriverWait(driver, 100)

        title = []
        date = []

        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div/a").click()  # Clicked on the "View More" tab.
        wait = WebDriverWait(driver, 60)

        # Extract the Title from the elements.
        title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "second-list-text")))
        extracted_title = [element.text for element in title_elements]
        title += extracted_title

        # Extract the Date from the elements.
        date_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "second-list-date")))
        extracted_date = [element.text for element in date_elements]
        date += extracted_date

        driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div/div[3]/div/a").click()  # Clicked on the "Demonstration Projects" tab.

        all_handles = driver.window_handles  # Stored all the handles that are currently opened.
        new_handle = all_handles[-1]
        driver.switch_to.window(new_handle)

        # Extract the Title from the elements.
        title_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "second-list-text")))
        extracted_title = [element.text for element in title_elements]
        title += extracted_title

        # Extract the Date from the elements.
        date_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "second-list-date")))
        extracted_date = [element.text for element in date_elements]
        date += extracted_date    
        
        driver.quit()
        return title, date





