import pandas as pd

def recommend_course(title, df, cosine_sim_mat, numrec=10):
    course_index = pd.Series(df.index, index=df['course title']).drop_duplicates()
    try:
        index = int(course_index[title])
    except KeyError:
        return {"error": f"Course title '{title}' not found in dataset."}

    scores = list(enumerate(cosine_sim_mat[index]))
    sorted_score = sorted(scores, key=lambda x: x[1], reverse=True)
    selected_course_index = [i[0] for i in sorted_score[1:numrec+1]]
    selected_course_score = [i[1] for i in sorted_score[1:numrec+1]]
    rec_df = df.iloc[selected_course_index]
    rec_df['similarity_score'] = selected_course_score
    final_recommended_courses = rec_df[['course title', 'similarity_score', 'course url', 'Ratings']]
    return final_recommended_courses.to_dict(orient='records')



