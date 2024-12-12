from typing import List, Optional

from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    hard_skills: int = Field(..., ge=0, le=10, example=8)
    soft_skills: int = Field(..., ge=0, le=10, example=7)
    education: int = Field(..., ge=0, le=10, example=8)
    languages: int = Field(..., ge=0, le=10, example=9)
    work_experience: int = Field(..., ge=0, le=10, example=6)
    projects_and_certificates: int = Field(..., ge=0, le=10, example=8)
    overall_structure: int = Field(..., ge=0, le=10, example=7)
    recommendations: List[str] = Field(
        ..., example=[
            "Уточнити досвід роботи над великими проєктами, якщо є.",
            "Додати приклади використання Python у реальних проєктах.",
            "Оптимізувати структуру резюме для уникнення повторів."
        ]
    )


class Resume(BaseModel):
    title: str = Field(..., example="Python Developer")
    name: str = Field(..., example="Олег")
    age: Optional[str] = Field(None, example="20 років")
    link: str = Field(..., example="https://www.work.ua/resumes/10464672/")
    location: Optional[str] = Field(None, example="Дистанційно")
    education: Optional[str] = Field(None, example="Незакінчена вища освіта · Повна зайнятість, неповна зайнятість")
    last_update: Optional[str] = Field(None, example="3 дні тому")
    resume_text: Optional[str] = Field(
        None,
        example=(
            "Wordpress developer\n"
            "Розробка та налаштування веб-сайтів на платформі WordPress.\n"
            "Інтеграція та налаштування WooCommerce для онлайн-магазинів."
        )
    )
    evaluation: Optional[Evaluation] = Field(None)
    average_score: Optional[float] = Field(..., ge=0, le=10, example=6.43)
