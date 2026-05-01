CREATE_RESUMES_TABLE = """
    CREATE TABLE IF NOT EXISTS resumes (
       id VARCHAR(255) PRIMARY KEY,
       category VARCHAR(255),
       job_title VARCHAR(255)
)
"""

CREATE_SKILLS_TABLE = """
    CREATE TABLE IF NOT EXISTS skills (
      id INT AUTO_INCREMENT PRIMARY KEY,
      resume_id VARCHAR(255),
      skill VARCHAR(255),
      FOREIGN KEY (resume_id) REFERENCES resumes(id)
)
"""

CREATE_EXPERIENCES_TABLE = """
    CREATE TABLE IF NOT EXISTS experiences (
        id INT AUTO_INCREMENT PRIMARY KEY,
        resume_id VARCHAR(255),
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        start_date VARCHAR(50),
        end_date VARCHAR(50),
        description TEXT,
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
)
"""

CREATE_EDUCATIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS educations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        resume_id VARCHAR(255),
        degree VARCHAR(255),
        institution VARCHAR(255),
        year VARCHAR(50),
        FOREIGN KEY (resume_id) REFERENCES resumes(id)
    )
"""