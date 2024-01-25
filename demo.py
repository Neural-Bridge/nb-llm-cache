"""Demo for FirestoreCache"""
from firestore_cache import FirestoreCache
from local_cache import LocalCache
from kv_store_interface import KVStoreInterface
from llm_cache import LLMCache
import openai
import time
def call_openai(model,
                openai_messages,
                temperature,
                timeout=50):
  client = openai.Client()
  completion = client.chat.completions.create(model=model,
                                              messages=openai_messages,
                                              temperature=temperature,
                                              timeout=timeout)
  return completion.choices[0].message.content

### FirestoreCache Demo
collection_name = "test_cache"
firestore_cache: KVStoreInterface = FirestoreCache(collection_name=collection_name)
llm_cache = LLMCache(firestore_cache)
print("DEMO FOR FIRESTORE CACHE")
print("------------------------")

start_time = time.time()
res = llm_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           timeout=40,
                           exclude_cache_params=["timeout"])
latency = time.time() - start_time
print(f"Firestore cache first call result: {res} and latency: {latency:0.2f} seconds")

start_time = time.time()
res = llm_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           timeout=90,
                           exclude_cache_params=["timeout"]
                           )
latency = time.time() - start_time
print(f"Firestore cache second call result: {res} and latency: {latency:0.2f} seconds")
print("------------------------")

### LocalCache Demo
cache_file_path = "test_cache.json"
local_cache: KVStoreInterface = LocalCache(file_path=cache_file_path)
llm_cache = LLMCache(local_cache)
print("DEMO FOR LOCAL CACHE")
print("------------------------")
start_time = time.time()
res = llm_cache.call(func=call_openai,
                       model="gpt-4",
                       openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                       temperature=0.8,
                       exclude_cache_params=["timeout"])
latency = time.time() - start_time
print(f"Local cache first call result: {res} and latency: {latency:0.2f} seconds")

start_time = time.time()
res = llm_cache.call(func=call_openai,
                       model="gpt-4",
                       openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                       temperature=0.8,
                       exclude_cache_params=["timeout"])
latency = time.time() - start_time
print(f"Local cache second call result: {res} and latency: {latency:0.2f} seconds")
print("------------------------")
