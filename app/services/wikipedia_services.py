import os
import wikipedia

from dotenv import load_dotenv
from typing import List

load_dotenv()


class WikipediaService:
    def __init__(self):
        email = os.getenv('WIKIPEDIA_USER_AGENT_EMAIL')
        if not email:
            raise ValueError('WIKIPEDIA_USER_AGENT_EMAIL must be set in .env file')

        wikipedia.set_lang("en")

    def search_titles(self, query: str, max_results: int = 5) -> List[str]:
        """Basic search to return titles."""
        try:
            results = wikipedia.search(query, results=max_results)
            print(f"Found {len(results)} results: {results}")

            return results
        except Exception as e:
            raise Exception(f"Wikipedia search failed: {str(e)}")

    def get_page_summary(self, title: str, sentences: int = 4) -> str:
        """Get summaries for a specific page"""
        try:
            return wikipedia.summary(title, sentences=sentences)
        except wikipedia.exceptions.DisambiguationError as e:
            # For disambiguation pages, try the first option
            try:
                return wikipedia.summary(e.options[0], sentences=sentences)
            except:
                return None
        except wikipedia.exceptions.PageError:
            return None
        except Exception as e:
            print(f"Summary error for '{title}': {e}")
            return None
