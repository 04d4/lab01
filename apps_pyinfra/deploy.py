from pyinfra.operations import server, dnf


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

server.shell(
    name="Install kubectl",
    commands=[
        'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"',
        'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"',
        'echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check || exit 1',
        'sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl'
    ]
)

dnf.packages(
    name="Insall packages: git",
    packages=["git"]
)
