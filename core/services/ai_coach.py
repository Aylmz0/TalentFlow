import litellm

class AICoach:

    def __init__(self):
        pass

     # Mülakat sorusu üretimi
    def generate_interview_questions(self, skills):
        prompt = f"""
        Generate 5 technical interview questions for a candidate with these skills:
        {', '.join(skills)}
        """

        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content']


    # 🚀 Tech stack önerisi
    def suggest_tech_stack(self, skills):
        prompt = f"""
        Suggest a modern tech stack for a developer with these skills:
        {', '.join(skills)}
        Include backend, frontend and cloud tools.
        """

        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return response['choices'][0]['message']['content']