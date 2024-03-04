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

<a href="https://github.com/Neural-Bridge/llm-cache/blob/main/LICENSE.md">![https://pypi.python.org/pypi/llm-cache/](https://img.shields.io/pypi/l/llm-cache.svg)</a>
<a href="https://pypi.python.org/pypi/llm-cache/">![https://pypi.python.org/pypi/llm-cache/](https://img.shields.io/pypi/pyversions/unstructured.svg)</a>
<a href="https://github.com/Neural-Bridge/llm-cache/blob/main/CODE_OF_CONDUCT.md">![code_of_conduct.md](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg) </a>
<a href="https://github.com/Neural-Bridge/llm-cache/releases">![GitHub release (latest by date)](https://img.shields.io/github/release/Neural-Bridge/llm-cache.svg?cacheSeconds=3600)
</a>

</div>

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
