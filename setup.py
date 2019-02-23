import boto3
import os
from pathlib import Path
import datetime

class grey_cli:

	def __init__(self):
		session = boto3.session.Session(
		    aws_access_key_id= "",
		    aws_secret_access_key= "",
		     region_name="us-east-1"  #"ap-south-1"
		)
		self.ec2 = session.resource('ec2')
		self.ec2_client = session.client('ec2')

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
		Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]  #filter instance by name
		instances = self.ec2.instances.filter(Filters=filters)
		
		for instance in instances:
			print(instance.id, instance.instance_type)

	def instance_id_for_name(self, tag_name = "greypie"):
		filters = [{'Name': 'tag:Name', 'Values': [tag_name]}] 	#filter instance by name
		instances = self.ec2.instances.filter(Filters=filters)
		i = 1
		instances_list = []
		for instance in instances:
			instances_list.append(instance.id)
			print(str(i)+")",instance.id)
			i+=1


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

	
	def terminate_instance(self, instance_id):
		self.ec2.instances.filter(InstanceIds=instance_id).terminate()


	def create_image(self, id, img_name = "greypie-image"):
		instance = self.ec2.Instance(id)
		image = instance.create_image(
		    Description='Image created on '+str(datetime.datetime.now()),
		    Name= img_name,
		    NoReboot=True
			)

		str_id = str(image)
		print("Image created with name= ** "+img_name+" **and id= **"+str_id[14:-2]+" **")




gcli = grey_cli()
gcli.create_image("i-07fd3a5b48b8237a4")