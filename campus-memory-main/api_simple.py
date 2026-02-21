"""
Event Recommendation API
Simple interface for getting event recommendations
"""

import pandas as pd
from recommendation_system import EventRecommendationSystem

class EventRecommendationAPI:
    def __init__(self):
        self.recommender = EventRecommendationSystem()
        self.df = pd.read_csv('event_feedback_dataset.csv')
        
    def get_recommendations(self, student_profile, event_list=None, top_n=5):
        """
        Get event recommendations for a student
        
        Args:
            student_profile: dict with student info
                Required keys: branch, year, gender, skill_level
                Optional keys: age, previous_participation, team_size, etc.
            event_list: list of event dicts (if None, uses all available events)
            top_n: number of recommendations to return
            
        Returns:
            List of recommended events
        """
        # Fill in defaults
        if 'age' not in student_profile:
            student_profile['age'] = 18 + student_profile.get('year', 2)
        if 'previous_participation' not in student_profile:
            student_profile['previous_participation'] = 'Low'
        if 'team_size' not in student_profile:
            student_profile['team_size'] = 3
        if 'participated_alone' not in student_profile:
            student_profile['participated_alone'] = 0
        if 'achievement' not in student_profile:
            student_profile['achievement'] = 'Participation'
            
        # Default events
        if event_list is None:
            event_list = [
                {'name': 'Hacksetu', 'type': 'Hackathon', 'level': 'National', 'duration_days': 2},
                {'name': 'Anveshan', 'type': 'Hackathon', 'level': 'University', 'duration_days': 1},
                {'name': 'Ami Chroma', 'type': 'Cultural', 'level': 'University', 'duration_days': 3},
                {'name': 'Smart India Hackathon', 'type': 'Hackathon', 'level': 'National', 'duration_days': 3},
                {'name': 'Init Maths', 'type': 'Training', 'level': 'Department', 'duration_days': 6},
                {'name': 'Convocation', 'type': 'Ceremony', 'level': 'University', 'duration_days': 1},
            ]
        
        # Find similar students to get better predictions
        similar_students = self.df[
            (self.df['student_branch'] == student_profile['branch']) &
            (self.df['student_year'] == student_profile['year']) &
            (self.df['skill_level'] == student_profile['skill_level'])
        ]
        
        past_feedback = None
        if len(similar_students) > 0:
            past_feedback = {
                'venue_rating': similar_students['venue_rating'].mean(),
                'organization_rating': similar_students['organization_rating'].mean(),
                'content_quality': similar_students['content_quality'].mean(),
                'mentor_support': similar_students['mentor_support'].mean(),
                'food_quality': similar_students['food_quality'].mean(),
                'prize_satisfaction': similar_students['prize_satisfaction'].mean(),
                'networking_opportunities': similar_students['networking_opportunities'].mean(),
                'time_management': similar_students['time_management'].mean(),
                'infrastructure': similar_students['infrastructure'].mean(),
                'registration_process': similar_students['registration_process'].mean(),
                'learning_outcome': similar_students['learning_outcome'].mean(),
            }
        
        recommendations = self.recommender.recommend_events_for_student(
            student_profile, 
            event_list, 
            past_feedback=past_feedback,
            top_n=top_n
        )
        
        return recommendations
    
    def predict_single_event(self, student_profile, event_info):
        """
        Predict outcome for a single event
        
        Returns:
            dict with prediction details
        """
        # Fill in defaults
        if 'age' not in student_profile:
            student_profile['age'] = 18 + student_profile.get('year', 2)
        if 'previous_participation' not in student_profile:
            student_profile['previous_participation'] = 'Low'
        if 'team_size' not in student_profile:
            student_profile['team_size'] = 3
        if 'participated_alone' not in student_profile:
            student_profile['participated_alone'] = 0
        if 'achievement' not in student_profile:
            student_profile['achievement'] = 'Participation'
            
        # Find similar students
        similar_students = self.df[
            (self.df['student_branch'] == student_profile['branch']) &
            (self.df['student_year'] == student_profile['year']) &
            (self.df['skill_level'] == student_profile['skill_level'])
        ]
        
        past_feedback = None
        if len(similar_students) > 0:
            past_feedback = {
                'venue_rating': similar_students['venue_rating'].mean(),
                'organization_rating': similar_students['organization_rating'].mean(),
                'content_quality': similar_students['content_quality'].mean(),
                'mentor_support': similar_students['mentor_support'].mean(),
                'food_quality': similar_students['food_quality'].mean(),
                'prize_satisfaction': similar_students['prize_satisfaction'].mean(),
                'networking_opportunities': similar_students['networking_opportunities'].mean(),
                'time_management': similar_students['time_management'].mean(),
                'infrastructure': similar_students['infrastructure'].mean(),
                'registration_process': similar_students['registration_process'].mean(),
                'learning_outcome': similar_students['learning_outcome'].mean(),
            }
        
        return self.recommender.predict_recommendation(student_profile, event_info, past_feedback)
    
    def get_event_statistics(self, event_name):
        """Get statistics for a specific event"""
        event_data = self.df[self.df['event_name'] == event_name]
        
        if len(event_data) == 0:
            return None
            
        return {
            'event_name': event_name,
            'total_feedback': len(event_data),
            'avg_satisfaction': event_data['overall_satisfaction'].mean(),
            'recommendation_rate': event_data['would_recommend'].mean(),
            'avg_organization': event_data['organization_rating'].mean(),
            'avg_content_quality': event_data['content_quality'].mean(),
            'avg_learning_outcome': event_data['learning_outcome'].mean(),
            'common_issues': event_data['issues_faced'].mode().values[0] if len(event_data) > 0 else 'None'
        }


# Example Usage
if __name__ == "__main__":
    print("="*80)
    print("EVENT RECOMMENDATION API - Quick Start Example")
    print("="*80)
    
    # Initialize API
    api = EventRecommendationAPI()
    
    # Example 1: Get recommendations for a student
    print("\n[Example 1] Get recommendations for a CSE 2nd year student")
    print("-"*80)
    
    student = {
        'branch': 'CSE',
        'year': 2,
        'gender': 'Male',
        'skill_level': 'Intermediate'
    }
    
    recommendations = api.get_recommendations(student, top_n=3)
    
    print(f"\nTop 3 recommendations for {student['branch']} Year-{student['year']} ({student['skill_level']}):\n")
    for i, rec in enumerate(recommendations, 1):
        status = "✓ RECOMMENDED" if rec['would_recommend'] else "✗ NOT RECOMMENDED"
        print(f"{i}. {rec['event_name']}")
        print(f"   {status}")
        print(f"   Confidence: {rec['confidence']*100:.1f}%")
        print(f"   Expected Satisfaction: {rec['predicted_satisfaction']:.2f}/10\n")
    
    # Example 2: Predict for specific event
    print("-"*80)
    print("[Example 2] Predict outcome for specific event: Hacksetu")
    print("-"*80)
    
    event = {'name': 'Hacksetu', 'type': 'Hackathon', 'level': 'National', 'duration_days': 2}
    
    prediction = api.predict_single_event(student, event)
    
    print(f"\nPrediction for {event['name']}:")
    print(f"  Would Recommend: {prediction['would_recommend']}")
    print(f"  Confidence: {prediction['confidence']*100:.1f}%")
    print(f"  Expected Satisfaction: {prediction['predicted_satisfaction']:.2f}/10")
    print(f"  Status: {prediction['recommendation_text']}")
    
    # Example 3: Get event statistics
    print("\n" + "-"*80)
    print("[Example 3] Get event statistics: Ami Chroma")
    print("-"*80)
    
    stats = api.get_event_statistics('Ami Chroma')
    
    if stats:
        print(f"\nStatistics for {stats['event_name']}:")
        print(f"  Total Feedback: {stats['total_feedback']:,}")
        print(f"  Average Satisfaction: {stats['avg_satisfaction']:.2f}/10")
        print(f"  Recommendation Rate: {stats['recommendation_rate']*100:.1f}%")
        print(f"  Organization Rating: {stats['avg_organization']:.2f}/10")
        print(f"  Content Quality: {stats['avg_content_quality']:.2f}/10")
        print(f"  Learning Outcome: {stats['avg_learning_outcome']:.2f}/10")
    
    print("\n" + "="*80)
    print("API READY FOR INTEGRATION!")
    print("="*80)
