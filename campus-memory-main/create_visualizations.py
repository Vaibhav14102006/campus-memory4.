import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for professional looking graphs
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('event_feedback_dataset.csv')
print(f"Loaded {len(df):,} records\n")

# Create output directory for images
import os
if not os.path.exists('presentation_visuals'):
    os.makedirs('presentation_visuals')

# ============================================================================
# 1. EVENT PARTICIPATION OVERVIEW
# ============================================================================
print("Creating visualization 1/12: Event Participation Overview...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Event Participation Overview - 100,000 Student Records', fontsize=18, fontweight='bold', y=0.995)

# Event type distribution
event_counts = df['event_type'].value_counts()
colors = sns.color_palette("viridis", len(event_counts))
axes[0, 0].barh(event_counts.index, event_counts.values, color=colors)
axes[0, 0].set_xlabel('Number of Participants', fontweight='bold')
axes[0, 0].set_title('Participation by Event Type', fontweight='bold', fontsize=14)
for i, v in enumerate(event_counts.values):
    axes[0, 0].text(v + 200, i, f'{v:,}', va='center', fontweight='bold')

# Top events
top_events = df['event_name'].value_counts().head(10)
axes[0, 1].barh(top_events.index, top_events.values, color=sns.color_palette("rocket", 10))
axes[0, 1].set_xlabel('Number of Participants', fontweight='bold')
axes[0, 1].set_title('Top 10 Most Popular Events', fontweight='bold', fontsize=14)
for i, v in enumerate(top_events.values):
    axes[0, 1].text(v + 100, i, f'{v:,}', va='center')

# Event level distribution
level_counts = df['event_level'].value_counts()
colors_pie = sns.color_palette("Set2", len(level_counts))
axes[1, 0].pie(level_counts.values, labels=level_counts.index, autopct='%1.1f%%', 
               colors=colors_pie, startangle=90)
axes[1, 0].set_title('Events by Level', fontweight='bold', fontsize=14)

# Branch participation
branch_counts = df['student_branch'].value_counts()
axes[1, 1].bar(branch_counts.index, branch_counts.values, color=sns.color_palette("mako", len(branch_counts)))
axes[1, 1].set_xlabel('Student Branch', fontweight='bold')
axes[1, 1].set_ylabel('Number of Students', fontweight='bold')
axes[1, 1].set_title('Participation by Student Branch', fontweight='bold', fontsize=14)
axes[1, 1].tick_params(axis='x', rotation=45)
for i, v in enumerate(branch_counts.values):
    axes[1, 1].text(i, v + 300, f'{v:,}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/01_event_participation_overview.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_event_participation_overview.png")
plt.close()

# ============================================================================
# 2. SATISFACTION & RATINGS ANALYSIS
# ============================================================================
print("Creating visualization 2/12: Satisfaction Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Student Satisfaction & Ratings Analysis', fontsize=18, fontweight='bold', y=0.995)

# Overall satisfaction by event type
satisfaction_by_type = df.groupby('event_type')['overall_satisfaction'].mean().sort_values(ascending=True)
colors = ['red' if x < 7 else 'orange' if x < 8 else 'green' for x in satisfaction_by_type.values]
axes[0, 0].barh(satisfaction_by_type.index, satisfaction_by_type.values, color=colors)
axes[0, 0].set_xlabel('Average Overall Satisfaction (0-10)', fontweight='bold')
axes[0, 0].set_title('Average Satisfaction by Event Type', fontweight='bold', fontsize=14)
axes[0, 0].axvline(x=7, color='red', linestyle='--', alpha=0.5, label='Critical: 7.0')
axes[0, 0].legend()
for i, v in enumerate(satisfaction_by_type.values):
    axes[0, 0].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# Distribution of ratings
rating_cols = ['venue_rating', 'organization_rating', 'content_quality', 'mentor_support', 
               'food_quality', 'infrastructure']
avg_ratings = df[rating_cols].mean().sort_values(ascending=True)
colors = ['red' if x < 7 else 'orange' if x < 8 else 'green' for x in avg_ratings.values]
axes[0, 1].barh(avg_ratings.index, avg_ratings.values, color=colors)
axes[0, 1].set_xlabel('Average Rating (0-10)', fontweight='bold')
axes[0, 1].set_title('Average Ratings Across Different Aspects', fontweight='bold', fontsize=14)
axes[0, 1].axvline(x=7, color='red', linestyle='--', alpha=0.5)
for i, v in enumerate(avg_ratings.values):
    axes[0, 1].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# Sentiment distribution
sentiment_counts = df['sentiment'].value_counts()
colors_pie = ['#28a745', '#ffc107', '#dc3545']  # green, yellow, red
axes[1, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[1, 0].set_title('Overall Sentiment Distribution', fontweight='bold', fontsize=14)

# Would recommend vs Would attend similar
recommend_vs_attend = pd.DataFrame({
    'Would Recommend': [df['would_recommend'].sum(), len(df) - df['would_recommend'].sum()],
    'Attend Similar Event': [df['attend_similar_event'].sum(), len(df) - df['attend_similar_event'].sum()]
}, index=['Yes', 'No'])
recommend_vs_attend.plot(kind='bar', ax=axes[1, 1], color=['#28a745', '#17a2b8'])
axes[1, 1].set_ylabel('Number of Students', fontweight='bold')
axes[1, 1].set_title('Student Recommendations & Future Interest', fontweight='bold', fontsize=14)
axes[1, 1].tick_params(axis='x', rotation=0)
axes[1, 1].legend(loc='upper right')
for container in axes[1, 1].containers:
    axes[1, 1].bar_label(container, fmt='%d', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/02_satisfaction_ratings_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_satisfaction_ratings_analysis.png")
plt.close()

# ============================================================================
# 3. COMMON ISSUES & CHALLENGES
# ============================================================================
print("Creating visualization 3/12: Common Issues Analysis...")
fig, axes = plt.subplots(2, 1, figsize=(16, 12))
fig.suptitle('Common Issues & Challenges Faced by Students', fontsize=18, fontweight='bold', y=0.995)

# Parse and count all issues
all_issues = []
for issues in df['issues_faced'].dropna():
    if issues and issues != 'None' and issues != '':
        issue_list = [i.strip() for i in str(issues).split(',')]
        all_issues.extend(issue_list)

issue_counts = Counter(all_issues)
top_issues = dict(sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10])

# Top 10 issues
axes[0].barh(list(top_issues.keys()), list(top_issues.values()), 
             color=sns.color_palette("Reds_r", len(top_issues)))
axes[0].set_xlabel('Number of Reports', fontweight='bold', fontsize=12)
axes[0].set_title('Top 10 Most Reported Issues', fontweight='bold', fontsize=14)
for i, v in enumerate(top_issues.values()):
    percentage = (v / len(df)) * 100
    axes[0].text(v + 100, i, f'{v:,} ({percentage:.1f}%)', va='center', fontweight='bold')

# Issues by event type
event_types = df['event_type'].unique()
issue_categories = ['Technical Issues', 'Poor Coordination', 'Food Quality', 
                   'Lack of Mentors', 'Communication Gap']

issue_by_event = []
for event_type in event_types:
    subset = df[df['event_type'] == event_type]
    counts = []
    for issue in issue_categories:
        count = subset['issues_faced'].astype(str).str.contains(issue, na=False).sum()
        counts.append(count)
    issue_by_event.append(counts)

x = np.arange(len(event_types))
width = 0.15
colors = sns.color_palette("Set2", len(issue_categories))

for i, issue in enumerate(issue_categories):
    values = [issue_by_event[j][i] for j in range(len(event_types))]
    axes[1].bar(x + i * width, values, width, label=issue, color=colors[i])

axes[1].set_xlabel('Event Type', fontweight='bold', fontsize=12)
axes[1].set_ylabel('Number of Reports', fontweight='bold', fontsize=12)
axes[1].set_title('Common Issues by Event Type', fontweight='bold', fontsize=14)
axes[1].set_xticks(x + width * 2)
axes[1].set_xticklabels(event_types, rotation=0)
axes[1].legend(loc='upper right')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('presentation_visuals/03_common_issues_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_common_issues_analysis.png")
plt.close()

# ============================================================================
# 4. STUDENT DEMOGRAPHICS
# ============================================================================
print("Creating visualization 4/12: Student Demographics...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Student Demographics & Participation Patterns', fontsize=18, fontweight='bold', y=0.995)

# Year distribution
year_counts = df['student_year'].value_counts().sort_index()
axes[0, 0].bar(year_counts.index, year_counts.values, color=sns.color_palette("coolwarm", len(year_counts)))
axes[0, 0].set_xlabel('Academic Year', fontweight='bold')
axes[0, 0].set_ylabel('Number of Students', fontweight='bold')
axes[0, 0].set_title('Participation by Academic Year', fontweight='bold', fontsize=14)
for i, v in enumerate(year_counts.values):
    axes[0, 0].text(year_counts.index[i], v + 500, f'{v:,}', ha='center', fontweight='bold')

# Gender distribution
gender_counts = df['gender'].value_counts()
colors_pie = sns.color_palette("pastel", len(gender_counts))
axes[0, 1].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0, 1].set_title('Gender Distribution', fontweight='bold', fontsize=14)

# Skill level distribution
skill_counts = df['skill_level'].value_counts()
skill_order = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
skill_counts = skill_counts.reindex(skill_order)
colors = sns.color_palette("YlGnBu", len(skill_counts))
axes[1, 0].bar(skill_counts.index, skill_counts.values, color=colors)
axes[1, 0].set_xlabel('Skill Level', fontweight='bold')
axes[1, 0].set_ylabel('Number of Students', fontweight='bold')
axes[1, 0].set_title('Student Skill Level Distribution', fontweight='bold', fontsize=14)
for i, v in enumerate(skill_counts.values):
    axes[1, 0].text(i, v + 500, f'{v:,}', ha='center', fontweight='bold')

# Team size analysis
team_size_counts = df['team_size'].value_counts().sort_index()
axes[1, 1].bar(team_size_counts.index, team_size_counts.values, 
               color=sns.color_palette("viridis", len(team_size_counts)))
axes[1, 1].set_xlabel('Team Size', fontweight='bold')
axes[1, 1].set_ylabel('Number of Participations', fontweight='bold')
axes[1, 1].set_title('Team Size Distribution', fontweight='bold', fontsize=14)
for i, v in enumerate(team_size_counts.values):
    axes[1, 1].text(team_size_counts.index[i], v + 500, f'{v:,}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/04_student_demographics.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_student_demographics.png")
plt.close()

# ============================================================================
# 5. ACHIEVEMENT & SUCCESS PATTERNS
# ============================================================================
print("Creating visualization 5/12: Achievement Patterns...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Achievement Patterns & Success Factors', fontsize=18, fontweight='bold', y=0.995)

# Achievement distribution
achievement_counts = df['achievement'].value_counts()
colors = ['gold', 'silver', '#cd7f32', 'lightblue', 'lightgray']  # gold, silver, bronze, etc
axes[0, 0].pie(achievement_counts.values, labels=achievement_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
axes[0, 0].set_title('Achievement Distribution', fontweight='bold', fontsize=14)

# Satisfaction by achievement
sat_by_achievement = df.groupby('achievement')['overall_satisfaction'].mean().sort_values(ascending=False)
colors = sns.color_palette("RdYlGn", len(sat_by_achievement))
axes[0, 1].barh(sat_by_achievement.index, sat_by_achievement.values, color=colors[::-1])
axes[0, 1].set_xlabel('Average Overall Satisfaction', fontweight='bold')
axes[0, 1].set_title('Satisfaction by Achievement Level', fontweight='bold', fontsize=14)
for i, v in enumerate(sat_by_achievement.values):
    axes[0, 1].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# Learning outcome by skill level
learning_by_skill = df.groupby('skill_level')['learning_outcome'].mean().reindex(skill_order)
axes[1, 0].plot(learning_by_skill.index, learning_by_skill.values, marker='o', 
                linewidth=3, markersize=10, color='#2E86AB')
axes[1, 0].fill_between(range(len(learning_by_skill)), learning_by_skill.values, alpha=0.3)
axes[1, 0].set_xlabel('Skill Level', fontweight='bold')
axes[1, 0].set_ylabel('Average Learning Outcome (0-10)', fontweight='bold')
axes[1, 0].set_title('Learning Outcome by Skill Level', fontweight='bold', fontsize=14)
axes[1, 0].grid(alpha=0.3)
for i, v in enumerate(learning_by_skill.values):
    axes[1, 0].text(i, v + 0.2, f'{v:.2f}', ha='center', fontweight='bold')

# Previous participation impact
prev_participation_order = ['None', 'Low', 'Medium', 'High']
sat_by_prev = df.groupby('previous_participation')['overall_satisfaction'].mean()
sat_by_prev = sat_by_prev.reindex(prev_participation_order)
colors = sns.color_palette("Blues", len(sat_by_prev))
axes[1, 1].bar(sat_by_prev.index, sat_by_prev.values, color=colors)
axes[1, 1].set_xlabel('Previous Participation Level', fontweight='bold')
axes[1, 1].set_ylabel('Average Overall Satisfaction', fontweight='bold')
axes[1, 1].set_title('Impact of Previous Participation on Satisfaction', fontweight='bold', fontsize=14)
for i, v in enumerate(sat_by_prev.values):
    axes[1, 1].text(i, v + 0.1, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/05_achievement_success_patterns.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 05_achievement_success_patterns.png")
plt.close()

# ============================================================================
# 6. CORRELATION HEATMAP
# ============================================================================
print("Creating visualization 6/12: Correlation Analysis...")
fig, ax = plt.subplots(figsize=(14, 10))

# Select numeric columns for correlation
numeric_cols = ['venue_rating', 'organization_rating', 'content_quality', 'mentor_support',
                'food_quality', 'prize_satisfaction', 'networking_opportunities', 'time_management',
                'infrastructure', 'registration_process', 'learning_outcome', 'overall_satisfaction']

correlation_matrix = df[numeric_cols].corr()
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Correlation Matrix - Factor Relationships', fontweight='bold', fontsize=16, pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('presentation_visuals/06_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 06_correlation_heatmap.png")
plt.close()

# ============================================================================
# 7. EVENT LEVEL COMPARISON
# ============================================================================
print("Creating visualization 7/12: Event Level Comparison...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Event Level Comparison Analysis', fontsize=18, fontweight='bold', y=0.995)

# Satisfaction by level
sat_by_level = df.groupby('event_level')['overall_satisfaction'].mean().sort_values()
colors = ['red' if x < 7 else 'orange' if x < 8 else 'green' for x in sat_by_level.values]
axes[0, 0].barh(sat_by_level.index, sat_by_level.values, color=colors)
axes[0, 0].set_xlabel('Average Overall Satisfaction', fontweight='bold')
axes[0, 0].set_title('Satisfaction by Event Level', fontweight='bold', fontsize=14)
for i, v in enumerate(sat_by_level.values):
    axes[0, 0].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# Participation count by level
level_participation = df['event_level'].value_counts()
axes[0, 1].bar(level_participation.index, level_participation.values, 
               color=sns.color_palette("muted", len(level_participation)))
axes[0, 1].set_xlabel('Event Level', fontweight='bold')
axes[0, 1].set_ylabel('Number of Participants', fontweight='bold')
axes[0, 1].set_title('Participation by Event Level', fontweight='bold', fontsize=14)
for i, v in enumerate(level_participation.values):
    axes[0, 1].text(i, v + 500, f'{v:,}', ha='center', fontweight='bold')

# Learning outcome by level
learning_by_level = df.groupby('event_level')['learning_outcome'].mean().sort_values()
axes[1, 0].barh(learning_by_level.index, learning_by_level.values, 
                color=sns.color_palette("Greens", len(learning_by_level)))
axes[1, 0].set_xlabel('Average Learning Outcome', fontweight='bold')
axes[1, 0].set_title('Learning Outcome by Event Level', fontweight='bold', fontsize=14)
for i, v in enumerate(learning_by_level.values):
    axes[1, 0].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# Box plot - satisfaction distribution by level
event_levels = df['event_level'].unique()
data_to_plot = [df[df['event_level'] == level]['overall_satisfaction'].values for level in event_levels]
bp = axes[1, 1].boxplot(data_to_plot, labels=event_levels, patch_artist=True)
for patch, color in zip(bp['boxes'], sns.color_palette("Set2", len(event_levels))):
    patch.set_facecolor(color)
axes[1, 1].set_xlabel('Event Level', fontweight='bold')
axes[1, 1].set_ylabel('Overall Satisfaction', fontweight='bold')
axes[1, 1].set_title('Satisfaction Distribution by Event Level', fontweight='bold', fontsize=14)
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('presentation_visuals/07_event_level_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 07_event_level_comparison.png")
plt.close()

# ============================================================================
# 8. TIME-BASED ANALYSIS
# ============================================================================
print("Creating visualization 8/12: Time-based Trends...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Time-based Trends & Patterns', fontsize=18, fontweight='bold', y=0.995)

# Convert dates
df['event_date'] = pd.to_datetime(df['event_date'])
df['event_month'] = df['event_date'].dt.month
df['event_year'] = df['event_date'].dt.year

# Events by month
monthly_events = df.groupby('event_month').size()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
axes[0, 0].plot(monthly_events.index, monthly_events.values, marker='o', linewidth=3, markersize=10, color='#E63946')
axes[0, 0].fill_between(monthly_events.index, monthly_events.values, alpha=0.3, color='#E63946')
axes[0, 0].set_xlabel('Month', fontweight='bold')
axes[0, 0].set_ylabel('Number of Events', fontweight='bold')
axes[0, 0].set_title('Event Distribution Throughout the Year', fontweight='bold', fontsize=14)
axes[0, 0].set_xticks(range(1, 13))
axes[0, 0].set_xticklabels(month_names, rotation=45)
axes[0, 0].grid(alpha=0.3)

# Satisfaction by month
sat_by_month = df.groupby('event_month')['overall_satisfaction'].mean()
axes[0, 1].bar(sat_by_month.index, sat_by_month.values, color=sns.color_palette("viridis", 12))
axes[0, 1].set_xlabel('Month', fontweight='bold')
axes[0, 1].set_ylabel('Average Satisfaction', fontweight='bold')
axes[0, 1].set_title('Average Satisfaction by Month', fontweight='bold', fontsize=14)
axes[0, 1].set_xticks(range(1, 13))
axes[0, 1].set_xticklabels(month_names, rotation=45)
axes[0, 1].axhline(y=df['overall_satisfaction'].mean(), color='red', linestyle='--', alpha=0.7, label='Overall Avg')
axes[0, 1].legend()

# Event duration impact
duration_sat = df.groupby('event_duration_days')['overall_satisfaction'].mean().sort_index()
axes[1, 0].plot(duration_sat.index, duration_sat.values, marker='o', linewidth=3, markersize=10, color='#2A9D8F')
axes[1, 0].fill_between(duration_sat.index, duration_sat.values, alpha=0.3, color='#2A9D8F')
axes[1, 0].set_xlabel('Event Duration (Days)', fontweight='bold')
axes[1, 0].set_ylabel('Average Satisfaction', fontweight='bold')
axes[1, 0].set_title('Impact of Event Duration on Satisfaction', fontweight='bold', fontsize=14)
axes[1, 0].grid(alpha=0.3)

# Participation trends by year
yearly_participation = df.groupby('event_year').size()
axes[1, 1].bar(yearly_participation.index, yearly_participation.values, 
               color=sns.color_palette("rocket", len(yearly_participation)))
axes[1, 1].set_xlabel('Year', fontweight='bold')
axes[1, 1].set_ylabel('Number of Participants', fontweight='bold')
axes[1, 1].set_title('Yearly Participation Trends', fontweight='bold', fontsize=14)
for i, v in enumerate(yearly_participation.values):
    axes[1, 1].text(yearly_participation.index[i], v + 500, f'{v:,}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/08_time_based_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 08_time_based_analysis.png")
plt.close()

# ============================================================================
# 9. KEY METRICS DASHBOARD
# ============================================================================
print("Creating visualization 9/12: Key Metrics Dashboard...")
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
fig.suptitle('Event Guidance System - Key Metrics Dashboard', fontsize=20, fontweight='bold', y=0.98)

# Big numbers
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.5, f"{len(df):,}", ha='center', va='center', fontsize=48, fontweight='bold', color='#2E86AB')
ax1.text(0.5, 0.2, 'Total Records', ha='center', va='center', fontsize=16, color='gray')
ax1.axis('off')

ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.5, f"{df['overall_satisfaction'].mean():.2f}/10", ha='center', va='center', 
         fontsize=48, fontweight='bold', color='#E63946')
ax2.text(0.5, 0.2, 'Avg Satisfaction', ha='center', va='center', fontsize=16, color='gray')
ax2.axis('off')

ax3 = fig.add_subplot(gs[0, 2])
recommend_pct = (df['would_recommend'].sum() / len(df)) * 100
ax3.text(0.5, 0.5, f"{recommend_pct:.1f}%", ha='center', va='center', 
         fontsize=48, fontweight='bold', color='#2A9D8F')
ax3.text(0.5, 0.2, 'Would Recommend', ha='center', va='center', fontsize=16, color='gray')
ax3.axis('off')

# Event distribution
ax4 = fig.add_subplot(gs[1, :2])
event_type_data = df.groupby('event_type').agg({
    'overall_satisfaction': 'mean',
    'event_name': 'count'
}).rename(columns={'event_name': 'count'})
x_pos = np.arange(len(event_type_data))
width = 0.35
ax4_twin = ax4.twinx()
bars1 = ax4.bar(x_pos - width/2, event_type_data['count'], width, label='Participation Count', color='#457B9D')
bars2 = ax4_twin.bar(x_pos + width/2, event_type_data['overall_satisfaction'], width, 
                     label='Avg Satisfaction', color='#E63946')
ax4.set_xlabel('Event Type', fontweight='bold', fontsize=12)
ax4.set_ylabel('Participation Count', fontweight='bold', fontsize=12, color='#457B9D')
ax4_twin.set_ylabel('Average Satisfaction', fontweight='bold', fontsize=12, color='#E63946')
ax4.set_title('Event Type: Participation vs Satisfaction', fontweight='bold', fontsize=14)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(event_type_data.index, rotation=45, ha='right')
ax4.legend(loc='upper left')
ax4_twin.legend(loc='upper right')
ax4.grid(alpha=0.3, axis='y')

# Sentiment pie
ax5 = fig.add_subplot(gs[1, 2])
sentiment_data = df['sentiment'].value_counts()
colors_sentiment = ['#28a745', '#ffc107', '#dc3545']
ax5.pie(sentiment_data.values, labels=sentiment_data.index, autopct='%1.1f%%',
        colors=colors_sentiment, startangle=90, textprops={'fontweight': 'bold'})
ax5.set_title('Sentiment Distribution', fontweight='bold', fontsize=14)

# Rating comparison
ax6 = fig.add_subplot(gs[2, :])
rating_categories = ['Venue', 'Organization', 'Content', 'Mentors', 'Food', 
                    'Infrastructure', 'Registration', 'Learning']
ratings_data = [
    df['venue_rating'].mean(),
    df['organization_rating'].mean(),
    df['content_quality'].mean(),
    df['mentor_support'].mean(),
    df['food_quality'].mean(),
    df['infrastructure'].mean(),
    df['registration_process'].mean(),
    df['learning_outcome'].mean()
]
colors_bar = ['green' if x >= 8 else 'orange' if x >= 7 else 'red' for x in ratings_data]
bars = ax6.bar(rating_categories, ratings_data, color=colors_bar, edgecolor='black', linewidth=1.5)
ax6.axhline(y=7, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Critical Threshold: 7.0')
ax6.axhline(y=8, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Good Threshold: 8.0')
ax6.set_ylabel('Average Rating (0-10)', fontweight='bold', fontsize=12)
ax6.set_title('Average Ratings Across All Categories', fontweight='bold', fontsize=14)
ax6.set_ylim(0, 10)
ax6.legend(loc='lower right')
ax6.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, ratings_data)):
    ax6.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.2f}', 
            ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.savefig('presentation_visuals/09_key_metrics_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 09_key_metrics_dashboard.png")
plt.close()

# ============================================================================
# 10. PROBLEM SEVERITY ANALYSIS
# ============================================================================
print("Creating visualization 10/12: Problem Severity Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Problem Severity & Impact Analysis', fontsize=18, fontweight='bold', y=0.995)

# Issues with no issues vs with issues
has_issues = df['issues_faced'].notna() & (df['issues_faced'] != '') & (df['issues_faced'] != 'None')
issue_impact = pd.DataFrame({
    'Category': ['No Issues', 'Had Issues'],
    'Satisfaction': [
        df[~has_issues]['overall_satisfaction'].mean(),
        df[has_issues]['overall_satisfaction'].mean()
    ],
    'Count': [
        (~has_issues).sum(),
        has_issues.sum()
    ]
})

x = np.arange(len(issue_impact))
width = 0.35
ax1_twin = axes[0, 0].twinx()
bars1 = axes[0, 0].bar(x - width/2, issue_impact['Count'], width, label='Count', color='#457B9D')
bars2 = ax1_twin.bar(x + width/2, issue_impact['Satisfaction'], width, label='Avg Satisfaction', color='#E63946')
axes[0, 0].set_xlabel('Issue Status', fontweight='bold')
axes[0, 0].set_ylabel('Count', fontweight='bold', color='#457B9D')
ax1_twin.set_ylabel('Avg Satisfaction', fontweight='bold', color='#E63946')
axes[0, 0].set_title('Impact of Issues on Satisfaction', fontweight='bold', fontsize=14)
axes[0, 0].set_xticks(x)
axes[0, 0].set_xticklabels(issue_impact['Category'])
axes[0, 0].legend(loc='upper left')
ax1_twin.legend(loc='upper right')

# Feedback quality
feedback_quality = pd.DataFrame({
    'Suggestions Given': [df['suggestions_given'].sum(), len(df) - df['suggestions_given'].sum()],
    'Issues Reported': [has_issues.sum(), (~has_issues).sum()]
}, index=['Yes', 'No'])
feedback_quality.T.plot(kind='bar', ax=axes[0, 1], color=['#28a745', '#dc3545'])
axes[0, 1].set_ylabel('Number of Students', fontweight='bold')
axes[0, 1].set_title('Feedback Quality Indicators', fontweight='bold', fontsize=14)
axes[0, 1].tick_params(axis='x', rotation=0)
axes[0, 1].legend(title='Response', loc='upper right')
for container in axes[0, 1].containers:
    axes[0, 1].bar_label(container, fmt='%d', fontweight='bold')

# Issue frequency by event
top_events_issues = df.groupby('event_name').apply(
    lambda x: (x['issues_faced'].notna() & (x['issues_faced'] != '') & (x['issues_faced'] != 'None')).sum()
).sort_values(ascending=False).head(10)
axes[1, 0].barh(top_events_issues.index, top_events_issues.values, color=sns.color_palette("Reds", 10))
axes[1, 0].set_xlabel('Number of Issue Reports', fontweight='bold')
axes[1, 0].set_title('Top 10 Events with Most Issues Reported', fontweight='bold', fontsize=14)
for i, v in enumerate(top_events_issues.values):
    axes[1, 0].text(v + 20, i, f'{v:,}', va='center', fontweight='bold')

# Feedback length analysis
axes[1, 1].hist(df['feedback_length'], bins=30, color='#2A9D8F', edgecolor='black', alpha=0.7)
axes[1, 1].axvline(df['feedback_length'].mean(), color='red', linestyle='--', linewidth=2, 
                   label=f"Mean: {df['feedback_length'].mean():.0f}")
axes[1, 1].set_xlabel('Feedback Length (characters)', fontweight='bold')
axes[1, 1].set_ylabel('Frequency', fontweight='bold')
axes[1, 1].set_title('Distribution of Feedback Length', fontweight='bold', fontsize=14)
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('presentation_visuals/10_problem_severity_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 10_problem_severity_analysis.png")
plt.close()

# ============================================================================
# 11. COMPARATIVE ANALYSIS
# ============================================================================
print("Creating visualization 11/12: Comparative Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Comparative Analysis: Team vs Solo & Other Factors', fontsize=18, fontweight='bold', y=0.995)

# Team vs Solo
team_vs_solo = df.groupby('participated_alone').agg({
    'overall_satisfaction': 'mean',
    'learning_outcome': 'mean',
    'would_recommend': 'mean'
})
team_vs_solo.index = ['Team', 'Solo']
team_vs_solo.plot(kind='bar', ax=axes[0, 0], color=['#E76F51', '#2A9D8F', '#F4A261'])
axes[0, 0].set_ylabel('Average Score', fontweight='bold')
axes[0, 0].set_title('Team vs Solo Participation Comparison', fontweight='bold', fontsize=14)
axes[0, 0].tick_params(axis='x', rotation=0)
axes[0, 0].legend(['Satisfaction', 'Learning', 'Would Recommend'], loc='lower right')
axes[0, 0].grid(alpha=0.3, axis='y')
for container in axes[0, 0].containers:
    axes[0, 0].bar_label(container, fmt='%.2f', fontweight='bold')

# Branch comparison - Top performing branches
branch_performance = df.groupby('student_branch')['overall_satisfaction'].mean().sort_values(ascending=False)
colors = sns.color_palette("RdYlGn", len(branch_performance))
axes[0, 1].barh(branch_performance.index, branch_performance.values, color=colors[::-1])
axes[0, 1].set_xlabel('Average Satisfaction', fontweight='bold')
axes[0, 1].set_title('Satisfaction by Student Branch', fontweight='bold', fontsize=14)
axes[0, 1].axvline(df['overall_satisfaction'].mean(), color='blue', linestyle='--', 
                   alpha=0.7, linewidth=2, label='Overall Avg')
axes[0, 1].legend()
for i, v in enumerate(branch_performance.values):
    axes[0, 1].text(v + 0.05, i, f'{v:.2f}', va='center', fontweight='bold')

# Gender-based satisfaction
gender_metrics = df.groupby('gender').agg({
    'overall_satisfaction': 'mean',
    'learning_outcome': 'mean',
    'networking_opportunities': 'mean'
}).round(2)
x = np.arange(len(gender_metrics))
width = 0.25
colors = ['#E63946', '#2A9D8F', '#F4A261']
for i, col in enumerate(gender_metrics.columns):
    axes[1, 0].bar(x + i*width, gender_metrics[col], width, label=col.replace('_', ' ').title(), color=colors[i])
axes[1, 0].set_ylabel('Average Rating', fontweight='bold')
axes[1, 0].set_xlabel('Gender', fontweight='bold')
axes[1, 0].set_title('Experience Metrics by Gender', fontweight='bold', fontsize=14)
axes[1, 0].set_xticks(x + width)
axes[1, 0].set_xticklabels(gender_metrics.index)
axes[1, 0].legend(loc='upper right')
axes[1, 0].grid(alpha=0.3, axis='y')

# Age group analysis
df['age_group'] = pd.cut(df['student_age'], bins=[17, 19, 21, 23, 25], labels=['18-19', '20-21', '22-23', '24+'])
age_satisfaction = df.groupby('age_group')['overall_satisfaction'].mean()
axes[1, 1].plot(range(len(age_satisfaction)), age_satisfaction.values, marker='o', 
                linewidth=3, markersize=12, color='#E76F51')
axes[1, 1].fill_between(range(len(age_satisfaction)), age_satisfaction.values, alpha=0.3, color='#E76F51')
axes[1, 1].set_xlabel('Age Group', fontweight='bold')
axes[1, 1].set_ylabel('Average Satisfaction', fontweight='bold')
axes[1, 1].set_title('Satisfaction Across Age Groups', fontweight='bold', fontsize=14)
axes[1, 1].set_xticks(range(len(age_satisfaction)))
axes[1, 1].set_xticklabels(age_satisfaction.index)
axes[1, 1].grid(alpha=0.3)
for i, v in enumerate(age_satisfaction.values):
    axes[1, 1].text(i, v + 0.1, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/11_comparative_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 11_comparative_analysis.png")
plt.close()

# ============================================================================
# 12. RECOMMENDATIONS IMPACT
# ============================================================================
print("Creating visualization 12/12: System Impact & Value...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Event Guidance System - Impact & Value Proposition', fontsize=18, fontweight='bold', y=0.995)

# Recommendation rate
rec_rate = (df['would_recommend'].sum() / len(df)) * 100
not_rec_rate = 100 - rec_rate
colors = ['#28a745', '#dc3545']
axes[0, 0].pie([rec_rate, not_rec_rate], labels=['Would Recommend', 'Would Not'], 
               autopct='%1.1f%%', colors=colors, startangle=90,
               textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[0, 0].set_title(f'Overall Recommendation Rate\n({df["would_recommend"].sum():,} out of {len(df):,})', 
                     fontweight='bold', fontsize=14)

# Key areas needing improvement
improvement_areas = {
    'Organization': df['organization_rating'].mean(),
    'Content Quality': df['content_quality'].mean(),
    'Food Quality': df['food_quality'].mean(),
    'Mentor Support': df['mentor_support'].mean(),
    'Time Management': df['time_management'].mean(),
}
improvement_areas = dict(sorted(improvement_areas.items(), key=lambda x: x[1]))
colors = ['red' if v < 7 else 'orange' if v < 8 else 'green' for v in improvement_areas.values()]
axes[0, 1].barh(list(improvement_areas.keys()), list(improvement_areas.values()), color=colors)
axes[0, 1].set_xlabel('Average Rating', fontweight='bold')
axes[0, 1].set_title('Key Areas Needing Improvement', fontweight='bold', fontsize=14)
axes[0, 1].axvline(x=7, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Critical: 7.0')
axes[0, 1].axvline(x=8, color='orange', linestyle='--', alpha=0.5, linewidth=2, label='Target: 8.0')
axes[0, 1].legend()
for i, v in enumerate(improvement_areas.values()):
    axes[0, 1].text(v + 0.1, i, f'{v:.2f}', va='center', fontweight='bold')

# System value - data coverage
coverage_data = {
    'Total Events': df['event_name'].nunique(),
    'Total Students': len(df),
    'Event Types': df['event_type'].nunique(),
    'Branches Covered': df['student_branch'].nunique(),
    'Feedback Records': len(df[df['suggestions_given'] == 1])
}
axes[1, 0].barh(list(coverage_data.keys()), list(coverage_data.values()), 
                color=sns.color_palette("viridis", len(coverage_data)))
axes[1, 0].set_xlabel('Count', fontweight='bold')
axes[1, 0].set_title('System Data Coverage & Reach', fontweight='bold', fontsize=14)
for i, v in enumerate(coverage_data.values()):
    axes[1, 0].text(v + 500, i, f'{v:,}', va='center', fontweight='bold')

# Success rate by event type
success_rate = df.groupby('event_type').apply(
    lambda x: (x['achievement'].isin(['Gold', 'Silver', 'Bronze'])).sum() / len(x) * 100
).sort_values(ascending=False)
axes[1, 1].bar(success_rate.index, success_rate.values, color=sns.color_palette("rocket", len(success_rate)))
axes[1, 1].set_xlabel('Event Type', fontweight='bold')
axes[1, 1].set_ylabel('Success Rate (%)', fontweight='bold')
axes[1, 1].set_title('Prize Success Rate by Event Type', fontweight='bold', fontsize=14)
axes[1, 1].tick_params(axis='x', rotation=45)
for i, v in enumerate(success_rate.values):
    axes[1, 1].text(i, v + 0.5, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_visuals/12_system_impact_value.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 12_system_impact_value.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✓ ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("="*70)
print(f"\n📁 Location: presentation_visuals/")
print(f"📊 Total Visualizations: 12")
print(f"📈 All images saved in high resolution (300 DPI)")
print("\nVisualization files:")
for i in range(1, 13):
    print(f"  {i:2d}. {str(i).zfill(2)}_*.png")
print("\n" + "="*70)
print("Ready for your presentation! 🎯")
print("="*70)
