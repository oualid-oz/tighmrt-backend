from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    user = relationship("User", back_populates="task_lists")
    tasks = relationship("Task", back_populates="task_list", cascade="all, delete-orphan")
