from openai import OpenAI
import json
import os
from database import DBManager
from analyzer import ContentAnalyzer

class PostGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.analyzer = ContentAnalyzer()
        self.db = DBManager()
    
    def _get_prompt(self, topic, tone, cta):
        top_hashtags = self.analyzer.get_top_hashtags()
        hashtags_str = ', '.join(top_hashtags[:5]) if top_hashtags else 'LinkedIn, AI, Content'
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
        prompt = self._get_prompt(topic, tone, cta)
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        try:
            posts = json.loads(response.choices[0].message.content)
            return posts
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            # Fallback simple posts
            return [
                {"content": f"{topic} is transforming the industry. Let's connect to discuss!", "hashtags": "#AI #LinkedIn"},
                {"content": f"Exploring new trends in {topic}. Join the conversation!", "hashtags": "#Innovation #Networking"},
                {"content": f"How {topic} impacts your business? Share your thoughts below.", "hashtags": "#Business #Growth"}
            ]
