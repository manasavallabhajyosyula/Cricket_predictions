from flask import Flask,  render_template,  url_for,  request
import pickle
import numpy as np
from csv import writer
import pandas as pd
import Strikerate
import Runrate
import Economy
import Wickets
import Team

India_T20=pd.read_csv(r".\data\India T20I.csv",delimiter=",")
India_T20=India_T20.drop(['ball'], axis = 1)
India_T20=India_T20.set_index(["Match ID","Playing Against"])

match_details=pd.read_csv(r".\data\Match details.csv",delimiter=",")
match_details=match_details.drop(['date','Umpire1','Umpire2'],axis=1)


        
venue_names=[]
team2_names=[]
innings_played=[1,2]
batsman_names=[]
over=[]
bowler_names=[]

for g,f in match_details.groupby("Venue"):
    venue_names.append(g.lower())
for g,f in India_T20.groupby("Playing Against"):
    team2_names.append(g.lower())

India_Batting=India_T20[India_T20["Batting"]=="India"]
for group,frame in India_Batting.groupby("Striker"):
    batsman_names.append(group.lower())
for g,f in India_T20.groupby("Over type"):
    over.append(g.lower())

for g,f in India_T20.groupby("Bowler"):
    bowler_names.append(g.lower())

app = Flask(__name__)

runrate_model = pickle.load(open('runrate.pkl',  'rb'))
economy_model = pickle.load(open('economy.pkl',  'rb'))
strikerate_model = pickle.load(open('strikerate.pkl',  'rb'))
wickets_model = pickle.load(open('wickets.pkl',  'rb'))
team_batsman_model=pickle.load(open('team_batsman.pkl', 'rb'))
team_bowler_model=pickle.load(open('team_bowler.pkl', 'rb'))

@app.route('/')
def main():
    return render_template('Main/index.html')

@app.route('/home')
def home():
    return render_template('Main/index.html')

@app.route('/aboutproject')
def aboutproject():
    return render_template('Main/AboutProject.html')

@app.route('/cricket_predictions')
def parameters_prediction():
    return render_template('Main/Cricket Predictions.html')

@app.route('/runrate')
def runrate():
    return render_template('Runrate/Input/Runrate Input.html')

@app.route('/runrate_predict', methods=['GET', 'POST'])
def runrate_predict():
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names)):
        return render_template('Runrate/Input/Runrate Input.html', message="Please give the correct information")
    else:
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[v,innings,o]]
        prediction=[round(runrate_model.predict(data)[0]-(Runrate.mae/2),2),round(runrate_model.predict(data)[0]+(Runrate.mae/2),2)]
        return render_template('Runrate/Output/Runrate Output.html', result=prediction)
        
@app.route('/player_stats')
def player_stats():
    return render_template('Player stats/Player stats.html')

@app.route('/strikerate')
def strikerate():
    return render_template('Player stats/Strikerate/Input/Strikerate Input.html')

@app.route('/strikerate_predict', methods=['GET', 'POST'])
def strikerate_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in batsman_names) or (overtype not in over)):
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    else:
        p=batsman_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=[round(strikerate_model.predict(data)[0]-(Strikerate.mae/2),2),round(strikerate_model.predict(data)[0]+(Strikerate.mae/2),2)]
        return render_template('Player stats/Strikerate/Output/Strikerate Output.html', result=prediction)

@app.route('/economy')
def economy():
    return render_template('Player stats/Economy/Input/Economy Input.html')

@app.route('/economy_predict', methods=['GET', 'POST'])
def economy_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in bowler_names) or (overtype not in over)):
        return render_template('Player stats/Economy/Input/Economy Input.html', message="Please give the correct information")
    else:
        p=bowler_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=[round(economy_model.predict(data)[0]-(Economy.mae/2),2),round(economy_model.predict(data)[0]+(Economy.mae/2),2)]
        return render_template('Player stats/Economy/Output/Economy Output.html', result=prediction)

@app.route('/wickets')
def wickets():
    return render_template('Player stats/Wickets/Input/Wickets Input.html')

@app.route('/wickets_predict', methods=['GET', 'POST'])
def wickets_predict():
    player=request.form['player'].lower()
    venue=request.form['venue'].lower()
    try:
        innings=int(request.form['innings'])
    except ValueError:
        return render_template('Player stats/Strikerate/Input/Strikerate Input.html', message="Please give the correct information")
    opposition=request.form['opposition'].lower()
    overtype=request.form['overtype'].lower()
    if((venue not in venue_names) or (innings not in innings_played) or (opposition not in team2_names) or (player not in bowler_names) or (overtype not in over)):
        return render_template('Player stats/Wickets/Input/Wickets Input.html', message="Please give the correct information")
    else:
        p=bowler_names.index(player)
        ov=over.index(overtype)
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        data=[[p,o,innings,v,ov]]
        prediction=round(wickets_model.predict(data)[0],2)
        return render_template('Player stats/Wickets/Output/Wickets Output.html', result=prediction)

@app.route('/team')
def team():
    return render_template('Team/Input/Team Input.html')

@app.route('/team_predict', methods=['GET', 'POST'])
def team_predict():
    venue=request.form['venue'].lower()
    opposition=request.form['opposition'].lower()
    exp=int(request.form['experience'])
    if((venue not in venue_names) or (opposition not in team2_names)):
        return render_template('Team/Input/Team Input.html', message="Please give the correct information")
    else:
        v=venue_names.index(venue)
        o=team2_names.index(opposition)
        Player_details=pd.read_csv(r"C:.\data\Player_details.csv",delimiter=",")
        Player_details=Player_details[(Player_details["International Status"]!="Retired")&(Player_details["International Status"]!="Banned")]
        Player_details=Player_details[(Player_details["Batting Experience"]>=exp)|(Player_details["Bowling Experience"]>=exp)]
        Player_details=Player_details.drop(['CAP'], axis = 1)
        toporder=Player_details[(Player_details["Role"]=="Batsman")|(Player_details["Role"]=="WK-Batsman")]
        toporder=toporder[toporder["Top Order"]==True]
        top_order_strikerate=[]
        top=[]
        top_order_batsman=[]
        for i in toporder["Player Name"]:
            a=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,0]])[0],2)
            b=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,1]])[0],2)
            c=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,2]])[0],2)
            top_order_strikerate.append([round((a+b+c)/3,2),i])
        top_order_strikerate.sort(reverse=True)
        top_order_strikerate=top_order_strikerate[:4]
        for i in range(len(top_order_strikerate)):
            for j in range(len(toporder["Player Name"])):
                if(toporder["Player Name"].iloc[j]==top_order_strikerate[i][1]):
                    top.append([toporder["Batting Average"].iloc[j],top_order_strikerate[i][1]])
        top.sort(reverse=True)
        try:
            for i in range(3):
                top_order_batsman.append(top[i][1])
        except IndexError:
            pass

        c=0
        for i in top_order_batsman:
            for j in range(len(toporder["Player Name"])):
                if(toporder["Player Name"].iloc[j]==i and toporder["Role"].iloc[j]=="WK-Batsman"):
                    c=1
                    break
        middle_order_batsman=[]
        if(c==1):
            m1=Player_details[(Player_details["Role"]=="Batsman")]
            m1=m1[m1["Top Order"]!=True]
            middle_order_strikerate=[]
            for i in m1["Player Name"]:
                a=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,0]])[0],2)
                b=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,1]])[0],2)
                c=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,2]])[0],2)
                middle_order_strikerate.append([round((a+b+c)/3,2),i])
            middle_order_strikerate.sort(reverse=True)
            try:
                middle_order_batsman.append(middle_order_strikerate[0][1])
                middle_order_batsman.append(middle_order_strikerate[1][1])
            except IndexError:
                pass
        else:
            wk=Player_details[(Player_details["Role"]=="WK-Batsman")]
            wk=wk[wk["Top Order"]!=True]
            wk_strikerate=[]
            for i in wk["Player Name"]:
                a=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,0]])[0],2)
                b=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,1]])[0],2)
                c=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,2]])[0],2)
                wk_strikerate.append([round((a+b+c)/3,2),i])
            wk_strikerate.sort(reverse=True)
            m1=Player_details[(Player_details["Role"]=="Batsman")]
            m1=m1[m1["Top Order"]!=True]
            m1_strikerate=[]
            for i in m1["Player Name"]:
                a=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,0]])[0],2)
                b=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,1]])[0],2)
                c=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,2]])[0],2)
                m1_strikerate.append([round((a+b+c)/3,2),i])
            m1_strikerate.sort(reverse=True)
            try:
                middle_order_batsman.append(wk_strikerate[0][1])
                middle_order_batsman.append(m1_strikerate[0][1])
            except IndexError:
                pass
        allrounder=Player_details[(Player_details["Role"]=="Batting Allrounder")|(Player_details["Role"]=="Bowling Allrounder")]
        allrounder=allrounder[(allrounder["Bowling Experience"]>=exp)&(allrounder["Batting Experience"]>=exp)]
        allrounder_strikerate=[]
        for i in allrounder["Player Name"]:
            a=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,0]])[0],2)
            b=round(team_batsman_model.predict([[batsman_names.index(i.lower()),o,v,1]])[0],2)
            allrounder_strikerate.append([round((a+b)/2,2),i])
        allrounder_strikerate.sort(reverse=True)
        try:
            middle_order_batsman.append(allrounder_strikerate[0][1])
            middle_order_batsman.append(allrounder_strikerate[1][1])
        except IndexError:
            pass
        
        bowlers=[]
        fast=Player_details[(Player_details["Role"]=="Bowler")&(Player_details["Bowling Type"]=="Fast bowler")]
        fast_bowlers_econommy=[]
        fast_bowlers_average=[]
        spin=Player_details[(Player_details["Role"]=="Bowler")&(Player_details["Bowling Type"]=="Spinner")]
        spin_bowlers_econommy=[]
        spin_bowlers_average=[]
        s=0
        for i in range(len(allrounder_strikerate)):
            for j in range(len(allrounder["Player Name"])):
                if(allrounder_strikerate[i][1]==allrounder["Player Name"].iloc[j] and allrounder["Bowling Type"].iloc[j]=="Spinner"):
                    s=s+1
        if(s==0):
            for i in range(len(fast["Player Name"])):
                fast_bowlers_average.append([fast["Bowling Average"].iloc[i],fast["Player Name"].iloc[i]])
            fast_bowlers_average.sort()
            fast_bowlers_average=fast_bowlers_average[:4]
            for i in fast_bowlers_average:
                fast_bowlers_econommy.append([round(team_bowler_model.predict([[bowler_names.index(i[1].lower()),o,v]])[0],2),i[1]])
            fast_bowlers_econommy.sort()
            try:
                for i in range(2):
                    bowlers.append(fast_bowlers_econommy[i][1])
            except IndexError:
                pass
            for i in range(len(spin["Player Name"])):
                spin_bowlers_average.append([spin["Bowling Average"].iloc[i],spin["Player Name"].iloc[i]])
            spin_bowlers_average.sort()
            spin_bowlers_average=spin_bowlers_average[:4]
            for i in spin_bowlers_average:
                spin_bowlers_econommy.append([round(team_bowler_model.predict([[bowler_names.index(i[1].lower()),o,v]])[0],2),i[1]])
            spin_bowlers_econommy.sort()
            try:
                for i in range(2):
                    bowlers.append(spin_bowlers_econommy[i][1])
            except IndexError:
                pass
        else:
            for i in range(len(fast["Player Name"])):
                fast_bowlers_average.append([fast["Bowling Average"].iloc[i],fast["Player Name"].iloc[i]])
            fast_bowlers_average.sort()
            fast_bowlers_average=fast_bowlers_average[:4]
            for i in fast_bowlers_average:
                fast_bowlers_econommy.append([round(team_bowler_model.predict([[bowler_names.index(i[1].lower()),o,v]])[0],2),i[1]])
            fast_bowlers_econommy.sort()
            try:
                for i in range(3):
                    bowlers.append(fast_bowlers_econommy[i][1])
            except IndexError:
                pass
            for i in range(len(spin["Player Name"])):
                spin_bowlers_average.append([spin["Bowling Average"].iloc[i],spin["Player Name"].iloc[i]])
            spin_bowlers_average.sort()
            spin_bowlers_average=spin_bowlers_average[:4]
            for i in spin_bowlers_average:
                spin_bowlers_econommy.append([round(team_bowler_model.predict([[bowler_names.index(i[1].lower()),o,v]])[0],2),i[1]])
            spin_bowlers_econommy.sort()
            try:
                for i in range(1):
                    bowlers.append(spin_bowlers_econommy[i][1])
            except IndexError:
                pass

        team=top_order_batsman+middle_order_batsman+bowlers
        if(len(team)==11):
            return render_template('Team/Output/Team Output.html', result=team)
        else:
            msg="Players are not available with the given experience: "+str(exp)
            return render_template('Team/Input/Team Input.html', message=msg)

@app.errorhandler(400)
def page_not_found(e):
    return render_template("Error/400.html")

@app.errorhandler(401)
def page_not_found1(e):
    return render_template("Error/401.html")

@app.errorhandler(403)
def page_not_found2(e):
    return render_template("Error/403.html")

@app.errorhandler(404)
def page_not_found3(e):
    return render_template("Error/404.html")

@app.errorhandler(408)
def page_not_found4(e):
    return render_template("Error/408.html")

@app.errorhandler(500)
def page_not_found5(e):
    return render_template("Error/500.html")

@app.errorhandler(501)
def page_not_found6(e):
    return render_template("Error/501.html")

@app.errorhandler(503)
def page_not_found7(e):
    return render_template("Error/503.html")


if __name__ == '__main__':
    app.run(debug=True)
