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
    days_per_week: str = Form(None),
    muscle_focus: str = Form(None),
    gym_access: str = Form(None)
):
    from app.services.generator import generate_workout
    
    # Validate form inputs
    errors = []
    
    if not days_per_week or days_per_week == "":
        errors.append("Please select how many days per week you want to workout.")
    
    if not muscle_focus or muscle_focus == "":
        errors.append("Please select which muscle group to focus on.")
    
    if not gym_access or gym_access == "":
        errors.append("Please select whether you have gym access.")
    
    # If there are validation errors, return the form with error messages
    if errors:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "errors": errors
        })
    
    # Convert string inputs to proper types
    try:
        days_per_week = int(days_per_week)
        gym_access = gym_access.lower() == "true"
    except ValueError:
        errors.append("Invalid input values. Please try again.")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "errors": errors
        })

    workout = generate_workout(days_per_week, muscle_focus, gym_access)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "workout": workout,
        "days_per_week": days_per_week,
        "muscle_focus": muscle_focus,
        "gym_access": gym_access
    })
