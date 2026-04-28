from .queries import (
    CREATE_RESUMES_TABLE,
    CREATE_SKILLS_TABLE,
    CREATE_EXPERIENCES_TABLE,
    CREATE_EDUCATIONS_TABLE
)

from .mysql_client import(
    get_connection,
    insert_resume,
    insert_skills,
    insert_experiences,
    insert_educations
)