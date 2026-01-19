import os
from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel, Field

class ArticleSchema(BaseModel):
    """Unified schema for all ingested articles."""
    title: str
    content: str
    source: str
    url: str = "N/A"
    # Using timezone-aware UTC for Python 3.12+ compatibility
    fetched_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )

class BaseFetcher:
    """Abstract base class for all data sources."""
    def fetch(self) -> List[ArticleSchema]:
        """Method to be overridden by specific fetchers."""
        raise NotImplementedError("Each fetcher must implement the fetch method.")