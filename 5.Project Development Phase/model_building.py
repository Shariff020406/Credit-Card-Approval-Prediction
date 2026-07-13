import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv(
    r"C:\Users\SHAIK AHMED SHARIFF\Downloads\archive (1)\application_record.csv"
)

# --------------------------------------------------
# Select Features
# --------------------------------------------------

df = df[
    ['NAME_INCOME_TYPE',
     'NAME_EDUCATION_TYPE',
     'AMT_INCOME_TOTAL']
].copy()

# Encode categorical columns

le1 = LabelEncoder()
le2 = LabelEncoder()

df['NAME_INCOME_TYPE'] = le1.fit_transform(
    df['NAME_INCOME_TYPE']
)

df['NAME_EDUCATION_TYPE'] = le2.fit_transform(
    df['NAME_EDUCATION_TYPE']
)

# Demo target (replace with real target if available)

df['TARGET'] = (
    df['AMT_INCOME_TOTAL'] >= 200000
).astype(int)

# --------------------------------------------------
# Features and Target
# --------------------------------------------------

X = df[
    ['NAME_INCOME_TYPE',
     'NAME_EDUCATION_TYPE',
     'AMT_INCOME_TOTAL']
]

y = df['TARGET']

# --------------------------------------------------
# Train Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# --------------------------------------------------
# Logistic Regression
# --------------------------------------------------

lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

print("\n===== Logistic Regression =====")
print("Accuracy:", accuracy_score(y_test, lr_pred))

# --------------------------------------------------
# Decision Tree
# --------------------------------------------------

dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

dt_pred = dt_model.predict(X_test)

print("\n===== Decision Tree =====")
print("Accuracy:", accuracy_score(y_test, dt_pred))

# --------------------------------------------------
# Random Forest
# --------------------------------------------------

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

print("\n===== Random Forest =====")
print("Accuracy:", accuracy_score(y_test, rf_pred))

# --------------------------------------------------
# Save Best Model
# --------------------------------------------------

joblib.dump(rf_model, 'credit_card_model.pkl')

print("\nModel saved successfully!")