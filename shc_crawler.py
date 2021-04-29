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
        village_select = Select(driver.find_element_by_id('village_cd2'))
        time.sleep(3)
        sub_dist.click()
        for each_village in village_select.options:
            try:
                if each_village.text == '--SELECT--':
                    continue
            except:
                dict_download[VILLAGE_DIR] = 0
                save_obj(dict_download, 'to_download')
            VILLAGE_DIR = os.path.join(STATE_DIR , dist.text , sub_dist.text , each_village.text)
            try :
                os.makedirs(VILLAGE_DIR)
            except FileExistsError as e :
                pass

            print( ' district is %s  sub_district is %s village is %s  ' %(dist.text , sub_dist.text , each_village.text)  )
            if VILLAGE_DIR in dict_download:
                if dict_download[VILLAGE_DIR] == 1:
                    continue
            time.sleep(2)
            each_village.click()
            driver.execute_script("SearchIngrid();")
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainTable')))
                table_of_records = driver.find_element(By.ID , 'MainTable')
                try :
                    rows = table_of_records.find_elements(By.TAG_NAME, "tr")
                    if len(rows) == 0:
                        print('no records in this village')
                        continue
                except  Exception as  e:
                    print('row does not exist ')
                    continue
            except Exception as  e:
                print('table not found  exception')
                continue

while(True):
    time.sleep(4)
    try :
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'MainTable')))
        table_of_records = driver.find_element(By.ID , 'MainTable')
        rows = table_of_records.find_elements(By.TAG_NAME, "tr")
        
        for row in rows:
            try :
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) <= 1:
                    continue
                print([ col.text for col in cols  ])
                try:
                    cols[9].click()
                    time.sleep(22)
                    try :
                        iframe = driver.find_elements_by_tag_name('iframe')[0]

                        driver.switch_to.frame(iframe)

                        butt = driver.find_element_by_id('ReportViewer1_ctl05_ctl04_ctl00_Menu')
                        options = butt.find_elements_by_tag_name('a')
                        driver.execute_script(options[7].get_attribute('onclick'))
                        num_of_tabs = len(driver.window_handles)


                        driver.switch_to.default_content()

                        time.sleep(2)
                        original_window_list = driver.window_handles
                        original_window = original_window_list[0]
                        for  handle in original_window_list:
                            if(handle != original_window):
                                driver.switch_to.window(handle)
                                driver.close()
                        driver.switch_to.window(original_window)



                    except Exception as e:
                        print('button exception')
                        print(e)
                except Exception as e:
                        print('print button exception')
                        print(e)
            except Exception as e :
                print('cols exception innner')
                print(e)
    except Exception as e:
        dict_download[VILLAGE_DIR] = 0
        save_obj(dict_download, 'to_download')
        print(' next button click row exception  ')
        print(e)
    try :
        driver.find_element_by_link_text('Next >').click()

    except :
        dict_download[VILLAGE_DIR] = 1
        save_obj(dict_download, 'to_download')
        for file in glob.glob("*.xml"):
            shutil.move(file,VILLAGE_DIR)
        break