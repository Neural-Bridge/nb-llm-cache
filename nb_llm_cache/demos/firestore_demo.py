"""Demo for FirestoreCache"""
from ..db_integrations.firestore_cache import FirestoreCache
from ..llm_cache import LLMCache
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

def openai_stream_call(model,
                       openai_messages,
                       temperature,
                       timeout=120):
  client = openai.Client()

  streaming_response = client.chat.completions.create(model=model,
                                                      messages=openai_messages,
                                                      temperature=temperature,
                                                      stream=True,
                                                      timeout=timeout)

  for chunk_res in streaming_response:
    if chunk_res.choices and chunk_res.choices[0].delta and chunk_res.choices[0].delta.content:
      yield chunk_res.choices[0].delta.content.encode("utf-8")

### FirestoreCache Demo
collection_name = "test_cache"
firestore_service_account_file = "firestore_key.json"
llm_cache: LLMCache = FirestoreCache(collection_name=collection_name,
                                     firestore_service_account_file=firestore_service_account_file)
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


### Demo for FirestoreCache with Streaming
print("\nDEMO FOR FIRESTORE CACHE WITH STREAMING")
print("---------------------------------------")

# Prepare messages for streaming call
streaming_messages = [
  {"role": "system", "content": "The following is a conversation with an AI assistant."},
  {"role": "user", "content": "Hello, how are you today?"}
]

# First call with streaming enabled - should populate the cache
print("Making the first streaming call ...")
start_time = time.time()
streaming_generator = llm_cache.stream_call(
  func=openai_stream_call,
  model="gpt-4",
  openai_messages=streaming_messages,
  temperature=0.8,
  timeout=120,
  exclude_cache_params=["timeout"],
  num_retries_call=2,
  backoff_intervals_call=[5, 10]
)

# Iterate over the generator to print streaming responses
for chunk in streaming_generator:
  print(chunk.decode("utf-8"))

latency = time.time() - start_time
print(f"Firestore cache first streaming call latency: {latency:0.2f} seconds")

# Second call with streaming enabled - should retrieve from the cache
print("\nMaking the second streaming call...")
start_time = time.time()
streaming_generator = llm_cache.stream_call(
  func=openai_stream_call,
  model="gpt-4",
  openai_messages=streaming_messages,
  temperature=0.8,
  timeout=120,
  exclude_cache_params=["timeout"],
  num_retries_call=2,
  backoff_intervals_call=[5, 10]
)

# Iterate over the generator to print streaming responses
for chunk in streaming_generator:
  print(chunk.decode("utf-8"))

latency = time.time() - start_time
print(f"Firestore cache second streaming call latency: {latency:0.2f} seconds")
