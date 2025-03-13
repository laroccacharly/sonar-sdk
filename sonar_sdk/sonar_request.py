from enum import Enum
from typing import Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field

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
    prompt_text: Optional[str] = None

    def get_prompt(self) -> str:
        if self.prompt_text is not None:
            return self.prompt_text
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
