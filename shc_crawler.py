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
