# Simple Node.js (Express) server on AWS EC2

- IaC on AWS EC2 instance with [Pulumi], [minikube], [docker] and [pyinfra]
- CI/CD by GitHub Actions

## Instructions and helps

- [Install Pulumi](https://www.pulumi.com/docs/iac/get-started/aws/begin/#install-pulumi)
- [Configure Pulumi to access your AWS account](https://www.pulumi.com/docs/iac/get-started/aws/begin/#configure-pulumi-to-access-your-aws-account)
- [Install kuebctl on Linux]([kubectl]: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)

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
```

Result of the last command should be:

```
Outputs:
    web_dns       : "ec2-16-171-227-145.eu-north-1.compute.amazonaws.com"
    web_private_ip: "10.0.0.176"
    web_public_ip : "16.171.227.145"
```

Save public IP to '/etc/hosts'.

```bash
echo '16.171.227.145    bastion' |sudo tee -a /etc/hosts
```

Setup SSH access to server 'bastion' in the file '~/.ssh/config':

```out
Host bastion
    IdentityFile /home/<USER>/.ssh/id_ed25519
    User ec2-user
```

Verify passworldless accesss to host 'bastion':

```bash
ssh bastion
```

Install software:

```bash
# install Docker and Minikube
cd apps_pyinfra
pyinfra inventory.py deploy.py
```

## Notes

- The name 'bastion' is used in 'apps_infra/inventory.py'
- I have installed AWS CLI
- I already have 'key_pair' for AWS EC2.
- User behind AWS_ACCESS_KEY_ID have admin rights.

[pyinfra]: https://pyinfra.com/
[Pulumi]: https://www.pulumi.com/
[minikube]: https://minikube.sigs.k8s.io/docs/
[docker]: https://docker.io
