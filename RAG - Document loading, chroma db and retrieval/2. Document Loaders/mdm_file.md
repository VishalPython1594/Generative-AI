# **Document Loaders**
Use document loaders to load data from a source as `Document`.

Document loaders provide a "load" method for loading data as documents from a configured source. They optionally implement a "lazy load" as well for lazily loading data into memory.

1. **Text Loaders**
```python
from langchain_community.document_loaders import TextLoader
loader = TextLoader("./index.md")
loader.load()
```

2. **CSV**
```python
from langchain_community.document_loaders.csv_loader import CSVLoader
loader = CSVLoader(file_path='./example_data/mlb_teams_2012.csv')
data = loader.load()
```
3. **HTML**
```python
from langchain_community.document_loaders import UnstructuredHTMLLoader
loader = UnstructuredHTMLLoader("example_data/fake-content.html")
data = loader.load()
```
4. **Web Base Loader**
```python
# !pip install beautifulsoup4
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
data = loader.load()
```
5. **JSON**  
[Click Here](https://python.langchain.com/docs/modules/data_connection/document_loaders/json) for detailed docs.  
Suppose we are interested in extracting the values under the `content` field within the `messages` key of the JSON data. This can easily be done through the JSONLoader as shown below.
```python
#!pip install jq
from langchain_community.document_loaders import JSONLoader
loader = JSONLoader(
    file_path='./example_data/facebook_chat.json',
    jq_schema='.messages[].content',
    text_content=False)

data = loader.load()
```

6. **PDF**  
[Click here](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf) for detailed docs.  
Make sure to install: `pip install pypdf`

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("example_data/layout-parser-paper.pdf")
pages = loader.load_and_split()
```

7. **File Directory**  
[Click Here](https://python.langchain.com/docs/modules/data_connection/document_loaders/file_directory) for detailed docs.
Under the hood it uses UnstructuredLoader.  
Make sure to install: `pip install "unstructured[all-docs]"`  
This covers how to load all documents in a directory. We can use the `glob` parameter to control which files to load.

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

loader = DirectoryLoader('../', glob="**/*.md", show_progress=True, loader_cls=TextLoader)
docs = loader.load()
```