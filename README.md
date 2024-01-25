# FirestoreCache and LocalCache Modules

## Introduction

`FirestoreCache` and `LocalCache` are Python modules that implement caching functionality. `FirestoreCache` uses Google Firestore as the backend, while `LocalCache` uses a local JSON file. Both are designed as subclasses of the `CacheInterface` class, providing methods for storing, retrieving, and managing cached data.

## Installation

Before using `FirestoreCache` or `LocalCache`, ensure you have the required packages installed:

```bash
pip install -r requirements.txt
```

## Repository Setup

1. **Download Configuration Files**:

   - Download the `drive_key.json` file from [this link](https://drive.google.com/file/d/1dN7uOMMI1lxTciWrnUGTOZtG4ybF1PmA/view?usp=sharing) and place it in the root folder of your project.
   - Download the `.env` file from [this link](https://drive.google.com/file/d/11XhcOHC_OyfD7FrCEdiJrOj2BKySEHqa/view?usp=sharing) and place it in the root folder of your project.
   - Download the firestore_key.json from [this link](https://drive.google.com/drive/folders/10CvwHwZV0TOsjNseTq4svK2kKUw_7qVR?usp=drive_link) and place it in the root folder of your project.

2. **Set Up Environment Variables**:

   - To set the environment variables, run the following command in your terminal:

     ```bash
     source .env
     ```

3. **Configure Git Hooks**:

   - To set up the Git hooks, make the `setup_hooks.sh` script executable and run it by executing the following command:

     ```bash
     chmod +x hooks_management/setup_hooks.sh && hooks_management/setup_hooks.sh
     ```

## Configuration

### FirestoreCache Configuration

To use `FirestoreCache`, you must have a Google Cloud Firestore project set up. Follow these steps to configure your environment:

1. Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/).
2. Set up Firestore in your Firebase project.
3. Generate a new private key for your Firebase service account.
4. Download the key JSON file (`firestore_key.json`) and place it in the root folder of your project.

### LocalCache Configuration

To use `LocalCache`, specify the path to a local JSON file. If the file does not exist, it will be created automatically.

## Usage

### Basic Usage of FirestoreCache

To use the `FirestoreCache` class, import it into your Python script and initialize it with the name of your Firestore collection:

```python
from firestore_cache import FirestoreCache

# Initialize FirestoreCache with your Firestore collection name
cache = FirestoreCache("my_collection")
```

### Basic Usage of LocalCache

To use the `LocalCache` class, import it into your Python script and specify the path to your local JSON file:

```python
from local_cache import LocalCache

# Initialize LocalCache with the path to your local JSON file
cache = LocalCache("path/to/cache.json")
```

### Common Usage

You can use the `call` method to interact with the cache for both `FirestoreCache` and `LocalCache`:

```python
def my_function(param1, param2, param3):
    return param1 + param2

# Example using FirestoreCache or LocalCache
result = cache.call(my_function, param1="Hello, ", param2="world!", exclude_cache_params=["param3"])
print(result)
```

### Running the Demo

A demo script is provided to showcase the usage of `FirestoreCache` and `LocalCache`. To run the demo, follow these steps:

#### For FirestoreCache

1. Place your `firestore_key.json` file in the root folder of the project.
2. Set the environment variable for the Firestore credentials by running:

   ```bash
   source keys.env
   ```

#### For LocalCache

1. Ensure the path to your local JSON file is correctly set in the demo script.

#### Run the Demo

3. Run the demo script:

   ```bash
   python3 demo.py
   ```

## Important Note

If you updated your local .env file, you need to update the .env file in Google Drive. To do so, run the following command in your terminal from the root folder of the project:

```bash
python3 hooks_management/update_env.py
```
