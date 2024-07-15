from typing import Optional
from pydantic import BaseModel

class Candidate(BaseModel):
    check: Optional[list]=[]
    # Title: Optional[list] = []
    FirstName: Optional[list] = []
    LastName: Optional[list] = []
    Experience: Optional[list] = []
    
# class WorkExperience(BaseModel):
#     check: Optional[list]=[]
#     Location: Optional[list] = []
    
class Education(BaseModel):
    check: Optional[list]=[]
    Degree: Optional[list]=[]
    Branch: Optional[list]=[]
    Institution: Optional[list]=[]
    Score: Optional[list] = []
    YearOfPassing: Optional[list]=[]
class WorkExperience(BaseModel):
    check: Optional[list]=[]
    Role: Optional[list]=[]
    Location: Optional[list] = []
    # Branch: Optional[list]=[]
    # Institution: Optional[list]=[]
    # Score: Optional[float] = []
    # YearOfPassing: Optional[list]=[]

class Contact(BaseModel):
    check: Optional[list]=[]
    # CandidateId: Optional[list] = []
    # ResumeId: Optional[list] = []
    Contact_type: Optional[list] = []
    Contact_value: Optional[list] = []

class Skill(BaseModel):
    check: Optional[list]=[]
    # ResumeId: Optional[list] = []
    SkillName: Optional[list] = []

class ResumeIdList(BaseModel):
    check: Optional[list]=[]
    ResumeIdValue: Optional[list] = []


class Address(BaseModel):
    check: Optional[list]=[]
    City: Optional[list] = []
    
class ResumeFilters(BaseModel):
    Candidate: Optional[Candidate]
    WorkExperience : Optional[WorkExperience]
    Education: Optional[Education]
    Contact: Optional[Contact]
    Skill: Optional[Skill]
    Address: Optional[Address]
    ResumeIdList: Optional[ResumeIdList]

# class ResumeFilters(BaseModel):
#     Candidate: Optional[Candidate]
#     WorkExperience : Optional[WorkExperience]
#     Education: Optional[Education]
#     Contact: Optional[Contact]
#     Skill: Optional[Skill]
#     ResumeIdList: Optional[ResumeIdList]
    