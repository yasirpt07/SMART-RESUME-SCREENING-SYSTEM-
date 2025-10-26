# Match extracted skills with job description
def match_score(resume_skills, job_desc):
    job_desc = job_desc.lower()
    matched = [s for s in resume_skills if s in job_desc]
    score = (len(matched) / len(resume_skills)) * 100 if resume_skills else 0
    return round(score, 2), matched
