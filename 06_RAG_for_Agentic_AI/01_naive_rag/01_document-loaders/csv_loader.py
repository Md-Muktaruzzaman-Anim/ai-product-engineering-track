from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path='06_Rag-for-Agentic-AI/01-naive-rag/01_document-loaders/Social_Network_Ads.csv')

docs = loader.load()

print(len(docs))
print(docs[1])