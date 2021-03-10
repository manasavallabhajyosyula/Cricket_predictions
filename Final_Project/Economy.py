import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
import pickle

India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

India_Bowling=India_T20[India_T20["Batting"]!="India"]

bowler_names=[]
for g,f in India_T20.groupby("Bowler"):
    bowler_names.append(g)



venue_names=[]
team2_names=[]
over=[]
for g,f in match_details.groupby("Venue"):
    venue_names.append(g)

for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g)

for g,f in India_T20.groupby("Over type"):
    over.append(g)


bowler_number=[]
over_type=[]
economy=[]
venue_number=[]
team2_number=[]
innings_played=[]

for group,frame in India_Bowling.groupby("Match ID"):
    
    for g,f in frame.groupby("Bowler"):
        p=m=d=0
        for i in range(3):
            bowler_number.append(bowler_names.index(g))
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
                p=round((np.sum(j["Runs"])*6)/len(j["Runs"]),2)
            if (i=="Middle Overs"):
                m=round((np.sum(j["Runs"])*6)/len(j["Runs"]),2)
            if (i=="Death Overs"):
                d=round((np.sum(j["Runs"])*6)/len(j["Runs"]),2)
        economy.append(p)
        over_type.append(over.index("Powerplay"))
        economy.append(m)
        over_type.append(over.index("Middle Overs"))
        economy.append(d)
        over_type.append(over.index("Death Overs"))


data={"Bowler":bowler_number,"Team 2":team2_number,"Innings":innings_played,"Venue":venue_number,"Over type":over_type,"Economy":economy}
df=pd.DataFrame(data)
df=df[df["Economy"]>0]


X = df[['Bowler', 'Team 2',"Innings","Venue","Over type"]]
y = df['Economy']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.05, random_state= 123)


knn_reg = KNeighborsRegressor(n_neighbors = 5)
knn_reg.fit(X_train, y_train)
pr=knn_reg.predict(X_test)

mae=round(metrics.mean_absolute_error(y_test,pr),2)
mape=round(metrics.mean_absolute_percentage_error(y_test,pr)*100,2)
print("Error Percentage for Economy = ",mape)
print("Absolute Error for Economy= ",mae)

pickle.dump(knn_reg, open('economy.pkl', 'wb'))
