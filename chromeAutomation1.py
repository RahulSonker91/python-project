from selenium import webdriver
import pandas as pd
from datetime import datetime
import numpy as np
# import openpyxl
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import numpy as np
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://nseoptionchain.ltpcalculator.com/")
driver.maximize_window()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME,"MuiInputBase-input"))
)
input_element_id = driver.find_element(By.CLASS_NAME,"MuiInputBase-input")
input_element_id.send_keys("rahul.sonker91@gmail.com")
input_element_pass = driver.find_element(By.CSS_SELECTOR,"input[type=\"password\"]")
input_element_pass.send_keys("WgkKhVjV")
input_element_tc = driver.find_element(By.CSS_SELECTOR,"input[type=\"checkbox\"]")
input_element_tc.click()
form_element_submit = driver.find_element(By.XPATH, "//button[text()='Login']")
form_element_submit.click()

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH,"//span[text()='DashBoard']"))
)
driver.get("https://nseoptionchain.ltpcalculator.com/detailed-optain-chain/idaddy-blast")

select_element = driver.find_element(By.CSS_SELECTOR, "div.navbar-middle > select.text-black")
select = Select(select_element)
options = select.options
# select.select_by_value("2024-12-02")
# selected_option = select.first_selected_option
# selected_option = select
for option in options:
    # print(option.get_attribute("value"))
    # Iterate through the options in the select element
    # select.select_by_value("2024-10-21")
    
   
    # for j  in range(select.options.index(selected_option),len(options)):
    for j  in range(len(options)):    
        print(j)
        # print(select.options.index(selected_option))
            
        # Select the current option
        select.select_by_index(j)
        
        # print(f"Selected option: {options[j].text}")
        print(f"{len(options)}")
        trade_date = options[j].text
        target_locator = (By.CSS_SELECTOR, "div[data-field=\"symbol\"] > div")

        # Wait for the page or content to update (adjust timeout as needed)
        try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(target_locator))
                print("Target element found!")
                

                # Rows  = driver.find_elements(By.CSS_SELECTOR, "div["data-rowindex"]")
                # loadedRows = len(Rows)
                # print(f"Total Rows Loaded - {loadedRows}")
                # print(Rows[0].get_attribute("data-rowindex"))
                # print(Rows[loadedRows].get_attribute("data-rowindex"))
                # time.sleep(10)
                # zoom_percentage = 24
                # driver.execute_script(f"document.body.style.zoom='{zoom_percentage}%'")
                # time.sleep(3)

                #############################################Temp########################################################################################################
                # Function to scrape data from visible rows
                def scrape_visible_rows():
                    # rows = driver.find_elements(By.CLASS_NAME, "MuiDataGrid-row")  # Locate rows dynamically

                    #improving logic
                    ####################################################################################################
                    rows = driver.find_elements(By.CSS_SELECTOR, "div[data-rowindex]")  # Locate rows dynamically
                    ####################################################################################################
                    data = []
                    row = set()
                    # print("Total Scraped rows "+str( len(scraped_set)))
                    # print(len(rows))
                    for row in rows:
                        # print(row.get_attribute("data-rowindex")
                        global start_index 
                        global max_index
                        if(int(row.get_attribute("data-rowindex")) > max_index):

                            row_index.append(int(row.get_attribute("data-rowindex")))
                            start_index = min(row_index)
                            max_index =max(row_index)
                            print(max_index)

                            try:
                                cells = row.find_elements(By.CLASS_NAME, "MuiDataGrid-cell")  # Locate cells dynamically
                                row_data = tuple(cell.text for cell in cells)  # Use tuple to make it hashable
                                # if row_data not in scraped_set:
                                #     scraped_set.add(row_data)
                                #     data.append(row_data)
                                # row.add(row_data)
                                print(row_data)
                                data.append(row_data)
                            except StaleElementReferenceException:
                                continue  # Skip stale rows
                    
                    all_data.extend(data)
                            
                    
                    # return data

                # # Function to scroll the grid incrementally and scrape visible data
                # def scroll_and_scrape(scraped_set):
                #     # Locate the vertical scrollbar container
                #     scrollbar = driver.find_element(By.CLASS_NAME, "MuiDataGrid-scrollbar--vertical")
                #     # all_data = []
                #     last_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                #     total_height = driver.execute_script("return arguments[0].scrollHeight;", scrollbar)

                #     while last_scroll_position < total_height:
                #         # Scrape data from visible rows
                #         all_data.extend(scrape_visible_rows(scraped_set))
                #         print('first batch scrapped under scroll & scrape - ' + str(len(all_data)))
                #         last_loaded_row = driver.find_element(By.CSS_SELECTOR,f'div[data-rowindex="{str(max_index)}"]') 
                        
                #         # print(last_loaded_row))

                #         # new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                #         # while len(driver.find_elements(By.CSS_SELECTOR, last_loaded_row)) != 0:
                        
                #         while (last_scroll_position < total_height and last_loaded_row.is_displayed()): 
                #             try:
                #                 all_data.extend(scrape_visible_rows(scraped_set))
                #                 print("scrolling")
                #                 # print(f"length = {len(driver.find_elements(By.CSS_SELECTOR, last_loaded_row))}")
                #                 # print(not driver.find_elements(By.CSS_SELECTOR, last_loaded_row))

                #                 # Scroll down incrementally
                #                 driver.execute_script("arguments[0].scrollTop += 190;", scrollbar)
                #                 time.sleep(1)  # Allow time for new rows to load
                #                 new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                #                 if new_scroll_position == last_scroll_position:
                #                     all_data.extend(scrape_visible_rows(scraped_set))  # Exit if no more rows are loaded
                #                     print('batch scrapped after scroll - ' + str(len(all_data)))
                #                     return all_data
                #                     # break
                #                 last_scroll_position = new_scroll_position
                                
                #             except NoSuchElementException:
                #                 # return all_data
                #                 pass
                #                 # Update scroll position
                #             if new_scroll_position == last_scroll_position:  # Exit if no more rows are loaded
                #                 print("scroll ended")
                #                 return all_data
                #                 # break
                #     all_data.extend(scrape_visible_rows(scraped_set))
                    
                #     print('batch scrapped at the end - ' + str(len(all_data)))    
                #     return all_data

                 # Function to scroll the grid incrementally and scrape visible data
                def scroll_and_scrape():
                    # Locate the vertical scrollbar container
                    scrollbar = driver.find_element(By.CLASS_NAME, "MuiDataGrid-scrollbar--vertical")
                    # all_data = []
                    last_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                    total_height = driver.execute_script("return arguments[0].scrollHeight;", scrollbar)
                    # all_data.extend(scrape_visible_rows(scraped_set))
                    while last_scroll_position < total_height:
                        # Scrape data from visible rows
                        # all_data.extend(scrape_visible_rows(scraped_set))
                        scrape_visible_rows()
                        print('first batch scrapped under scroll & scrape - ' + str(len(all_data)))
                        last_loaded_row = driver.find_element(By.CSS_SELECTOR,f'div[data-rowindex="{str(max_index)}"]') 
                        while (last_loaded_row.is_displayed()): 
                            try:
                                print("scrolling")
                                print('Total Scrapped Data - ' + str(len(all_data)))
                                # Scroll down incrementally
                                driver.execute_script("arguments[0].scrollTop += 190;", scrollbar)
                                time.sleep(0.5)  # Allow time for new rows to load
                                new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                                
                                print(f"total Height : {total_height} - new Scroll Position: {new_scroll_position}  ")
                                if new_scroll_position == last_scroll_position:  # Exit if no more rows are loaded
                                    # all_data.extend(scrape_visible_rows(scraped_set))
                                    scrape_visible_rows()
                                    return
                                # return all_data
                                last_scroll_position = new_scroll_position 
                            except NoSuchElementException:
                                # all_data.extend(scrape_visible_rows(scraped_set))
                                print("scrolling complete.scrapping")
                                # return all_data
                                break
                                # pass
                            # if last_scroll_position < total_height:
                            #     return all_data
                                # break
                                # Update scroll position
                        # if new_scroll_position == last_scroll_position:  # Exit if no more rows are loaded
                        #     # return all_data
                        #     break
                        # all_data.extend(scrape_visible_rows(scraped_set))                        
                    # return all_data

                # Function to reset scroll position to the top
                def reset_scroll():
                    scrollbar = driver.find_element(By.CLASS_NAME, "MuiDataGrid-scrollbar--vertical")
                    driver.execute_script("arguments[0].scrollTop = 0;", scrollbar)
                    time.sleep(1)  # Allow time for the reset
                    global max_index
                    max_index = -1
                # Function to navigate to the next page
                def go_to_next_page():
                    global max_index
                    max_index = -1
                    try:
                        next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(2)  # Allow time for the next page to load
                            reset_scroll()  # Reset scroll to the top of the new page
                            return True
                        else:
                            return False
                    except:
                        return False

                # Main scraping logic
                all_data = []
                # scraped_set = set()  # To keep track of already scraped rows

                row_index = []
                start_index = -1
                max_index = -1
                # start_index = None
                # max_index = None

                
                while True:
                    try:
                        # Scrape all data from the current page
                        # all_data.extend(scroll_and_scrape(scraped_set))

                        scroll_and_scrape()
                        print("Total Scrapped rows"+str(len(all_data)))
                        # Check if there is a next page
                        if not go_to_next_page():
                            break
                    except StaleElementReferenceException:
                        continue  # Retry on stale element exception
                #############################################################################################################################################################
                #####################################################################################################################################################################
                # Function to scrape data from visible rows based on aria-rowindex
                # def scrape_visible_rows(scraped_set, max_rows=100):
                #     data = []
                #     rows_scraped = 0
                #     while rows_scraped < max_rows:
                #         try:
                #             # Locate the rows using aria-rowindex (dynamic row locator)
                #             rows = driver.find_elements(By.CSS_SELECTOR, "[aria-rowindex]")
                            
                #             for row in rows:
                #                 # Skip the row if it has already been scraped
                #                 cells = row.find_elements(By.CLASS_NAME, "MuiDataGrid-cell")
                #                 row_data = tuple(cell.text for cell in cells)
                                
                #                 if row_data not in scraped_set:
                #                     scraped_set.add(row_data)
                #                     data.append(row_data)
                #                     rows_scraped += 1

                #                 # Stop if we reach the maximum number of rows
                #                 if rows_scraped >= max_rows:
                #                     break
                #         except Exception as e:
                #             print(f"Error while scraping: {e}")
                #             break
                #     return data

                # # Function to scroll the grid incrementally and scrape visible data
                # def scroll_and_scrape(scraped_set, max_rows=100):
                #     all_data = []
                #     last_scroll_position = 0

                #     while True:
                #         all_data.extend(scrape_visible_rows(scraped_set, max_rows))
                        
                #         # Check if we've scraped enough rows
                #         if len(all_data) >= max_rows:
                #             break
                        
                #         # Scroll the grid to load more rows if needed
                #         driver.execute_script("window.scrollBy(0, 500)")  # Adjust the scroll distance as needed
                #         time.sleep(0.5)  # Allow time for the grid to load more data

                #     return all_data

                # # Main scraping logic
                # scraped_set = set()  # To keep track of already scraped rows
                # all_data = scroll_and_scrape(scraped_set, max_rows=100)    

                #############################temp############################################################################
                try:
                    stock_data
                    print("Total Scrapped rows"+str(len(all_data)))
                except NameError:
                    stock_data = pd.DataFrame(all_data)
                    stock_data.insert(0,'Date',trade_date)
                    # stock_data['date'] = trade_date
                else:
                    # If DataFrame exists, append new data
                    new_stock_data = pd.DataFrame(all_data)
                    new_stock_data.insert(0,'Date',trade_date)
                    stock_data = pd.concat([stock_data, new_stock_data])
                
                print(stock_data)
                stock_data.to_csv("Scrapped_IdaddyBlastData_20122024.csv"
                )
                ##############################################################################################################
                
                                                        
                            # Print the scraped data
                            # for row in all_data:
                            #     print(row)

                            # # zoom_percentage = 24
                            # # driver.execute_script(f"document.body.style.zoom='{zoom_percentage}%'")

                            # stock_names = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"symbol\"] > div.clickable-cell")
                            # Volumes = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"totalVolume\"][role=\"gridcell\"]")
                            # PointValues = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"strikeDifference\"][role=\"gridcell\"]")
                            # BullishRisks = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"callRating\"][role=\"gridcell\"]")
                            # C2Levels = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"callEntry2\"][role=\"gridcell\"]")
                            # C1Levels = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"callEntry1\"][role=\"gridcell\"]")
                            # CMPrices = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"priceS\"][role=\"gridcell\"]")
                            # P1Levels = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"putEntry1\"][role=\"gridcell\"]")
                            # P2Levels = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"putEntry2\"][role=\"gridcell\"]")
                            # BearishRisks = driver.find_elements(By.CSS_SELECTOR, "div[data-field=\"putRating\"][role=\"gridcell\"]")
                            
                            # # stock_data = pd.DataFrame({'Stock Name': list(map(lambda stock_name: stock_name.text, stock_names)), 'Volume' : list(map(lambda Volume: Volume.text, Volumes)) , 'Point Value':list(map(lambda point_value: point_value.text, PointValues)),'Bullish Risk': list(map(lambda Bullish_Risk: Bullish_Risk.text, BullishRisks)), 'C2': list(map(lambda C2_Level: C2_Level.text, C2Levels)),'C1': list(map(lambda C1_Level: C1_Level.text, C1Levels)),'CMP' : list(map(lambda CMP: CMP.text, CMPrice)), 'P1' : list(map(lambda P1_Level: P1_Level.text, P1Levels)),'P1' : list(map(lambda P2_Level: P2_Level.text, P2Levels)), 'Bearish Risk' : list(map(lambda BearishRisk: BearishRisk.text, BearishRisks))} )
                            
                            # # Stock_name = pd.Series({'Stock Name': list(map(lambda stock_name: stock_name.text, stock_names))})
                            # # print(Stock_name)
                            # # print(f"{stock_names[0].text}  + total length-{len(stock_names)} ")
            
                            # TradeDate = []
                            # stock_name =[]
                            # Volume = []
                            # PValue = []
                            # BullishRisk = []
                            # C2Level = []
                            # C1Level = []
                            # CMPrice = []
                            # P1Level = [] 
                            # P2Level = []
                            # BearishRisk = []

                            # for i in range(0,len(stock_names)):
                            #         print(f"{trade_date} - {stock_names[i].text} - {Volumes[i].text} - {PointValues[i].text} - {BullishRisks[i].text} - {C2Levels[i].text} - {C1Levels[i].text} - {CMPrices[i].text} - {P1Levels[i].text} - {P2Levels[i].text} - {BearishRisks[i].text}")
                            #         TradeDate.append(trade_date)
                            #         stock_name.append(stock_names[i].text)
                            #         Volume.append(Volumes[i].text)
                            #         PValue.append(PointValues[i].text)
                            #         BullishRisk.append(BullishRisks[i].text)
                            #         C2Level.append(C2Levels[i].text)
                            #         C1Level.append(C1Levels[i].text)
                            #         CMPrice.append(CMPrices[i].text)
                            #         P1Level.append(P1Levels[i].text)
                            #         P2Level.append(P2Levels[i].text)
                            #         BearishRisk.append(BearishRisks[i].text)
                            

                            # stock_data = pd.DataFrame({'Date':TradeDate,'Stock Name': stock_name, 'Volume':Volume,'Bullish Risk':BullishRisk,'C2 Level' : C2Level,'C1 Level': C1Level,'CMP': CMPrice,'P1 Level' : P1Level,'P2 Level':P2Level,'Bearish Risk':BearishRisk} )
                            # print(stock_data)
                            # print(f"""Total Stock Name:{len(stock_names)},
                            #         Total Volume : {len(Volumes)},
                            #         Total Point Values : {len(PointValues)},
                            #         Total Bullish Risks : {len(BullishRisks)},
                            #         Total C2Levels : {len(C2Levels)},
                            #         Total C1Levels : {len(C1Levels)},
                            #         Total CMP : {len(CMPrice)},
                            #         Total P1Levels : {len(P1Levels)}
                            #         Total P2Levels : {len(P2Levels)}
                            #         Total BearishRisks: {len(BearishRisks)}                                    
                            #         """)
                            
                            # for stock_name in stock_names:
                            #     print(stock_name.text)

                            
                # break
        except TimeoutException:
            print("Target element not found, trying the next option...")

time.sleep(30)

driver.quit()