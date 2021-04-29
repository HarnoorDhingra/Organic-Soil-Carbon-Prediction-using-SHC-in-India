from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import os,glob,shutil
import pickle

profile = webdriver.FirefoxProfile()

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

try:
    dict_download = load_obj('to_download')
except (OSError, IOError) as e:
    my_dict = {}
    save_obj( my_dict , 'to_download')
BASE_DIR = os.getcwd()
# print(BASE_DIR)

profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', BASE_DIR)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/xml')
profile.set_preference("general.warnOnAboutConfig", False)
driver = webdriver.Firefox(profile)
driver.get("https://soilhealth.dac.gov.in/HealthCard/HealthCard/HealthCardPNew")

state_select = Select(driver.find_element_by_id('State_cd2'))
state_index = 8
state_select.options[state_index].click()
STATE_DIR  = os.path.join( BASE_DIR  ,state_select.options[state_index].text)
try:
    os.mkdir(STATE_DIR)
except FileExistsError as e:
    pass

district_select = Select(driver.find_element_by_id('Dist_cd2'))

for dist in district_select.options:
    if dist.text =='--SELECT--':
        continue

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Sub_dis2')))
        subdistrict_select = Select(driver.find_element_by_id('Sub_dis2'))
        time.sleep(3)
        dist.click()

        for sub_dist in subdistrict_select.options:
        if sub_dist.text == '--SELECT--':
            continue

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'village_cd2')))