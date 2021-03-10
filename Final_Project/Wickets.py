import pandas as pd
import pickle
import numpy as np

India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

India_Bowling=India_T20[India_T20["Batting"]!="India"]

bowler_names=[]
venue_names=[]
team2_names=[]
over=[]

for g,f in India_T20.groupby("Bowler"):
    bowler_names.append(g)

for g,f in match_details.groupby("Venue"):
    venue_names.append(g)

for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g)

for g,f in India_T20.groupby("Over type"):
    over.append(g)


bowler_number=[]
over_type=[]
wickets=[]
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
                p=0
                for k in range(len(j["Out"])):
                    if(j['Out'].iloc[k]=='lbw' or j['Out'].iloc[k]=='bowled' or j['Out'].iloc[k]=='caught' or 
                   j['Out'].iloc[k]=='caught and bowled' or j['Out'].iloc[k]=='stumped'):
                        p=p+1
                        
            if (i=="Middle Overs"):
                m=0
                for k in range(len(j["Out"])):
                    if(j['Out'].iloc[k]=='lbw' or j['Out'].iloc[k]=='bowled' or j['Out'].iloc[k]=='caught' or 
                   j['Out'].iloc[k]=='caught and bowled' or j['Out'].iloc[k]=='stumped'):
                        m=m+1
            if (i=="Death Overs"):
                d=0
                for k in range(len(j["Out"])):
                    if(j['Out'].iloc[k]=='lbw' or j['Out'].iloc[k]=='bowled' or j['Out'].iloc[k]=='caught' or 
                   j['Out'].iloc[k]=='caught and bowled' or j['Out'].iloc[k]=='stumped'):
                        d=d+1
        wickets.append(p)
        over_type.append(over.index("Powerplay"))
        wickets.append(m)
        over_type.append(over.index("Middle Overs"))
        wickets.append(d)
        over_type.append(over.index("Death Overs"))

data={"Bowler":bowler_number,"Team 2":team2_number,"Innings":innings_played,"Venue":venue_number,"Over type":over_type,"Wickets":wickets}
df=pd.DataFrame(data)

from sklearn.model_selection import train_test_split
X = df[['Bowler', 'Team 2',"Innings","Venue","Over type"]]
y = df['Wickets']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state= 123)


from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
rfa = RandomForestClassifier(n_estimators=20, random_state=0)
rfa.fit(X_train, y_train)
pr = rfa.predict(X_test)
print("Accuracy for Wickets = ",round(metrics.accuracy_score(y_test,pr)*100,2))



pickle.dump(rfa, open('wickets.pkl', 'wb'))
