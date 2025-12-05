"""SQLModel models for AutoSciLab with async-friendly usage.

Includes: User, Paper, Vector, Task
"""
from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Paper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    abstract: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    doi: Optional[str] = None
    year: Optional[int] = None
    authors: Optional[str] = None  # comma-separated for simplicity
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Vector(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paper_id: Optional[int] = Field(default=None, foreign_key="paper.id")
    vector: Optional[str] = Field(sa_column=Column(JSON), default=None)  # store JSON array
    metadata: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: Optional[str] = None  # external task id (celery)
    job_type: str = Field(index=True)
    params: Optional[str] = Field(sa_column=Column(JSON), default=None)
    status: str = Field(default='pending', index=True)
    result: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
