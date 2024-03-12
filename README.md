<h1 align="center">
  <img
    src="assets/nb_logo.png"
    height="200"
  >
</h1>

<div align="center">

<h2>
Completely Open-Source! Entirely Free! Fully Private!
</h2>

<a href="https://github.com/Neural-Bridge/llm-cache/blob/main/LICENSE.md">![https://pypi.org/project/llmcache-test-nb](https://img.shields.io/pypi/l/llmcache-test-nb.svg)</a>
<a href="https://pypi.python.org/pypi/llm-cache/">![https://pypi.org/project/llmcache-test-nb](https://img.shields.io/pypi/pyversions/llmcache-test-nb.svg)</a>
<a href="https://github.com/Neural-Bridge/llm-cache/blob/main/CODE_OF_CONDUCT.md">![code_of_conduct.md](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg) </a>
<a href="https://github.com/Neural-Bridge/llm-cache/releases">![GitHub release (latest by date)](https://img.shields.io/github/release/Neural-Bridge/llm-cache.svg?cacheSeconds=3600)
</a>

</div>

**LLMCache** is an open-source caching solution designed to operate seamlessly within your cloud infrastructure, offering custom database integrations and more than just caching. With robust features including automatic retries for enhanced reliability, it empowers developers to efficiently manage data-intensive operations. 


## ⭐ Features

- **Customizable Database Integrations:** Out-of-the-box support for Firestore and local cache, with the flexibility for custom database integrations to meet your specific needs.
- **Efficient Caching:** Optimizes your application by caching function responses, significantly reducing calling times and improving responsiveness.
- **Retry Logic with Backoff Intervals:** Enhances reliability through robust retry mechanisms, including configurable backoff intervals to handle failures gracefully.
- **Reduced Latency:** Minimizes delays in data retrieval, ensuring your application runs smoothly and efficiently.
- **Scalable and Cloud-Ready:** Designed to seamlessly integrate with your cloud infrastructure, making it ideal for scaling applications.
- **Open Source:** Provides the freedom to modify, extend, and tailor the solution to your project's requirements, backed by a community-driven support system.
- **Simplified Data Handling:** Streamlines the process of storing and retrieving data, allowing for more focused development on core functionalities.

For feature requests, please reach out to us via [this form]().


## 🗄️ Supported Database Integrations

| Cache Integration Type         | Status        |
|--------------------------------|---------------|
| Local Cache                    | Completed ✅   |
| Firestore                      | Completed ✅   |
| MongoDB                        | In Progress 🚧 |
| Redis                          | In Progress 🚧 |

## ⚙️ Installation

Install via pip with just one command:

```
pip install llm_cache
```

## 🎉 Usage

LLMCache simplifies integrating efficient caching mechanisms into your applications, supporting both local and cloud-based environments. Below are demonstrations of how LLMCache can be utilized with local cache and Firestore, including support for streaming data.

### Local Cache

For applications requiring rapid access without external dependencies, LLMCache offers a local caching solution:

```python
from db_integrations.local_cache import LocalCache
from llm_cache import LLMCache
import openai

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

# Initialize the local cache
cache_file_path = "test_cache.json"
local_cache = LocalCache(file_path=cache_file_path)
llm_cache = LLMCache(local_cache)

# Example function call using the local cache
res = llm_cache.call(func=call_openai,
                     model="gpt-4",
                     openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                     temperature=0.8,
                     exclude_cache_params=["timeout"])
```

### Firestore Cache


```python
from db_integrations.firestore_cache import FirestoreCache
from llm_cache import LLMCache
import openai

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

# Configure Firestore cache
collection_name = "test_cache"
firestore_service_account_file = "firestore_key.json"
firestore_cache = FirestoreCache(collection_name=collection_name,
                                 firestore_service_account_file=firestore_service_account_file)
llm_cache = LLMCache(firestore_cache)

# Utilizing Firestore for caching
res = llm_cache.call(func=call_openai,
                     model="gpt-4",
                     openai_messages=[{"content": "Hello, how are you?", "role": "user"}],
                     temperature=0.8,
                     timeout=40,
                     exclude_cache_params=["timeout"],
                     num_retries_call=2,
                     backoff_intervals_call=[5, 10])
```
**Note on Firestore Cache:** When using Firestore as your caching solution, it's recommended to implement a Time-To-Live (TTL) policy for your cache entries. This ensures that your database does not indefinitely grow with stale data, which can lead to increased costs and decreased performance. Setting a TTL allows Firestore to automatically delete entries after a specified duration, keeping your database optimized and your costs in check.

### Streaming Support

LLMCache also supports streaming responses for real-time data handling, enhancing applications that require continuous data flow:

```python

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

# Streaming call demonstration with Firestore cache
streaming_messages = [
    {"role": "system", "content": "The following is a conversation with an AI assistant."},
    {"role": "user", "content": "Hello, how are you today?"}
]

streaming_generator = llm_cache.stream_call(
    func=openai_stream_call,
    model="gpt-4",
    openai_messages=streaming_messages,
    temperature=0.8)

# Iterate over and print streaming responses
for chunk in streaming_generator:
    print(chunk.decode("utf-8"))
```

## ❓ Frequently Asked Questions

#### _What types of applications can benefit from **LLMCache**?_

**LLMCache** is particularly beneficial for applications that frequently interact with large language models (LLMs) or perform data-intensive operations. It's ideal for improving response times and reducing API costs in AI-powered apps, web services, and data analysis tools.

#### _Can **LLMCache** be integrated with any database?_

While **LLMCache** currently has built-in support for Firestore and local caching, it's designed to allow custom database integrations. Developers can extend **LLMCache** to work with databases like MongoDB and Redis, as well as others according to their project requirements.

#### _Is **LLMCache** open-source?_

Yes, **LLMCache** is an open-source project. This means you can freely use, modify, and distribute it under its licensing terms. It also allows the community to contribute to its development.

#### _Can **LLMCache** improve the performance of my application?_

Absolutely. By caching responses, **LLMCache** can significantly reduce the time it takes for your application to respond to user requests. This results in faster performance, especially for operations that involve heavy computational work or external API calls.

## 👥 Contributions

We welcome contributions from everyone who is looking to improve or add value to this project! Whether you're interested in fixing bugs, adding new features, or improving documentation, your help is appreciated.

If you would like to contribute, please fill out [this form]() with your details and how you'd like to help. We'll review your submission and get back to you as soon as possible with the next steps.

Thank you for considering to contribute, and we look forward to collaborating with you!

## 🔔 Subscribe to updates

Stay updated with LLM Cache by subscribing through [this form]()

## ⚖️ License

For detailed licensing information, please refer to the [LICENSE file](https://github.com/Neural-Bridge/llm-cache/blob/master/LICENSE).


<!-- ## Overview

LLM Cache is a Python-based caching system designed to efficiently store and retrieve data for various applications. This project includes implementations for both local file-based caching and cloud-based caching using Firestore, as well as an interface for database integration.

## Modules

### DBIntegrationInterface

- **Purpose**: Defines the interface for a cache.
- **Description**: This abstract class outlines the basic structure for cache implementations, specifying methods for retrieving (`get_from_cache`) and adding data (`add_to_cache`) to the cache.

### FirestoreCache

- **Purpose**: Implements caching using Google Cloud Firestore.
- **Description**: Extends `DBIntegrationInterface` to provide a caching solution using Firestore, suitable for distributed systems and cloud-based applications.

### LocalCache

- **Purpose**: Implements caching using a local JSON file.
- **Description**: Extends `DBIntegrationInterface` to offer a simple, file-based caching mechanism, ideal for lightweight applications or environments where cloud access is limited.

### LLMCache

- **Purpose**: A caching layer for function responses.
- **Description**: This class uses a `DBIntegrationInterface` to cache and retrieve responses of functions based on their arguments. It supports features like retrying function calls and excluding specific arguments from cache keys.

## Features

- **Versatile Caching**: Supports both local (JSON file) and remote (Firestore) caching.
- **Function Response Caching**: Optimizes performance by caching the results of function calls.
- **Retry Mechanism**: Includes a retry logic with backoff intervals for failed function calls.
- **Customizable**: Allows exclusion of certain parameters from the cache key.
- **Error Handling**: Robust error handling with custom exceptions for both local and Firestore caches.

## Installation

To use LLM Cache in your project, clone this repository and install the required dependencies:

```bash
git clone https://github.com/Neural-Bridge/llm-cache.git
cd llm-cache
pip install -r requirements.txt
```

## Usage

1. **Initialization**:

   - Initialize the desired cache implementation (FirestoreCache or LocalCache) by providing necessary parameters like collection name or file path.
   - Instantiate LLMCache with the cache object.

2. **Caching Function Calls**:

   - Use `LLMCache.call()` to call a function and cache its response. You can specify parameters to exclude from the cache key and define retry logic.

3. **Retrieving and Storing Data**:
   - Use `get_from_cache` and `add_to_cache` methods from your cache implementation to directly interact with the cache.

## Example

```python
# Example of using LLMCache with LocalCache
from db_integrations.local_cache import LocalCache
from db_integration_interface import DBIntegrationInterface
from llm_cache import LLMCache

# Initialize the LocalCache
cache_file_path = "test_cache.json"
local_cache: DBIntegrationInterface = LocalCache(file_path=cache_file_path)
llm_cache = LLMCache(local_cache)

# Function to cache
def example_function(param1, param2):
    # Function logic
    return result

# Using LLMCache to call and cache the function response
response = llm_cache.call(example_function,
                          param1=value1,
                          param2=value2,
                          exclude_params=['param2'],
                          num_retries_call=2, # Retry twice if function call fails
                          backoff_intervals_call=[5, 10] # Wait 5s and 10s before retrying
                          )
```

## Demos

The `llm_cache` project contains two demonstration scripts located in the `demos` folder to showcase the usage of `FirestoreCache` and `LocalCache`.

### FirestoreCache Demo (`firestore_demo.py`)

This demo illustrates how to use the `FirestoreCache` with the `LLMCache` to cache responses from OpenAI's GPT-4 model. The script demonstrates the caching functionality and latency improvements when making repeated calls to the same API endpoint with identical parameters.

To run the FirestoreCache demo, ensure you have the Firestore service account file and update the `firestore_service_account_file` variable accordingly. The script measures and prints the latency for the first and second calls to highlight the caching effect.

### LocalCache Demo (`local_demo.py`)

This demo shows the use of `LocalCache` with `LLMCache` to cache responses from the GPT-4 model locally. Similar to the FirestoreCache demo, it demonstrates the latency benefits when caching is applied to repeated API requests.

Before running the demo, ensure you have a writable JSON file path specified for the local cache. The script then performs API calls and prints out the latency for each call to showcase the effectiveness of the local cache.

### Running the Demos

To run these demos, first you need to install the OpenAI Python library and set up OPENAI_API_KEY environment variable. Then from root folder execute the scripts:

```bash
pip install openai==1.3.7
python3 -m demos.firestore_demo.py
python3 -m demos.local_demo.py
``` -->
