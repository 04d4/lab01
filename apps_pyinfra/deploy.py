from pyinfra.operations import server, dnf, git, systemd
from pyinfra import host
from pyinfra.facts.server import Which


dnf.packages(
    name="Insall Docker, git",
    packages=['docker', 'git'],
    _sudo=True
)

server.user(
    name='Add ec2-user to group "docker"',
    groups=['docker'],
    user='ec2-user',
    _sudo=True
)

systemd.service(
    name="Enable the docker service",
    service="docker.service",
    enabled=True,
    running=True,
    _sudo=True
)

if not host.get_fact(Which, 'minikube'):
    server.shell(
        name="Install Minicube",
        commands=[
            "curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64",
            "sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64",
            "minikube start"
        ],
        _run_once=True
    )

if not host.get_fact(Which, 'kubectl'):
    server.shell(
        name="Install kubectl",
        commands=[
            'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"',
            'curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"',
            'echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check || exit 1',
            'sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl'
        ],
        _run_once=True
    )

git.repo(
    name="Clone Lab1 repo",
    src="https://github.com/04d4/lab01.git",
    dest="/home/ec2-user/lab01"
)
