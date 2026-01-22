from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, engine
from models import Base, Match
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="IPL Data Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}


#_________________________________________________________________

@app.get("/matches")
def get_matches(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    team: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Match)

    if team:
        query = query.filter(
            (Match.team_a == team.upper()) | (Match.team_b == team.upper())
        )

    total = query.count()

    matches = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": matches
    }

#______________________________________________________


@app.get("/stats/wins-by-team")
def wins_by_team(db: Session = Depends(get_db)):
    results = (
        db.query(Match.winner, func.count(Match.id))
        .group_by(Match.winner)
        .all()
    )

    return {winner: count for winner, count in results if winner}


#____________________________________________

@app.get("/stats/matches-by-venue")
def matches_by_venue(db: Session = Depends(get_db)):
    results = (
        db.query(Match.venue, func.count(Match.id))
        .group_by(Match.venue)
        .all()
    )

    return {venue: count for venue, count in results}
