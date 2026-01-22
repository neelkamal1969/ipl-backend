from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    match_number = Column(String)
    season = Column(String)
    team_a = Column(String)
    team_b = Column(String)
    team_a_score = Column(String)
    team_b_score = Column(String)
    winner = Column(String)
    result = Column(String)
    venue = Column(String)
    city = Column(String)
    match_date = Column(DateTime)
