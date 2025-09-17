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

#Helper function to select unique exercise from a list, avoiding duplicates
def select_unique_exercise(exercise_list, selected_exercises):
    available_exercises = [ex for ex in exercise_list if ex not in selected_exercises]
    if available_exercises:
        return random.choice(available_exercises)
    else:
        # If all exercises in the list are already selected, return a random one anyway
        return random.choice(exercise_list) if exercise_list else None







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
            elif back_category_1:
                selected_exercises.append(select_unique_exercise(back_category_1, selected_exercises))
            else:
                # Fallback to category 2+3 back exercises if no category 1 back exercises
                selected_exercises.append(select_unique_exercise(back_category_2 + back_category_3, selected_exercises))
        else:
            if back_category_1:
                selected_exercises.append(select_unique_exercise(back_category_1, selected_exercises))
            else:
                selected_exercises.append(select_unique_exercise(back_category_2 + back_category_3, selected_exercises))
            
        if legs_category_1:
            legs_exercise = select_unique_exercise(legs_category_1, selected_exercises)
            if legs_exercise:
                selected_exercises.append(legs_exercise)
        else:
            legs_exercise = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises)
            if legs_exercise:
                selected_exercises.append(legs_exercise)
            
        if chest_category_1:
            chest_exercise = select_unique_exercise(chest_category_1, selected_exercises)
            if chest_exercise:
                selected_exercises.append(chest_exercise)
        else:
            chest_exercise = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises)
            if chest_exercise:
                selected_exercises.append(chest_exercise)
        
        # Add muscle focus exercise
        focus_exercise = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_exercise and focus_exercise not in selected_exercises:
            selected_exercises.append(focus_exercise)
        elif focus_exercise:
            # If the focus exercise is a duplicate, try to find a unique one from the same pool
            focus_pool = []
            if muscle_focus == "Chest":
                focus_pool = chest_category_2 + chest_category_3
            elif muscle_focus == "Back":
                focus_pool = back_category_2 + back_category_3
            elif muscle_focus == "Legs":
                focus_pool = legs_category_2 + legs_category_3
            else:
                focus_pool = category_2_exercises + category_3_exercises
            
            unique_focus = select_unique_exercise(focus_pool, selected_exercises)
            if unique_focus:
                selected_exercises.append(unique_focus)
        
        return {"day_1": selected_exercises}
    
    #If user wants to workout twice per week
    elif days_per_week == 2:
        selected_exercises_day_1 = []
        selected_exercises_day_2 = []
        
        # Day 1: Legs + Back focus
        if legs_category_1:
            legs_ex = select_unique_exercise(legs_category_1, selected_exercises_day_1)
            if legs_ex:
                selected_exercises_day_1.append(legs_ex)
        else:
            legs_ex = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_1)
            if legs_ex:
                selected_exercises_day_1.append(legs_ex)
            
        if muscle_focus == "Back":
            deadlift = get_deadlift_exercise(back_category_1)
            if deadlift and deadlift not in selected_exercises_day_1:
                selected_exercises_day_1.append(deadlift)
            elif back_category_1:
                back_ex = select_unique_exercise(back_category_1, selected_exercises_day_1)
                if back_ex:
                    selected_exercises_day_1.append(back_ex)
            else:
                back_ex = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_1)
                if back_ex:
                    selected_exercises_day_1.append(back_ex)
        else:
            if back_category_1:
                back_ex = select_unique_exercise(back_category_1, selected_exercises_day_1)
                if back_ex:
                    selected_exercises_day_1.append(back_ex)
            else:
                back_ex = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_1)
                if back_ex:
                    selected_exercises_day_1.append(back_ex)
                    
        legs_ex2 = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_1)
        if legs_ex2:
            selected_exercises_day_1.append(legs_ex2)
            
        focus_ex = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_ex and focus_ex not in selected_exercises_day_1:
            selected_exercises_day_1.append(focus_ex)
        
        # Day 2: Chest + Back focus 
        if chest_category_1:
            chest_ex = select_unique_exercise(chest_category_1, selected_exercises_day_2)
            if chest_ex:
                selected_exercises_day_2.append(chest_ex)
        else:
            chest_ex = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_2)
            if chest_ex:
                selected_exercises_day_2.append(chest_ex)
            
        if back_category_1:
            back_ex2 = select_unique_exercise(back_category_1, selected_exercises_day_2)
            if back_ex2:
                selected_exercises_day_2.append(back_ex2)
        else:
            back_ex2 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_2)
            if back_ex2:
                selected_exercises_day_2.append(back_ex2)
                
        chest_ex2 = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_2)
        if chest_ex2:
            selected_exercises_day_2.append(chest_ex2)
            
        focus_ex2 = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_ex2 and focus_ex2 not in selected_exercises_day_2:
            selected_exercises_day_2.append(focus_ex2)
        
        return {"day_1": selected_exercises_day_1, "day_2": selected_exercises_day_2}

    elif days_per_week == 3:
        selected_exercises_day_1 = []
        selected_exercises_day_2 = []
        selected_exercises_day_3 = []
        
        # Day 1: Legs focused
        if legs_category_1:
            legs_ex1 = select_unique_exercise(legs_category_1, selected_exercises_day_1)
            if legs_ex1:
                selected_exercises_day_1.append(legs_ex1)
        else:
            legs_ex1 = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_1)
            if legs_ex1:
                selected_exercises_day_1.append(legs_ex1)
                
        legs_ex2 = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_1)
        if legs_ex2:
            selected_exercises_day_1.append(legs_ex2)
            
        back_ex1 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_1)
        if back_ex1:
            selected_exercises_day_1.append(back_ex1)
            
        chest_ex1 = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_1)
        if chest_ex1:
            selected_exercises_day_1.append(chest_ex1)
            
        focus_ex1 = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_ex1 and focus_ex1 not in selected_exercises_day_1:
            selected_exercises_day_1.append(focus_ex1)

        # Day 2: Back focused - guarantee deadlift if back is muscle focus
        if muscle_focus == "Back":
            deadlift = get_deadlift_exercise(back_category_1)
            if deadlift and deadlift not in selected_exercises_day_2:
                selected_exercises_day_2.append(deadlift)
            elif back_category_1:
                back_ex2 = select_unique_exercise(back_category_1, selected_exercises_day_2)
                if back_ex2:
                    selected_exercises_day_2.append(back_ex2)
            else:
                back_ex2 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_2)
                if back_ex2:
                    selected_exercises_day_2.append(back_ex2)
        else:
            if back_category_1:
                back_ex2 = select_unique_exercise(back_category_1, selected_exercises_day_2)
                if back_ex2:
                    selected_exercises_day_2.append(back_ex2)
            else:
                back_ex2 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_2)
                if back_ex2:
                    selected_exercises_day_2.append(back_ex2)
                    
        back_ex3 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_2)
        if back_ex3:
            selected_exercises_day_2.append(back_ex3)
            
        legs_ex3 = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_2)
        if legs_ex3:
            selected_exercises_day_2.append(legs_ex3)
            
        chest_ex2 = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_2)
        if chest_ex2:
            selected_exercises_day_2.append(chest_ex2)
            
        focus_ex2 = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_ex2 and focus_ex2 not in selected_exercises_day_2:
            selected_exercises_day_2.append(focus_ex2)

        # Day 3: Chest focused
        if chest_category_1:
            chest_ex3 = select_unique_exercise(chest_category_1, selected_exercises_day_3)
            if chest_ex3:
                selected_exercises_day_3.append(chest_ex3)
        else:
            chest_ex3 = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_3)
            if chest_ex3:
                selected_exercises_day_3.append(chest_ex3)
                
        chest_ex4 = select_unique_exercise(chest_category_2 + chest_category_3, selected_exercises_day_3)
        if chest_ex4:
            selected_exercises_day_3.append(chest_ex4)
            
        legs_ex4 = select_unique_exercise(legs_category_2 + legs_category_3, selected_exercises_day_3)
        if legs_ex4:
            selected_exercises_day_3.append(legs_ex4)
            
        back_ex4 = select_unique_exercise(back_category_2 + back_category_3, selected_exercises_day_3)
        if back_ex4:
            selected_exercises_day_3.append(back_ex4)
            
        focus_ex3 = get_muscle_focus_exercise(muscle_focus, legs_category_2, back_category_2, chest_category_2, legs_category_3, back_category_3, chest_category_3, category_2_exercises, category_3_exercises)
        if focus_ex3 and focus_ex3 not in selected_exercises_day_3:
            selected_exercises_day_3.append(focus_ex3)
        
        return {"day_1": selected_exercises_day_1, "day_2": selected_exercises_day_2, "day_3": selected_exercises_day_3}
    
    session.close()
