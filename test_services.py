import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.services.resume_parser import ResumeParser
from core.services.matchmaking_service import MatchmakingService


text = "I know Python and Docker. I have 2 years experience."


parser = ResumeParser(text)
data = parser.parse()


matcher = MatchmakingService(data)
result = matcher.get_result()


print("Parsed:", data)
print("Match Result:", result)