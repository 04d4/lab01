from pulumi import Config, export
from pulumi_aws import ec2
from infra_pulumi.security_groups import sg_default
from infra_pulumi.networks import subnet_pub_1


# Get configuration
config = Config()
aws_ami = config.get("aws-ami")
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
)


export('web_dns', web_server_1.public_dns)
export('web_private_ip', web_server_1.private_ip)
export('web_public_ip', web_server_1.public_ip)
