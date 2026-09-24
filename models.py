from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

class PillarMasterModel(Base):
    __tablename__ = "pillar_master"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_reference = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    pillar_metrics = relationship("PillarMetricModel", back_populates="master", cascade="all, delete-orphan")

class PillarMetricModel(Base):
    __tablename__ = "pillar_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    master_id = Column(Integer, ForeignKey("pillar_master.id"), nullable=False)
    pillar_name = Column(String(50), nullable=False)
    metric_score = Column(Float, default=0.0)
    details = Column(Text, nullable=True)
    
    master = relationship("PillarMasterModel", back_populates="pillar_metrics")
