import sys
import getopt
import boto3
import os


def main(argv):
    #Local Variables
    resource = boto3.resource('s3')
    client = boto3.client('s3')

    #Attempt to assign input.
    try:
        inputMode = argv[0]
        inputSource = argv[1]
        inputDestination = argv[2]
    except getopt.GetoptError:
        print("cloudBackup.py <backup/restore> <source_directory/source_bucket:directory> <destination_bucket:directory/destination_directory>")
        sys.exit(2)

    #Choose path based on inputMode
    if inputMode == "backup":
        bucket = resource.Bucket(inputDestination.split(':')[0])  #check if bucket exists.
        if bucket not in resource.buckets.all():
            print("Cannot backup to a bucket that does not exist.")
            exit(2)
        #check if folder exists inside.
        folder = resource.ObjectSummary(bucket_name=inputDestination.split(':')[0], key=(inputDestination.split(':')[1]+ '/'))
        if folder not in bucket.objects.all():
            client.put_object(Bucket = inputDestination.split(':')[0], Key = inputDestination.split(':')[1]+ '/')
            print("created the folder the backups are to be written to")

        Backup(inputSource, inputSource, inputDestination)
        print("Finished backing up.")

    elif inputMode == "restore":
        bucket = resource.Bucket(inputSource.split(':')[0])  #check if bucket exists.
        if bucket not in resource.buckets.all():
            print("Cannot restore from bucket that does not exist.")
            exit(2)
        #check if folder exists inside.
        folder = resource.ObjectSummary(bucket_name=inputSource.split(':')[0], key=(inputSource.split(':')[1]+ '/'))
        if folder not in bucket.objects.all():
            print("Cannot restore from a bucket that does not have the given folder.")
            exit(2)
        Restore(inputSource, inputDestination, inputDestination)
        print("Finished restoring.")
    else:
        #This handles bad modes.
        print("cloudBackup.py <backup/restore> <source_directory/source_bucket:directory> <destination_bucket:directory/destination_directory>")

def Backup(source, originalSource, destination):
    #Local Variables
    bucket = destination.split(':')[0]
    folder = destination.split(':')[1] + '/'
    client = boto3.client('s3')
    resource = boto3.resource('s3')
    destinationFolder = resource.ObjectSummary(bucket_name=bucket, key=folder)

    #find files in location.
    for entry in os.scandir(source):
        seen = False
        if entry.is_file():
            for obj in resource.Bucket(bucket).objects.all():
                if obj.key.rstrip('/') == folder + entry.path[len(originalSource)+1:].replace('\\', '/'):
                    seen = True
                    if obj.last_modified.timestamp() < os.path.getmtime(entry.path):
                        client.upload_file(entry.path, bucket, folder + entry.path[len(originalSource)+1:].replace('\\', '/')) #File date modified checker, if it is there.
                        print("updated " + entry.name)
        else:
            Backup(entry.path, originalSource, destination)
            #find folder.
            for obj in resource.Bucket(bucket).objects.all():
                if obj.key.rstrip('/') == folder + entry.path[len(originalSource)+1:].replace('\\', '/'):
                    seen = True

        if not seen: #If file is not in the cloud at all, we can just copy and move on.
            if entry.is_file():
                client.upload_file(entry.path, bucket, folder + entry.path[len(originalSource)+1:].replace('\\', '/'))
                print("created " + entry.name)
            else:
                client.put_object(Bucket=bucket, Key = folder + entry.path[len(originalSource)+1:].replace('\\', '/') + '/')
                print("created " + entry.name + " folder.")
                Backup(entry.path, originalSource, destination)


def Restore(source, destination, Originaldestination):
    #Local Variables
    bucket = source.split(':')[0]
    folder = source.split(':')[1] + '/'
    client = boto3.client('s3')
    resource = boto3.resource('s3')

    #Check if inital folder exists.
    if not os.path.exists(destination):
        os.mkdir(destination)

    #find files in location.
    for obj in resource.Bucket(bucket).objects.all():
        if obj.key != folder:
            #convert S3 file storage into windows-format.
            cloudFile = destination + '\\' + obj.key[len(folder):].replace('/', '\\')
            if obj.key[-1] != '/':
                if os.path.exists(cloudFile):
                    if obj.last_modified.timestamp() > os.path.getmtime(cloudFile):
                        client.download_file(bucket, obj.key, cloudFile) #File date modified checker, if it is there.
                        print("downloaded and updated " + obj.key.split('/')[-1])
                else:
                    client.download_file(bucket, obj.key, cloudFile)
                    print("downloaded " + obj.key.split('/')[-1])

            else:
                #check if folder exists, if not create it.
                if not os.path.exists(cloudFile):
                    os.mkdir(cloudFile)
                    print("created " + obj.key.split('/')[-2] + " folder")

#Run Main
if __name__ == "__main__":
   main(sys.argv[1:])