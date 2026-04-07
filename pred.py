import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ---------------- STEP 1: LOAD & SHUFFLE DATA ----------------
file_name = "traffic_data_fast_5000.csv"
df = pd.read_csv(file_name)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle rows

# ---------------- STEP 2: DEFINE FEATURES & TARGET ----------------
y = df["Green_Lane"]  # target

# Remove leaky columns like 'Green_Time' and potentially overly predictive columns
X = df[[
    "L1_Density","L2_Density","L3_Density","L4_Density",
    "L1_Wait","L2_Wait","L3_Wait","L4_Wait",
    "Emergency_Type","Reason"
]]

# ---------------- STEP 3: ENCODE CATEGORICAL ----------------
le_emergency = LabelEncoder()
X["Emergency_Type"] = le_emergency.fit_transform(X["Emergency_Type"])

le_reason = LabelEncoder()
X["Reason"] = le_reason.fit_transform(X["Reason"])

le_green = LabelEncoder()
y = le_green.fit_transform(y)

# ---------------- STEP 4: TRAIN/TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------- STEP 5: TRAIN MODEL ----------------
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# ---------------- STEP 6: PREDICT & EVALUATE ----------------
y_pred = model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ---------------- STEP 7: FEATURE IMPORTANCE (Optional) ----------------
importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nFeature Importances:\n", importances)