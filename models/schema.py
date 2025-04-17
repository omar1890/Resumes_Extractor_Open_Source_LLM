from pydantic import BaseModel, Field, validator
from typing import Union, List, Any, Optional


class CVExtraction(BaseModel):
    full_name: Optional[str] = Field(default="", alias="Full Name")
    email: Optional[str] = Field(default="", alias="Email")
    phone_number: Optional[str] = Field(default="", alias="Phone Number")
    education: Optional[Union[str, List[Any], dict]] = Field(default="", alias="Education")
    work_experience: Optional[Union[str, List[Any], dict]] = Field(default="", alias="Work Experience")
    skills: Optional[Union[str, List[Any], dict]] = Field(default="", alias="Skills")

    @validator("education", "work_experience", "skills", pre=True)
    def flatten_fields(cls, v):
        if isinstance(v, list):
            return " ".join(str(item) for item in v)
        if isinstance(v, dict):
            return " ".join(str(val) for val in v.values())
        return str(v or "")
