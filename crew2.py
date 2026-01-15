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

# Import Phase 1 outputs (if running as part of main.py flow)
# If running crew2.py standalone, these will use the test values below
try:
    from crew1 import selected_roles, location, experience_level
except (ImportError, NameError):
    # Fallback values for standalone testing
    print("⚠️  Running crew2.py standalone - using test values")
    selected_roles = ["ML Engineer"]
    location = "Remote"
    experience_level = "junior"


# -------- PHASE 2 CREW --------
phase2_crew = Crew(
    agents=[job_search_agent, resume_optimizer_agent],
    tasks=[job_search_task, resume_optimizer_task],
    manager_llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=google_api_key
    ),
    process=Process.sequential,  # Changed from hierarchical to sequential
    verbose=True
)

# -------- PHASE 2A: JOB SEARCH --------
print("\n" + "=" * 60)
print("PHASE 2A: JOB SEARCH")
print("=" * 60)

# NOTE: These inputs come from crew1.py's human-in-the-loop section
# For standalone testing of crew2.py, uncomment the lines below:
# selected_roles = ["ML Engineer"]
# location = "Remote"
# experience_level = "junior"

phase2_inputs = {
    "selected_roles": selected_roles,
    "location": location,
    "experience_level": experience_level,
    "resume_file": "/Users/apple/Desktop/jobhunt-crewai/resume.pdf"
}

print(f"\n🔍 Searching for jobs...")
print(f"Roles: {phase2_inputs['selected_roles']}")
print(f"Location: {phase2_inputs['location']}")
print(f"Experience: {phase2_inputs['experience_level']}\n")

# Run job search first
from crewai import Crew
job_search_only_crew = Crew(
    agents=[job_search_agent],
    tasks=[job_search_task],
    process=Process.sequential,
    verbose=True
)

job_search_result = job_search_only_crew.kickoff(inputs=phase2_inputs)

# Access the output correctly from CrewOutput
job_search_output = job_search_result.raw if hasattr(job_search_result, 'raw') else str(job_search_result)

# Clean JSON from markdown code blocks if present
if "```json" in job_search_output:
    job_search_output = job_search_output.split("```json")[1].split("```")[0].strip()
elif "```" in job_search_output:
    job_search_output = job_search_output.split("```")[1].split("```")[0].strip()

job_search_data = json.loads(job_search_output)
jobs = job_search_data["jobs"]

# -------- DISPLAY JOB RESULTS --------
print("\n" + "=" * 60)
print("JOB SEARCH RESULTS")
print("=" * 60)

if not jobs:
    print("\n⚠️  No jobs found. Try different roles or location.")
    exit()

for idx, job in enumerate(jobs[:5], 1):  # Show top 5
    print(f"\n{idx}. {job['title']}")
    print(f"   Company: {job['company']}")
    print(f"   Location: {job['location']}")
    print(f"   Link: {job.get('apply_link', 'N/A')}")
    if job.get('posted_days_ago'):
        print(f"   Posted: {job['posted_days_ago']} days ago")

# -------- HUMAN INPUT: SELECT JOB --------
print("\n" + "=" * 60)
print("SELECT A JOB FOR RESUME OPTIMIZATION")
print("=" * 60)

job_choice = input(f"\nEnter job number (1-{len(jobs[:5])}): ").strip()
try:
    job_idx = int(job_choice) - 1
    if job_idx < 0 or job_idx >= len(jobs[:5]):
        print("Invalid choice. Selecting first job by default.")
        job_idx = 0
except ValueError:
    print("Invalid input. Selecting first job by default.")
    job_idx = 0

selected_job = jobs[job_idx]
print(f"\n✓ Selected: {selected_job['title']} at {selected_job['company']}")

# -------- PHASE 2B: RESUME OPTIMIZATION --------
print("\n" + "=" * 60)
print("PHASE 2B: RESUME OPTIMIZATION")
print("=" * 60)

resume_opt_inputs = {
    "resume_file": "/Users/apple/Desktop/jobhunt-crewai/resume.pdf",
    "selected_job": selected_job
}

print(f"\n📝 Optimizing resume for: {selected_job['title']}...\n")

resume_opt_crew = Crew(
    agents=[resume_optimizer_agent],
    tasks=[resume_optimizer_task],
    process=Process.sequential,
    verbose=True
)

resume_opt_result = resume_opt_crew.kickoff(inputs=resume_opt_inputs)

# Access the output correctly from CrewOutput
resume_opt_output = resume_opt_result.raw if hasattr(resume_opt_result, 'raw') else str(resume_opt_result)

# Clean JSON from markdown code blocks if present
if "```json" in resume_opt_output:
    resume_opt_output = resume_opt_output.split("```json")[1].split("```")[0].strip()
elif "```" in resume_opt_output:
    resume_opt_output = resume_opt_output.split("```")[1].split("```")[0].strip()

resume_suggestions = json.loads(resume_opt_output)

# -------- DISPLAY RESUME SUGGESTIONS --------
print("\n" + "=" * 60)
print("RESUME OPTIMIZATION SUGGESTIONS")
print("=" * 60)

print("\n📌 SECTION IMPROVEMENTS:")
for section, tips in resume_suggestions.get("section_improvements", {}).items():
    if tips:
        print(f"\n  {section.upper()}:")
        for tip in tips:
            print(f"    • {tip}")

print("\n✏️  REWRITTEN BULLETS:")
for bullet in resume_suggestions.get("rewritten_bullets", []):
    print(f"\n  Before: {bullet.get('before', 'N/A')}")
    print(f"  After:  {bullet.get('after', 'N/A')}")

print("\n➕ KEYWORDS TO ADD:")
for kw in resume_suggestions.get("keywords_to_add", []):
    print(f"  • {kw}")

print("\n➖ KEYWORDS TO REMOVE:")
for kw in resume_suggestions.get("keywords_to_remove", []):
    print(f"  • {kw}")

print("\n" + "=" * 60)
print("✅ PROCESS COMPLETE")
print("=" * 60)