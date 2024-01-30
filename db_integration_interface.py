"""This module defines the interface for a cache."""
class DBIntegrationInterface:
  """
  This class defines the interface for a cache.
  """
  def get_from_cache(self, key: str) -> str:
    """
    Returns the data associated with the key.

    Args:
      key: The key to get the data for.
    
    Returns:
      str: A string containing the response
    """

    raise NotImplementedError

  def add_to_cache(self, key: str, value: str) -> bool:
    """
    Sets the data associated with the key.

    Args:
      key: The key to set the data for.
      value: The data to set.
    
    Returns:
      True if the data was successfully set.
    """

    raise NotImplementedError
