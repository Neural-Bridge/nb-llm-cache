"""
This module implements the FirestoreCache class, which is a subclass of the CacheInterface class.
"""
from typing import Callable, Any
from google.cloud import firestore
from cache_interface import CacheInterface
import logging
import time
import json
import hashlib

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FirestoreCache(CacheInterface):
  """
  This class implements the CacheInterface class for Firestore.
  """
  def __init__(self, collection_name):
    self._db: firestore.Client = firestore.Client()
    self._cache: firestore.CollectionReference = self._db.collection(collection_name)

  def _get_from_cache(self, key: str, num_retries: int=3)->str:
    """
    Returns the data associated with the key.

    Args:
      key: The key to get the data for.
    
    Returns:
      The data associated with the key.

    Raises:
      FirestoreCacheException: If there is an error getting the data from the cache.
    """
    try:
      doc: firestore.DocumentSnapshot = self._cache.document(key).get()
      if doc.exists:
        return doc.to_dict().get("response")
      return ""
    except Exception as e:
      if num_retries > 0:
        logger.error(f"Error getting from cache: {e}. Sleeping 2 seconds then retrying...")
        time.sleep(2)
        return self._get_from_cache(key, num_retries - 1)
      raise FirestoreCacheException(f"Firestore get cache failed after {num_retries} retries. " \
                                    f"Last error: {e}") from e

  def _add_to_cache(self, key: str, data: dict, num_retries: int=3)->bool:
    """
    Sets the data associated with the key.

    Args:
      key: The key to set the data for.
      data: The data to set.

    Returns:
      True if the data was successfully set.

    Raises:
      FirestoreCacheException: If there is an error setting the data in the cache.
    """
    try:
      self._cache.document(key).set(data)
      return True
    except Exception as e:
      if num_retries > 0:
        logger.error(f"Error adding to cache: {e}. Sleeping 2 seconds then retrying...")
        time.sleep(2)
        return self._add_to_cache(key, data, num_retries - 1)
      raise FirestoreCacheException(f"Firestore add cache failed after {num_retries} retries. " \
                                    f"Last error: {e}") from e

  def _generate_cache_key(self, func_name: str, cache_params: dict)->str:
    """
    Generates a unique cache key based on the function name and arguments.

    Args:
        func_name: The name of the function.
        cache_params: Parameters to use for caching.

    Returns:
        A unique cache key as a string.
    """
    hash_input: str = json.dumps([func_name, cache_params], sort_keys=True)
    return hashlib.sha256(hash_input.encode()).hexdigest()


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
    cache_params: dict = {k: v for k, v in kwargs.items() if k not in exclude_cache_params}
    key: str = self._generate_cache_key(func.__name__, cache_params)

    cached_result = self._get_from_cache(key)
    if cached_result:
      logger.info("Returning cached result.")
      return cached_result

    logger.info("No cached result found. Calling function.")
    try:
      result = func(**kwargs)
      self._add_to_cache(key, {"response": result, "cache_params": cache_params})
      return result
    except Exception as e:
      logger.error(f"An error occurred while executing the function: {e}")
      raise FirestoreCacheException(f"An error occurred while executing the function: {e}") from e

class FirestoreCacheException(Exception):
  """
  This class defines an exception for FirestoreCache.
  """
