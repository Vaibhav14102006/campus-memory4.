import gradio as gr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time

# Load and prepare model
print("Loading ML Model Dashboard...")
df = pd.read_csv('event_feedback_dataset.csv')

# Prepare features
le_event = LabelEncoder()
le_branch = LabelEncoder()
le_level = LabelEncoder()
le_type = LabelEncoder()
le_gender = LabelEncoder()
le_skill = LabelEncoder()
le_prev = LabelEncoder()

df['event_encoded'] = le_event.fit_transform(df['event_name'])
df['branch_encoded'] = le_branch.fit_transform(df['student_branch'])
df['level_encoded'] = le_level.fit_transform(df['event_level'])
df['type_encoded'] = le_type.fit_transform(df['event_type'])
df['gender_encoded'] = le_gender.fit_transform(df['gender'])
df['skill_encoded'] = le_skill.fit_transform(df['skill_level'])
df['prev_encoded'] = le_prev.fit_transform(df['previous_participation'])

features = ['event_encoded', 'type_encoded', 'level_encoded', 'branch_encoded', 
            'student_year', 'gender_encoded', 'skill_encoded', 'prev_encoded', 
            'team_size', 'participated_alone', 'event_duration_days']

X = df[features]
y = df['overall_satisfaction']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"✓ Model Loaded | Training R²: {train_score:.4f} | Test R²: {test_score:.4f}")


def predict_satisfaction(event_name, branch, year, skill_level, previous_participation, team_size):
    """Real-time ML prediction with visualization"""
    
    # Encode inputs
    event_enc = le_event.transform([event_name])[0]
    branch_enc = le_branch.transform([branch])[0]
    skill_enc = le_skill.transform([skill_level])[0]
    prev_enc = le_prev.transform([previous_participation])[0]
    
    # Get event info
    event_info = df[df['event_name'] == event_name].iloc[0]
    type_enc = le_type.transform([event_info['event_type']])[0]
    level_enc = le_level.transform([event_info['event_level']])[0]
    duration = event_info['event_duration_days']
    
    # Assume student gender for demo
    gender_enc = le_gender.transform(['Male'])[0]
    participated_alone = 1 if team_size == 1 else 0
    
    # Create feature vector
    input_features = np.array([[event_enc, type_enc, level_enc, branch_enc, year, 
                                gender_enc, skill_enc, prev_enc, team_size, 
                                participated_alone, duration]])
    
    # Make prediction
    start_time = time.time()
    prediction = model.predict(input_features)[0]
    pred_time = (time.time() - start_time) * 1000  # in milliseconds
    
    # Get individual tree predictions for confidence
    tree_predictions = [tree.predict(input_features)[0] for tree in model.estimators_]
    confidence = (1 - min(np.std(tree_predictions) / 2, 1)) * 100
    
    # Create visualizations
    
    # 1. Gauge Chart - Predicted Satisfaction
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prediction,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Predicted Satisfaction Score", 'font': {'size': 24}},
        delta={'reference': 7.0, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge={
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 5], 'color': '#fee2e2'},
                {'range': [5, 7], 'color': '#fef3c7'},
                {'range': [7, 10], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    fig_gauge.update_layout(height=400, font={'size': 16})
    
    # 2. Tree Predictions Distribution
    fig_trees = go.Figure()
    fig_trees.add_trace(go.Histogram(
        x=tree_predictions,
        nbinsx=30,
        name='Tree Predictions',
        marker_color='#3b82f6',
        opacity=0.75
    ))
    fig_trees.add_vline(x=prediction, line_dash="dash", line_color="red", line_width=3,
                        annotation_text=f"Final: {prediction:.2f}")
    fig_trees.update_layout(
        title="100 Decision Trees Predictions",
        xaxis_title="Predicted Satisfaction",
        yaxis_title="Number of Trees",
        height=400,
        showlegend=False
    )
    
    # 3. Feature Importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=True).tail(8)
    
    fig_importance = go.Figure(go.Bar(
        x=feature_importance['importance'],
        y=feature_importance['feature'],
        orientation='h',
        marker_color='#8b5cf6'
    ))
    fig_importance.update_layout(
        title="Top Features Driving This Prediction",
        xaxis_title="Importance",
        yaxis_title="Feature",
        height=400
    )
    
    # 4. Confidence Meter
    fig_confidence = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Model Confidence", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "green" if confidence > 70 else "orange" if confidence > 50 else "red"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "#fef3c7"},
                {'range': [75, 100], 'color': "#d1fae5"}
            ],
        }
    ))
    fig_confidence.update_layout(height=400, font={'size': 16})
    
    # Summary text
    summary = f"""
### 🎯 ML Prediction Summary

**Predicted Satisfaction:** {prediction:.2f}/10  
**Model Confidence:** {confidence:.1f}%  
**Processing Time:** {pred_time:.2f}ms  
**Model Accuracy (Test R²):** {test_score:.2%}

---

### 📊 Input Features Processed:
- Event: {event_name}
- Branch: {branch}
- Year: {year}
- Skill: {skill_level}
- Previous Participation: {previous_participation}
- Team Size: {team_size}

---

### 🤖 Model Details:
- **Algorithm:** Random Forest Regressor
- **Estimators:** 100 Decision Trees
- **Training Samples:** {len(X_train):,}
- **Features Used:** {len(features)}

---

### ✅ Status: Model ACTIVE & Predicting
"""
    
    return fig_gauge, fig_trees, fig_importance, fig_confidence, summary


# Get unique values for dropdowns
events = sorted(df['event_name'].unique().tolist())
branches = sorted(df['student_branch'].unique().tolist())
skills = ["Beginner", "Intermediate", "Advanced", "Expert"]
prev_participation = ["None", "Low", "Medium", "High"]

# Create Gradio Dashboard
with gr.Blocks(title="ML Model Dashboard - Real-Time Predictions") as demo:
    gr.Markdown("""
    # 🤖 MACHINE LEARNING MODEL DASHBOARD
    ## Real-Time Satisfaction Prediction System
    **Watch the ML model process inputs and generate predictions with confidence scores!**
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Input Features")
            event_input = gr.Dropdown(choices=events, label="Event Name", value=events[0])
            branch_input = gr.Dropdown(choices=branches, label="Student Branch", value="CSE")
            year_input = gr.Slider(1, 4, value=2, step=1, label="Academic Year")
            skill_input = gr.Dropdown(choices=skills, label="Skill Level", value="Intermediate")
            prev_input = gr.Dropdown(choices=prev_participation, label="Previous Participation", value="Low")
            team_input = gr.Slider(1, 5, value=3, step=1, label="Team Size")
            
            predict_btn = gr.Button("🚀 Run ML Prediction", variant="primary", size="lg")
    
    with gr.Row():
        gauge_output = gr.Plot(label="Predicted Score")
        confidence_output = gr.Plot(label="Model Confidence")
    
    with gr.Row():
        trees_output = gr.Plot(label="Tree Predictions Distribution")
        importance_output = gr.Plot(label="Feature Importance")
    
    with gr.Row():
        summary_output = gr.Markdown()
    
    predict_btn.click(
        fn=predict_satisfaction,
        inputs=[event_input, branch_input, year_input, skill_input, prev_input, team_input],
        outputs=[gauge_output, trees_output, importance_output, confidence_output, summary_output]
    )
    
    # Auto-run on load
    demo.load(
        fn=predict_satisfaction,
        inputs=[event_input, branch_input, year_input, skill_input, prev_input, team_input],
        outputs=[gauge_output, trees_output, importance_output, confidence_output, summary_output]
    )

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 LAUNCHING ML MODEL DASHBOARD")
    print("="*70)
    print("\n🎯 This dashboard shows:")
    print("   • Real-time ML predictions")
    print("   • Confidence scores")
    print("   • Decision tree visualizations")
    print("   • Feature importance")
    print("\n📱 Perfect for demonstrating your ML model in action!\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False,
        inbrowser=True
    )
