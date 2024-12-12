# Resume Scraper API

This project is a FastAPI-based application designed to scrape, process, and evaluate resumes from the job platform [Work.ua](https://www.work.ua). The API provides structured resume data and optional AI-based evaluation to assist recruiters, HR professionals, and developers in automating and optimizing resume analysis.

---

## Features

- **Scraping Resumes from Work.ua**: Fetch resumes based on a specified job position.
- **Real-Time Resume Processing**: Extract detailed information like name, age, location, and education.
- **AI-Powered Evaluation**: Optionally evaluate resumes using OpenAI's GPT models to provide insights into hard skills, soft skills, and overall structure.
- **FastAPI Framework**: Built with FastAPI for high performance and intuitive API documentation.
- **Asynchronous Processing**: Ensures high efficiency when handling multiple resumes simultaneously.

---

## Installation

### Prerequisites

- Python 3.9+
- `pip` package manager
- API key for OpenAI services

### Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/resume-scraper-api.git
    cd resume-scraper-api
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.	**Set up environment variables**:
    Create a .env file in the project root and add the following:
    OPENAI_API_KEY=your_openai_api_key
    TELEGRAM_BOT_TOKEN=7telegram_bot_token
    HOST=your_host_ip
    PORT=8110

5.	**Run the application**:
    ```bash
    python multi.py
    ```


6.	**Access the API**:
Open your browser and navigate to http://127.0.0.1:8000/docs to view the Swagger documentation.

### Endpoints

GET /resumes/work

Retrieve resumes for a specified job position from Work.ua.
	•	Parameters:
	•	position (required): The job position to search for resumes.
	•	Response:
	•	List of resumes with the following fields:
	•	title: Job title in the resume.
	•	name: Candidate’s name.
	•	age: Candidate’s age.
	•	link: Link to the resume on Work.ua.
	•	location: Candidate’s location.
	•	education: Candidate’s education details.
	•	last_update: Date the resume was last updated.
	•	resume_text: Full text of the resume.
	•	evaluation: AI evaluation scores and recommendations (if enabled).

### Project Structure

    resume-scraper-api/
    │
    ├── app/
    │   ├── __init__.py          # Module initialization
    │   ├── main.py              # FastAPI application entry point
    │   ├── models.py            # Pydantic models for validation
    │   ├── routes.py            # API routes
    │   ├── services.py          # Core logic for scraping and evaluation
    │   └── utils.py             # Helper functions (if any)
    │
    ├── .env                     # Environment variables
    ├── requirements.txt         # Python dependencies
    ├── README.md                # Project documentation
    └── .gitignore               # Git ignored files

### Example Usage

## Request
    ``bash 
    curl -X 'GET' \
    'http://127.0.0.1:8000/resumes/work?position=Python+Developer' \
    -H 'accept: application/json'
## Response
    [
    {
        "title": "Python Developer",
        "name": "John Doe",
        "age": "30 years",
        "link": "https://www.work.ua/resumes/123456/",
        "location": "Kyiv",
        "education": "Master's in Computer Science",
        "last_update": "1 day ago",
        "resume_text": "Full resume text here...",
        "evaluation": {
        "hard_skills": 8,
        "soft_skills": 9,
        "education": 7,
        "languages": 8,
        "work_experience": 7,
        "projects_and_certificates": 9,
        "overall_structure": 8,
        "recommendations": [
            "Highlight leadership skills.",
            "Provide more details on recent projects."
        ]
        }
    }
    ]

## Technology Stack
	•	Backend Framework: FastAPI
	•	Web Scraping: BeautifulSoup and aiohttp
	•	AI Integration: OpenAI GPT-3.5 Turbo
	•	Async Programming: asyncio and aiohttp


## Future Enhancements
	•	Add support for other job platforms.
	•	Include pagination for large resume datasets.
	•	Implement more detailed evaluation categories.
	•	Optimize scraping and error handling.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For support or questions, please contact:
	•	Name: Your Name
	•	Email: your-email@example.com
	•	GitHub: your-username