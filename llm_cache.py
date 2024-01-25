"""
This module implements the LLMCache class, which is a subclass of the CacheInterface class.
"""
from kv_store_interface import KVStoreInterface
from typing import Callable, Any
import json
import hashlib
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class LLMCache():
  """
  A caching layer that cache function responses based on the function's arguments.
  """
  def __init__(self, kv: KVStoreInterface):
    """
    Initializes the LLMCache instance with a key-value store.

    Args:
      kv (KVStoreInterface): An instance of a class that implements the KVStoreInterface.
    """
    self.kv = kv

  def call(self, func: Callable,
           exclude_cache_params=None,
           num_retries_call=3,
           backoff_intervals_call=None,
           **kwargs: Any)->Any:
    """
    Calls the specified function with provided arguments, 
    caching and retrieving the response from the cache when possible.
    Supports retrying the function call with specified backoff intervals in case of failures.

    Args:
      func (Callable): The function to be called.
      exclude_cache_params (list, optional): A list of arguments to be excluded from cache key.
      num_retries_call (int, optional): The number of retries in case of function call failure.
      backoff_intervals_call (list, optional): A list of intervals to wait between retries.
      **kwargs (Any): Arbitrary keyword arguments to be passed to the function.

    Returns:
      Any: The response from the function call, either from the cache or directly from the function.

    Raises:
      ValueError: If the length of backoff_intervals does not match num_retries_call.
      Exception: Propagates exceptions from the function call after exhausting retries.
    """

    if exclude_cache_params is None:
      exclude_cache_params = []

    if backoff_intervals_call is None:
      backoff_intervals_call = [5, 30, 60]

    if len(backoff_intervals_call) != num_retries_call:
      raise ValueError(f"The length of backoff_intervals ({len(backoff_intervals_call)}) "\
                       f"must match num_retries ({num_retries_call}).")

    cache_params = {k: v for k, v in kwargs.items() if k not in exclude_cache_params}
    func_name = func.__name__
    cached_response, cache_key = self._get_cached_response(func_name, cache_params)
    if cached_response:
      logger.info(f"Cache hit for key: {cache_key}")
      return cached_response
    logger.info("No cached result found. Calling function.")
    try:
      response = func(**kwargs)
      self.kv.add_to_cache(cache_key, {"response": response, "cache_params": cache_params})
      return response
    except Exception as e:
      logger.error(f"Error calling function with name {func_name}: {e}")
      if num_retries_call > 0:
        logger.info(f"Sleeping Retrying in {backoff_intervals_call[0]} seconds...")
        time.sleep(backoff_intervals_call[0])
        return self.call(func,
                         exclude_cache_params,
                         num_retries_call=num_retries_call-1,
                         backoff_intervals_call=backoff_intervals_call[1:],
                         **kwargs)
      else:
        logger.error(f"No more retries left. The last error: {e}")
        raise

  def _get_cached_response(self, func_name, cache_params)->Any:
    """
    Attempts to retrieve a cached response for the function call based on the provided arguments.

    Args:
      func (Callable): The function for which the cached response is sought.
      cache_params (dict): The parameters used in the cache key.
      **kwargs (Any): Arbitrary keyword arguments that were passed to the function.

    Returns:
      Any: The cached response, if available, otherwise None.
      str: The cache key used for the attempted cache retrieval.
    """
    cache_key = self._generate_cache_key(func_name, cache_params)
    try:
      return self.kv.get_from_cache(key=cache_key, cache_params=cache_params), cache_key
    except Exception as e:
      logger.error(f"Error getting from cache: {e}")
      return None, cache_key

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
