from enum import Enum
from typing import Dict, List
from pathlib import Path
from pydantic import BaseModel

class SonarModels(Enum):
    SONAR_DEEP_RESEARCH = "sonar-deep-research"
    SONAR_REASONING_PRO = "sonar-reasoning-pro"
    SONAR_REASONING = "sonar-reasoning"
    SONAR_PRO = "sonar-pro"
    SONAR = "sonar"

class SonarRequest(BaseModel):
    prompt_path: Path = Path("prompt.txt")
    model: SonarModels = SonarModels.SONAR
    system_prompt: str = "You are a helpful assistance that can answer questions."
    save_response: bool = True

    def get_prompt(self) -> str:
        with open(self.prompt_path, "r") as f:
            return f.read()

    def get_messages(self) -> List[Dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    self.system_prompt
                ),
            },
            {   
                "role": "user",
                "content": (
                    self.get_prompt()
                ),
                },
            ]
