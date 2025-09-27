import pymongo
import gridfs
import os
import pandas as pd
from AudioFile import AudioFile

class MongoDBAccess:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # Prevent re-initialization
            self._initialized = True
            self.client = None  # Public attribute for MongoDB client
            self.DB = None # Private attribute for database
            self.coll = None  # Private attribute for collection

    def connect(self, uri, db_name, coll_name):
        """Connect to MongoDB and set the database and collection."""
        self.client = pymongo.MongoClient(uri)
        self.DB = self.client[db_name]
        self.coll = self.DB[coll_name]

    def insert_document(self, audDoc : AudioFile):
        """Insert a document into the collection."""
        if self.coll is None:
            #self.connect("mongodb://localhost:27017/", "recordings", "callcenter")
            self.connect("mongodb+srv://callcenter_db_user:mongopass@cluster0.h3ufcah.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0","recordings", "callcenter")
            if self.coll is None:
                raise Exception("Database not connected. Call connect() first.")
        fs = gridfs.GridFS(self.DB)

        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)   
        # Construct the path for the saved file
        file_path = os.path.join(temp_dir, audDoc.file.name)

        with open(file_path, 'rb') as f:
            file_id = fs.put(f, filename=audDoc.file.name, content_type='audio/mpeg')
        return self.coll.insert_one({
            "file_name": audDoc.file.name,
            "transcription": audDoc.text,
            "summary": audDoc.summary,
            "sentiment": audDoc.sentiment,
            "file_id": file_id
        })  
                    
    def get_recordings(self):
        """Insert a document into the collection."""
        try:
            if self.coll is None:
                self.connect("mongodb://localhost:27017/", "recordings", "callcenter")
            if self.client is None:
                return pd.DataFrame() # Return empty if connection fails
            
            items = self.coll.find()
            items_df = pd.DataFrame(list(items))
            if not items_df.empty:
                items_df.drop(columns=['_id'], inplace=True, errors='ignore')
            return items_df
        except Exception as e:
            print(f"Error retrieving recordings: {e}")
        return pd.DataFrame()