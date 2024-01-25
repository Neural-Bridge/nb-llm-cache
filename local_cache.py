"""This module implements a local cache using a JSON file."""
from kv_store_interface import KVStoreInterface
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class LocalCache(KVStoreInterface):
  """
  This class implements a local cache using a JSON file.
  """
  def __init__(self, file_path: str):
    self.file_path = file_path
    self._ensure_file_exists()

  def _ensure_file_exists(self):
    if not os.path.exists(self.file_path):
      with open(self.file_path, "w", encoding="utf=8") as file:
        json.dump({}, file)

  def _read_cache(self)->dict:
    try:
      with open(self.file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    except json.JSONDecodeError:
      logger.error("Error reading from cache: JSON file is empty or malformed." \
                   " Returning empty cache.")
      return {}

  def _write_cache(self, data: dict):
    with open(self.file_path, "w", encoding="utf=8") as file:
      json.dump(data, file, indent=2)

  def get_from_cache(self, key: str, cache_params: dict)->str:
    try:
      cache = self._read_cache()
      res = cache.get(key, {})
      if res and res.get("cache_params") == cache_params:
        return res.get("response")
    except Exception as e:
      logger.error(f"Error reading from cache: {e}")
      raise LocalCacheException(f"Error reading from cache: {e}") from e

  def add_to_cache(self, key: str, value: dict)->bool:
    try:
      cache = self._read_cache()
      cache[key] = value
      self._write_cache(cache)
      return True
    except Exception as e:
      logger.error(f"Error writing to cache: {e}")
      raise LocalCacheException(f"Error writing to cache: {e}") from e

class LocalCacheException(Exception):
  """
  This class defines an exception for LocalCache.
  """
