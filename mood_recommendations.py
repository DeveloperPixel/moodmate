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
            },
            'excited': {
                'actions': [
                    "Channel your energy into creative projects",
                    "Share your excitement with others",
                    "Plan something you've been wanting to do",
                    "Write down your ideas and inspirations",
                    "Try a new physical activity"
                ],
                'chatbot_responses': [
                    "Your enthusiasm is wonderful! What's got you so excited?",
                    "I love your energy! Want to brainstorm ways to channel it?",
                    "It's great to see you so energized! What are you looking forward to?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Focus this energy into achieving a goal",
                        "Start that project you've been dreaming about",
                        "Organize a group activity or event"
                    ],
                    'medium': [
                        "Make a vision board or plan",
                        "Try a new hobby or skill",
                        "Connect with others who share your interests"
                    ],
                    'low': [
                        "Write down your positive thoughts",
                        "Listen to upbeat music",
                        "Take a fun photo or selfie"
                    ]
                }
            },
            'calm': {
                'actions': [
                    "Practice mindful meditation",
                    "Do gentle yoga or stretching",
                    "Read a relaxing book",
                    "Spend time in nature",
                    "Practice deep breathing"
                ],
                'chatbot_responses': [
                    "You seem peaceful today. Would you like to maintain this tranquility?",
                    "It's nice to feel calm. What helped you reach this state?",
                    "Peaceful moments are precious. Shall we explore ways to extend this feeling?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Start a meditation practice",
                        "Create a peaceful corner in your space",
                        "Write reflectively about this feeling"
                    ],
                    'medium': [
                        "Take a mindful walk",
                        "Practice gratitude",
                        "Listen to calming music"
                    ],
                    'low': [
                        "Take deep breaths",
                        "Observe your surroundings",
                        "Enjoy a quiet moment"
                    ]
                }
            },
            'confused': {
                'actions': [
                    "Break tasks into smaller steps",
                    "Write down your thoughts",
                    "Talk to someone you trust",
                    "Take a break to clear your mind",
                    "Make a pros and cons list"
                ],
                'chatbot_responses': [
                    "It's okay to feel uncertain. Want to talk through what's confusing you?",
                    "Let's try to break this down together. What's on your mind?",
                    "Sometimes things can be overwhelming. Should we organize your thoughts?"
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Seek professional guidance",
                        "Use mind mapping techniques",
                        "Take a complete break from the situation"
                    ],
                    'medium': [
                        "Write down specific questions",
                        "Research reliable information",
                        "Discuss with a mentor or friend"
                    ],
                    'low': [
                        "Take a short walk to clear your head",
                        "Focus on what you know for sure",
                        "Make a simple action plan"
                    ]
                }
            },
            'frustrated': {
                'actions': [
                    "Take a short break",
                    "Express your feelings in writing",
                    "Do physical exercise",
                    "Practice problem-solving techniques",
                    "Use stress-relief tools"
                ],
                'chatbot_responses': [
                    "I can hear your frustration. Would you like to talk about what's bothering you?",
                    "Sometimes things don't go as planned. How can I help you work through this?",
                    "Let's take a step back and look at this from a different angle."
                ],
                'intensity_based_recommendations': {
                    'high': [
                        "Step away from the situation",
                        "Do intense physical exercise",
                        "Practice anger management techniques"
                    ],
                    'medium': [
                        "Break the problem into smaller parts",
                        "Try alternative approaches",
                        "Talk to someone for perspective"
                    ],
                    'low': [
                        "Take deep breaths",
                        "List possible solutions",
                        "Focus on what you can control"
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