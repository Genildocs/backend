from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    message: str
    type: str

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: bool

class Notification(NotificationBase):
    id: str
    vendedor_id: str
    is_read: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 