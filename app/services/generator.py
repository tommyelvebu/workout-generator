from app.database import SessionLocal
from app.models.exercise import Exercise
import random

#Predefined muscle group targets which needs to be hit at least once

#Legs exercises
def is_legs_exercise(exercise):
    all_muscles = exercise.target_muscles + exercise.secondary_muscles
    return "legs" in all_muscles

#Back exercises  
def is_back_exercise(exercise):
    all_muscles = exercise.target_muscles + exercise.secondary_muscles
    return "back" in all_muscles

#Chest exercises
def is_chest_exercise(exercise):
    all_muscles = exercise.target_muscles + exercise.secondary_muscles
    return "chest" in all_muscles

#Selected muscle focus
def get_muscle_focus_exercise(muscle_focus, legs_cat2, back_cat2, chest_cat2, legs_cat3, back_cat3, chest_cat3, category_2_exercises, category_3_exercises):
    if muscle_focus == "Chest":
        # Randomly choose between category 2 and 3 chest exercises
        chest_pool = chest_cat2 + chest_cat3
        return random.choice(chest_pool) if chest_pool else random.choice(category_2_exercises + category_3_exercises)
    elif muscle_focus == "Back":
        back_pool = back_cat2 + back_cat3
        return random.choice(back_pool) if back_pool else random.choice(category_2_exercises + category_3_exercises)
    elif muscle_focus == "Legs":
        legs_pool = legs_cat2 + legs_cat3
        return random.choice(legs_pool) if legs_pool else random.choice(category_2_exercises + category_3_exercises)
    else:
        return random.choice(category_2_exercises + category_3_exercises)

#Get deadlift specifically for back focus
def get_deadlift_exercise(back_cat1):
    deadlift_exercises = [ex for ex in back_cat1 if "deadlift" in ex.name.lower()]
    if deadlift_exercises:
        return random.choice(deadlift_exercises)
    return None







#Generate a workout program based on user inputs
def generate_workout(days_per_week: int, muscle_focus: str, gym_access: bool):
    session = SessionLocal()
    
    #Determine if gym access or no, for filtering exercises
    if gym_access:
        available_exercises = session.query(Exercise).all()
    else:
        available_exercises = session.query(Exercise).filter(Exercise.gym_required == False).all()
    
    #Categorize relevant exercises into category 1, 2, and 3
    category_1_exercises = [ex for ex in available_exercises if ex.exercise_category == 1]
    category_2_exercises = [ex for ex in available_exercises if ex.exercise_category == 2]
    category_3_exercises = [ex for ex in available_exercises if ex.exercise_category == 3]

    legs_category_1 = [ex for ex in category_1_exercises if is_legs_exercise(ex)]
    back_category_1 = [ex for ex in category_1_exercises if is_back_exercise(ex)]
    chest_category_1 = [ex for ex in category_1_exercises if is_chest_exercise(ex)]

    legs_category_2 = [ex for ex in category_2_exercises if is_legs_exercise(ex)]
    back_category_2 = [ex for ex in category_2_exercises if is_back_exercise(ex)]
    chest_category_2 = [ex for ex in category_2_exercises if is_chest_exercise(ex)]
    
    legs_category_3 = [ex for ex in category_3_exercises if is_legs_exercise(ex)]
    back_category_3 = [ex for ex in category_3_exercises if is_back_exercise(ex)]
    chest_category_3 = [ex for ex in category_3_exercises if is_chest_exercise(ex)]

    #If user wants to workout once per week
    if days_per_week == 1:
        selected_exercises = []
        
        # Add the 3 main category 1 exercises, ensuring deadlift for back focus
        if muscle_focus == "Back":
            deadlift = get_deadlift_exercise(back_category_1)
            if deadlift:
                selected_exercises.append(deadlift)
            else:
                selected_exercises.append(random.choice(back_category_1))
        else:
            selected_exercises.append(random.choice(back_category_1))
            
        selected_exercises.append(random.choice(legs_category_1))
        selected_exercises.append(random.choice(chest_category_1))
        
        # Add muscle focus exercise
        selected_exercises.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))
        
        return {"day_1": selected_exercises}
    
    #If user wants to workout twice per week
    elif days_per_week == 2:
        selected_exercises_day_1 = []
        selected_exercises_day_2 = []
        
        # Day 1: Legs + Back focus
        selected_exercises_day_1.append(random.choice(legs_category_1))
        if muscle_focus == "Back":
            deadlift = get_deadlift_exercise(back_category_1)
            if deadlift:
                selected_exercises_day_1.append(deadlift)
            else:
                selected_exercises_day_1.append(random.choice(back_category_1))
        else:
            selected_exercises_day_1.append(random.choice(back_category_1))
        selected_exercises_day_1.append(random.choice(legs_category_2 + legs_category_3))
        selected_exercises_day_1.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))
        
        # Day 2: Chest + Back focus 
        selected_exercises_day_2.append(random.choice(chest_category_1))
        selected_exercises_day_2.append(random.choice(back_category_1))
        selected_exercises_day_2.append(random.choice(chest_category_2 + chest_category_3))
        selected_exercises_day_2.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))
        
        return {"day_1": selected_exercises_day_1, "day_2": selected_exercises_day_2}

    elif days_per_week == 3:
        selected_exercises_day_1 = []
        selected_exercises_day_2 = []
        selected_exercises_day_3 = []
        
        # Day 1: Legs focused
        selected_exercises_day_1.append(random.choice(legs_category_1))
        selected_exercises_day_1.append(random.choice(legs_category_2 + legs_category_3))
        selected_exercises_day_1.append(random.choice(back_category_2 + back_category_3))
        selected_exercises_day_1.append(random.choice(chest_category_2 + chest_category_3))
        selected_exercises_day_1.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))

        # Day 2: Back focused - guarantee deadlift if back is muscle focus
        if muscle_focus == "Back":
            deadlift = get_deadlift_exercise(back_category_1)
            if deadlift:
                selected_exercises_day_2.append(deadlift)
            else:
                selected_exercises_day_2.append(random.choice(back_category_1))
        else:
            selected_exercises_day_2.append(random.choice(back_category_1))
        selected_exercises_day_2.append(random.choice(back_category_2 + back_category_3))
        selected_exercises_day_2.append(random.choice(legs_category_2 + legs_category_3))
        selected_exercises_day_2.append(random.choice(chest_category_2 + chest_category_3))
        selected_exercises_day_2.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))

        # Day 3: Chest focused
        selected_exercises_day_3.append(random.choice(chest_category_1))
        selected_exercises_day_3.append(random.choice(chest_category_2 + chest_category_3))
        selected_exercises_day_3.append(random.choice(legs_category_2 + legs_category_3))
        selected_exercises_day_3.append(random.choice(back_category_2 + back_category_3))
        selected_exercises_day_3.append(get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises))
        
        return {"day_1": selected_exercises_day_1, "day_2": selected_exercises_day_2, "day_3": selected_exercises_day_3}
    
    session.close()
