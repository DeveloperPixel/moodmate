from typing import List, Dict

class MoodRecommendationEngine:
    def __init__(self):
        self.mood_categories = {
            'happy': {
                'actions': [
                    "Share your joy with friends or family",
                    "Document what made you happy today",
                    "Express gratitude through journaling",
                    "Plan a fun activity to maintain momentum",
                    "Try a new hobby while in good spirits"
                ],
                'chatbot_responses': [
                    "I'm so glad you're feeling happy! Would you like to share what made your day special?",
                    "Your positive energy is contagious! Let's plan something fun to keep this momentum going.",
                    "It's wonderful to see you in such good spirits! Have you considered sharing this joy with others?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Channel your positive energy into a creative project",
                        "Consider mentoring or helping others",
                        "Start a gratitude journal to remember these moments"
                    ],
                    'medium': [
                        "Share your good mood through small acts of kindness",
                        "Take photos to capture this happy moment",
                        "Plan a social activity with friends"
                    ],
                    'low': [
                        "Build on this feeling with some light exercise",
                        "Listen to upbeat music",
                        "Call a friend for a quick chat"
                    ]
                }
            },
            'sad': {
                'actions': [
                    "Practice gentle self-care activities",
                    "Try light exercise or stretching",
                    "Listen to calming music",
                    "Reach out to a trusted friend",
                    "Write down your feelings"
                ],
                'chatbot_responses': [
                    "I hear you're feeling down. Would you like to talk about what's bothering you?",
                    "It's okay to feel sad. How about we try something gentle to lift your spirits?",
                    "Remember, this feeling is temporary. Should we explore some calming activities together?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Consider speaking with a mental health professional",
                        "Practice deep breathing exercises",
                        "Use grounding techniques to stay present"
                    ],
                    'medium': [
                        "Take a relaxing walk in nature",
                        "Try journaling your thoughts",
                        "Do some light stretching exercises"
                    ],
                    'low': [
                        "Watch a comfort movie or show",
                        "Have a warm, soothing drink",
                        "Listen to peaceful music"
                    ]
                }
            },
            'angry': {
                'actions': [
                    "Practice deep breathing exercises",
                    "Go for a brisk walk",
                    "Write down what's bothering you",
                    "Find a private space to cool down",
                    "Try progressive muscle relaxation"
                ],
                'chatbot_responses': [
                    "I understand you're feeling angry. Would you like to talk about what triggered this?",
                    "Let's take a moment to breathe together. Ready to try some calming exercises?",
                    "Your feelings are valid. How about we channel this energy into something productive?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Step away from the situation temporarily",
                        "Practice anger management techniques",
                        "Consider professional guidance"
                    ],
                    'medium': [
                        "Do physical exercise to release tension",
                        "Write down your thoughts",
                        "Practice counting to ten slowly"
                    ],
                    'low': [
                        "Listen to calming music",
                        "Try simple breathing exercises",
                        "Change your environment briefly"
                    ]
                }
            },
            'anxious': {
                'actions': [
                    "Try the 5-4-3-2-1 grounding exercise",
                    "Practice slow, deep breathing",
                    "Go for a mindful walk",
                    "Write down your worries",
                    "Do gentle stretching"
                ],
                'chatbot_responses': [
                    "I notice you're feeling anxious. Would you like to try a quick grounding exercise?",
                    "Let's take this moment by moment. How about we focus on your breathing together?",
                    "You're not alone in this. Should we explore some calming techniques?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Use the STOP technique (Stop, Take a breath, Observe, Proceed)",
                        "Contact a mental health professional",
                        "Practice progressive muscle relaxation"
                    ],
                    'medium': [
                        "Try mindfulness meditation",
                        "Make a list of current concerns",
                        "Do some light physical activity"
                    ],
                    'low': [
                        "Have some herbal tea",
                        "Listen to nature sounds",
                        "Practice gentle stretching"
                    ]
                }
            }
        }

    def get_intensity_level(self, intensity: int) -> str:
        if intensity >= 8:
            return 'high'
        elif intensity >= 5:
            return 'medium'
        else:
            return 'low'

    def get_recommendations(self, mood: str, intensity: int) -> Dict:
        if mood not in self.mood_categories:
            return {
                'actions': ["Take some time to reflect on your feelings"],
                'chatbot_response': "I'm here to listen. Would you like to talk about how you're feeling?",
                'intensity_specific': ["Practice self-awareness"]
            }

        intensity_level = self.get_intensity_level(intensity)
        mood_data = self.mood_categories[mood]

        return {
            'actions': mood_data['actions'],
            'chatbot_response': mood_data['chatbot_responses'][0],  # Get first response for now
            'intensity_specific': mood_data['intensity_based_recommendations'][intensity_level]
        }