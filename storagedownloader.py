import os 
import json
from google.cloud import storage
from google.oauth2 import service_account

seperator = '/'
temp_folder = seperator + 'tmp'

class BucketNavigator(): 
    
    def __init__(self, bucket_name, path_to_servicekey):
        if not os.path.exists(path_to_servicekey): 
            raise ValueError("The path to service key (" + path_to_servicekey + ") doesn't exist")
        info = None 
        with open(path_to_servicekey) as source:
            info = json.load(source)
        try: 
            storage_credentials = service_account.Credentials.from_service_account_info(info)
            storage_client = storage.Client(credentials=storage_credentials)
        except Exception as e: 
            raise ValueError("The credentials in the service key are not valid")
        try: 
            self.bucket = storage_client.get_bucket(bucket_name)
            self.bucket_name = bucket_name
        except Exception as e: 
            raise ValueError("A bucket with name " + bucket_name + " was not found")

    def save_blob(self, current_blob, base_path): 
        save_path = os.path.join(base_path, current_blob.name)
        if not os.path.exists(save_path): 
            broken = str(current_blob.name).split(seperator)
            for index in range(len(broken) - 1): 
                base_path = os.path.join(base_path, broken[index])
                self.makefolder(base_path)
            #Only download the object if the blob object is a file
            if('.' in save_path):
                current_blob.download_to_filename(save_path)
        return save_path

    def makefolder(self, folder_path): 
        if not os.path.exists(folder_path): 
            os.mkdir(folder_path)

    def get_all_file_blobs(self): 
        storage_client = storage.Client()
        files = []
        for blob in self.bucket.list_blobs():
            files.append(blob)
        return files
    
    def starting_sequence(self): 
        all_files = self.get_all_file_blobs()
        starting_folder = os.path.join(temp_folder, self.bucket_name)
        self.makefolder(starting_folder)
        return all_files, starting_folder

    def download_entire_bucket(self): 
        all_files, starting_folder = self.starting_sequence()
        for blob in all_files:
            self.save_blob(blob, starting_folder)
        return starting_folder
    
    def initialize_dictionary(self, names): 
        data = {}
        for name in names: 
            data[name] = None 
        return data
    
    def download_files(self, file_names): 
        file_paths = self.initialize_dictionary(file_names)
        all_files, starting_folder = self.starting_sequence()
        for blob in all_files: 
            for file_name in file_names: 
                if(file_name in blob.name): 
                    save_path = self.save_blob(blob, starting_folder)
                    file_paths[file_name] = save_path
                    break
        return file_paths
    
    def download_folders(self, folder_names): 
        folder_paths = self.initialize_dictionary(folder_names)
        all_files, starting_folder = self.starting_sequence()
        for blob in all_files:
            for folder_name in folder_names: 
                if(folder_name in blob.name):
                    #Ensures that the blob object is a folder
                    bucket_path = blob.name
                    folder_index = bucket_path.index(folder_name)
                    if(seperator in bucket_path[folder_index: ]):
                        save_path = self.save_blob(blob, starting_folder)
                        #Save path of folder if haven't saved a path for it before
                        if(folder_paths[folder_name] == None): 
                            relative_path_to_folder = os.path.join( bucket_path[ : folder_index], folder_name)
                            folder_paths[folder_name] = os.path.join(starting_folder, relative_path_to_folder)
                        break
        return folder_paths