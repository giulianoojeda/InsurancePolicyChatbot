""" This is a tool that returns web search results from Google. """
from langchain.agents import tool
from langchain.utilities import GoogleSearchAPIWrapper


@tool(
    "google_search",
    """Util para cuando necesitas buscar en internet para responder 
            preguntas acerca de noticias o informacion relevante a las polizas 
            de seguro en general que no se encuentran en la base de datos de 
            polizas de seguro""",
)
def google_search(query: str, google_api_key: str, google_cse_id: str) -> str:
    """This is a tool that returns web search results from Google.

    Parameters
    ----------
    query : str
        The query to search for.
    google_api_key : str
        The API key for Google Custom Search Engine.
    google_cse_id : str
        The ID for Google Custom Search Engine.

    Returns
    -------
    str
        A string with the search results.

    """
    search = GoogleSearchAPIWrapper(google_api_key, google_cse_id)

    return search.run(query)
