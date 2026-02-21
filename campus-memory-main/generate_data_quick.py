"""
Quick Data Generation Script
Generate 100k rows of synthetic training data for ML models
Can run independently without training
"""

print("=" * 80)
print("📊 SYNTHETIC TRAINING DATA GENERATION")
print("=" * 80)

import os
import random
import json
import pandas as pd
from datetime import datetime, timedelta

# Create training_data directory
os.makedirs("training_data", exist_ok=True)

# Event categories and schools
EVENT_CATEGORIES = [
    "Technical", "Workshop", "Cultural", "Sports", 
    "Career", "Awareness", "Webinar"
]

AMITY_SCHOOLS = [
    "Amity School of Engineering & Technology",
    "Amity School of Business",
    "Amity School of Communication",
    "Amity School of Computer Science",
    "Amity School of Architecture & Planning",
    "Amity School of Fine Arts",
    "Amity School of Law",
    "Amity School of Applied Sciences",
    "Amity School of Biotechnology",
    "Amity School of Hospitality",
    "Amity School of Liberal Arts",
    "Amity School of Design"
]

# Keywords for each category
CATEGORY_KEYWORDS = {
    "Technical": ["hackathon", "coding", "AI", "ML", "tech", "programming", "software", "development"],
    "Workshop": ["workshop", "training", "session", "learn", "skill", "hands-on", "tutorial"],
    "Cultural": ["cultural", "fest", "dance", "music", "art", "talent", "performance"],
    "Sports": ["sports", "tournament", "match", "cricket", "football", "athletics", "game"],
    "Career": ["career", "placement", "job", "internship", "recruitment", "interview", "skills"],
    "Awareness": ["awareness", "social", "campaign", "health", "environment", "sustainability"],
    "Webinar": ["webinar", "online", "virtual", "session", "talk", "seminar", "discussion"]
}

print("\n📝 Generating Category Classification Dataset...")
print("-" * 80)

# Generate category classification data
category_data = []
rows_per_category = 100000 // len(EVENT_CATEGORIES)

for category in EVENT_CATEGORIES:
    keywords = CATEGORY_KEYWORDS[category]
    for i in range(rows_per_category):
        # Generate synthetic text
        num_keywords = random.randint(2, 5)
        selected_keywords = random.sample(keywords, min(num_keywords, len(keywords)))
        
        text = f"Join us for an exciting {category.lower()} event! "
        text += " ".join(selected_keywords)
        text += f" Register now for this amazing {category.lower()} opportunity!"
        
        category_data.append({
            "text": text,
            "category": category
        })

# Shuffle and split
random.shuffle(category_data)
split = int(len(category_data) * 0.8)

train_df = pd.DataFrame(category_data[:split])
val_df = pd.DataFrame(category_data[split:])

train_df.to_csv("training_data/category_train.csv", index=False)
val_df.to_csv("training_data/category_val.csv", index=False)

print(f"✅ Generated {len(train_df):,} training samples")
print(f"✅ Generated {len(val_df):,} validation samples")

print("\n📝 Generating School Classification Dataset...")
print("-" * 80)

# Generate school classification data
school_data = []
rows_per_school = 100000 // len(AMITY_SCHOOLS)

for school in AMITY_SCHOOLS:
    for i in range(rows_per_school):
        # Generate synthetic text mentioning the school
        text = f"Event organized by {school}. "
        text += f"Students from {school} are invited. "
        text += random.choice([
            "Amazing opportunity!",
            "Don't miss out!",
            "Register today!",
            "Limited seats available!"
        ])
        
        school_data.append({
            "text": text,
            "school": school
        })

# Shuffle and split
random.shuffle(school_data)
split = int(len(school_data) * 0.8)

train_df = pd.DataFrame(school_data[:split])
val_df = pd.DataFrame(school_data[split:])

train_df.to_csv("training_data/school_train.csv", index=False)
val_df.to_csv("training_data/school_val.csv", index=False)

print(f"✅ Generated {len(train_df):,} training samples")
print(f"✅ Generated {len(val_df):,} validation samples")

print("\n📝 Generating NER Dataset...")
print("-" * 80)

# Generate NER data
ner_data = []
sample_titles = ["Tech Fest", "Cultural Night", "Sports Meet", "Career Fair", "Workshop Session"]
sample_locations = ["Auditorium", "Main Hall", "Sports Complex", "Seminar Hall", "Open Ground"]

for i in range(10000):
    title = random.choice(sample_titles) + " " + str(2026)
    location = random.choice(sample_locations)
    date = (datetime.now() + timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
    time = f"{random.randint(9, 17)}:00 {random.choice(['AM', 'PM'])}"
    
    text = f"{title} will be held at {location} on {date} at {time}."
    
    # Simple entity tagging
    entities = [
        {"text": title, "label": "TITLE"},
        {"text": location, "label": "LOCATION"},
        {"text": date, "label": "DATE"},
        {"text": time, "label": "TIME"}
    ]
    
    ner_data.append({
        "text": text,
        "entities": json.dumps(entities)
    })

# Split
random.shuffle(ner_data)
split = int(len(ner_data) * 0.8)

train_df = pd.DataFrame(ner_data[:split])
val_df = pd.DataFrame(ner_data[split:])

train_df.to_csv("training_data/ner_train.csv", index=False)
val_df.to_csv("training_data/ner_val.csv", index=False)

print(f"✅ Generated {len(train_df):,} training samples")
print(f"✅ Generated {len(val_df):,} validation samples")

# Summary
print("\n" + "=" * 80)
print("✅ DATA GENERATION COMPLETE!")
print("=" * 80)

# Calculate total size
total_rows = len(category_data) + len(school_data) + len(ner_data)
print(f"\n📊 Total rows generated: {total_rows:,}")
print(f"📁 Location: ./training_data/")

print("\n📋 Files created:")
files = [
    "category_train.csv",
    "category_val.csv", 
    "school_train.csv",
    "school_val.csv",
    "ner_train.csv",
    "ner_val.csv"
]

for f in files:
    path = os.path.join("training_data", f)
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"   ✅ {f} ({size_mb:.2f} MB)")

print("\n📝 Next step: Run model training")
print("   python train_ai_models.py")
print("=" * 80)
