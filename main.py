import sys
import getopt
import boto3

def main(argv):
    #Local Variables
    print("hi")
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
        bucket = s3.Bucket(inputDestination)
        Backup(inputSource, bucket)

    elif inputMode == "restore":
        bucket = s3.Bucket(inputSource)
        Restore(bucket, inputDestination)
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