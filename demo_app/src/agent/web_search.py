from langchain.utilities import GoogleSearchAPIWrapper


class WebSearch:
    """
    The WebSearch class is a wrapper around the GoogleSearchAPIWrapper class that
    provides a simple interface for interacting with the Google Search API.

    The WebSearch class is initialized with the following parameters:
    - google_api_key: The Google API key.
    - google_cse_id: The Google Custom Search Engine ID.

    """

    def __init__(
        self,
        google_api_key: str,
        google_cse_id: str,
    ):
        """Initialize the WebSearch with required components."""
        if not all([google_api_key, google_cse_id]):
            raise ValueError("All parameters must be provided and not be None.")

        self.google_search_api_wrapper = self._initialize_google_search_api_wrapper(
            google_api_key,
            google_cse_id,
        )

    def _initialize_google_search_api_wrapper(
        self,
        google_api_key: str,
        google_cse_id: str,
    ) -> GoogleSearchAPIWrapper:
        """
        Internal method to initialize the google search api wrapper.

        Args:
            google_api_key (str): Google API key.
            google_cse_id (str): Google Custom Search Engine ID.

        Returns:
            GoogleSearchAPIWrapper: Initialized google search api wrapper instance.
        """

        return GoogleSearchAPIWrapper(
            google_api_key=google_api_key,
            google_cse_id=google_cse_id,
        )
