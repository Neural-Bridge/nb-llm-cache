"""This module defines the interface for a cache."""
from typing import Callable, Any

class CacheInterface:
  """
  This class defines the interface for a cache.
  """
  def _get_from_cache(self, key: str) -> str:
    """
    Returns the data associated with the key.

    Args:
      key: The key to get the data for.
    
    Returns:
      The data associated with the key.
    """

    raise NotImplementedError

  def _add_to_cache(self, key: str, data: dict) -> bool:
    """
    Sets the data associated with the key.

    Args:
      key: The key to set the data for.
      data: The data to set.
    
    Returns:
      True if the data was successfully set.
    """

    raise NotImplementedError

  # def _generate_cache_key(self, func_name: str, cache_params: dict)->str:
  #   """
  #   Generates a cache key from the function name and the provided keyword arguments.

  #   Args:
  #     func_name: The name of the function to generate the cache key for.
  #     cache_params: The keyword arguments to generate the cache key from.

  #   Returns:
  #     The cache key.
  #   """

  #   raise NotImplementedError

  def call(self, func: Callable, exclude_cache_params=None, **kwargs: Any)->Any:
    """
    Calls a function with the provided keyword arguments and caches the result.
    Excludes specified parameters from being considered in cache key generation.

    Args:
      func: The function to call.
      exclude_cache_params: List of parameter names to exclude from caching.
      **kwargs: Keyword arguments to pass to the function.

    Returns:
      The result of the function call.
    """

    raise NotImplementedError

