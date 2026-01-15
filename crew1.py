from tools import job_search_tool, resume_reader_tool
from agents import job_search_agent, resume_optimizer_agent, resume_parser_agent, career_fit_agent
from tasks import job_search_task, resume_optimizer_task, resume_parsing_task, career_fit_task
from crewai import Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
import json

from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]

# Phase 1 crew
from crewai import Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

phase1_crew = Crew(
    agents=[resume_parser_agent, career_fit_agent],
    tasks=[resume_parsing_task, career_fit_task],
    manager_llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=google_api_key
    ),
    process=Process.sequential,
    verbose=True
)

# -------- PHASE 1 RUN --------
print("=" * 60)
print("PHASE 1: CAREER DISCOVERY")
print("=" * 60)

phase1_inputs = {
    "resume_file": "/Users/apple/Desktop/jobhunt-crewai/resume.pdf",
    "preferred_roles": ["ML Engineer", "Data Scientist"],
    "preferred_domains": ["AI", "FinTech"]
}

print("\n📄 Analyzing resume...")
print(f"Resume file: {phase1_inputs['resume_file']}")
print(f"Preferred roles: {phase1_inputs['preferred_roles']}")
print(f"Preferred domains: {phase1_inputs['preferred_domains']}\n")

phase1_result = phase1_crew.kickoff(inputs=phase1_inputs)

import json

# Access the output correctly from CrewOutput
phase1_output = phase1_result.raw if hasattr(phase1_result, 'raw') else str(phase1_result)

# Clean JSON from markdown code blocks if present
if "```json" in phase1_output:
    phase1_output = phase1_output.split("```json")[1].split("```")[0].strip()
elif "```" in phase1_output:
    phase1_output = phase1_output.split("```")[1].split("```")[0].strip()

phase1_data = json.loads(phase1_output)

good_fit_roles = phase1_data["good_fit_roles"]
stretch_roles = phase1_data["stretch_roles"]
poor_fit_roles = phase1_data["poor_fit_roles"]
skill_gaps = phase1_data["skill_gaps"]
reasoning = phase1_data["reasoning"]

# -------- DISPLAY PHASE 1 RESULTS --------
print("\n" + "=" * 60)
print("PHASE 1 RESULTS: CAREER FIT ANALYSIS")
print("=" * 60)

print("\n✅ GOOD FIT ROLES:")
for role in good_fit_roles:
    print(f"  • {role}")

print("\n⚡ STRETCH ROLES (need some upskilling):")
for role in stretch_roles:
    print(f"  • {role}")

print("\n❌ POOR FIT ROLES:")
for role in poor_fit_roles:
    print(f"  • {role}")

print("\n📊 SKILL GAPS IDENTIFIED:")
for gap in skill_gaps:
    print(f"  • {gap}")

print(f"\n💡 REASONING: {reasoning}")

# -------- HUMAN INPUT FOR PHASE 2 --------
print("\n" + "=" * 60)
print("USER INPUT REQUIRED FOR JOB SEARCH")
print("=" * 60)

# Get selected roles
print(f"\nAvailable roles to pursue: {good_fit_roles + stretch_roles}")
selected_roles_input = input("Enter roles you want to search for (comma-separated): ").strip()
selected_roles = [r.strip() for r in selected_roles_input.split(",")] if selected_roles_input else good_fit_roles[:1]

# Get location
location = input("Enter preferred job location (e.g., 'Remote', 'Mumbai', 'Bangalore'): ").strip() or "Remote"

# Get experience level
print("\nExperience levels: intern, junior, mid, senior")
experience_level = input("Enter your experience level: ").strip().lower()
if experience_level not in ["intern", "junior", "mid", "senior"]:
    experience_level = "junior"  # default

print(f"\n✓ Selected roles: {selected_roles}")
print(f"✓ Location: {location}")
print(f"✓ Experience level: {experience_level}")


