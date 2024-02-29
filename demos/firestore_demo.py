"""Demo for FirestoreCache"""
from db_integrations.firestore_cache import FirestoreCache
from db_integration_interface import DBIntegrationInterface
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
firestore_service_account_file = "firestore_key.json"
firestore_cache: DBIntegrationInterface = FirestoreCache(collection_name=collection_name,
                                                         firestore_service_account_file=firestore_service_account_file)
llm_cache = LLMCache(firestore_cache)
print("DEMO FOR FIRESTORE CACHE")
print("------------------------")

start_time = time.time()
res = llm_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           timeout=40,
                           exclude_cache_params=["timeout"],
                           num_retries_call=2,
                           backoff_intervals_call=[5, 10])
latency = time.time() - start_time
print(f"Firestore cache first call result: {res} and latency: {latency:0.2f} seconds")

start_time = time.time()
res = llm_cache.call(func=call_openai,
                           model="gpt-4",
                           openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                           temperature=0.8,
                           timeout=90,
                           exclude_cache_params=["timeout"],
                           num_retries_call=2,
                           backoff_intervals_call=[5, 10]
                           )
latency = time.time() - start_time
print(f"Firestore cache second call result: {res} and latency: {latency:0.2f} seconds")


