from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.environ.get("GOOGLE_API_KEY")
gemini_model = "gemini-2.5-flash-lite"  # default model


from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import job_search_tool, resume_reader_tool

# Agent 1: Resume Parser
resume_parser_agent = Agent(
    role="Resume Parser",
    goal=(
        "Extract a structured professional profile from the user's resume. "
        "Identify skills, domains, experience level, projects, and strengths. "
        "Output must strictly follow the given JSON schema."
    ),
    backstory=(
        "You are an expert in resume analysis for hiring systems. "
        "You do not evaluate or judge candidates. "
        "You only extract factual information from resumes and convert it into clean, "
        "machine-readable structured data for downstream agents."
    ),
    verbose=True,
    allow_delegation=True, # Changed to True
    tools=[resume_reader_tool],
    llm=ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=google_api_key,
        temperature=0
    )
)

#Agent 2: Career fit analyser
career_fit_agent = Agent(
    role="Career Fit Analyst",
    goal=(
        "Compare the user's professional profile with their stated role and domain interests. "
        "Classify roles into good fit, stretch fit, and poor fit. "
        "Identify key skill gaps. Output must strictly follow the given JSON schema."
    ),
    backstory=(
        "You are a decision-support system for job matching. "
        "You do not motivate or encourage users. "
        "You provide objective, explainable assessments based only on evidence from the profile."
    ),
    verbose=True,
    allow_delegation=True, # Changed to True
    llm=ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=google_api_key,
        temperature=0
    )
)

# Agent 3: Job Search Agent 
job_search_agent = Agent(
    role="Job Search Agent",
    goal=(
        "Find current job openings for the selected roles and location. "
        "Use the job search tool to fetch real listings. "
        "Return only structured job data in the specified JSON schema."
    ),
    backstory=(
        "You are an automated job discovery system. "
        "You do not speculate or summarize the market. "
        "You only retrieve, normalize, and return verifiable job listings."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[job_search_tool],
    llm=ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=google_api_key,
        temperature=0
    )
)

# Agent 4: Resume Optimizer
resume_optimizer_agent = Agent(
    role="Resume Optimizer",
    goal=(
        "Refine the user's resume for a specific target role or job. "
        "Use the original resume content and the selected job context. "
        "Do NOT invent experience. "
        "Output only targeted improvements, not a full rewritten resume, "
        "unless explicitly asked."
    ),
    backstory=(
        "You are a precision resume editor for hiring systems. "
        "You optimize clarity, relevance, and keyword alignment. "
        "You never fabricate skills, metrics, or experiences."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[resume_reader_tool],  # re-read resume safely
    llm=ChatGoogleGenerativeAI(
        model=gemini_model,
        google_api_key=google_api_key,
        temperature=0
    )
)