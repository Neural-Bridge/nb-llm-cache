from setuptools import setup, find_packages

setup(
  name='llm_cache_test',
  version='0.1.0',
  packages=find_packages(),
  license='Apache License 2.0',
  description='LLMCache is an open-source caching solution designed to operate seamlessly within your cloud infrastructure.',
  long_description=open('README.md', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author='Neural Bridge',
  # url='https://github.com/NeuralBridge/llm-cache',
  install_requires=[
    'google-cloud==0.34.0',
    'google-auth==2.27.0',
  ],
  python_requires='>=3.6',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
  ],
)
