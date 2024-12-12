from typing import List

from fastapi import APIRouter, Query

from app.models import Resume
from app.services import fetch_resumes_with_evaluation

# Initialize the API router
router = APIRouter()


@router.get(
    "/resumes/work", 
    tags=["Work.ua"], 
    response_model=List[Resume],
    summary="Fetch resumes from Work.ua",
    description=(
        "Retrieve a list of resumes from Work.ua based on the specified job position. "
        "This endpoint scrapes resume data from the platform, processes it, and optionally evaluates the quality of the resumes using AI models. "
        "The resulting data includes detailed resume information such as name, age, location, education, and evaluation scores for easier decision-making."
    )
)
async def get_work_resumes(
    position: str = Query(..., description="The job position to search for resumes (required).")
):
    """
    Fetch resumes from Work.ua for a given job position.

    This endpoint allows users to retrieve resumes from Work.ua by specifying a job title. 
    It processes the resumes in real-time by:
    - Scraping relevant data such as name, age, location, and education.
    - Evaluating the quality of each resume using AI models (if enabled).
    - Returning a structured list of resumes with all necessary details.

    Parameters:
    - **position** (str): The job position for which resumes are searched. This is a required parameter.

    Returns:
    - A list of resumes with structured details including:
        - Title
        - Name
        - Age
        - Location
        - Education
        - AI-based evaluation scores
    """
    # Fetch and process resumes with evaluation
    resumes = await fetch_resumes_with_evaluation(position)

    # Return the processed resumes
    return resumes
