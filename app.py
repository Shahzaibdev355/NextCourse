
from flask import Flask, request, jsonify
import pickle
import pandas as pd

from helper import recommend_course
from gpa_helper import recommend_courses



app = Flask(__name__)


# Model search recommendation file

with open("recommendation_model.pkl", "rb") as file:
    similarity_model = pickle.load(file)

df = similarity_model['df']
cosine_sim_mat = similarity_model['cosine_sim_mat']



# Model course recommendation file
with open("course_recommendation_pipeline.pkl", "rb") as file:
    gpa_pipeline = pickle.load(file)

course_df = gpa_pipeline['course']




# API 1: Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend is running!"})



# API 2: Course Recommendation by Similarity
@app.route('/api/recommend_by_similarity', methods=['POST'])
def recommend_by_similarity():
    data = request.get_json()
    course_title = data.get('course_title')

    if not course_title:
        return jsonify({"error": "Please provide a course_name"}), 400

    recommendations = recommend_course(course_title, df, cosine_sim_mat)
    return jsonify(recommendations)




# API 3: GPA-based Course Recommendation
@app.route('/api/recommend_by_gpa', methods=['POST'])
def recommend_by_gpa():
    data = request.get_json()
    user_gpa = data.get('user_gpa')

    if not user_gpa:
        return jsonify({"error": "Please provide user_gpa as a dictionary."}), 400

    try:
        recommendations = recommend_courses(user_gpa, course_df)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(recommendations.to_dict(orient='records'))




# Run app
if __name__ == "__main__":
    app.run(debug=True)
