# AWS EC2 instance with [Pulumi] and [pyinfra]

## Instructions and helps

[Install Pulumi](https://www.pulumi.com/docs/iac/get-started/aws/begin/#install-pulumi)
[Configure Pulumi to access your AWS account](https://www.pulumi.com/docs/iac/get-started/aws/begin/#configure-pulumi-to-access-your-aws-account)

## How to start

```bash
# install Pulumi
curl -fsSL https://get.pulumi.com | sh
# copy GitHup repository
git clone https://github.com/04d4/lab01.git
cd lab01
# create virtual environment, activate and install packages
python3 -m venv venv
source ./venv/bin/activate
pip instal -r requiremens/base.txt
# Configure Pulumi to access your AWS account
export AWS_ACCESS_KEY_ID="<YOUR_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_SECRET_ACCESS_KEY>"
# update AWS parameters (region, instance type and coresponding AMI)
code Pulumi.dev.yaml
# deploy
pulumi up -s dev
# install Docker and Minikube
pyinfra apps_pyinfra/inventory.py apps_pyinfra/deploy.py
```

[pyinfra]: https://pyinfra.com/
[Pulumi]: https://www.pulumi.com/
