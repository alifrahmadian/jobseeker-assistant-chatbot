from pdf2image import convert_from_path
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from app.utils import logger, load_llm
from app.schemas import UserBackground
from app.prompts import CV_PARSER_PROMPT

import base64
from io import BytesIO

llm = load_llm(temperature=0.0, model="gpt-4o")
llm_structured = llm.with_structured_output(UserBackground)

def parse_pdf(pdf_path: str) -> list:
    try:
        logger.info(f"Parsing PDF at path: {pdf_path}")
        images = convert_from_path(pdf_path)
        
        image_data = []
        for image in images:
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
            image_data.append(base64_image)
            
        logger.info(f"PDF parsed successfuly! {len(image_data)} pages found.")
        return image_data
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise

@tool
def cv_parser_tool(pdf_path: str) -> str:
    """
    Use this tool to parse and extract information from a user's CV/resume in PDF format. Use this when the user uplaods or provides a PDF file path of their CV/resume. This tool uses multimodal AI to read and extract information from the PDF, including text-based and image-based (scanned) CVs/
    
    Returns a UserBackground object containing:
    - job_title: Current or most recent job title
    - skills: List of skills
    - experiences: List of work experiences
    - educations: List of education background
    - raw_text: Raw text extracted from CV
    
    Example:
    1. User uploads their CV for job recommendation
    2. User wants their CV analyzed for skill gap analysis
    3. User wants their CV scored against other resumes
    """
    
    image_data = parse_pdf(pdf_path)
    
    try:
        logger.info("Invoking CV parser tool with multimodal input...")

        content = [
            {
                "type": "text",
                "text": CV_PARSER_PROMPT
            }
        ]
        
        for image in image_data:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                }
            })
        
        result = llm_structured.invoke([HumanMessage(content=content)])
        logger.info("CV parser tool executed successfully!")
        
        return result.model_dump_json()
    except Exception as e:
        logger.error(f"Error in CV parser tool: {e}")
        return f"Error parsing CV: {e}"