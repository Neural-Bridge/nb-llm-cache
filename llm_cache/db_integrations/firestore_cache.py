"""
This module implements the FirestoreCache class,
which is a subclass of the DBIntegrationInterface class.
"""
from google.cloud import firestore
from google.oauth2 import service_account
from ..db_integration_interface import DBIntegrationInterface
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class FirestoreCache(DBIntegrationInterface):
  """
  This class implements the DBIntegrationInterface class for Firestore.
  """
  def __init__(self, collection_name, firestore_service_account_file):
    try:
      credentials = service_account.Credentials.from_service_account_file(firestore_service_account_file)
      self._db = firestore.Client(credentials=credentials)
      self._cache: firestore.CollectionReference = self._db.collection(collection_name)
    except Exception as e:
      logger.error(f"Error initializing Firestore cache: {e}.")
      raise FirestoreCacheException(f"Firestore initialization failed: {e}") from e


  def get_from_cache(self, key: str)->str:
    """
    Retrieves the data associated with the specified key from a Firestore database.

    This method fetches a document identified by 'key' from a specific Firestore collection.
    If the document exists, its data is returned, otherwise, an empty string is returned.
    The data is expected to be in a dictionary format stored in the Firestore document.

    Args:
      key (str): The key identifying the document to retrieve the data from.
      This is typically a unique identifier corresponding to a document in the Firestore collection.

    Returns:
      str: A string containing the 'response' and 'cache_params' from the Firestore document.
      If the document does not exist, returns an empty string.

    Raises:
      FirestoreCacheException: If there is an error retrieving the data from the Firestore database.
    """
    try:
      doc: firestore.DocumentSnapshot = self._cache.document(key).get()
      if doc.exists:
        result = doc.to_dict()
        return json.dumps(result)
      return ""
    except Exception as e:
      logger.error(f"Error getting from cache: {e}.")
      raise FirestoreCacheException(f"Firestore get cache failed: {e}") from e

  def add_to_cache(self, key: str, value: str)->bool:
    """
    Sets the data associated with the key in a Firestore database.

    This method updates a document identified by 'key' in a specific Firestore collection 
    with the provided 'value'.
    If the document does not exist, a new one is created. 
    The value should be a stringified dictionary where each key-value pair represents 
    a field and its value in the Firestore document.

    Args:
      key (str): The key identifying the document to set the data for.
      value (str): The data to set in the document.
    Returns:
      bool: True if the data was successfully set.

    Raises:
      FirestoreCacheException: If there is an error setting the data in the Firestore database.
      This might occur due to network issues, permission errors, or invalid data formats.

    Note:
      This function requires that the Firestore database is properly initialized and that 
      the collection is correctly specified in the implementation.
    """
    try:
      value_dict = json.loads(value)
      self._cache.document(key).set(value_dict)
      return True
    except Exception as e:
      logger.error(f"Error adding to cache: {e}.")
      raise FirestoreCacheException(f"Firestore add cache failed: {e}") from e

class FirestoreCacheException(Exception):
  """
  This class defines an exception for FirestoreCache.
  """
