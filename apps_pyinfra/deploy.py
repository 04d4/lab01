from pyinfra.operations import server


server.shell(
    name="Install Docker",
    commands=[
        "sudo yum update -y",
        "sudo yum install -y docker",
        "sudo usermod -a -G docker ec2-user",
        "sudo systemctl enable --now docker",
        "sudo systemctl start docker"
    ]
)


server.shell(
    name="Install Minicube",
    commands=[
        "curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64",
        "sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64",
        "minikube start"
    ]
)
