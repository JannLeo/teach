import numpy as np
import pandas as pd

file_path='Student List A2.csv'
student_data = pd.read_csv('Student_List_A2.csv')
print("Columns before fillna operation:", student_data.columns)
grade_mapping={0:'A',1:'B',2:'C',3:'D',4:'F'}
student_data['GradeClass']= student_data['GradeClass'].map(grade_mapping).astype(str)
# grade_start ={'A':0,'B':1,'C':2,'D':3,'F':4}
# student_data['GradeClass']= student_data['GradeClass'].map(grade_start)
print("Columns after fillna operation:", student_data.columns)
print("After mapping to numeric values:")
print(student_data['GradeClass'].isnull().sum())  # 查看有多少NaN值
print(student_data['GradeClass'].unique())  # 查看唯一值

# numeric_cols = student_data.select_dtypes(include=[np.number]).columns
# student_data[numeric_cols] = student_data[numeric_cols].fillna(student_data[numeric_cols].median())
# grade_mapping={0:'A',1:'B',2:'C',3:'D',4:'F'}
# student_data['GradeClass']= student_data['GradeClass'].map(grade_mapping).astype(str)
student_data.to_csv(file_path,index=False)