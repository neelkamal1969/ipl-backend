import json
import os
from datetime import datetime
from database import SessionLocal
from models import Match

DATA_DIR = r"C:\Users\neel7\Downloads\Indian_Premier_League_2022-03-26\Indian_Premier_League_2022-03-26\match_info"

db = SessionLocal()

for file in os.listdir(DATA_DIR):
    if not file.endswith(".json"):
        continue

    with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
        data = json.load(f)

        match = Match(
            id=data["match_id"],
            title=data["title"],
            match_number=data["match_number"],
            season=data["competition"]["season"],
            team_a=data["teama"]["short_name"],
            team_b=data["teamb"]["short_name"],
            team_a_score=data["teama"]["scores"],
            team_b_score=data["teamb"]["scores"],
            winner=str(data.get("winning_team_id")),
            result=data["result"],
            venue=data["venue"]["name"],
            city=data["venue"]["location"],
            match_date=datetime.fromisoformat(data["date_start_ist"])
        )

        db.merge(match)

db.commit()
db.close()

print("Data loaded successfully")
