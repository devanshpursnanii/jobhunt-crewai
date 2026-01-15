## System Architecture

### Tools

**PDF Search Tool**
- Extracts and searches content from PDF resumes
- Uses Google Generative AI embeddings for semantic search
- ChromaDB vector database for efficient document retrieval

**Job Search Tool (Custom CrewAI BaseTool)**
- Wraps Serper API to access Google Jobs data
- Input: role, location, experience_level
- Output: normalized list of job postings with title, company, location, apply link

### Agents

**Resume Parser Agent**
- Extracts structured data from resume PDF
- Output: skills, domains, experience level, projects (with title, impact, tech stack), strengths

**Career Fit Agent**
- Compares resume profile with user interests
- Output: good_fit_roles, stretch_roles, poor_fit_roles, skill_gaps, reasoning

**Job Search Agent**
- Uses a custom Job Search Tool to fetch real job openings
- Output: jobs list with company details and application links

**Resume Optimizer Agent**
- Refines resume for a selected role or job
- Does not rewrite the entire resume
- Output: section_improvements, rewritten_bullets (before/after), keywords_to_add, keywords_to_remove

### Two-Phase Crew Design

**Phase 1: Career Discovery**
- Agents: Resume Parser, Career Fit Analyst
- Process: Sequential execution
- Goal: Understand the candidate and determine suitable roles
- Input: resume_file, preferred_roles, preferred_domains
- Output: good_fit_roles, stretch_roles, poor_fit_roles, skill_gaps
- Human reviews this output and selects roles to pursue

**Phase 2: Job Action**
- Agents: Job Search Agent, Resume Optimizer Agent
- Process: Sequential execution with sub-phases
- Goal: Convert decisions into actionable results
- Input: selected_roles, location, experience_level, resume_file, selected_job
- Output: job listings and targeted resume suggestions
