# GCSNavigator
A class to easily download data from Google Cloud Storage buckets in GCP functions. The class helps simplify the process of downloading files from Google Cloud Storage into the temporary storage while running Google Cloud functions with easy to use functions for getting paths to the data files. 

## Bucket Navigator class  

The bucket navigator class can be imported from the storagedownloader class using the falling import statement: ```from storagedownloader import BucketNavigator```. 

### Class Initializer 

The initializer of the class takes in the name of the bucket on the which the operations are going to be performed. For example, the code below will initialize a BucketNavigator class for a bucket in storage named *sample-bucket-testing*: 
```
bucket_name = "sample-bucket-testing"
navigator = BucketNavigator(bucket_name)
```

### Downloading entire bucket 

You can download all the files in the bucket passed in through the constructor and **returns the path in the local directory of the folder containing the entire bucket**. This function **preserves the original directory structure (i.e. file depth levels are preserved)** so a file named *testing.txt* inside a folder named *basic* inside the bucket we are operating in can be accessed through the following code: 
```
bucket_path = navigator.download_entire_bucket()
relative_file_path = os.path.join("basic", "testing.txt")
full_file_path = os.path.join(bucket_path, relative_file_path)
```

### Downloading specific files 

You can dowload specific files from the bucket if you don't want to download the entire bucket just to use a single file from the bucket. The functions takes in **a list of strings which contain the names of file we want to download** and the function returns a **dicitonary where the keys are all the files in the input parameter and the value is either the path to the file if the file exists or None if the file doesn't exist**. For example, assuming we have a bucket having the following directory structure: 
```
|---_basic1
|   |---_testing1.txt
|---_basic2
|   |---_testing2.txt
|---_testing.txt
|---_basic3
```
and if we run the following code: 
```
files_to_download = ['testing.txt','testing1.txt', 'testing2.txt', 'testing3.txt']
file_paths = navigator.download_files(files_to_download)
```
The file_paths dictionary would look like this if we printed it out: 
```
'testing.txt': '/tmp/sample-bucket-testing/testing.txt', 
'testing1.txt': '/tmp/sample-bucket-testing/basic1/testing1.txt', 
'testing2.txt': '/tmp/sample-bucket-testing/basic2/testing2.txt', 
'testing3.txt': None}
```

## Downloading specific folders

We can download specific folders using the **download_folders** method which works similarily to the *download_files* method but rather than downloading specific files it downloads all the files inside the given folders. The function takes in **a list of strings which contains the name of the folders we want to download** and returns **a dicitonary where the keys are the names of all the folders and the value is either the path to the folder if the folder exists or None if the folder doesn't exist**. All the folders that are downloaded have their directory structure preserved like in the *download_entire_bucket* function. 

If we have the same bucket structure as in the *downloading specific files* example and we run the following code: 
```
folders_to_download = ['basic1', 'basic2', 'basic3', 'basic4']
folder_paths = navigator.download_folders(folders_to_download)
```
The folder_paths dictionary would look like this if we printed it out: 
```
{'basic1': '/tmp/sample-bucket-testing/basic1', 
'basic2': '/tmp/sample-bucket-testing/basic2', 
'basic3': '/tmp/sample-bucket-testing/basic3', 
'basic4': None}
```
