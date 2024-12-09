from selenium import webdriver
import pandas as pd
from datetime import datetime
# import openpyxl
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
for option in options:
    # print(option.get_attribute("value"))
    # Iterate through the options in the select element
    for j in range(len(options)):
        print(j)
        # Select the current option
        select.select_by_index(j)
        print(f"Selected option: {options[j].text}")
        print(f"{len(options)}")
        trade_date = options[j].text
        target_locator = (By.CSS_SELECTOR, "div[data-field=\"symbol\"] > div")

        # Wait for the page or content to update (adjust timeout as needed)
        try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(target_locator))
                print("Target element found!")
                
                # zoom_percentage = 24
                # driver.execute_script(f"document.body.style.zoom='{zoom_percentage}%'")
                # time.sleep(3)

                # Function to scrape data from visible rows
                def scrape_visible_rows(scraped_set):
                    rows = driver.find_elements(By.CLASS_NAME, "MuiDataGrid-row")  # Locate rows dynamically
                    data = []
                   
                    for row in rows: 
                        try:
                            cells = row.find_elements(By.CLASS_NAME, "MuiDataGrid-cell")  # Locate cells dynamically
                            row_data = tuple(cell.text for cell in cells)  # Use tuple to make it hashable
                            if row_data not in scraped_set:
                                scraped_set.add(row_data)
                                data.append(row_data)
                        except StaleElementReferenceException:
                            continue  # Skip stale rows
                    return data

                # Function to scroll the grid incrementally and scrape visible data
                def scroll_and_scrape(scraped_set):
                    # Locate the vertical scrollbar container
                    scrollbar = driver.find_element(By.CLASS_NAME, "MuiDataGrid-scrollbar--vertical")
                    all_data = []
                    last_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                    total_height = driver.execute_script("return arguments[0].scrollHeight;", scrollbar)

                    while last_scroll_position < total_height:
                        # Scrape data from visible rows
                        all_data.extend(scrape_visible_rows(scraped_set))
                        
                        # Scroll down incrementally
                        driver.execute_script("arguments[0].scrollTop += 200;", scrollbar)
                        time.sleep(0.2)  # Allow time for new rows to load
                        
                        # Update scroll position
                        new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
                        if new_scroll_position == last_scroll_position:  # Exit if no more rows are loaded
                            break
                        last_scroll_position = new_scroll_position

                    return all_data

                # Function to reset scroll position to the top
                def reset_scroll():
                    scrollbar = driver.find_element(By.CLASS_NAME, "MuiDataGrid-scrollbar--vertical")
                    driver.execute_script("arguments[0].scrollTop = 0;", scrollbar)
                    time.sleep(1)  # Allow time for the reset

                # Function to navigate to the next page
                def go_to_next_page():
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
                scraped_set = set()  # To keep track of already scraped rows

                while True:
                    try:
                        # Scrape all data from the current page
                        all_data.extend(scroll_and_scrape(scraped_set))
                        print("Total Scrapped rows"+str(len(all_data)))
                        # Check if there is a next page
                        if not go_to_next_page():
                            break
                    except StaleElementReferenceException:
                        continue  # Retry on stale element exception

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

                try:
                    stock_data
                except NameError:
                    stock_data = pd.DataFrame(all_data)
                    stock_data['date'] = trade_date
                else:
                    # If DataFrame exists, append new data
                    new_stock_data = pd.DataFrame(all_data)
                    new_stock_data['date'] = trade_date
                    stock_data = pd.concat([stock_data, new_stock_data], ignore_index=True)
                
                print(stock_data)
                                                        
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