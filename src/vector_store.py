from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

class VectorStoreBuilder:
    def __init__(self,csv_path:str,perist_dir:str="chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = perist_dir
        # self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.embedding = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")

    def build_and_save_vector_store(self):
        # Load the CSV file
        loader = CSVLoader(file_path=self.csv_path,
                           encoding="utf-8",
                           metadata_columns=[])
        
        data = loader.load()

        # Split the text into chunks
        splitter= CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
        )
        texts=splitter.split_documents(data)

        # Create the vector store
        db = Chroma.from_documents(texts,self.embedding,persist_directory=self.persist_dir)
        # Persist the vector store
        db.persist()

    def load_vector_store(self):
        # Load the vector store from the persisted directory
        return Chroma(
            embedding_function=self.embedding,
            persist_directory=self.persist_dir
        )

