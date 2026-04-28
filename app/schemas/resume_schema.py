from pydantic import BaseModel
from typing import List, Optional


class Experience(BaseModel):
    job_title: Optional[str] = None
    company_name: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    
class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None

class Resume(BaseModel):
    job_title: str
    skills: List[str] = []
    experiences: List[Experience] = []
    educations: List[Education] = []
    