import openai
import json
import os
from .database import DBManager  # ✅ Correct
from .analyzer import ContentAnalyzer

class PostGenerator:
    def __init__(self):
        # Set up OpenAI API key from environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.analyzer = ContentAnalyzer()
        self.db = DBManager()
    
    def _get_prompt(self, topic, tone, cta):
        # Get top hashtags from analyzer
        top_hashtags = self.analyzer.get_top_hashtags()
        hashtags_str = ', '.join(top_hashtags[:5]) if top_hashtags else 'LinkedIn, AI, Content'
        
        # Form the prompt for OpenAI's API
        return f"""Generate 3 LinkedIn posts about "{topic}" with these guidelines:
- Tone: {tone}
- Include 2-3 of these hashtags: {hashtags_str}
- Include a call-to-action: {cta}
- Each post max 3 sentences.
- Format the output as a JSON array with objects having "content" and "hashtags" keys.
Example:
[
  {{
    "content": "Your post text here",
    "hashtags": "#example #hashtag"
  }},
  ...
]
"""
    
    def generate_posts(self, topic, tone='Professional', cta='Engage with comments'):
        # Generate the prompt for the AI model
        prompt = self._get_prompt(topic, tone, cta)
        
        try:
            # Make the API request to OpenAI for generating posts
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # You can switch to "gpt-3.5-turbo" if needed
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            
            # Parse the AI response and return the posts
            posts = json.loads(response['choices'][0]['message']['content'])
            return posts
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            # Log the error in the database
            self.db.log_error(f"Error parsing AI response: {str(e)}")
            # Fallback simple posts in case of an error
            return [
                {"content": f"{topic} is transforming the industry. Let's connect to discuss!", "hashtags": "#AI #LinkedIn"},
                {"content": f"Exploring new trends in {topic}. Join the conversation!", "hashtags": "#Innovation #Networking"},
                {"content": f"How {topic} impacts your business? Share your thoughts below.", "hashtags": "#Business #Growth"}
            ]
