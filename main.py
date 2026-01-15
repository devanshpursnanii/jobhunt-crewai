"""
JobHunt CrewAI - Main Entry Point
Complete flow with human-in-the-loop interactions
"""

print("=" * 60)
print("🎯 JOBHUNT CREWAI - MULTI-AGENT JOB SEARCH SYSTEM")
print("=" * 60)
print("\nThis system will:")
print("1. Analyze your resume")
print("2. Suggest career fits based on your interests")
print("3. Search for real job openings")
print("4. Provide targeted resume optimization\n")

# Import and run Phase 1
print("Starting Phase 1: Career Discovery...\n")
import crew1

# Phase 1 outputs these variables that Phase 2 needs:
# - selected_roles
# - location  
# - experience_level

print("\n\nStarting Phase 2: Job Search & Resume Optimization...\n")

# Import Phase 2 (it will use the variables from crew1)
import crew2

print("\n\n🎉 All done! Good luck with your job search!")
