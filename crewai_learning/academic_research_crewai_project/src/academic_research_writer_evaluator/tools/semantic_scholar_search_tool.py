from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests


class SemanticScholarSearchToolInput(BaseModel):
    """Input schema for SemanticScholarSearchTool."""

    query: str = Field(
        ...,
        description="The search query string to find academic papers on Semantic Scholar.",
    )


class SemanticScholarSearchTool(BaseTool):
    """Tool for searching academic papers via the Semantic Scholar API."""

    name: str = "SemanticScholarSearchTool"
    description: str = (
        "Search Semantic Scholar for peer-reviewed academic papers. "
        "Returns a list of papers with title, authors, year, abstract, citation count, and URL."
    )
    args_schema: Type[BaseModel] = SemanticScholarSearchToolInput

    def _run(self, query: str) -> str:
        """
        Search the Semantic Scholar API for academic papers matching the query.

        Args:
            query: The search string for finding academic papers.

        Returns:
            A formatted string listing all matching papers with their details.
        """
        api_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "fields": "title,authors,year,abstract,citationCount,externalIds,url",
            "limit": 10,
        }

        try:
            response = requests.get(api_url, params=params, timeout=15)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            return "Error: Unable to connect to the Semantic Scholar API. Please check your internet connection."
        except requests.exceptions.Timeout:
            return "Error: The request to Semantic Scholar API timed out. Please try again later."
        except requests.exceptions.HTTPError as e:
            return f"Error: Semantic Scholar API returned an HTTP error: {e}"
        except requests.exceptions.RequestException as e:
            return f"Error: An unexpected error occurred while calling the Semantic Scholar API: {e}"

        try:
            data = response.json()
        except ValueError:
            return "Error: Failed to parse the response from Semantic Scholar API."

        papers = data.get("data", [])

        if not papers:
            return f"No academic papers found for query: '{query}'. Try different or broader search terms."

        results = []
        for idx, paper in enumerate(papers, start=1):
            # Extract title
            title = paper.get("title") or "N/A"

            # Extract authors — each author is a dict with a "name" field
            authors_list = paper.get("authors") or []
            authors = ", ".join(
                author.get("name", "Unknown") for author in authors_list
            ) if authors_list else "N/A"

            # Extract year
            year = paper.get("year") or "N/A"

            # Extract and truncate abstract
            abstract_raw = paper.get("abstract") or "No abstract available."
            abstract = (
                abstract_raw[:500] + "..."
                if len(abstract_raw) > 500
                else abstract_raw
            )

            # Extract citation count
            citation_count = paper.get("citationCount")
            citation_count = citation_count if citation_count is not None else "N/A"

            # Build URL
            url = paper.get("url") or ""
            if not url:
                external_ids = paper.get("externalIds") or {}
                doi = external_ids.get("DOI")
                arxiv_id = external_ids.get("ArXiv")
                paper_id = paper.get("paperId", "")

                if doi:
                    url = f"https://doi.org/{doi}"
                elif arxiv_id:
                    url = f"https://arxiv.org/abs/{arxiv_id}"
                elif paper_id:
                    url = f"https://www.semanticscholar.org/paper/{paper_id}"
                else:
                    url = "N/A"

            # Format each paper entry
            paper_entry = (
                f"Paper #{idx}\n"
                f"  Title:          {title}\n"
                f"  Authors:        {authors}\n"
                f"  Year:           {year}\n"
                f"  Citations:      {citation_count}\n"
                f"  URL:            {url}\n"
                f"  Source:         Semantic Scholar\n"
                f"  Abstract:       {abstract}"
            )
            results.append(paper_entry)

        separator = "\n" + "-" * 80 + "\n"
        header = f"Semantic Scholar Search Results for: '{query}'\n{'=' * 80}\n"
        return header + separator.join(results)
