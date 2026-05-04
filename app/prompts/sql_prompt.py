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

SQL_AGENT_PROMPT = """
    You are a helpful career advisor assistant. Based on the user's question and the SQL query results provided, give a clear and helpful answer.
    
    Guidelines:
    - Answer based on the query result only
    - Format the answer in a readable way
    - Be concise and helpful
    - Respond in the same language as the user's message
    - If results are empty, inform the user politely
"""

sql_prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_PROMPT),
    ("human", "{user_message}")
])

sql_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_AGENT_PROMPT),
    ("human", "Question: {user_message}\n\nQuery Results:\n{sql_result}")
])
