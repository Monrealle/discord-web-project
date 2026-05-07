import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    discord_id = Column(String, unique=True, nullable=False, index=True)
    discord_name = Column(String, nullable=False)
    profile_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
