import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("EVENT RECOMMENDATION ML MODEL TRAINING")
print("="*80)

# Load dataset
print("\n[1/8] Loading dataset...")
df = pd.read_csv('event_feedback_dataset.csv')
print(f"Dataset loaded: {df.shape[0]} records, {df.shape[1]} features")

# Feature Engineering
print("\n[2/8] Feature Engineering...")

# Create label encoders
label_encoders = {}
categorical_columns = ['event_name', 'event_type', 'event_level', 'student_branch', 
                       'gender', 'previous_participation', 'skill_level', 'achievement', 'sentiment']

df_encoded = df.copy()

for col in categorical_columns:
    le = LabelEncoder()
    df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col])
    label_encoders[col] = le

# Create additional features
df_encoded['total_experience_score'] = (
    df_encoded['venue_rating'] + df_encoded['organization_rating'] + 
    df_encoded['content_quality'] + df_encoded['mentor_support']
) / 4

df_encoded['facility_score'] = (
    df_encoded['food_quality'] + df_encoded['infrastructure'] + 
    df_encoded['registration_process']
) / 3

df_encoded['engagement_score'] = (
    df_encoded['networking_opportunities'] + df_encoded['time_management'] + 
    df_encoded['learning_outcome']
) / 3

# Feature selection for recommendation prediction
feature_columns = [
    'event_name_encoded', 'event_type_encoded', 'event_level_encoded', 
    'event_duration_days', 'student_branch_encoded', 'student_year', 'student_age',
    'gender_encoded', 'previous_participation_encoded', 'skill_level_encoded',
    'team_size', 'participated_alone', 'achievement_encoded',
    'venue_rating', 'organization_rating', 'content_quality', 'mentor_support',
    'food_quality', 'prize_satisfaction', 'networking_opportunities',
    'time_management', 'infrastructure', 'registration_process', 'learning_outcome',
    'total_experience_score', 'facility_score', 'engagement_score',
    'sentiment_encoded', 'feedback_length', 'suggestions_given'
]

X = df_encoded[feature_columns]
y_recommendation = df_encoded['would_recommend']
y_satisfaction = df_encoded['overall_satisfaction']

print(f"Features prepared: {len(feature_columns)} features")
print(f"Target 1: Recommendation (Classification) - {y_recommendation.value_counts().to_dict()}")
print(f"Target 2: Satisfaction (Regression) - Mean: {y_satisfaction.mean():.2f}")

# Split data
print("\n[3/8] Splitting data (80% train, 20% test)...")
X_train, X_test, y_rec_train, y_rec_test, y_sat_train, y_sat_test = train_test_split(
    X, y_recommendation, y_satisfaction, test_size=0.2, random_state=42, stratify=y_recommendation
)

print(f"Training set: {X_train.shape[0]} records")
print(f"Testing set: {X_test.shape[0]} records")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==================== MODEL 1: RECOMMENDATION CLASSIFIER ====================
print("\n" + "="*80)
print("TASK 1: EVENT RECOMMENDATION PREDICTION (CLASSIFICATION)")
print("="*80)

# Model 1.1: Random Forest
print("\n[4/8] Training Random Forest Classifier...")
rf_classifier = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_classifier.fit(X_train, y_rec_train)
rf_pred = rf_classifier.predict(X_test)
rf_accuracy = accuracy_score(y_rec_test, rf_pred)
print(f"Random Forest Accuracy: {rf_accuracy*100:.2f}%")

# Model 1.2: XGBoost
print("\n[5/8] Training XGBoost Classifier...")
xgb_classifier = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=10,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)
xgb_classifier.fit(X_train, y_rec_train)
xgb_pred = xgb_classifier.predict(X_test)
xgb_accuracy = accuracy_score(y_rec_test, xgb_pred)
print(f"XGBoost Accuracy: {xgb_accuracy*100:.2f}%")

# Model 1.3: Gradient Boosting
print("\n[6/8] Training Gradient Boosting Classifier...")
gb_classifier = GradientBoostingClassifier(
    n_estimators=150,
    max_depth=10,
    learning_rate=0.1,
    random_state=42
)
gb_classifier.fit(X_train, y_rec_train)
gb_pred = gb_classifier.predict(X_test)
gb_accuracy = accuracy_score(y_rec_test, gb_pred)
print(f"Gradient Boosting Accuracy: {gb_accuracy*100:.2f}%")

# Model 1.4: Neural Network
print("\n[7/8] Training Neural Network Classifier...")
nn_classifier = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    max_iter=300,
    random_state=42
)
nn_classifier.fit(X_train_scaled, y_rec_train)
nn_pred = nn_classifier.predict(X_test_scaled)
nn_accuracy = accuracy_score(y_rec_test, nn_pred)
print(f"Neural Network Accuracy: {nn_accuracy*100:.2f}%")

# Select best model
models_comparison = {
    'Random Forest': (rf_accuracy, rf_classifier, rf_pred),
    'XGBoost': (xgb_accuracy, xgb_classifier, xgb_pred),
    'Gradient Boosting': (gb_accuracy, gb_classifier, gb_pred),
    'Neural Network': (nn_accuracy, nn_classifier, nn_pred)
}

best_model_name = max(models_comparison, key=lambda x: models_comparison[x][0])
best_accuracy, best_model, best_pred = models_comparison[best_model_name]

print("\n" + "="*80)
print(f"BEST CLASSIFICATION MODEL: {best_model_name}")
print(f"ACCURACY: {best_accuracy*100:.2f}%")
print("="*80)

print("\nDetailed Classification Report:")
print(classification_report(y_rec_test, best_pred, target_names=['Not Recommend', 'Recommend']))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_rec_test, best_pred)
print(f"True Negatives: {cm[0][0]:,} | False Positives: {cm[0][1]:,}")
print(f"False Negatives: {cm[1][0]:,} | True Positives: {cm[1][1]:,}")

# ==================== MODEL 2: SATISFACTION PREDICTOR ====================
print("\n" + "="*80)
print("TASK 2: SATISFACTION SCORE PREDICTION (REGRESSION)")
print("="*80)

print("\n[8/8] Training Random Forest Regressor for Satisfaction Prediction...")
rf_regressor = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
rf_regressor.fit(X_train, y_sat_train)
sat_pred = rf_regressor.predict(X_test)

# Regression metrics
mse = mean_squared_error(y_sat_test, sat_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_sat_test, sat_pred)
mae = np.mean(np.abs(y_sat_test - sat_pred))

print(f"\nSatisfaction Prediction Performance:")
print(f"  R² Score: {r2*100:.2f}%")
print(f"  RMSE: {rmse:.4f}")
print(f"  MAE: {mae:.4f}")

# Feature importance
print("\n" + "="*80)
print("TOP 15 MOST IMPORTANT FEATURES")
print("="*80)
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': best_model.feature_importances_ if hasattr(best_model, 'feature_importances_') else rf_classifier.feature_importances_
}).sort_values('importance', ascending=False).head(15)

for idx, row in feature_importance.iterrows():
    print(f"{row['feature']:40s} : {row['importance']:.4f}")

# Save models and encoders
print("\n" + "="*80)
print("SAVING MODELS")
print("="*80)

joblib.dump(best_model, 'recommendation_model.pkl')
print("✓ Recommendation model saved: recommendation_model.pkl")

joblib.dump(rf_regressor, 'satisfaction_model.pkl')
print("✓ Satisfaction model saved: satisfaction_model.pkl")

joblib.dump(scaler, 'scaler.pkl')
print("✓ Scaler saved: scaler.pkl")

joblib.dump(label_encoders, 'label_encoders.pkl')
print("✓ Label encoders saved: label_encoders.pkl")

joblib.dump({
    'feature_columns': feature_columns,
    'categorical_columns': categorical_columns,
    'best_model_name': best_model_name,
    'accuracy': best_accuracy,
    'r2_score': r2
}, 'model_metadata.pkl')
print("✓ Model metadata saved: model_metadata.pkl")

# Summary
print("\n" + "="*80)
print("TRAINING SUMMARY")
print("="*80)
print(f"✓ Dataset Size: {df.shape[0]:,} records")
print(f"✓ Best Classification Model: {best_model_name}")
print(f"✓ Classification Accuracy: {best_accuracy*100:.2f}%")
print(f"✓ Regression R² Score: {r2*100:.2f}%")
print(f"✓ Models saved and ready for predictions!")
print("="*80)
