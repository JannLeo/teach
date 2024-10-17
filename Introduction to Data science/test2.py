from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
file_path='Student List A2.csv'
student_data = pd.read_csv('Student_List_A2.csv')
# print("Columns before fillna operation:", student_data.columns)
grade_mapping={0:'A',1:'B',2:'C',3:'D',4:'F'}
student_data['GradeClass']= student_data['GradeClass'].map(grade_mapping).astype(str)
# 假设数据集已经加载到 student_data 数据框中
# student_data = pd.read_csv('your_dataset.csv') # 如果数据集是从文件加载的
# 分离特征和标签
X = student_data.drop(['StudentID', 'GradeClass', 'GPA'], axis=1)  # 特征
y = student_data['GradeClass']  # 标签

# 划分训练集和测试集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化数据
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# 创建决策树模型
dt_model = DecisionTreeClassifier(random_state=45)

# 训练模型
dt_model.fit(X_train_scaled, y_train)

# 预测
y_pred_dt = dt_model.predict(X_test_scaled)

# 评估模型性能
print("决策树分类模型性能评估：")
print("准确率：", accuracy_score(y_test, y_pred_dt))
print("混淆矩阵：\n", confusion_matrix(y_test, y_pred_dt))
print("分类报告：\n", classification_report(y_test, y_pred_dt))
