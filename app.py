from flask import Flask, render_template, request
import pandas as pd
import os
from recommendations import career_recommendations
import csv
from datetime import date

app = Flask(__name__)


DATA_FILE = os.path.join("data","data.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])

def submit():

    name = request.form["name"]
    skill = request.form["skill"]
    domain = request.form["domain"]
    hours = float(request.form["hours"])
    interest = float(request.form["interest"])
    today = date.today().strftime("%d/%m/%Y")

    df = pd.read_csv(DATA_FILE)

    new_row = {
        "name": name,
        "skill": skill,
        "domain": domain,
        "hours": hours,
        "interest": interest,
        "date" : today 
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    
    df.to_csv(DATA_FILE, index=False)

    
    user_df = df[df["name"] == name]

    grouped = user_df.groupby("domain").agg({
        "hours": "sum",
        "interest": "mean"
    })

    
    grouped["score"] = grouped["hours"] * grouped["interest"]

    
    best_domain = grouped["score"].idxmax()

    career = career_recommendations[best_domain]["career"]
    steps = career_recommendations[best_domain]["next_steps"]

    analysis = grouped.to_dict()


    return render_template(
        "result.html",
        name=name,
        best_domain=best_domain,
        career=career,
        steps=steps,
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)



>>>>>>> c6aa499f02ba0cceb4f5cd0deea61f5526ce9ce1
