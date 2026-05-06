class MatchmakingService:

    def __init__(self, resume_data):
        self.resume_data = resume_data

    def match_skills(self):
        job_skills = ["python", "docker", "kubernetes"]

        matched = []

        for skill in job_skills:
            if skill in self.resume_data["skills"]:
                matched.append(skill)

        return matched

    def get_result(self):
        matched = self.match_skills()

        score = len(matched) * 30

        return {
            "matched_skills": matched,
            "score": score
        }