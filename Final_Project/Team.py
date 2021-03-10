import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
from sklearn import svm


India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

Player_details=pd.read_csv(r"C:.\data\Player_details.csv",delimiter=",")
Player_details=Player_details[(Player_details["International Status"]!="Retired")&(Player_details["International Status"]!="Banned")]
Player_details=Player_details[(Player_details["Batting Experience"]>=15)|(Player_details["Bowling Experience"]>=15)]
Player_details=Player_details.drop(['CAP'], axis = 1)

venue_names=[]
team2_names=[]
batsman_names=[]
bowler_names=[]
over=[]

for g,f in match_details.groupby("Venue"):
    venue_names.append(g)
for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g)

India_Batting=India_T20[India_T20["Batting"]=="India"]
for group,frame in India_Batting.groupby("Striker"):
    batsman_names.append(group.lower())

for g,f in India_T20.groupby("Bowler"):
    bowler_names.append(g.lower())

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
            batsman_number.append(batsman_names.index(g.lower()))
            innings_played.append(frame["Innings"].iloc[0])
            for j in range(len(match_details["Match ID"])):
                if(group==match_details["Match ID"].iloc[j]):
                    venue_number.append(venue_names.index(match_details["Venue"].iloc[j]))
                    if(match_details["Team 1"].iloc[j]!="India"):
                        team2_number.append(team2_names.index(match_details["Team 1"].iloc[j]))
                    else:
                        team2_number.append(team2_names.index(match_details["Team 2"].iloc[j]))
        
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

data={"Batsman":batsman_number,"Team 2":team2_number,"Venue":venue_number,"Over type":over_type,"Strikerate":strikerate,}
df=pd.DataFrame(data)
df=df[(df["Strikerate"]>0) & (df["Strikerate"]<600)]


X = df[['Batsman', 'Team 2',"Venue","Over type"]]
y = df['Strikerate']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state= 123)


gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=1.0, max_depth=1)
gbr.fit(X_train, y_train)
pr=gbr.predict(X_test)
s_mae=round(metrics.mean_absolute_error(y_test, pr),2)
s_mape=round(metrics.mean_absolute_percentage_error(y_test, pr)*100,2)
print("Mean absolute error for batsman Strikerate = ",s_mae)
print("Percentage Error for batsman Strikerate = ",s_mape)

pickle.dump(gbr, open('team_batsman.pkl', 'wb'))


India_Bowling=India_T20[India_T20["Batting"]!="India"]
bowler_number=[]
economy=[]
venue_number=[]
team2_number=[]
innings_played=[]
for group,frame in India_Bowling.groupby("Match ID"):
    for g,f in frame.groupby("Bowler"):
        bowler_number.append(bowler_names.index(g.lower()))
        innings_played.append(frame["Innings"].iloc[0])
        for j in range(len(match_details["Match ID"])):
            if(group==match_details["Match ID"][j]):
                venue_number.append(venue_names.index(match_details["Venue"][j]))
                if(match_details["Team 1"][j]!="India"):
                    team2_number.append(team2_names.index(match_details["Team 1"][j]))
                else:
                    team2_number.append(team2_names.index(match_details["Team 2"][j]))
        e=round((np.sum(f["Runs"])*6)/len(f["Runs"]),2)
        economy.append(e)

data1={"Bowler":bowler_number,"Team 2":team2_number,"Innings":innings_played,"Venue":venue_number,"Economy":economy}
df1=pd.DataFrame(data1)

X1 = df1[['Bowler', 'Team 2',"Venue"]]
y1 = df1['Economy']
X_train1, X_test1, y_train1, y_test1 = train_test_split(X1, y1, test_size= 0.3, random_state= 123)

sv=svm.SVR()
sv.fit(X_train1, y_train1)
pr1=sv.predict(X_test1)
e_mae=round(metrics.mean_absolute_error(y_test1, pr1),2)
e_mape=round(metrics.mean_absolute_percentage_error(y_test1, pr1)*100,2)
print("Mean absolute error for bowler Economy = ",e_mae)
print("Percentage Error for bowler Economy = ",e_mape)

pickle.dump(sv, open('team_bowler.pkl', 'wb'))






