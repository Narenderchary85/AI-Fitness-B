from bson import ObjectId

def serialize_mongo(doc):
    if not doc:
        return doc
    doc = dict(doc)
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

def build_plan_prompt(user):
    return f"""
You are an AI fitness coach. Generate a structured workout & diet plan.

Return JSON EXACTLY in this format:

{{
  "workout_plan": {{
    "days": [
      {{
        "day": "Day 1",
        "exercises": [
          {{
            "name": "",
            "sets": "",
            "reps": "",
            "rest": "",
            "notes": ""
          }}
        ]
      }}
    ]
  }},
  "diet_plan": {{
    "breakfast": "",
    "lunch": "",
    "dinner": "",
    "snacks": ""
  }}
}}

User Details:
Name: {user['name']}
Age: {user['age']}
Gender: {user['gender']}
Height: {user['height']}
Weight: {user['weight']}
Goal: {user['goal']}
Fitness Level: {user['fitness_level']}
Diet Preferences: {user['diet']}
Workout Location: {user['location']}
"""
