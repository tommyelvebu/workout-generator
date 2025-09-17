import json
from app.database import SessionLocal
from app.models.exercise import Exercise

def seed_exercises():
    session = SessionLocal()

    try:
        if session.query(Exercise).count() > 0:
            print("Exercise already seeded!")
            return
        
        with open("app/data/exercises.json", "r") as file:
            exercises_data = json.load(file)

        for data in exercises_data:
            exercise = Exercise(
                exercise_id = data["exercise_id"],
                exercise_category = data["exercise_category"],
                name = data["name"],
                target_muscles = data["target_muscles"],
                secondary_muscles = data["secondary_muscles"],
                equipments = data["equipments"],
                gym_required = data["gym_required"]
            )
            session.add(exercise)

        session.commit()
        print(f"successfully seeded {len(exercises_data)} exercises!")

    except Exception as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    
    finally:
        session.close()

if __name__ == "__main__":
    seed_exercises()



