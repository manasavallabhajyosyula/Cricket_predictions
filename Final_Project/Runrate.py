import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn import metrics
import pickle

India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)

team2=[]
runrate=[]
venue=[]
innings_played=[]
for group,frame in India_T20.groupby("Match ID"):
    runs=0
    number_of_balls=0
    rate=0
    for i in range(len(frame["Batting"])):
        if(frame["Batting"].iloc[i]=="India"):
            runs=runs+frame["Runs"].iloc[i]+frame["Extras"].iloc[i]
            number_of_balls=number_of_balls+1
            innings=frame["Innings"].iloc[i]
    if(number_of_balls!=0):
        rate=(runs*6)/number_of_balls
    runrate.append(rate)
    if(innings==3):
        innings_played.append(2)
    elif(innings==4):
        innings_played.append(1)
    else:
        innings_played.append(innings)
    for j in range(len(match_details["Match ID"])):
        if(group==match_details["Match ID"][j]):
            venue.append((match_details["Venue"][j].lower()))
            if(match_details["Team 1"][j]!="India"):
                team2.append(match_details["Team 1"][j].lower())
            else:
                team2.append(match_details["Team 2"][j].lower())


venue_names=[]
team2_names=[]
venue_num=[]
team2_num=[]
innings_index=[0,1,2]
for g,f in match_details.groupby("Venue"):
    venue_names.append(g.lower())
for i in venue:
    venue_num.append(venue_names.index(i))

for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g.lower())
for i in team2:
    team2_num.append(team2_names.index(i))


data={"Team 2":team2_num,"Runrate":runrate,"Venue":venue_num,"Innings":innings_played}
df=pd.DataFrame(data)



X = df[['Venue', 'Innings',"Team 2"]]
y = df['Runrate']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


knn_reg = KNeighborsRegressor(n_neighbors = 5)
knn_reg.fit(X_train, y_train)
pr=knn_reg.predict(X_test)

mae=round(metrics.mean_absolute_error(y_test, pr),2)
mape=round(metrics.mean_absolute_percentage_error(y_test,pr)*100,2)
print("Error Percentage for Runrate = ",mape)
print("Absolute Error for Runrate = ",mae)

pickle.dump(knn_reg, open('runrate.pkl', 'wb'))
