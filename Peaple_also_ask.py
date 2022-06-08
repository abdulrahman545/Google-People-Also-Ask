# Libraries

from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import glob
import sys

# ----------------------------------------------------------------------------------------------------

driver = webdriver.Chrome(ChromeDriverManager().install())

# open keywords.text
key_words = open("keywords.txt", "r")

# loop for every keyword
for key_word in key_words:

    # open google serch for the first keyword
    driver.get(f"https://www.google.com/search?q={key_word}")
    excel = str(f'{key_word}').strip()

    try:
        i= 1
        while i <= 60: # number of clicks on questions ( Depending on your device capabiblity !! )

            questions_n_expanded = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[@aria-expanded="false"]'))) 
            
            for t in questions_n_expanded:

                # click to expand every question clicked
                driver.execute_script("arguments[0].click();", t)
                questions_expanded = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[@aria-expanded="true"]'))) 
                i = i + 1         

            print(i)

        else:
            pass

        print(f"{excel} clicks - success")

    except:
        print(f"{excel} clicks - empty")
        continue

# ----------------------------------------------------------------------------------------------------

    # xpaths for ( questions, answers, link and link text) for the current keyword
    answers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div//div[1]/span[1]/span[1]'))) 
    questions = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[@aria-expanded]'))) 
    answer_link = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[1]')))  #try
    answer_link_text = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Wt5Tfe"]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[1]/h3'))) #try 
    for k in range(1,len(questions)+1):
        pass

    
    key_word_list = []
    questions_list = []
    answers_list = []
    sourclink_list = []
    linktext_list = []
    for a,b,c,d in zip(answers, questions, answer_link, answer_link_text):

        key_word_list.append(key_word.strip())
        answers_list.append(a.text)
        questions_list.append(b.text)
        sourclink_list.append(c.get_attribute('href'))
        linktext_list.append(d.text)

    df = pd.DataFrame({'Keyword': key_word_list, 'Question': questions_list, 'Answer': answers_list, 'sourcelink': sourclink_list, 'linktext': linktext_list})
     
    # save current keyword as a csv in draft folder
    df.to_csv(f'{sys.path[0]}\draft\{excel}.csv', index=False)

    print("\n**********************************")
    print(f'saving ({excel}) to csv - finished')
    print("**********************************")

driver.quit()


# ----------------------------------------------------------------------------------------------------

path = sys.path[0] + "/draft"

file_list = glob.glob(path + "/*.csv")

excl_list = []

for file in file_list:
	excl_list.append(pd.read_csv(file))

excl_merged = pd.DataFrame()

for excl_file in excl_list:
	
	excl_merged = excl_merged.append(
	excl_file, ignore_index=True)

# merge all csv files from draft folder then save then as one csv file in output folder
excl_merged.to_csv(f'{sys.path[0]}\output\people also ask.csv', index=False)


