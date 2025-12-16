"""
__filename__ = "hw_1.py"
__coursename__ = "SDEV 400 7380 - Secure Programming in the Cloud (2232)"
__author__ = "Earl Thomas"
__copyright__ = "None"
__credits__ = ["Earl Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Earl Thomas"
__email__ = "ethomas112@student.umgc.edu"
__status__ = "Final"
"""
import datetime
import os
import boto3
import botocore
from S3_Python_Methods import create_bucket, put_object
from S3_Python_Methods import delete_object, delete_bucket, copy_object

def make_bucket(bname):
    """
    Creates an S3 Bucket
    :param generic_name(str): Name of Bucket
    :return No return
    *create_bucket is an example provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    try:
        create_bucket.create_bucket(bname)
        prompt = bname + " has been successfully created."
        print(prompt)
    except Exception as exception:
        print(exception)

def move_obj(bucket, obj):
    """
    Moves a local file to an S3 Bucket
    :param generic_name(str): Name of Bucket
    :param generic_name(str): Name of file
    :return No return
    *move_obj is an example provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    try:
        put_object.put_object(bucket, obj, "HW1/src/" + obj)
        prompt = str("\n"+ obj +" has been moved.\n")
        print(prompt + str(datetime.datetime.now())+"\n")
    except Exception as exception:
        print(exception)
def del_obj(bucket, obj):
    """
    Deletes an object in an S3 Bucket
    :param generic_name(str): Name of Bucket
    :param generic_name(str): Name of Object
    :return No return
    *del_obj is an example provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    try:
        delete_object.delete_object(bucket, obj)
        prompt = str("\n"+ obj +" has been deleted.\n")
        print(prompt + str(datetime.datetime.now())+"\n")
    except  Exception  as exception:
        print(exception)
def del_bucket(bucket):
    """
    Deletes an S3 Bucket
    :param generic_name(str): Name of Bucket
    :return No return
    *del_bucket is an example provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    try:
        delete_bucket.delete_bucket(bucket)
        prompt = str("\n" + bucket + " has been deleted.\n")
        print(prompt + str(datetime.datetime.now())+"\n")
    except Exception as exception:
        print(exception)
def copy_obj(source_bucket, obj, dest_bucket):
    """
    Copies an object from one S3 Bucket to another
    :param generic_name(str): Name of Source Bucket
    :param generic_name(str): Name of Object
    :param generic_name(str): Name of Destination Bucket
    :return No return
    *copy_obj is an example provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    try:
        copy_object.copy_object(source_bucket, obj, dest_bucket)
        prompt = str("\n" + obj + " has been copied to " + dest_bucket + ".\n")
        print(prompt + str(datetime.datetime.now())+"\n")
    except Exception as exception:
        print(exception)
def download(bucket, obj):
    """
    Downloads an object from an S3 Bucket
    :param generic_name(str): Name of Bucket
    :param generic_name(str): Name of Object
    :return No return
    *download uses example code provided by University of Maryland
     Global Campus (UMGC) from AWS.
    """
    s_3 = boto3.resource('s3')
    try:
       s_3.Bucket(bucket).download_file(obj, obj)
       os.system("mv " + obj + " ./HW1/Downloads")
    except botocore.exceptions.ClientError as exception:
        if exception.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
    prompt = str("\n" + obj + " has been downloaded to the Downloads directory.\n")
    print(prompt + str(datetime.datetime.now())+"\n")
def check_option(options, uin):
    """
    Confirms if user's input is a valid option in the program.
    :param generic_options(list): List of options availabe in the program's menu.
    :param generic_choice(str): User's input
    :rtype ***bool***
    :return Returns boolean result to confirm if user's input is a valid option.
    """
    try:
        con = any(uin in options for val in options)
        print(con)
        return con
    except Exception as exception:
        print(exception)
def run():
    """
    Main driver of program
    :return No return
    """
    loop_kill = False
    try:
        while not loop_kill:
            options = ["1", "2", "3", "4", "5", "6", "q"]
            prompt = str("Main Menu\n\nEnter q to exit.\n\nSelect an Option:\n\n" +
            "1. Create an S3 Bucket\n2. Move Object\n3. Delete Object\n4. Delete Bucket\n" +
            "5. Copy Object to another bucket\n6. Download Object\n")
            uin = str(input(prompt))
            if uin == "1":
                bname = str(input("Enter bucket name:\n"))
                make_bucket(bname)
            elif uin == "2":
                bucket = str(input("Enter bucket name:\n"))
                obj = str(input("Enter name of object:\n"))
                move_obj(bucket, obj)
            elif uin == "3":
                bucket = str(input("Enter bucket name:\n"))
                obj = str(input("Enter name of object:\n"))
                del_obj(bucket, obj)
            elif uin == "4":
                bucket = str(input("Enter name of bucket:\n"))
                del_bucket(bucket)
            elif uin == "5":
                source_bucket = str(input("Enter name of source bucket:\n"))
                obj = str(input("Enter name of object:\n"))
                dest_bucket = str(input("Enter name of destination bucket:\n"))
                copy_obj(source_bucket, obj, dest_bucket)
            elif uin == "6":
                bucket = str(input("Enter name of source bucket:\n"))
                obj = str(input("Enter name of object:\n"))
                download(bucket, obj)
            elif uin == "q":
                loop_kill = True
                print("Exit Code 0: " + str(datetime.datetime.now()))
            elif not check_option(options, uin):
                print("\nInvalid entry. Please try again.\n")
    except Exception as exception:
        print(exception)
        