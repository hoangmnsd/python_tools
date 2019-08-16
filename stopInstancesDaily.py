import boto3, logging
from botocore.exceptions import ClientError

# Logger settings - CloudWatch
# Set level to DEBUG for debugging, INFO for general usage.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def filterInstances():
    """
    Tries to filter EC2 do not having tag AutoStop=No. If a ThrottlingException is encountered
    recursively calls itself until success.
    """
    try:
        ec2 = boto3.client('ec2')
        # filter the instances running
        reservations_1 = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
            ).get(
            'Reservations', []
            )
        all_instances = sum(
        [
            [i['InstanceId'] for i in r['Instances']]
            for r in reservations_1
        ], [])

        # get all instances running with tag AutoStop=No
        reservations_2 = ec2.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']},
                {'Name': 'tag:AutoStop', 'Values': ['NO', 'No', 'no']}
            ]
            ).get(
            'Reservations', []
            )
        instances_with_tag = sum(
        [
            [i['InstanceId'] for i in r['Instances']]
            for r in reservations_2
        ], [])

        # get all instances running without tag AutoStop=No
        instances_without_tag = [to_stop for to_stop in all_instances if to_stop not in [i for i in instances_with_tag]]
        logger.info("Number of running ec2 instances without tag AutoStop=No: {0}".format( len(instances_without_tag)) )
        return instances_without_tag

    except ClientError as err:
        if 'ThrottlingException' in str(err):
            logger.info("Filter Instances throttled, automatically retrying...")
            filterInstances()
        else:
            logger.error("Filter Instances Failed!\n%s", str(err))
            return False
    except:
        logger.info('Filter Instances Failed!')
        return False


def lambda_handler(event, context):
    # Filter for instances is running and do not having the tag "AutoStop=NO/no/No" 
    instances = filterInstances()
    logger.info(instances)
    ec2 = boto3.client('ec2')
    if len(instances) > 0:
        #perform the stop
        logger.info("Stop all running ec2 instances without tag AutoStop=NO/no/No")
        ec2.stop_instances(InstanceIds=instances)
        return instances
    else:
        logger.info("Nothing to stop")
        return True
    
