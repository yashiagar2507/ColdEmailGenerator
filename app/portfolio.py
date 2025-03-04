import os
import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self):
        # Get absolute directory path
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the CSV file
        self.file_path = os.path.join(base_dir, "resource", "my_portfolio.csv")

        # Debugging: Print the file path to confirm correctness
        print(f"🔍 Looking for CSV at: {self.file_path}")

        # Check if the file actually exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"🚨 CSV file not found at: {self.file_path}")

        # Load the CSV file
        self.data = pd.read_csv(self.file_path)

        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:  # ✅ Check if collection is empty
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],  # ✅ Ensure it's a list
                    metadatas=[{"links": row["Links"]}],  # ✅ Ensure it's a list
                    ids=[str(uuid.uuid4())]  # ✅ Ensure it's a list
                )

    def query_links(self, skills):
        if isinstance(skills, str): 
            skills = [skills]


        if not skills:
              return []
        response = self.collection.query(
        query_texts=skills,  # ✅ Use 'query_texts' instead of 'documents'
        n_results=2
    )
        return response.get('metadatas', [])
  
  
  
  
  
  












