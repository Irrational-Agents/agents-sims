from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PersonalityTraits(BaseModel):
    openness: int = Field(ge=0, le=10)
    conscientiousness: int = Field(ge=0, le=10)
    extraversion: int = Field(ge=0, le=10)
    agreeableness: int = Field(ge=0, le=10)
    neuroticism: int = Field(ge=0, le=10)

class Skill(BaseModel):
    skill: str
    level: int = Field(ge=0, le=10)

class Goal(BaseModel):
    long_term: Optional[str] = None
    mid_term: Optional[List[Dict[str, Any]]] = None

class SocialRelationship(BaseModel):
    relationship: str
    closeness: int = Field(ge=0, le=10)

class ImportantMemories(BaseModel):
    first_design_project: str
    surfing_breakthrough: str
    cats_arrival: str
    tsinghua_graduation: str
    hainan_villa_dream: str

class NPCModel(BaseModel):
    id: Optional[int] = None
    name: str
    birthday: str
    description: List[str]
    personality_traits: PersonalityTraits
    skills: List[Skill]
    goals: Goal
    social_relationships: Dict[str, SocialRelationship]
    important_memories: ImportantMemories

    class Config:
        schema_extra = {
            "example": {
                "name": "Zhang San",
                "birthday": "2002-04-15",
                # 其他字段按照JSON结构填充
            }
        }