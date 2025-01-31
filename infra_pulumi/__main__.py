import pulumi
from pulumi_aws import ec2
from security_groups import sg_default
from networks import subnet_pub_1


# Get configuration
config = pulumi.Config()
aws_ami = config.get("aws-ami-ubuntu-2404")
aws_instance_type = config.get("aws-instance")
ssh_key_name = config.get("ssh-key")


# EC2 instance
web_server_1 = ec2.Instance(
    "web-server-1",
    instance_type=aws_instance_type,
    vpc_security_group_ids=[sg_default.id],
    ami=aws_ami,
    subnet_id=subnet_pub_1.id,
    key_name=ssh_key_name,
    tags={"Name": "web-server-1"},
    root_block_device={
        "volume_size": 15
    }
)


pulumi.export('web_dns', web_server_1.public_dns)
pulumi.export('web_private_ip', web_server_1.private_ip)
pulumi.export('web_public_ip', web_server_1.public_ip)
