import asyncio
import os
import re
from typing import List

import aiohttp
import openai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pydantic import ValidationError

from app.models import Evaluation, Resume

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


async def fetch_resume_details(session: aiohttp.ClientSession, link: str, headers: dict) -> str:
    """
    Asynchronously fetches the resume text from a given link.
    """
    async with session.get(link, headers=headers) as response:
        response.raise_for_status()
        soup = BeautifulSoup(await response.text(), "html.parser")

        # Locate the sections of interest in the resume
        start_section = soup.find("h2", string="Досвід роботи")
        end_section = soup.find("div", class_="card mt-0 card-indent-p hidden-print")
        extracted_text = []

        # Extract text between the identified sections
        if start_section and end_section:
            for element in start_section.find_all_next():
                if element == end_section:
                    break
                extracted_text.append(element.get_text(separator="\n", strip=True))

        result_text = "\n\n".join(extracted_text)

        # If no result is found, try fallback sections
        if not result_text:
            start_section = soup.find("div", class_="panel-collapse panel-collapse-alert collapse in")
            end_section = soup.find("p", class_="mb-0 mt-md hidden-print")
            if start_section and end_section:
                for element in start_section.find_all_next():
                    if element == end_section:
                        break
                    extracted_text.append(element.get_text(separator="\n", strip=True))
            result_text = "\n\n".join(extracted_text)

        return result_text


async def evaluate_resume_with_gpt(resume_text: str) -> Evaluation:
    """
    Asynchronously sends the resume text to GPT for evaluation.
    """
    prompt = f"""
    Ти експерт з аналізу резюме. Оціни наступний текст резюме за шкалою від 0 до 10 у наступних категоріях:
    1. Hard skills (технічні навички)
    2. Soft skills (комунікаційні та міжособистісні навички)
    3. Education (освіта)
    4. Languages (володіння мовами)
    5. Work experience (досвід роботи)
    6. Projects and certificates (проекти та сертифікати)
    7. Overall structure (загальна структура та деталізація)
    Також надай список рекомендацій для покращення резюме.

    Ось текст резюме:
    {resume_text}

    Відповідай у форматі JSON:
    {{
        "hard_skills": 0-10,
        "soft_skills": 0-10,
        "education": 0-10,
        "languages": 0-10,
        "work_experience": 0-10,
        "projects_and_certificates": 0-10,
        "overall_structure": 0-10,
        "recommendations": ["порада 1", "порада 2", ...]
    }}
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти експерт з аналізу резюме."},
                {"role": "user", "content": prompt}
            ]
        )
        evaluation_data = response["choices"][0]["message"]["content"]
        return Evaluation.parse_raw(evaluation_data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise
    except Exception as e:
        print(f"Error during resume evaluation: {e}")
        raise


async def fetch_resumes_with_evaluation(position: str) -> List[Resume]:
    """
    Asynchronously parses resumes from work.ua and evaluates them using GPT.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    resumes = []
    links_to_parse = []
    async with aiohttp.ClientSession() as session:
        current_page = 1
        while True:
            base_url = "https://www.work.ua/resumes/"
            params = {
                "search": position.replace(" ", "+"),
                "page": current_page,
                "_pjax": "#pjax"
            }
            async with session.get(base_url, params=params, headers=headers) as response:
                if response.status != 200:
                    break
                soup = BeautifulSoup(await response.text(), "html.parser")
                resume_cards = soup.find_all("div", class_=re.compile("resume-link"))

                if not resume_cards:
                    break

                # Extract details from each resume card
                for card in resume_cards:
                    title_tag = card.find("h2")
                    title = title_tag.get_text(strip=True) if title_tag else "No title"
                    link_tag = title_tag.find("a", href=True) if title_tag else None
                    link = "https://www.work.ua" + link_tag["href"] if link_tag else None
                    location_tag = card.find("p", class_="mt-xs mb-0")
                    location = location_tag.get_text(strip=True).split(",")[-1] if location_tag else "Unknown location"
                    name_tag = card.find("span", class_="strong-600")
                    name = name_tag.get_text(strip=True) if name_tag else "No name"
                    card_age_employment = card.find(class_="mt-xs mb-0")
                    age_tag = card_age_employment.find("span", string=lambda text: "років" in text if text else False)
                    age = age_tag.get_text(strip=True) if age_tag else "No age"
                    education_tag = card.find("p", class_="mb-0 mt-xs text-default-7")
                    education = education_tag.get_text(strip=True) if education_tag else "No education"
                    date_tag = card.find("time")
                    last_update = date_tag.get_text(strip=True) if date_tag else "Unknown date"

                    links_to_parse.append({
                        "title": title,
                        "name": name,
                        "age": age,
                        "link": link,
                        "location": location,
                        "education": education,
                        "last_update": last_update,
                    })

            current_page += 1

        # Fetch resume texts in parallel
        tasks = [fetch_resume_details(session, item["link"], headers) for item in links_to_parse]
        details = await asyncio.gather(*tasks, return_exceptions=True)

        # Prepare for parallel evaluation
        evaluation_tasks = []
        for idx, detail in enumerate(details):
            if isinstance(detail, str):
                item = links_to_parse[idx]
                item["resume_text"] = detail
                evaluation_tasks.append(evaluate_resume_with_gpt(detail))

        # Perform parallel evaluation of resumes
        evaluations = await asyncio.gather(*evaluation_tasks, return_exceptions=True)

        # Collect final data
        for idx, detail in enumerate(details):
            try:
                if isinstance(detail, str):
                    item = links_to_parse[idx]
                    evaluation = evaluations[idx] if isinstance(evaluations[idx], Evaluation) else None
                    if evaluation:
                        scores = [
                            evaluation.hard_skills,
                            evaluation.soft_skills,
                            evaluation.education,
                            evaluation.languages,
                            evaluation.work_experience,
                            evaluation.projects_and_certificates,
                            evaluation.overall_structure,
                        ]
                        average_score = sum(scores) / len(scores)
                        item["average_score"] = round(average_score, 2)
                    else:
                        item["average_score"] = None
                    item["evaluation"] = evaluation
                    resumes.append(Resume(**item))
            except Exception as e:
                print(f"Failed to process resume at {links_to_parse[idx]['link']}: {e}")

    resumes = sorted(resumes, key=lambda resume: resume.average_score or 0, reverse=True)
    return resumes
