"""This module implements a local cache using a JSON file."""
from ..llm_cache import LLMCache
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class LocalCache(LLMCache):
  """
  Implements a local cache mechanism using a JSON file for storage.

  This class allows storing and retrieving key-value pairs in a local JSON file.
  It is useful for scenarios where a lightweight, file-based cache is required.
  """
  def __init__(self, file_path: str):
    self.file_path = file_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    """
    Ensures the existence of the JSON file at the specified file path.
    If the file does not exist, creates a new file with an empty JSON object.
    """
    if not os.path.exists(self.file_path):
      with open(self.file_path, "w", encoding="utf=8") as file:
        json.dump({}, file)

  def _read_cache(self)->dict:
    """
    Reads and returns the content of the cache from the JSON file.

    Returns:
      dict: The content of the cache as a dictionary.

    Raises:
      LocalCacheException: If there is an error reading the file.
    """
    try:
      with open(self.file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    except json.JSONDecodeError:
      logger.error("Error reading from cache: JSON file is empty or malformed." \
                   " Returning empty cache.")
      return {}

  def get_from_cache(self, key: str)->str:
    """
    Retrieves the value associated with a given key from the cache.

    Args:
      key (str): The key for which the value needs to be retrieved.

    Returns:
      str: The value associated with the key in JSON format.
      Returns an empty string if the key is not found.

    Raises:
      LocalCacheException: If there is an error during the retrieval process.
    """
    try:
      cache = self._read_cache()
      if key not in cache:
        return ""
      res = cache.get(key)
      return json.dumps(res)
    except Exception as e:
      logger.error(f"Error reading from cache: {e}")
      raise LocalCacheException(f"Error reading from cache: {e}") from e

  def add_to_cache(self, key: str, value: str)->bool:
    """
    Adds a new key-value pair to the cache or updates an existing one.

    Args:
      key (str): The key under which the value should be stored.
      value (str): The value to store in the cache, in JSON format.

    Returns:
      bool: True if the operation was successful, False otherwise.

    Raises:
      LocalCacheException: If there is an error during the update process.
    """
    try:
      cache = self._read_cache()
      value_dict = json.loads(value)
      cache[key] = value_dict
      with open(self.file_path, "w", encoding="utf=8") as file:
        json.dump(cache, file, indent=2)
      return True
    except Exception as e:
      logger.error(f"Error writing to cache: {e}")
      raise LocalCacheException(f"Error writing to cache: {e}") from e

class LocalCacheException(Exception):
  """
  This class defines an exception for LocalCache.
  """
