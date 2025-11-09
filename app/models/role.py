from app.db.base_class import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )

    def __repr__(self):
        return f"Role(id={self.id}, name={self.name}, code={self.code}, description={self.description})"
