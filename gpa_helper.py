import pandas as pd

def recommend_courses(gpa_dict, course_df):
    std = pd.DataFrame({'Student': ['Ali']})
    for course, gpa in gpa_dict.items():
        std[course] = gpa

    melted_df = std.melt(var_name='course', value_name='GPA')[1:]

    low_gpa_students = melted_df[melted_df['GPA'] <= 2.5]

    result = pd.merge(low_gpa_students, course_df, left_on='course', right_on='course title')

    return result[['course title', 'GPA', 'course url']]
