"""This module implements a local cache using a JSON file."""
from typing import Callable, Any
from cache_interface import CacheInterface
import json
import hashlib
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class LocalCache(CacheInterface):
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

  def _generate_cache_key(self, func_name: str, cache_params: dict)->str:
    hash_input = json.dumps([func_name, cache_params], sort_keys=True)
    return hashlib.sha256(hash_input.encode()).hexdigest()

  def _get_from_cache(self, key: str)->str:
    try:
      cache = self._read_cache()
      return cache.get(key, {}).get("response")
    except Exception as e:
      logger.error(f"Error reading from cache: {e}")
      raise LocalCacheException(f"Error reading from cache: {e}") from e

  def _add_to_cache(self, key: str, data: dict)->bool:
    try:
      cache = self._read_cache()
      cache[key] = data
      self._write_cache(cache)
      return True
    except Exception as e:
      logger.error(f"Error writing to cache: {e}")
      raise LocalCacheException(f"Error writing to cache: {e}") from e

  def call(self, func: Callable, exclude_cache_params=None, **kwargs: Any)->Any:
    if exclude_cache_params is None:
      exclude_cache_params = []

    cache_params = {k: v for k, v in kwargs.items() if k not in exclude_cache_params}
    key = self._generate_cache_key(func.__name__, cache_params)

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
      raise LocalCacheException(f"An error occurred while executing the function: {e}") from e

class LocalCacheException(Exception):
  """
  This class defines an exception for LocalCache.
  """
