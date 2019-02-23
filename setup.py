import boto3
import os
from pathlib import Path

class grey_cli:

	def __init__(self):
		session = boto3.session.Session(
		    aws_access_key_id= "",
		    aws_secret_access_key= "",
		     region_name="us-east-1"  #"ap-south-1"
		)
		self.ec2 = session.resource('ec2')
		print("connected")

	def create_instances(self, instance_name="greypie", keyname="greypie_key"):

		self.result = self.ec2.create_instances(ImageId='ami-035be7bafff33b6b6',
				InstanceType = 't2.micro',
				MinCount=1, 
				MaxCount=1,
				KeyName = keyname,
				DryRun=False,
				TagSpecifications=[
			        {
			        	'ResourceType': 'instance',
			            'Tags': [
			                {
			                    'Key': 'Name',
			                    'Value': instance_name    #adds name tag to an instance
			                },
			            ]
			        },
			    ],
			)

		print(self.result)


	def display_instances(self):
		filters = [{'Name': 'tag:Name', 'Values': ['greypie']}] 	#filter instance by name
		Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]  #filter instance by name
		instances = self.ec2.instances.filter(Filters=filters)
		
		for instance in instances:
			print(instance.id, instance.instance_type)

	def instance_id_for_name(self, tag_name = ""):

	def create_key(self,key_name = "greypie_key"):
		cwd = os.getcwd()
		key_file = Path(cwd+"/"+key_name+".pem")
		if not key_file.is_file():
			key_file = open(key_name+".pem",'w')
			key_pair = self.ec2.create_key_pair(KeyName=key_name)
			KeyPairOut = str(key_pair.key_material)
			key_file.write(KeyPairOut)
		else:
			print("key already exit")


gcli = grey_cli()
gcli.create_key()