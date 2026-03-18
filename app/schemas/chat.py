from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    role: str = Field(..., description="Role of the message e.g. 'user', 'assistant', or 'system'")
    content: str = Field(..., description="The content of the message")

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="Qwen/Qwen2.5-1.5B-Instruct-AWQ", description="The name of the model")
    messages: List[Message] = Field(..., description="The list of messages")
    temperature: Optional[float] = Field(default=0.7, description="The temperature")
    max_tokens: int = Field(default=512, le=1024, description="Max tokens (hard cap at 1024)")
    stream: Optional[bool] = Field(default=False, description="Do model has stream mode")


