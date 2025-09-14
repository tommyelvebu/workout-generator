import requests
from app.models.exercise import Exercise

def fetch_exercises():
    url = 'https://www.exercisedb.dev/api/v1/exercises/search?offset=0&limit=10&q=chest%20push&threshold=0.3'
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        exercises = []

        for exercise_data in json_data["data"]:
              exercise = Exercise(
                  exercise_id=exercise_data["exerciseId"],
                  name=exercise_data["name"],
                  gif_url=exercise_data["gifUrl"],
                  target_muscles=exercise_data["targetMuscles"],
                  secondary_muscles=exercise_data["secondaryMuscles"],
                  body_parts=exercise_data["bodyParts"],
                  equipments=exercise_data["equipments"],
                  instructions=exercise_data["instructions"]
              )
              exercises.append(exercise)

        return exercises
    else:
        print(f"API call failed with status code: {response.status_code}")
        return []


