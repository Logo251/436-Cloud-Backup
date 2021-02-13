import sys
import getopt
import boto3

def main(argv):
    #Local Variables
    s3 = boto3.resource('s3')

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
        bucket = s3.Bucket(inputSource.split(':')[0])
        # check if bucket exists.
        if bucket not in s3.buckets.all():
            print("Bucket to save to does not exist.")
            exit(2)

        # check if folder exists inside.
        folder = s3.ObjectSummary(bucket_name=inputSource.split(':')[0], key=(inputSource.split(':')[1] + '/'))
        if folder not in bucket.objects.all():
            print("Folder to save to inside bucket does not exist.")
            exit(2)

        Backup(inputSource, folder)

    elif inputMode == "restore":
        bucket = s3.Bucket(inputSource.split(':')[0])
        #check if bucket exists.
        if bucket not in s3.buckets.all():
            print("Cannot restore from bucket that does not exist.")
            exit(2)

        #check if folder exists inside.
        folder = s3.ObjectSummary(bucket_name=inputSource.split(':')[0], key=(inputSource.split(':')[1]+ '/'))
        if folder not in bucket.objects.all():
            print("Cannot restore from a bucket that does not have the given folder.")
            exit(2)

        Restore(folder, inputDestination)
    else:
        #This handles bad modes.
        print("cloudBackup.py <backup/restore> <source_directory/source_bucket:directory> <destination_bucket:directory/destination_directory>")

def Backup(source, destination):
    for my_bucket_object in destination.objects.all():
        print(my_bucket_object)

def Restore(source, destination):
    for my_bucket_object in source.objects.all():
        print(my_bucket_object)

#Run Main
if __name__ == "__main__":
   main(sys.argv[1:])