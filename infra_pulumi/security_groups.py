from pulumi_aws import ec2, vpc
from networks import custom_vpc

# default security group for custom-vpc
sg_default = ec2.DefaultSecurityGroup(
    "defaul-sg",
    vpc_id=custom_vpc.id,
    tags={
        "Name": "default-sg",
        "description": "Default SG for Custom-VPC"
    }
)

# ingress rules for default security group
sg_default_ingress_allow_8080 = vpc.SecurityGroupIngressRule(
    resource_name="ingress-tcp-8080",
    security_group_id=sg_default.id,
    cidr_ipv4="0.0.0.0/0",
    from_port=8080,
    to_port=8080,
    ip_protocol="tcp"
)

sg_default_ingress_allow_22 = vpc.SecurityGroupIngressRule(
    resource_name="ingress-tcp-ssh",
    security_group_id=sg_default.id,
    cidr_ipv4='0.0.0.0/0',
    from_port=22,
    to_port=22,
    ip_protocol='tcp'
)

sg_default_ingress_allow_51820 = vpc.SecurityGroupIngressRule(
    resource_name="ingress-wireguard",
    security_group_id=sg_default.id,
    cidr_ipv4='0.0.0.0/0',
    from_port=51820,
    to_port=51820,
    ip_protocol='udp'
)


# egress rules fro default security group
sg_default_egress_allow_all = vpc.SecurityGroupEgressRule(
    resource_name="egress-all",
    security_group_id=sg_default.id,
    cidr_ipv4="0.0.0.0/0",
    ip_protocol=-1
)
