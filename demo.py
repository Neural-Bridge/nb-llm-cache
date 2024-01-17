"""Demo for FirestoreCache"""
from firestore_cache import FirestoreCache
from local_cache import LocalCache
from cache_interface import CacheInterface
import openai
def call_openai(model,
                openai_messages,
                temperature,
                num_retries=5):
  client = openai.Client()
  completion = client.chat.completions.create(model=model,
                                              messages=openai_messages,
                                              temperature=temperature)
  return completion.choices[0].message.content

### FirestoreCache Demo
collection_name = "test_cache"
firestore_cache: CacheInterface = FirestoreCache(collection_name=collection_name)
print("DEMO FOR FIRESTORE CACHE")
print("------------------------")
res = firestore_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           num_retries=4,
                           exclude_cache_params=["num_retries"])
print("Firestore cache first call result:", res)
res = firestore_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           num_retries=9,
                           exclude_cache_params=["num_retries"])
print("Firestore cache second call result:", res)
print("------------------------")

### LocalCache Demo
cache_file_path = "test_cache.json"
local_cache: CacheInterface = LocalCache(file_path=cache_file_path)
print("DEMO FOR LOCAL CACHE")
print("------------------------")
res = local_cache.call(func=call_openai,
                       model="gpt-4",
                       openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                       temperature=0.8,
                       num_retries=4,
                       exclude_cache_params=["num_retries"])
print("Local cache first call result:", res)
res = local_cache.call(func=call_openai,
                       model="gpt-4",
                       openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                       temperature=0.8,
                       num_retries=9,
                       exclude_cache_params=["num_retries"])
print("Local cache second call result:", res)
print("------------------------")
