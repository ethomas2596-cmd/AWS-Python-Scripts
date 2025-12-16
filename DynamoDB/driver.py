"""
__filename__ = "hw_2.py"
__coursename__ = "SDEV 400 7380 - Secure Programming in the Cloud (2232)"
__author__ = "Earl Thomas"
__copyright__ = "None"
__credits__ = ["Earl Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Earl Thomas"
__email__ = "ethomas112@student.umgc.edu"
__status__ = "Test"
"""
import datetime
import json
import boto3
from boto3.dynamodb.conditions import Key
def make_table():
    """
    Creates a Table in Dynamodb
    :return table
    """
    dynamodb = boto3.client('dynamodb')
    table = dynamodb.create_table(
        TableName='Courses',
        KeySchema=[
            {
                'AttributeName' : 'course_id',
                'KeyType' : 'HASH'
            },
            {
                'AttributeName' : 'subject',
                'KeyType' : 'RANGE'
            }
            ],
        AttributeDefinitions=[
            {
                'AttributeName' : 'course_id',
                'AttributeType' : 'N'
            },
            {
                'AttributeName' : 'subject',
                'AttributeType' : 'S'
            },
            {
                'AttributeName' : 'catalog_num',
                'AttributeType' : 'N'
            }
            ],
        GlobalSecondaryIndexes=[{
            'IndexName': 'subject-index',
            'KeySchema': [
                {'AttributeName': 'subject', 'KeyType': 'HASH'},
                {'AttributeName': 'catalog_num', 'KeyType': 'RANGE'}
                ],
            'Projection': {
                'ProjectionType': 'ALL'
                },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
                }
            }],
        ProvisionedThroughput={
            'ReadCapacityUnits' : 10,
            'WriteCapacityUnits' : 10
            })
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName='Courses')
    print("Table has been created...")
    return table
def get_subject():
    """
    Gathers user input for subject
    :rtype ***str***
    :return Name of subject
    """
    subject = str(input("Welcome!\n\nEnter q to quit.\n\nEnter the subject:\n"))
    return subject
def add_item(course_id, subject, catalog_num, title, num_credits):
    """
    Adds an Item in the Courses table
    :param generic_name(int): Course ID Number
    :param generic_name(str): Name of subject
    :param generic_name(int): Catalog Number
    :param generic_name(str): Title of the class
    :param generic_name(int): Number of credits
    :param generic_name(table): Dynamodb table storing information
    :return No return
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Courses')
    table.put_item(
        Item={
            'subject' : subject,
            'catalog_num' : catalog_num,
            'title' : title,
            'num_credits' : num_credits,
            'course_id' : course_id
            }
        )
def update_table():
    """
    Inserts all course information from Courses.json into specified table in Dynamodb
    :return No return
    """
    json_file_path = "HW2/src/Courses.json"

    with open(json_file_path, 'r') as j:
        contents = json.load(j)
        for e in contents['data']:
            add_item(e['course_id'], e['subject'], e['catalog_num'], e['title'], e['num_credits'])
    print("Update Complete! Table is ready to use\n")
def query(subject, catalog_num):
    """
    Queries results based on user input
    :return No return
    """
    dydb = boto3.client('dynamodb')
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Courses')
        response = table.query(
            IndexName="subject-index",
            KeyConditionExpression=Key('subject').eq(str(subject)) &
            Key('catalog_num').eq(int(catalog_num))
        )
        if response['ScannedCount'] <= 0:
            print("\nUnable to find course information. Please try again\n")
        else:
            for i in response['Items']:
                print("\nThe title of", i['subject'], i['catalog_num'], "is", i['title']+".\n")
    except dydb.exceptions.ClientError:
        print("\nInvalid Entry. Please try again.\n")
def run():
    """
    Main driver of program
    :return No return
    """
    make_table()
    update_table()
    loop_kill = False
    subject = get_subject()
    while not loop_kill:
        try:
            catalog_num = int(input("\nEnter the Catalog Number:\n\n"))
        except ValueError:
            continue
        query(subject, catalog_num)
        loop_kill_2 = False
        while not loop_kill_2:
            uin = str(input("\nWould you like to search for another title? (Y/N):\n"))
            if uin in ("n", "N"):
                loop_kill = True
                loop_kill_2 = True
                print("Exit Code 0: " + str(datetime.datetime.now()))
                continue
            elif uin in ("y", "Y"):
                loop_kill_2 = True
                subject = str(input("\nEnter q to quit.\n\nEnter the subject:\n"))
                continue
            else:
                print("Invalid entry. Please try again.")
                