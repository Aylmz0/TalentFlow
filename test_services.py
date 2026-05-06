import sys
import os

# Path problemi çözümü
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.services.resume_parser import ResumeParser
from core.services.matchmaking_service import MatchmakingService

# Test verisi
text = "I know Python and Docker. I have 2 years experience."

# Parse işlemi
parser = ResumeParser(text)
data = parser.parse()

# Match işlemi
matcher = MatchmakingService(data)
result = matcher.get_result()

# Sonuçları yazdır
print("Parsed:", data)
print("Match Result:", result)