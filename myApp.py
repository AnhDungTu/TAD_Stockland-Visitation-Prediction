import streamlit as st 
from PIL import Image
from datetime import date
from datetime import datetime
import pandas as pd 
import numpy as np 
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

##model = pickle.load(open('finalModel.pkl'))

def main():
    
    ## Building Random Forest Regression with optimized hyper parameters
    img = Image.open("stockland_Logo.png")
    st.image(img, width=300)
    st.title('Stockland Visitation Prediction')
    
    df_1 = pd.read_csv("data/Stockland - Visitation Data.csv", encoding=None )
    df_2 = pd.read_csv("data/weather.csv", encoding=None)
    df_full = pd.merge(df_1, df_2, on = ['Asset','Date'], how = "inner")
    df_full['Rainfall ']=df_full['Rainfall '].fillna(0)
    df_full['Raining period']= df_full['Raining period'].bfill()
    for i in range(len(df_full)):
        if df_full['Rainfall '].loc[i]==0:
            df_full['Raining period'].loc[i]=0 
    df_full['Max temperature']=df_full['Max temperature'].ffill()
    df_full['Min temperature']=df_full['Min temperature'].ffill()
    df_full['Solar exposure']=df_full['Solar exposure'].ffill()
    df_full = pd.get_dummies(df_full,columns=['Asset'])
    
    for i in range(len(df_full)):   
        df_full['Date'].loc[i]= datetime.strptime(df_full['Date'].loc[i],'%d/%m/%Y')


    df_full['Date'].loc[1].month
    df_full['Month']= ""
    for i in range(len(df_full)):
        df_full['Month'].loc[i]=df_full['Date'].loc[i].month
        
    df_full['Month']= df_full['Month'].astype(str)
    df_full = pd.get_dummies(df_full,columns=['Month'])
    
    df_clean = df_full[df_full['Count visitation'].notna() ]
    
    df_clean =shuffle(df_clean)
    
    y_train = df_clean['Count visitation']
    X_train = df_clean.drop(columns = ['Count visitation', 'Date'])
    final = RandomForestRegressor(n_estimators= 250, max_features= 11, max_depth= 20, bootstrap= True)
    final.fit(X_train, y_train)
    
    
    #input variables
    asset = st.selectbox("Please choose your Asset location",('Baldivis', 'Balgowlah', 'Birtinya', 'Bull Creek', 'Burleigh', 'Gladstone','Glendale','Green Hills','Harrisdale','Hervey Bay','Merrylands','Riverton','Rockhampton','Wendouree','Wetherill Park'))
    st.write("You've selected:", asset)
    
    min_temp = st.slider('Min temperature (Celcius Degree)', min_value=-3.0, max_value=30.0, step=0.1)
    max_temp = st.slider('Max temperature (Celcius Degree)', min_value= 5.0, max_value=44.0, step=0.1)
    solar_exposure = st.slider('Solar exposure (MJ/m2)', min_value=0.0, max_value=33.0, step=0.1)
    rain_fall=st.slider('Rainfall (mm)', min_value=0.0, max_value=255.0, step=1.0)
    rain_period = st.slider('Raining period (number of possible continous raining day)',min_value=0,max_value=14,step=1)
    
    d = st.date_input("Which day you want to predict?", date(2022, 7, 1))
    month = d.month
    
   
    Asset_Baldivis=0          
    Asset_Balgowlah=0   
    Asset_Birtinya=0       
    Asset_BullCreek=0   
    Asset_Burleigh=0
    Asset_Gladstone=0
    Asset_Glendale=0
    Asset_GreenHills=0
    Asset_Harrisdale=0
    Asset_HerveyBay=0
    Asset_Merrylands=0
    Asset_Riverton=0
    Asset_Rockhampton=0
    Asset_Wendouree=0
    Asset_WetherillPark=0
    Month_1=0
    Month_10=0
    Month_11=0
    Month_12=0
    Month_2=0
    Month_3=0
    Month_4=0
    Month_5=0
    Month_6=0
    Month_7=0
    Month_8=0
    Month_9=0
    
    if asset == 'Baldivis':
        Asset_Baldivis=1
    elif asset =='Balgowlah':
        Asset_Balgowlah=1
    elif asset=='Birtinya':
        Asset_Birtinya=1
    elif asset == 'Bull Creek':
        Asset_BullCreek=1
    elif asset == 'Burleigh':
        Asset_Burleigh=1
    elif asset == 'Gladstone':
        Asset_Gladstone=1
    elif asset == 'Glendale':
        Asset_Glendale=1
    elif asset == 'Green Hills':
        Asset_GreenHills=1
    elif asset == 'Harrisdale':
        Asset_Harrisdale=1
    elif asset == 'Hervey Bay':
        Asset_HerveyBay=1
    elif asset == 'Merrylands':
        Asset_Merrylands=1
    elif asset == 'Riverton':
        Asset_Riverton=1
    elif asset == 'Rockhampton':
        Asset_Rockhampton=1
    elif asset == 'Wendouree':
        Asset_Wendouree=1
    else :
        Asset_WetherillPark=1
    
    if month ==1:
        Month_1=1
    elif month ==2:
        Month_2 =1
    elif month ==3:
        Month_3 =1
    elif month ==4:
        Month_4 =1
    elif month ==5:
        Month_5 =1
    elif month ==6:
        Month_6 =1
    elif month ==7:
        Month_7 =1
    elif month ==8:
        Month_8 =1
    elif month ==9:
        Month_9 =1
    elif month ==10:
        Month_10 =1
    elif month ==11:
        Month_11 =1
    else:
        Month_12 =1
        
    # Prediction code 
    if st.button('Predict'):
        makeprediction = final.predict([[min_temp, max_temp, solar_exposure, rain_fall, rain_period, 
                                         Asset_Baldivis, Asset_Balgowlah, Asset_Birtinya, Asset_BullCreek,
                                         Asset_Burleigh, Asset_Gladstone,Asset_Glendale, Asset_GreenHills, 
                                         Asset_Harrisdale, Asset_HerveyBay, Asset_Merrylands, Asset_Riverton,
                                         Asset_Rockhampton, Asset_Wendouree, Asset_WetherillPark,
                                         Month_1, Month_10, Month_11, Month_12, Month_2, Month_3,
                                         Month_4, Month_5, Month_6, Month_7, Month_8, Month_9]])
        output = round(makeprediction[0],0)
        st.success('Expected number of visitors on selected date: {}'.format(output) )
    
    
if __name__ == '__main__':
    main() 
    





