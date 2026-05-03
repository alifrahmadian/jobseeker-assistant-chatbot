from langchain_core.prompts import ChatPromptTemplate

SCHEMA_DESCRIPTION = """
Table: resumes (id VARCHAR, category VARCHAR, job_title VARCHAR)
Table: skills (id INT, resume_id VARCHAR, skill VARCHAR)
Table: experiences (id INT, resume_id VARCHAR, job_title VARCHAR, company_name VARCHAR, start_date VARCHAR, end_date VARCHAR, description TEXT)
Table: educations (id INT, resume_id VARCHAR, degree VARCHAR, institution VARCHAR, year VARCHAR)
"""

SQL_PROMPT = f"""
You are a professional SQL expert. Generate a valid MySQL query based on the user input. Only return MySQL query, nothing else. No explanation, no markdown, no backticks.
If the question cannot be answered with the available schema, return 'INVALID_QUERY'.

The query should be based on the following database schema:
{SCHEMA_DESCRIPTION}
"""

sql_prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_PROMPT),
    ("human", "{user_message}")
])
