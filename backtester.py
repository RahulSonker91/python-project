# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
import pandas as pd
from datetime import datetime
from logzero import logger
import openpyxl
import pandas as pd
import numpy as np


############################API credentails for login##################################
api_key = 'RgOlMNVl'
username = 'MNGZA1072'
pwd = '5315'
smartApi = SmartConnect(api_key)
try:
    token = "AWBIH65LNVEYLFRR7TC53YPHNQ"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)

if data['status'] == False:
    logger.error(data)
    
else:
    # login api call
    # logger.info(f"You Credentials: {data}")
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    # fetch the feedtoken
    feedToken = smartApi.getfeedToken()
    # fetch User Profile
    res = smartApi.getProfile(refreshToken)
    smartApi.generateToken(refreshToken)
    res=res['data']['exchanges']
 
wb=openpyxl.load_workbook("NSE_stockTokens.xlsx")
sh1=wb['Sheet1']
row=sh1.max_row

def getCandleData(exchange="NSE",symbolToken="7",interval="ONE_MINUTE",fromDate = datetime.today().strftime('%Y-%m-%d'),toDate=datetime.today().strftime('%Y-%m-%d'),startTime = "09:15",EndTime="15:30" ):
ehistoricParam={
        "exchange": exchange,
        "symboltoken": symbolToken,
        "interval": interval,
        "fromdate": fromDate+" "+startTime, 
        "todate": toDate+" "+EndTime
        }
        return ehistoricParam
 #Historic api
try:
       #query tp fetch the data from broker  
        historicParam={
        "exchange": "NSE",
        "symboltoken": "7",
        "interval": "ONE_MINUTE",
        "fromdate": "2024-10-18 09:15", 
        "todate": "2024-10-18 15:17"
        }

        #fetchng data from broker
        CS_data = smartApi.getCandleData(historicParam)
        

        #Handling fetched data and transfering it to dataframe
        df=pd.DataFrame(CS_data['data'])

        #converting timedata to readable excel format
        df[0] = pd.to_datetime(df[0], format='%Y-%m-%dT%H:%M:%S%z')
        df[0] = df[0].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        #renaming indexes to time,OHLC,values
        df.rename(columns={0: 'datetime'}, inplace=True)
        df.rename(columns={1: 'open'}, inplace=True)
        df.rename(columns={2: 'high'}, inplace=True)
        df.rename(columns={3: 'low'}, inplace=True)
        df.rename(columns={4: 'close'}, inplace=True)
        df.rename(columns={5: 'volume'}, inplace=True)
        
        #writing the data to csv file 
        df.to_csv('candleStickData.csv',index=False)
        
        #printing data
        print(df)

except Exception as e:
        logger.exception(f"Historic Api failed: {e}")
    #logout
try:
        logout=smartApi.terminateSession('MNGZA1072')
        logger.info("Logout Successfull")
except Exception as e:
        logger.exception(f"Logout failed: {e}")
        print(getCandleData())