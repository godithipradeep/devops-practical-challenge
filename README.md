#Task: Create & deploy a simple NGINX web server using Ansible.


Approach I would like to take for this scenario keeping the below in mind.

Manage the infrastructure with Terraform
Have a Jenkins server to run the playbooks.
Have 1 nginx server


Create 2 ec2 instances
1.Jenkins and Ansible control node(playbooks will run from Jenkins pipeline)
2.Nginx (installed and configured by Ansible)

Instead of creating the ec2 instance with Ansible, I would prefer to use Terraform to create the instances and networking, and use Ansible (via Jenkins pipeline) to install and configure nginx on the second server. If time permits, I will set up nginx on docker.

This git repo has all the files required.


---Basic terraform script in terraform directory.

Create vpc  (us-east-1)
Create internet gateway
Create a public subnet and associate a route to it
Create instance for  jenkins/ansible and install jenkins/ansible with user data(using ubuntu server)
Create instance for nginx
Create jenkins security group(8080 from anywhere, 22 from provided cidr(my public ip) in vars file)
Create nginx security group(80 from anywhere, 22 from jenkins security group)
Output the required IP addresses

Note: Using an ssh key I have in the console named “mykey” for ec2.


After terraform apply, get the private ip of nginx server and update the ansible inventory file in the repo(This can be automated, mentioned below)
Visit http:jenkins-public-ip:8080 to configure jenkins
Install ansible plugin
Add the ssh private key to jenkins credentials with name “ansible”
Create the pipeline with “Jenkinsfile” in the repository.
Ansible inventory and playbook are in the repo along with files required for nginx config.
Run the pipeline

Ansible configuration:

Using an inventory file “inventory” to maintain the inventory. For this test purpose, I manually added the private ip of nginx provided by terraform output to inventory file.
configured a single playbook with the tasks required.
  installing nginx
  copying files to the server
  restarting nginx to use the new files


Jenkins configuration:
Install Ansible plugin and set global variable
Add a credential(username with private key to run playbooks on nginx servers)
Set up a pipeline job with Jenkins file in the repository
Build the pipeline
This should run the playbook on the nginx server

Verify nginx by using the public ip from terraform output


What more can we do?

Skipping those since this is a test. Will be good to have for scalability

Create an alb and put the nginx server behind it.
Configure an autoscaling group for nginx
Set up a lambda function to check the load balancer response 200 and send a notification if it fails.

To handle multiple nginx servers, we can configure aws ec2 plugin for ansible to get the ip addresses dynamically by using the ‘tag: Name:nginx’ we gave in terraform. Also an iam role(ec2-readonly) for ansible to get the nginx private ips for dynamic inventory.


What can be done more in terms of security?

We already have the below.
SSH to jenkins is limited to my IP via variable in terraform.
SSH to nginx is allowed only from the Jenkins security group.
Saved the nginx private key in jenkins credentials instead of in the ansible node.
In case of load balancer, nginx can be moved into a private subnet and setup https at load balancer.








