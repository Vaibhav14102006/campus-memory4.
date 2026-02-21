"""
Custom Test - Event Guidance for Your Student Profile
"""

from event_guidance_system import EventGuidanceSystem, print_guidance

print("="*80)
print("TESTING EVENT GUIDANCE SYSTEM")
print("="*80)

# Initialize system
system = EventGuidanceSystem()

# Your custom student profile
student = {
    'branch': 'CSE',
    'year': 2,
    'skill_level': 'Intermediate',
    'gender': 'Male'  # Default
}

# Event registered
event_name = 'Ami Chroma'

print("\n📋 STUDENT PROFILE:")
print("-"*80)
print(f"  Branch        : {student['branch']}")
print(f"  Year          : {student['year']}")
print(f"  Skill Level   : {student['skill_level']}")
print(f"  Event         : {event_name}")

print("\n🔍 Analyzing 100,000+ past feedback records...")
print("   Finding similar students and common patterns...")

# Get guidance
guidance = system.get_recommendations_for_registered_event(student, event_name)

# Display full guidance
print("\n")
print_guidance(guidance)

# Additional insights
print("\n" + "="*80)
print("QUICK SUMMARY FOR YOU")
print("="*80)

print(f"\n✓ Based on {guidance['total_past_attendees']:,} students who attended this event")
print(f"✓ {guidance['similar_profile_attendees']:,} had similar profile as you")

if guidance['overall_satisfaction'] >= 7.5:
    print(f"\n✅ GOOD NEWS! This is a highly-rated event ({guidance['overall_satisfaction']:.2f}/10)")
    print(f"   {guidance['recommendation_rate']:.1f}% of past attendees recommend it")
elif guidance['overall_satisfaction'] >= 6.5:
    print(f"\n⚠️  MIXED REVIEWS: Average satisfaction is {guidance['overall_satisfaction']:.2f}/10")
    print(f"   {guidance['recommendation_rate']:.1f}% recommend it - prepare well!")
else:
    print(f"\n🔴 CHALLENGING EVENT: Low satisfaction at {guidance['overall_satisfaction']:.2f}/10")
    print(f"   Only {guidance['recommendation_rate']:.1f}% recommend it - be extra prepared!")

print(f"\n📊 YOUR EXPECTED SATISFACTION:")
print(f"   Similar students rated it: {guidance['expectations'].get('similar_students_satisfaction', guidance['overall_satisfaction']):.2f}/10")

if guidance['common_issues']:
    print(f"\n⚠️  TOP 3 THINGS TO WATCH OUT FOR:")
    for i, issue in enumerate(guidance['common_issues'][:3], 1):
        print(f"   {i}. {issue['issue']} - {issue['percentage']:.1f}% reported this")

if guidance['recommendations']:
    high_priority = [r for r in guidance['recommendations'] if r['priority'] == 'High']
    if high_priority:
        print(f"\n🔥 {len(high_priority)} HIGH PRIORITY RECOMMENDATIONS:")
        for i, rec in enumerate(high_priority, 1):
            print(f"   {i}. {rec['category']}")
            print(f"      → {rec['advice']}")

if guidance['success_tips']:
    print(f"\n💡 QUICK SUCCESS TIPS:")
    for i, tip in enumerate(guidance['success_tips'][:3], 1):
        print(f"   {i}. {tip}")

print("\n" + "="*80)
print("TEST COMPLETE! Use this guidance to prepare for your event 🎯")
print("="*80)
