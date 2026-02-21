import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Dataset file name
DATASET_FILE = 'event_feedback_dataset.csv'

# Define event types and specific events
events_data = {
    'Hacksetu': {
        'type': 'Hackathon',
        'level': 'National',
        'duration_days': 2,
        'capacity': 500,
        'prizes': 'High',
        'difficulty': 'Hard'
    },
    'Anveshan': {
        'type': 'Hackathon',
        'level': 'University',
        'duration_days': 1,
        'capacity': 300,
        'prizes': 'Medium',
        'difficulty': 'Medium'
    },
    'Ami Chroma': {
        'type': 'Cultural',
        'level': 'University',
        'duration_days': 3,
        'capacity': 1000,
        'prizes': 'Medium',
        'difficulty': 'Easy'
    },
    'Smart India Hackathon': {
        'type': 'Hackathon',
        'level': 'National',
        'duration_days': 3,
        'capacity': 600,
        'prizes': 'Very High',
        'difficulty': 'Very Hard'
    },
    'Init Maths': {
        'type': 'Training',
        'level': 'Department',
        'duration_days': 6,
        'capacity': 100,
        'prizes': 'NA',
        'difficulty': 'Medium'
    },
    'Convocation': {
        'type': 'Ceremony',
        'level': 'University',
        'duration_days': 1,
        'capacity': 2000,
        'prizes': 'NA',
        'difficulty': 'Easy'
    },
    'Code Sprint': {
        'type': 'Hackathon',
        'level': 'University',
        'duration_days': 1,
        'capacity': 200,
        'prizes': 'Low',
        'difficulty': 'Easy'
    },
    'Tech Fest': {
        'type': 'Technical',
        'level': 'University',
        'duration_days': 2,
        'capacity': 800,
        'prizes': 'Medium',
        'difficulty': 'Medium'
    },
    'Workshop AI/ML': {
        'type': 'Workshop',
        'level': 'Department',
        'duration_days': 2,
        'capacity': 150,
        'prizes': 'NA',
        'difficulty': 'Medium'
    },
    'Project Expo': {
        'type': 'Exhibition',
        'level': 'University',
        'duration_days': 1,
        'capacity': 400,
        'prizes': 'Medium',
        'difficulty': 'Medium'
    },
    'Gaming Tournament': {
        'type': 'Gaming',
        'level': 'University',
        'duration_days': 2,
        'capacity': 250,
        'prizes': 'Medium',
        'difficulty': 'Easy'
    }
}

# Student demographics
branches = ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil', 'BBA', 'BCA', 'B.Tech', 'MBA']
years = [1, 2, 3, 4]
genders = ['Male', 'Female', 'Other']
previous_event_participation = ['None', 'Low', 'Medium', 'High']
skills_level = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

# Check if dataset already exists
if os.path.exists(DATASET_FILE):
    print(f"Loading existing dataset from {DATASET_FILE}...")
    df = pd.read_csv(DATASET_FILE)
    print(f"Dataset loaded successfully with {len(df)} records!")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst few records:")
    print(df.head())
    print(f"\nEvent distribution:")
    print(df['event_name'].value_counts())
    print(f"\nOverall satisfaction distribution:")
    print(df['overall_satisfaction'].describe())
    print(f"\nRecommendation rate: {df['would_recommend'].mean()*100:.2f}%")
else:
    print(f"Dataset not found. Generating new dataset...")
    
    # Generate large dataset
    num_records = 100000  # 1 Lakh records

    data = []

    for i in range(num_records):
        # Random student info
        student_id = f"STU{10000 + i}"
        event_name = random.choice(list(events_data.keys()))
        event_info = events_data[event_name]
        
        # Student demographics
        branch = random.choice(branches)
        year = random.choice(years)
        gender = random.choice(genders)
        age = 18 + year + random.randint(-1, 2)
        prev_participation = random.choice(previous_event_participation)
        skill_level = random.choice(skills_level)
        
        # Event date (random dates in past 2 years)
        days_ago = random.randint(1, 730)
        event_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Feedback ratings (1-10 scale)
        # Add some correlation based on event type and student characteristics
        base_rating = random.uniform(5, 9)
        
        # Adjust based on difficulty and skill level
        difficulty_factor = {'Easy': 1.2, 'Medium': 1.0, 'Hard': 0.8, 'Very Hard': 0.6}
        skill_factor = {'Beginner': 0.8, 'Intermediate': 1.0, 'Advanced': 1.1, 'Expert': 1.2}
        
        adjustment = difficulty_factor.get(event_info['difficulty'], 1.0) * skill_factor[skill_level]
        
        venue_rating = max(1, min(10, base_rating + random.uniform(-1.5, 1.5)))
        organization_rating = max(1, min(10, base_rating * adjustment + random.uniform(-1, 1)))
        content_quality = max(1, min(10, base_rating * adjustment + random.uniform(-1.5, 1.5)))
        mentor_support = max(1, min(10, base_rating + random.uniform(-2, 2)))
        food_quality = max(1, min(10, random.uniform(4, 9)))
        prize_satisfaction = max(1, min(10, base_rating + random.uniform(-1, 1.5)))
        networking_opportunities = max(1, min(10, base_rating + random.uniform(-1, 1.5)))
        time_management = max(1, min(10, base_rating + random.uniform(-2, 2)))
        infrastructure = max(1, min(10, base_rating + random.uniform(-1, 1)))
        registration_process = max(1, min(10, random.uniform(6, 10)))
        
        # Overall satisfaction (weighted average)
        overall_satisfaction = (
            organization_rating * 0.2 +
            content_quality * 0.25 +
            mentor_support * 0.15 +
            venue_rating * 0.1 +
            food_quality * 0.05 +
            prize_satisfaction * 0.1 +
            networking_opportunities * 0.1 +
            infrastructure * 0.05
        )
        
        # Would recommend (based on overall satisfaction)
        would_recommend = 1 if overall_satisfaction >= 6.5 else 0
        
        # Likelihood to attend similar event
        attend_similar = max(1, min(10, overall_satisfaction + random.uniform(-1, 1)))
        
        # Learning outcome rating
        learning_outcome = max(1, min(10, content_quality * 0.6 + mentor_support * 0.4 + random.uniform(-1, 1)))
        
        # Feedback text sentiment (simplified)
        if overall_satisfaction >= 8:
            sentiment = 'Very Positive'
            feedback_length = random.randint(100, 300)
        elif overall_satisfaction >= 6.5:
            sentiment = 'Positive'
            feedback_length = random.randint(80, 200)
        elif overall_satisfaction >= 5:
            sentiment = 'Neutral'
            feedback_length = random.randint(50, 150)
        else:
            sentiment = 'Negative'
            feedback_length = random.randint(60, 180)
        
        # Issues faced
        possible_issues = ['None', 'Technical Issues', 'Poor Coordination', 'Timing Issues', 
                          'Venue Problems', 'Food Quality', 'Lack of Mentors', 'Prize Delay',
                          'Communication Gap', 'Registration Issues']
        
        if overall_satisfaction < 6:
            issues = random.sample(possible_issues[1:], k=random.randint(1, 3))
        elif overall_satisfaction < 7.5:
            issues = random.sample(possible_issues, k=random.randint(0, 2))
        else:
            issues = [random.choice(possible_issues[:3])]
        
        issues_faced = ', '.join(issues)
        
        # Suggestions for improvement
        suggestions_given = 1 if random.random() > 0.3 else 0
        
        # Team participation (for hackathons)
        if event_info['type'] == 'Hackathon':
            team_size = random.choice([1, 2, 3, 4, 5])
            participated_alone = 1 if team_size == 1 else 0
        else:
            team_size = 1 if event_info['type'] in ['Training', 'Workshop'] else random.choice([1, 2, 3])
            participated_alone = 1 if team_size == 1 else 0
        
        # Achievement
        achievements = ['Won Prize', 'Runner Up', 'Participation', 'Special Mention', 'No Award']
        if event_info['prizes'] in ['High', 'Very High']:
            achievement = random.choices(achievements, weights=[0.05, 0.08, 0.75, 0.07, 0.05])[0]
        elif event_info['prizes'] == 'Medium':
            achievement = random.choices(achievements, weights=[0.03, 0.05, 0.82, 0.05, 0.05])[0]
        else:
            achievement = random.choices(achievements, weights=[0.01, 0.02, 0.87, 0.05, 0.05])[0]
        
        # Create record
        record = {
            'student_id': student_id,
            'event_name': event_name,
            'event_type': event_info['type'],
            'event_level': event_info['level'],
            'event_duration_days': event_info['duration_days'],
            'event_date': event_date,
            'student_branch': branch,
            'student_year': year,
            'student_age': age,
            'gender': gender,
            'previous_participation': prev_participation,
            'skill_level': skill_level,
            'team_size': team_size,
            'participated_alone': participated_alone,
            'achievement': achievement,
            
            # Ratings
            'venue_rating': round(venue_rating, 2),
            'organization_rating': round(organization_rating, 2),
            'content_quality': round(content_quality, 2),
            'mentor_support': round(mentor_support, 2),
            'food_quality': round(food_quality, 2),
            'prize_satisfaction': round(prize_satisfaction, 2),
            'networking_opportunities': round(networking_opportunities, 2),
            'time_management': round(time_management, 2),
            'infrastructure': round(infrastructure, 2),
            'registration_process': round(registration_process, 2),
            'learning_outcome': round(learning_outcome, 2),
            
            # Overall metrics
            'overall_satisfaction': round(overall_satisfaction, 2),
            'would_recommend': would_recommend,
            'attend_similar_event': round(attend_similar, 2),
            
            # Feedback details
            'sentiment': sentiment,
            'feedback_length': feedback_length,
            'issues_faced': issues_faced,
            'suggestions_given': suggestions_given,
            
            # Timestamp
            'feedback_submitted_date': event_date
        }
        
        data.append(record)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(DATASET_FILE, index=False)
    print(f"Dataset generated successfully with {len(df)} records!")
    print(f"Dataset saved to {DATASET_FILE}")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nFirst few records:")
    print(df.head())
    print(f"\nDataset info:")
    print(df.info())
    print(f"\nBasic statistics:")
    print(df.describe())
    print(f"\nEvent distribution:")
    print(df['event_name'].value_counts())
    print(f"\nOverall satisfaction distribution:")
    print(df['overall_satisfaction'].describe())
    print(f"\nRecommendation rate: {df['would_recommend'].mean()*100:.2f}%")
