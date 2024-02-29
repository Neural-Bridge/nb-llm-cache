"""Demo for FirestoreCache"""
from db_integrations.local_cache import LocalCache
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

### LocalCache Demo
cache_file_path = "test_cache.json"
local_cache: DBIntegrationInterface = LocalCache(file_path=cache_file_path)
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
