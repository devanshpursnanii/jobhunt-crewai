from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]

from crewai import Task
from agents import resume_parser_agent, career_fit_agent, job_search_agent, resume_optimizer_agent

# Task for Resume Parser Agent
resume_parsing_task = Task(
    description=(
        "Read and analyze the resume PDF file using the PDF reader tool. "
        "The resume is located at: {resume_file} "
        "Search through the entire PDF content to extract: "
        "1) All technical and soft skills mentioned, "
        "2) Domains/industries of expertise, "
        "3) Experience level (intern/junior/mid/senior) based on years and roles, "
        "4) Projects with their titles, impact/achievements, and technologies used, "
        "5) Key strengths and capabilities. "
        "Be thorough and comprehensive. Output ONLY valid JSON matching the expected schema."
    ),
    expected_output="""
{
  "skills": ["string"],
  "domains": ["string"],
  "experience_level": "intern|junior|mid|senior",
  "projects": [
    { "title": "string", "impact": "string", "tech": ["string"] }
  ],
  "strengths": ["string"]
}
""",
    agent=resume_parser_agent
)

# Task for Career Fit Analyser
career_fit_task = Task(
    description=(
        "Analyze the structured resume profile from the previous task. "
        "The user is interested in these roles: {preferred_roles} "
        "The user is interested in these domains: {preferred_domains} "
        "Classify each role into good fit, stretch fit, or poor fit based on the resume profile. "
        "Identify key skill gaps. "
        "Output ONLY valid JSON matching the exact schema."
    ),
    expected_output="""
{
  "good_fit_roles": ["string"],
  "stretch_roles": ["string"],
  "poor_fit_roles": ["string"],
  "skill_gaps": ["string"],
  "reasoning": "string"
}
""",
    agent=career_fit_agent,
    context=[resume_parsing_task]  # Receives output from previous task
)

# Task for Job Search Agent 
job_search_task = Task(
    description=(
        "Search for job openings with these parameters: "
        "Roles: {selected_roles} "
        "Location: {location} "
        "Experience level: {experience_level} "
        "Use the job search tool to fetch current openings. "
        "Return ONLY the top 5 most relevant jobs. "
        "Output must strictly follow the JSON schema."
    ),
    expected_output="""
{
  "jobs": [
    {
      "title": "string",
      "company": "string",
      "location": "string",
      "apply_link": "string",
      "posted_days_ago": "number|null"
    }
  ]
}
""",
    agent=job_search_agent
)

# Task for Resume Optimizer Agent
resume_optimizer_task = Task(
    description=(
        "Read and analyze the resume PDF file using the PDF reader tool. "
        "The resume is at: {resume_file} "
        "Review it against this selected job: {selected_job} "
        "Provide targeted resume improvements including: "
        "1) Section-by-section improvement suggestions (summary, experience, projects, skills), "
        "2) Specific bullets to rewrite with before/after versions, "
        "3) Keywords to add for ATS optimization, "
        "4) Keywords to remove if not relevant. "
        "Do NOT fabricate experience. Provide only factual refinements based on existing content."
    ),
    expected_output="""
{
  "section_improvements": {
    "summary": ["string"],
    "experience": ["string"],
    "projects": ["string"],
    "skills": ["string"]
  },
  "rewritten_bullets": [
    { "before": "string", "after": "string" }
  ],
  "keywords_to_add": ["string"],
  "keywords_to_remove": ["string"]
}
""",
    agent=resume_optimizer_agent
)
