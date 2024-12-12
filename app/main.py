from fastapi import FastAPI

from app.routes import router

# Initialize the FastAPI application
app = FastAPI(
    title="Resume Scraper API",  # The title of the API displayed in the documentation
    description=(
        "This API is designed for scraping, parsing, and filtering resumes from various sources. "
        "It provides endpoints to fetch resume data, process it, and evaluate its quality using AI models. "
        "Ideal for recruiters, HR professionals, and automated systems needing structured resume analysis."
    ),
    version="1.0.0",  # Versioning for the API to track changes and improvements
    contact={
        "name": "Serhii Dratovanyi",
        "email": "sboniole@gmail.com",
        "url": "https://github.com/Boniole"  # Replace with the actual support URL if available
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"  # Replace with your license information if applicable
    }
)

# Include the router for handling API endpoints
app.include_router(router)
