# imports
from selenium import webdriver
from time import sleep
import pandas as pd

# parameters
url = 'https://br.linkedin.com/jobs/ci%C3%AAncia-de-dados-vagas?position=1&pageNum=0'

# xpaths
title = '/html/body/main/section/div[2]/section[1]/div[1]/div[1]/a/h2'
company = '/html/body/main/section/div[2]/section[1]/div[1]/div[1]/h3[1]/span[1]/a'
location = '/html/body/main/section/div[2]/section[1]/div[1]/div[1]/h3[1]/span[2]'
publication_ago = '/html/body/main/section/div[2]/section[1]/div[1]/div[1]/h3[2]/span'
description = '/html/body/main/section/div[2]/section[2]/div/section/div'
jobs_information = '/html/body/main/section/div[2]/section[2]/ul'

# functions and classes

# code
if __name__ == '__main__':
    # open google Chrome controled by Selenium
    driver = webdriver.Chrome()
    
    # open the research of data science jobs
    driver.get(url)
    driver.implicitly_wait(10)
    
    # get the results of jobs
    results = driver.find_elements_by_class_name('result-card')
    
    title_list = []
    company_list = []
    location_list = []
    publication_list = []
    description_list = []
    information_list = []
    
    # create a loop to collect all the results until the page stop showing jobs
    while True:
        # loop to collect the job informations
        for i in results[len(title_list):]:
            i.click()
            sleep(5)
            # collect the informations, and in case of error the program pass the item puting an empety item in the lists
            try:
                title_list.append(driver.find_element_by_xpath(title).text)
            except:
                title_list.append('')
                pass
            
            try:
                company_list.append(driver.find_element_by_xpath(company).text)
            except:
                company_list.append('')
                pass
            
            try:
                location_list.append(driver.find_element_by_xpath(location).text)
            except:
                location_list.append('')
                pass
            
            try:
                publication_list.append(driver.find_element_by_xpath(publication_ago).text)
            except:
                publication_list.append('')
                pass
            
            try:
                description_list.append(driver.find_element_by_xpath(description).text)
            except:
                description_list.append('')
                pass
            
            try:
                information_list.append(driver.find_element_by_xpath(jobs_information).text)
            except:
                information_list.append('')
                pass
        
        # collect the new result that is shown in page update
        results = driver.find_elements_by_class_name('result-card')
        
        # if to stop the while when the pages stop updating and showing new jobs
        if len(results) == len(title_list):
            break
    
    # verify and replace the elements which causes encode character errors
    for i in description_list:
        i = (i.encode('ascii', 'ignore')).decode("utf-8")
    
    # creat a dictionary with all the lists
    table_result = {'title':title_list, 'company':company_list, 'location':location_list, 'date':publication_list, 'description':description_list, 'jobs criteria':information_list}
    
    # converting the list into a DataFrame to save and excel file
    df = pd.DataFrame(table_result)
    df.to_excel('vagas_data_science.xlsx')
    
    # closes the Chrome page
    driver.quit()
