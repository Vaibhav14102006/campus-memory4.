"""
Simple API for Event Guidance System
Easy interface to get recommendations for registered events
"""

from event_guidance_system import EventGuidanceSystem, print_guidance

def get_event_guidance(student_profile, event_name):
    """
    Get comprehensive guidance for a student registered for an event
    
    Args:
        student_profile: dict with keys:
            - branch: e.g., 'CSE', 'IT', 'ECE', etc.
            - year: 1, 2, 3, or 4
            - skill_level: 'Beginner', 'Intermediate', 'Advanced', 'Expert'
            - gender: 'Male', 'Female', 'Other'
            
        event_name: Name of event (e.g., 'Hacksetu', 'Ami Chroma', 'Convocation')
        
    Returns:
        dict with recommendations, tips, common issues, etc.
    """
    system = EventGuidanceSystem()
    guidance = system.get_recommendations_for_registered_event(student_profile, event_name)
    return guidance


# Quick examples
if __name__ == "__main__":
    print("="*80)
    print("EVENT GUIDANCE API - QUICK EXAMPLES")
    print("="*80)
    
    system = EventGuidanceSystem()
    
    # Example 1: CSE student registered for Smart India Hackathon
    print("\n📋 Example 1: CSE 3rd year student registered for Smart India Hackathon")
    print("-"*80)
    
    student1 = {
        'branch': 'CSE',
        'year': 3,
        'skill_level': 'Advanced',
        'gender': 'Female'
    }
    
    guidance1 = system.get_recommendations_for_registered_event(student1, 'Smart India Hackathon')
    
    print(f"\n📊 Quick Summary:")
    print(f"  Past Attendees: {guidance1['total_past_attendees']:,}")
    print(f"  Average Satisfaction: {guidance1['overall_satisfaction']:.2f}/10")
    print(f"  Recommendation Rate: {guidance1['recommendation_rate']:.1f}%")
    
    print(f"\n⚠️  Top 3 Issues to Watch Out For:")
    for i, issue in enumerate(guidance1['common_issues'][:3], 1):
        print(f"  {i}. {issue['issue']} ({issue['percentage']:.1f}% reported)")
    
    print(f"\n💡 Top 3 Recommendations:")
    for i, rec in enumerate(guidance1['recommendations'][:3], 1):
        print(f"  {i}. [{rec['priority']}] {rec['category']}")
        print(f"     → {rec['advice']}")
    
    # Example 2: Civil engineering student for Init Maths
    print("\n\n📋 Example 2: Civil 1st year student registered for Init Maths")
    print("-"*80)
    
    student2 = {
        'branch': 'Civil',
        'year': 1,
        'skill_level': 'Beginner',
        'gender': 'Male'
    }
    
    guidance2 = system.get_recommendations_for_registered_event(student2, 'Init Maths')
    
    print(f"\n📊 Quick Summary:")
    print(f"  Past Attendees: {guidance2['total_past_attendees']:,}")
    print(f"  Average Satisfaction: {guidance2['overall_satisfaction']:.2f}/10")
    print(f"  Recommendation Rate: {guidance2['recommendation_rate']:.1f}%")
    
    print(f"\n✅ Event Strengths:")
    for strength in guidance2['strengths'][:3]:
        print(f"  • {strength['area']}: {strength['average_rating']:.2f}/10")
    
    print(f"\n🏆 Success Tips:")
    for i, tip in enumerate(guidance2['success_tips'][:3], 1):
        print(f"  {i}. {tip}")
    
    # Example 3: Full detailed guidance
    print("\n\n📋 Example 3: Full Detailed Guidance for Convocation")
    print("-"*80)
    
    student3 = {
        'branch': 'BBA',
        'year': 4,
        'skill_level': 'Intermediate',
        'gender': 'Female'
    }
    
    guidance3 = system.get_recommendations_for_registered_event(student3, 'Convocation')
    print_guidance(guidance3)
    
    print("\n\n" + "="*80)
    print("SIMPLE USAGE IN YOUR CODE:")
    print("="*80)
    print("""
from event_guidance_api import get_event_guidance

# When student registers for event
student = {
    'branch': 'CSE',
    'year': 2,
    'skill_level': 'Intermediate',
    'gender': 'Male'
}

# Get guidance
guidance = get_event_guidance(student, 'Hacksetu')

# Use the data
print(f"Expected Satisfaction: {guidance['overall_satisfaction']:.2f}/10")
print(f"Common Issues: {len(guidance['common_issues'])} identified")
print(f"Recommendations: {len(guidance['recommendations'])} actionable tips")

# Show to student
for rec in guidance['recommendations']:
    print(f"- {rec['advice']}")
""")
    print("="*80)
