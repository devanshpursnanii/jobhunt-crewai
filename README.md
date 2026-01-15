# JobHunt CrewAI - Multi-Agent Career Matching System

## Overview

This project is a multi-agent job discovery system that transforms a resume into career-fit insights, real job opportunities, and targeted resume improvement suggestions. Unlike simple resume fixers, this system focuses on decision support: helping users decide where to apply before optimizing how to apply.

## What It Does

**Given:**
- A resume (PDF format)
- Preferred roles and domains
- Location and experience level preferences

**The System:**
1. Analyzes the resume into a structured professional profile
2. Classifies career roles into good fit, stretch fit, and poor fit categories
3. Finds real job openings using live job search API (Serper/Google Jobs)
4. Generates targeted resume refinements for the chosen role and job

## Technology Stack

**Core Framework:**
- CrewAI - Multi-agent orchestration framework
- Python 3.11+

**LLM & Embeddings:**
- Google Gemini (via langchain-google-genai)
- Google Generative AI embeddings (text-embedding-004)
- LiteLLM - LLM integration layer

**Tools & APIs:**
- Serper API - Google Jobs search
- PDFSearchTool (crewai-tools) - PDF processing
- ChromaDB - Vector database for document embeddings
- PyPDF - PDF text extraction

**Additional Libraries:**
- Pydantic - Data validation and serialization
- python-dotenv - Environment variable management

## Project Structure

```
jobhunt-crewai/
├── agents.py           # Defines all 4 agents with LLM configuration
├── tasks.py            # Task definitions for each agent
├── tools.py            # Custom job search tool and PDF reader setup
├── crew1.py            # Phase 1: Career Discovery crew
├── crew2.py            # Phase 2: Job Search + Resume Optimization crew
├── main.py             # Entry point orchestrating both phases
├── requirements.txt    # Python dependencies
├── .env                # API keys and configuration (not in repo)
└── resume.pdf          # User's resume (not in repo)
```

## Installation and Setup

### 1. Clone and Navigate
```bash
cd jobhunt-crewai
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- crewai
- crewai_tools
- langchain_community
- langchain-google-genai
- chromadb
- pypdf
- litellm
- google-generativeai

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 5. Add Your Resume

Place your resume as `resume.pdf` in the project root directory:
```
/path/to/jobhunt-crewai/resume.pdf
```

## Running the System

### Full Flow (Recommended)
```bash
python main.py
```

This runs both Phase 1 and Phase 2 with human-in-the-loop interactions.

### Individual Phases

**Phase 1 Only (Career Discovery):**
```bash
python crew1.py
```

**Phase 2 Only (Job Search - requires Phase 1 outputs):**
```bash
python crew2.py
```

## Example Use Case

A user uploads their resume and selects interest in:
- ML Engineer
- Data Scientist

**The system:**
1. Classifies ML Engineer as good fit, Data Scientist as stretch
2. Identifies skill gaps (e.g., MLOps experience, cloud deployment)
3. Finds live ML Engineer roles in Remote/Bangalore
4. Suggests resume bullet improvements emphasizing relevant projects

**Result:**
- Clear direction on what to apply for
- Clear guidance on how to improve before applying

## Why This Project Is Different

- Uses multi-agent orchestration for real-world workflows
- Focuses on career decision-making, not just resume rewriting
- Integrates live job market data, not static examples
- Enforces structured JSON contracts between agents
- Designed with human-in-the-loop control at key decision points
- Production-oriented architecture with stateless phase separation

This is a mini hiring-tech system, not a chatbot demo.

## Output Format

All agent outputs follow strict JSON schemas:

**Resume Profile:**
```json
{
  "skills": ["Python", "Machine Learning"],
  "domains": ["AI", "FinTech"],
  "experience_level": "junior",
  "projects": [{"title": "...", "impact": "...", "tech": [...]}],
  "strengths": ["..."]
}
```

**Career Fit Analysis:**
```json
{
  "good_fit_roles": ["ML Engineer"],
  "stretch_roles": ["Data Scientist"],
  "poor_fit_roles": ["DevOps Engineer"],
  "skill_gaps": ["MLOps", "Cloud platforms"],
  "reasoning": "..."
}
```

**Job Listings:**
```json
{
  "jobs": [
    {
      "title": "ML Engineer",
      "company": "Tech Corp",
      "location": "Remote",
      "apply_link": "https://...",
      "posted_days_ago": 3
    }
  ]
}
```

**Resume Suggestions:**
```json
{
  "section_improvements": {
    "summary": ["Add quantified impact metrics"],
    "experience": ["Emphasize ML project outcomes"],
    "projects": ["Highlight production deployment"],
    "skills": ["Add cloud technologies"]
  },
  "rewritten_bullets": [
    {
      "before": "Built ML model",
      "after": "Developed ML model achieving 92% accuracy, deployed to serve 10K+ users"
    }
  ],
  "keywords_to_add": ["TensorFlow", "AWS", "CI/CD"],
  "keywords_to_remove": ["Outdated framework names"]
}
```

## Future Enhancements

- Redis caching for job search results
- ATS keyword scoring system
- Skill-gap learning path generator
- Multi-resume comparison mode
- Integration with LinkedIn API
- Email notifications for new matching jobs
- Resume version control and A/B testing

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes.

## Acknowledgments

Built with CrewAI framework and Google Gemini models.
