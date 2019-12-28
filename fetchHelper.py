import pandas as pd 
import numpy as np
import datetime
from datetime import timedelta  


DATE_FORMAT = '%Y-%m-%d'
databaseFilename = 'data/database_main.xls'

def prettyPrintDate(date):
    return date.strftime(DATE_FORMAT); 
 #x[4] if len(x) == 4 else 'No'
def safeGet(obj, key, defaultVal = np.nan):
    return obj.get(key, defaultVal)  

def percent(val):
    return np.ceil(val*100)

def filterArrObj(arrList, keyName, keyValue):
    for arrItem in arrList:
        if arrItem.get(keyName) == keyValue:
            return arrItem
    return {} 

def mergeDicts(dicts):
    super_dict = {}
    for singleDict in dicts:
        for k, v in singleDict.items(): 
            super_dict[k] = v
    return super_dict


class DatabaseFactory:
    def __init__(self, databaseFilename, auth2_client, auth2_client_new):
        self.databaseFilename = databaseFilename
        self.auth2_client = auth2_client
        self.auth2_client_new = auth2_client_new

    def connectAndLoadDb(self):
        print("Connecting database...")
        database = pd.read_excel(databaseFilename)
        print("Database connected!")
        return database;

    def getLastEntryDate(self, database):
        lastDateEntry = database.iloc[-1]['Date']
        lastDateEntry = datetime.datetime.strptime(lastDateEntry, DATE_FORMAT)    
        return lastDateEntry

    def addEntriesInDB(self, dictionary, database):
        #print(dictionary)
        self.database = self.database.append(dictionary, ignore_index=True)
        return addEntriesInDB;

    def writeDbToExcelFile(self, database):
        print('Writing database to filename: '+ databaseFilename)
        writer = pd.ExcelWriter(databaseFilename)
        database.to_excel(writer, 'main')
        writer.save()
        print('Database updated with new entries!!')
    

    def getActivities(self, date):
        activitiyResponse = self.auth2_client.activities(date=date)

        activitySummary = activitiyResponse['summary'];
        activityData = {
            'Calories Burned':safeGet(activitySummary,'caloriesOut'),
            'Calories BMR': safeGet(activitySummary,'caloriesBMR'),
            'Resting Heart Rate':safeGet(activitySummary,'restingHeartRate'),
            'Steps':safeGet(activitySummary,'steps'),
            'Distance (Km)':filterArrObj(activitySummary.get('distances', []), 'activity', 'total').get('distance', np.nan),
            'Elevation (Ft)':activitySummary['elevation'],
            'Floors':activitySummary['floors'],
            'Minutes Sedentary':activitySummary['sedentaryMinutes'],
            'Minutes Lightly Active':activitySummary['lightlyActiveMinutes'],
            'Minutes Fairly Active':activitySummary['fairlyActiveMinutes'],
            'Minutes Very Active':activitySummary['veryActiveMinutes'],
            'Activity Calories': activitySummary['activityCalories'],
            'Active Score': activitySummary['activeScore'],
            'Cardio minutes': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Cardio').get('minutes', np.nan),
            'Cardio calories': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Cardio').get('caloriesOut', np.nan),
            'Fat Burn minutes': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Fat Burn').get('minutes', np.nan),
            'Fat Burn calories': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Fat Burn').get('caloriesOut', np.nan),
            'Peak minutes': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Peak').get('minutes', np.nan),
            'Peak calories': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Peak').get('caloriesOut', np.nan),
            'Normal Cardio minutes': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Out of Range').get('minutes', np.nan),
            'Normal Cardio calories': filterArrObj(activitySummary.get('heartRateZones', []), 'name', 'Out of Range').get('caloriesOut', np.nan),
        }

        return activityData

    def getSleep(self, date):
        sleepResponse = self.auth2_client_new.sleep(date=date)

        sleepData = {}
        for sleepLog in sleepResponse.get('sleep', []):
            if sleepLog.get('isMainSleep'):
                sleepLevelsSummary = sleepLog.get('levels', {}).get('summary', {})

                sleepData['Sleep Efficiency'] = safeGet(sleepLog, 'efficiency')
                sleepData['Minutes Asleep'] = safeGet(sleepLog, 'minutesAsleep')
                sleepData['Minutes to fall asleep'] = safeGet(sleepLog, 'minutesToFallAsleep')
                sleepData['Sleep Start time'] = safeGet(sleepLog, 'startTime')
                sleepData['Sleep End time'] = safeGet(sleepLog, 'endTime')

                sleepData['Time in bed'] = safeGet(sleepLog, 'timeInBed')

                sleepData['Minutes Deep sleep'] = safeGet(sleepLevelsSummary.get('deep', {}), 'minutes')
                sleepData['Deep sleep count'] = safeGet(sleepLevelsSummary.get('deep', {}), 'count')
                sleepData['% Deep sleep'] = percent(safeGet(sleepData, 'Minutes Deep sleep', 0)/safeGet(sleepData, 'Time in bed', 0))

                sleepData['Minutes Light sleep'] = safeGet(sleepLevelsSummary.get('light', {}), 'minutes')
                sleepData['Light sleep count'] = safeGet(sleepLevelsSummary.get('light', {}), 'count')
                sleepData['% Light sleep'] = percent(safeGet(sleepData, 'Minutes Light sleep', 0)/safeGet(sleepData, 'Time in bed', 0))

                sleepData['Minutes REM sleep'] = safeGet(sleepLevelsSummary.get('rem', {}), 'minutes')
                sleepData['REM sleep count'] = safeGet(sleepLevelsSummary.get('rem', {}), 'count')
                sleepData['% REM sleep'] = percent(safeGet(sleepData, 'Minutes REM sleep', 0)/safeGet(sleepData, 'Time in bed', 0))

                sleepData['Minutes Asleep'] = sleepData['Minutes Deep sleep'] + sleepData['Minutes Light sleep'] + sleepData['Minutes REM sleep']
                sleepData['Minutes Awake'] = safeGet(sleepLevelsSummary.get('wake', {}), 'minutes')
                sleepData['Minutes Awake count'] = safeGet(sleepLevelsSummary.get('wake', {}), 'count')            
        return sleepData

    def getDateData(self, date):
        weekDayNum = date.isoweekday()
        return {
            'Day of Week': weekDayNum,
            'Is Weekday': weekDayNum<6,
            'Is Weekend': weekDayNum>5,
            'Date': prettyPrintDate(date)
        };

    def fetchAllData(self, date):
        dateStr = prettyPrintDate(date)

        print("Fetching fitbit data for: " + dateStr)

        nextDate = date + timedelta(days=1)
        sleepData = self.getSleep(prettyPrintDate(nextDate))

        activitiesData = self.getActivities(dateStr)
        dateData = self.getDateData(date)

        mergedData = mergeDicts([sleepData, activitiesData, dateData])
        return mergedData
    
    def shouldFetchDataForProvidedDate(self, providedDate, todaysDate, API_COUNTER):
        return (providedDate < todaysDate) and API_COUNTER < 100;

    def fetchAndAppendToDb(self, date, database):    
        mergedData = self.fetchAllData(date)
        database = database.append(mergedData, ignore_index=True)
        return database;

    def fetchData(self, database, refetchAll = False):
        API_COUNTER = 0
        
        lastEntryDate = self.getLastEntryDate(database)
        
        yesterDay = datetime.datetime.today() - timedelta(days=1)
        
        dateToFetch = lastEntryDate

        print("Date today is :" + prettyPrintDate(yesterDay))
        
        while self.shouldFetchDataForProvidedDate(dateToFetch, yesterDay, API_COUNTER):    
            database = self.fetchAndAppendToDb(dateToFetch, database)
            dateToFetch = dateToFetch + timedelta(days=1)
            API_COUNTER = API_COUNTER+1

        print("----------------------------------------------")
        print("Data fill completed! 👍👍")
        return database