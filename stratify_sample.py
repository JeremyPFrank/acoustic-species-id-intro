import pandas as pd
import datetime as dt

def stratify():
    file = pd.read_csv("Peru_2019_AudioMoth_Data_Full.csv")
    
    #remove audio clips less than 60 secs
    file = file.drop(file[file['Duration'] < 60].index)
    
    #remove clips that are too small
    file = file.drop(file[file['FileSize'] < 46080360].index) 
    
    #Convert StartDateTime to datetime objects
    file['StartDateTime'] = pd.to_datetime((file["StartDateTime"]))
    
    #Get all audio moth codes
    audio_moth_codes = file.drop_duplicates(subset=['AudioMothCode'], 
                                            keep = 'first')
    
    stratified_data = pd.DataFrame(columns=file.columns)
    
    #Iterate through each device
    for device in audio_moth_codes['AudioMothCode']:
    
        #device_filtered is the first strata for each of the devices
        device_filtered = file[file['AudioMothCode'] == device] 
        
        #Loop through every hour of the day
        for hour in range(0,24):
            
            #time_filtered is the second strata for each hour for each device
            time_filtered = device_filtered[device_filtered['StartDateTime'].dt.hour == hour]
            
            #Concat random row to stratified_data if time_filtered is not empty
            if time_filtered.empty:
                break
            #Get random row  
            random_row = time_filtered.sample().iloc[0]  
            stratified_data = pd.concat([stratified_data, 
                                         pd.DataFrame([random_row])], ignore_index=True)
    if (len(stratified_data.index) == 0):
        print("No Valid AudioMoth Devices - Stratified Sampling Failed")
        return False
    stratified_data.to_csv('stratified_audiomoth_data.csv', index=False)  
    print(stratified_data['StartDateTime'])
    return True

#for testing purposes
print(stratify())
