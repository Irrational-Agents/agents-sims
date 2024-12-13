from pydantic import BaseModel, Field, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class NPCGetRequest(BaseModel):
    names: List[str]
    isDetails: bool = Field(False, description="""
                            whether to return detailed information about the NPC, otherwise only:
                                name: str
                                prefered_name: str
                                birthday: str
                                description: List[str]     
                            """)


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

class NPCModel(BaseModel):
    id: Optional[int] = Field(None, description="Dont fill it. Just keep it for future extension")
    name: str = Field(
        description="the real name of the NPC",
        examples=["zhang_san"]
    )
    prefered_name: str = Field(
        description="Only use when creating, prefered_name will be convert to zhang_san into name",
        examples=["Zhang San"]
    )
    birthday: str
    description: List[str]
    personality_traits: PersonalityTraits
    skills: List[Skill]
    goals: List[Any]
    social_relationships: Dict[str, Any] = None
    important_memories: Dict[str, Any] = None
    status: Dict[str, Any] = None

    @root_validator(pre=True)
    def prefill(cls, values):
        values['prefered_name'] = values['name'].lower().replace(" ", "_")
        return values

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Zhang San",
                "birthday": "2002-04-15",
                "description": [
                    "Zhang San is an interior architect, who graduated from Tsinghua University's Academy of Arts",
                    "Zhang San is particularly interested in modern minimalist style and the fusion of natural elements, often incorporating oceanic themes into his work",
                    "Currently, Zhang San is designing the interior of suites for a high-end seaside hotel",
                    "Zhang San frequently attends industry seminars and design exhibitions to stay updated on the latest design trends",
                    "Zhang San lives in a small apartment in Beijing's Chaoyang District with his two Maine Coon cats named 'Bobo' and 'Langley'",
                    "Zhang San's best friend, Li Si, is a surfing instructor, and they often go surfing and diving together in Hainan Island",
                    "Zhang San appreciates Li Si's adventurous spirit and love for the ocean",
                    "Zhang San is a member of the Beijing Designers Association, where he has made many like-minded friends",
                    "Zhang San occasionally keeps in touch with his university classmates, Wang Wu and Zhao Liu, who work at different design firms",
                    "Zhang San's dream is to buy a beachfront villa in Hainan Island, combining his studio and home to create an ideal living and working environment",
                    "Zhang San usually wakes up around 10:00 AM and goes to bed around 2:00 AM. He works for about 5 hours in the afternoons on weekdays, and on weekends, he pursues his hobbies."
                ],
                "personality_traits": {
                    "openness": 9,
                    "conscientiousness": 7,
                    "extraversion": 8,
                    "agreeableness": 9,
                    "neuroticism": 4
                },
                "skills": [
                    {
                        "skill": "Interior Design",
                        "level": 9
                    },
                    {
                        "skill": "3D Modeling",
                        "level": 8
                    },
                    {
                        "skill": "Color Theory",
                        "level": 9
                    },
                    {
                        "skill": "Project Management",
                        "level": 7
                    },
                    {
                        "skill": "Client Communication",
                        "level": 8
                    },
                    {
                        "skill": "Sustainability Design",
                        "level": 7
                    },
                    {
                        "skill": "Surfing",
                        "level": 6
                    },
                    {
                        "skill": "Scuba Diving",
                        "level": 5
                    },
                    {
                        "skill": "Digital Illustration",
                        "level": 8
                    },
                    {
                        "skill": "Feng Shui",
                        "level": 6
                    },
                    {
                        "skill": "Furniture Design",
                        "level": 7
                    },
                    {
                        "skill": "Networking",
                        "level": 8
                    },
                    {
                        "skill": "Trend Analysis",
                        "level": 8
                    },
                    {
                        "skill": "Photography",
                        "level": 6
                    },
                    {
                        "skill": "Public Speaking",
                        "level": 7
                    },
                    {
                        "skill": "English",
                        "level": 7
                    }
                ],
                "goals": [
                    {
                        "long_term": "Buy a beachfront villa in Hainan Island, combining his studio and home to create an ideal living and working environment"
                    },
                    {
                        "mid_term": [
                            {
                                "description": "To establish his own boutique interior design studio for high-end residential and hospitality projects.",
                                "deadline": "2027-07=5-31"
                            }
                        ]
                    }
                ],
                "social_relationships": {
                    "social_relationships": {
                        "Li Si": {
                            "relationship": "Best friend",
                            "closeness": 9
                        },
                        "Chen Mei": {
                            "relationship": "Girlfriend",
                            "closeness": 8
                        },
                        "Kenta Takahashi": {
                            "relationship": "Design collaborator",
                            "closeness": 6
                        },
                        "Sakura Sato": {
                            "relationship": "Language exchange partner",
                            "closeness": 5
                        },
                        "Professor Yang": {
                            "relationship": "Mentor",
                            "closeness": 7
                        }
                    }
                },
                "important_memories": {
                    "first_design_project": "Completing his first independent interior design project, with the client praising his use of ocean elements",
                    "surfing_breakthrough": "The exhilarating moment of successfully riding a big wave while surfing with his best friend Li Si in Hainan",
                    "cats_arrival": "Adopting two Maine Coon cats, Bobo and Langley, from a shelter, bringing life to his apartment",
                    "tsinghua_graduation": "Graduating from Tsinghua University's Academy of Arts, feeling confident after receiving high praise from his mentor",
                    "hainan_villa_dream": "Standing on a beach in Hainan during a vacation, suddenly envisioning his dream of owning a villa there"
                }
            }
        }


class NPCInfoModel(BaseModel):
    id: Optional[int] = Field(None, description="Dont fill it. Just keep it for future extension")
    name: str
    prefered_name: str
    birthday: str
    description: List[str]
    current_location: Optional[str] = None
    current_position: Optional[Dict[str, int]] = None

    @root_validator(pre=True)
    def prefill(cls, values):
        values['prefered_name'] = values['name'].lower().replace(" ", "_")
        return values

####################
# Player 相关模型
class PlayerInfo(BaseModel):
    id: str
    name: str
    level: int = Field(ge=1)
    exp: int = Field(ge=0)
    position: Optional[Dict[str, int]] = None
    last_login: Optional[datetime] = None

class PlayerResponse(BaseModel):
    player: PlayerInfo

# Map 
class Position(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)

class MapObject(BaseModel):
    id: str
    type: str  # building, npc, etc.
    position: Position
    properties: Optional[Dict[str, Any]] = None

class MapTown(BaseModel):
    id: str
    name: str
    size: Dict[str, int]  # width, height
    objects: List[MapObject]
    background: Optional[str] = None

class MapScene(BaseModel):
    id: str
    name: str
    type: str  # indoor, outdoor, etc.
    objects: List[MapObject]
    properties: Optional[Dict[str, Any]] = None

class MapTownResponse(BaseModel):
    town: MapTown

class MapSceneResponse(BaseModel):
    scene: MapScene

# Navigation 
class NavigateRequest(BaseModel):
    npc_id: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)

class NavigateResponse(BaseModel):
    success: bool
    position: Position
    path: Optional[List[Position]] = None
    estimated_time: Optional[float] = None

# Config
class EquipmentConfig(BaseModel):
    id: str
    name: str
    type: str
    level: int = Field(ge=1)
    properties: Dict[str, Any]
    requirements: Optional[Dict[str, Any]] = None

class BuildingConfig(BaseModel):
    id: str
    name: str
    type: str
    size: Dict[str, int]  # width, height
    properties: Dict[str, Any]
    requirements: Optional[Dict[str, Any]] = None

class EquipmentsConfigResponse(BaseModel):
    equipments: List[EquipmentConfig]
    categories: Optional[Dict[str, List[str]]] = None
    total: int

class BuildingsConfigResponse(BaseModel):
    buildings: List[BuildingConfig]
    categories: Optional[Dict[str, List[str]]] = None
    total: int

# Chat
class ChatMessage(BaseModel):
    id: str
    sender: str
    receiver: str
    content: str
    timestamp: datetime
    type: str = "text"  # text, emotion, action, etc.
    properties: Optional[Dict[str, Any]] = None

class NPCChatUpdate(BaseModel):
    npc_id: str
    messages: List[ChatMessage]
    emotions: Optional[Dict[str, float]] = None  # 情绪状态
    context: Optional[Dict[str, Any]] = None  # 对话上下文

class NPCChatUpdateResponse(BaseModel):
    updated: bool
    chat_id: Optional[str] = None
    last_message: Optional[ChatMessage] = None
    next_update: Optional[datetime] = None