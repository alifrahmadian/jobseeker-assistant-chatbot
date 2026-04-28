from langchain_core.prompts import ChatPromptTemplate

EXTRACTION_PROMPT = """
    You are a resume information extractor. Your task is to extract all the relevant information accurately. If field is not found, return null or empty list. Extract the resume in an original language. Be consistent and thorough in extracting information.
"""

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", EXTRACTION_PROMPT),
    ("human", "{resume_text}")
])