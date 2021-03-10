import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor 
from sklearn import metrics
import pickle


India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

India_Batting=India_T20[India_T20["Batting"]=="India"]

batsman_names=[]
venue_names=[]
team2_names=[]
over=[]
for g,f in match_details.groupby("Venue"):
    venue_names.append(g)

for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g)

for group,frame in India_Batting.groupby("Striker"):
    batsman_names.append(group)
for g,f in India_T20.groupby("Over type"):
    over.append(g)



batsman_number=[]
over_type=[]
strikerate=[]
venue_number=[]
team2_number=[]
innings_played=[]

for group,frame in India_Batting.groupby("Match ID"):
    for g,f in frame.groupby("Striker"):
        p=m=d=0
        for i in range(3):
            batsman_number.append(batsman_names.index(g))
            innings_played.append(frame["Innings"].iloc[0])
            for j in range(len(match_details["Match ID"])):
                if(group==match_details["Match ID"][j]):
                    venue_number.append(venue_names.index(match_details["Venue"][j]))
                    if(match_details["Team 1"][j]!="India"):
                        team2_number.append(team2_names.index(match_details["Team 1"][j]))
                    else:
                        team2_number.append(team2_names.index(match_details["Team 2"][j]))
        for i,j in f.groupby("Over type"):
            if (i=="Powerplay"):
                p=round((np.sum(j["Runs"])*100)/len(j["Runs"]),2)
            if (i=="Middle Overs"):
                m=round((np.sum(j["Runs"])*100)/len(j["Runs"]),2)
            if (i=="Death Overs"):
                d=round((np.sum(j["Runs"])*100)/len(j["Runs"]),2)
        strikerate.append(p)
        over_type.append(over.index("Powerplay"))
        strikerate.append(m)
        over_type.append(over.index("Middle Overs"))
        strikerate.append(d)
        over_type.append(over.index("Death Overs"))

data={"Batsman":batsman_number,"Team 2":team2_number,"Innings":innings_played,"Venue":venue_number,"Over type":over_type,"Strikerate":strikerate,}
df=pd.DataFrame(data)
df=df[(df["Strikerate"]>0) & (df["Strikerate"]<600)]


X = df[['Batsman', 'Team 2',"Innings","Venue","Over type"]]
y = df['Strikerate']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state= 123)

gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
gbr.fit(X_train, y_train)
pr=gbr.predict(X_test)
mae=round(metrics.mean_absolute_error(y_test, pr),2)
mape=round(metrics.mean_absolute_percentage_error(y_test,pr)*100,2)
print("Error Percentage for Strikerate = ",mape)
print("Absolute Error for Strikerate = ",mae)
pickle.dump(gbr, open('strikerate.pkl', 'wb'))
