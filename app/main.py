from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="frontend/templates")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/exercises")
def get_all_exercises():
    from app.database import SessionLocal
    from app.models.exercise import Exercise

    session = SessionLocal()
    exercises = session.query(Exercise).all()
    session.close()

    return {"count": len(exercises), "exercises": [{"name": ex.name, "category": ex.exercise_category} for ex in exercises]}


@app.post("/generate-workout")
def create_workout(
    request: Request,
    days_per_week: int = Form(),
    muscle_focus: str = Form(),
    gym_access: bool = Form()
):
    from app.services.generator import generate_workout

    workout = generate_workout(days_per_week, muscle_focus, gym_access)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "workout": workout,
        "days_per_week": days_per_week,
        "muscle_focus": muscle_focus,
        "gym_access": gym_access
    })
