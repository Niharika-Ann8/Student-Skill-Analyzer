from flask import Flask, render_template, request
import pandas as pd
from recommendations import career_recommendations
import csv
from datetime import date 

import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/submit", methods=["POST"])


def submit():

    name = request.form["name"]
    skill = request.form["skill"]
    domain = request.form["domain"]
    hours = float(request.form["hours"])
    today = date.today().strftime("%d/%m/%Y")
    

    supabase.table("your_table_name").insert({
        "name": name,
        "skill": skill,
        "domain": domain,
        "hours": hours,
        "date": today
    }).execute()

    supabase.table("your_table_name").insert({
        "name": name,
        "skill": skill,
        "domain": domain,
        "hours": hours,
        "date": today
    }).execute()

    response = supabase.table("your_table_name").select("*").eq("name", name).execute()
    user_df = pd.DataFrame(response.data)

    if len(user_df) <= 1:
        return render_template(
            "result.html",
            name=name,
            first_time=True,
            best_domain=domain,
            career=career_recommendations[domain]["career"],
            steps=career_recommendations[domain]["next_steps"],
             analysis=None
        ) 

    total_logs = len(user_df)
    domain_logs = user_df.groupby("domain")["domain"].count()
    interest = (domain_logs / total_logs) * 10

    grouped = user_df.groupby("domain").agg({
        "hours": "sum"
    })
    grouped["interest"] = interest
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



