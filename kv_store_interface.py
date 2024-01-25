"""This module defines the interface for a cache."""
class KVStoreInterface:
  """
  This class defines the interface for a cache.
  """
  def get_from_cache(self, key: str, cache_params: dict) -> str:
    """
    Returns the data associated with the key.

    Args:
      key: The key to get the data for.
      cache_params: The parameters used in the cache key.
    
    Returns:
      The data associated with the key.
    """

    raise NotImplementedError

  def add_to_cache(self, key: str, value: dict) -> bool:
    """
    Sets the data associated with the key.

    Args:
      key: The key to set the data for.
      value: The data to set.
    
    Returns:
      True if the data was successfully set.
    """

    raise NotImplementedError
