"""
This module implements the FirestoreCache class, which is a subclass of the CacheInterface class.
"""
from google.cloud import firestore
from kv_store_interface import KVStoreInterface
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FirestoreCache(KVStoreInterface):
  """
  This class implements the CacheInterface class for Firestore.
  """
  def __init__(self, collection_name):
    self._db: firestore.Client = firestore.Client()
    self._cache: firestore.CollectionReference = self._db.collection(collection_name)

  def get_from_cache(self, key: str, cache_params: dict)->str:
    """
    Returns the data associated with the key.

    Args:
      key: The key to get the data for.
      cache_params: The parameters used in the cache key.
    
    Returns:
      The data associated with the key.

    Raises:
      FirestoreCacheException: If there is an error getting the data from the cache.
    """
    try:
      doc: firestore.DocumentSnapshot = self._cache.document(key).get()
      if doc.exists and doc.to_dict().get("cache_params") == cache_params:
        return doc.to_dict().get("response")
      return ""
    except Exception as e:
      logger.error(f"Error getting from cache: {e}.")
      raise FirestoreCacheException(f"Firestore get cache failed: {e}") from e

  def add_to_cache(self, key: str, value: dict)->bool:
    """
    Sets the data associated with the key.

    Args:
      key: The key to set the data for.
      value: The data to set.

    Returns:
      True if the data was successfully set.

    Raises:
      FirestoreCacheException: If there is an error setting the data in the cache.
    """
    try:
      self._cache.document(key).set(value)
      return True
    except Exception as e:
      logger.error(f"Error adding to cache: {e}.")
      raise FirestoreCacheException(f"Firestore add cache failed: {e}") from e

class FirestoreCacheException(Exception):
  """
  This class defines an exception for FirestoreCache.
  """
