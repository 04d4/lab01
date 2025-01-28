import pulumi_aws as aws
from pulumi_aws import ec2

# Create a VPC
custom_vpc = ec2.Vpc(
    "custom-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": "custom-vpc"}
)

# Main gateway for new VPC
igw = ec2.InternetGateway(
    "vpc-igw",
    vpc_id=custom_vpc.id,
    tags={"Name": "custom-igw"}
)

availability_zones = aws.get_availability_zones(
    state="available", filters=[{"name": "opt-in-status", "values": ["opt-in-not-required"]}])
az1 = availability_zones.names[0]

# Subnets and ec2 instances in one availability zone
subnet_pub_1 = ec2.Subnet(
    "subnet-pub-az1",
    vpc_id=custom_vpc.id,
    availability_zone= az1,
    cidr_block="10.0.0.0/24",
    map_public_ip_on_launch=True,
    tags={"Name": "public-subnet-az1"}
)

subnet_priv_1 = ec2.Subnet(
    "subnet-priv-az1",
    vpc_id=custom_vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone= az1,
    tags={"Name": "private-subnet-az1"}
)

route_table_default = ec2.DefaultRouteTable(
    "route-table-default",
    default_route_table_id=custom_vpc.default_route_table_id,
    routes=[
        ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igw.id
        )
    ],
    tags={"Name": "route-table-default"}
)

route_table_private = ec2.RouteTable(
    "route-table-private",
    vpc_id=custom_vpc.id,
    routes=[ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=igw.id,
    )],
    tags={"Name": "private-route-table"}
)

ec2.RouteTableAssociation(
    "route-table-association-priv-1",
    subnet_id=subnet_priv_1.id,
    route_table_id=route_table_private.id
)

ec2.RouteTableAssociation(
    "default-rt-assoc-subnet-pub-1",
    subnet_id=subnet_pub_1.id,
    route_table_id=route_table_default.id
)