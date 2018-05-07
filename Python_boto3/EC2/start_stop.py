import sys
import os
import time 
try:
	import boto3
	print "Imported boto3"
except Exception as e:
	print e
	sys.exit(1)

def display_regions(ec2_con_re):
   print"The list of available ec2 regions:" 
   list_of_regions=[]
   for each in  ec2_con_re.meta.client.describe_regions()['Regions']:
        print  each['RegionName']
        list_of_regions.append(each['RegionName'])
   #print "list_of_regions: {}".format(list_of_regions)
   region_name=raw_input("Enter your region name from the above list: ")
   while True:
      if region_name not in list_of_regions:
          print"you entered invalid regions name: "
          for each in list_of_regions:
                print each
          region_name=raw_input("Enter your region name from the above list: ")
          continue
      else:
          break
   return region_name
def get_connection(r_name='us-east-1'):
	ec2_con_re_r=boto3.resource("ec2",region_name=r_name)
	return ec2_con_re_r
def display_instance_ids(ec2_con):
	print"The available instances ids are:"
	for each in ec2_con.instances.all():
		print each.id 
	my_id=raw_input("Select your instance id from above list: ")
	return my_id
def get_status_of_ec2(ec2_con_re_for_region,my_instance_id):
	filter1={"Name":"instance-id","Values":[my_instance_id]}
	for each in ec2_con_re_for_region.instances.filter(Filters=[filter1]):
		return  each.state['Name']




def start_ec2_instance(ec2_con_re_for_region,my_instance_id):
    pr_st=get_status_of_ec2(ec2_con_re_for_region,my_instance_id)
    if pr_st=="running":
    	print"alredy it is running"
    else:
    	filter1={"Name":"instance-id","Values":[my_instance_id]}
	for each in ec2_con_re_for_region.instances.filter(Filters=[filter1]):
	    each.start()
	    each.wait_until_running()

	    print"your instance is started"
	

			





def stop_ec2_instance(ec2_con_re_for_region,my_instance_id):
	pr_st=get_status_of_ec2(ec2_con_re_for_region,my_instance_id)
	if pr_st=="stopped":
		print"already it is stopped"
	else:
            filter1={"Name":"instance-id","Values":[my_instance_id]}
            for each in ec2_con_re_for_region.instances.filter(Filters=[filter1]):
            	print dir(each)
                each.stop()
                '''
                try:
                	each.wait_until_stopped()
                except Exception as e:
                	print e 
'''				while True:
					time.spleep(60)
					pr_st=get_status_of_ec2(ec2_con_re_for_region,my_instance_id)
					if pr_st=="stopped":
						break

                print"your instance is stopped"


def main():
    ec2_con_re=get_connection()
    my_region=display_regions(ec2_con_re)
    ec2_con_re_for_region=get_connection(my_region)
    my_instance_id=display_instance_ids(ec2_con_re_for_region)
    start_stop=raw_input("Enter your cmd to start/stop your ec2 instance:")
    my_cmds=["stop","start"]
    if start_stop in my_cmds:
	if start_stop=="start":
            start_ec2_instance(ec2_con_re_for_region,my_instance_id)
	if start_stop=="stop":
	    stop_ec2_instance(ec2_con_re_for_region,my_instance_id)




if __name__=="__main__":
	os.system('cls')
	main() 
