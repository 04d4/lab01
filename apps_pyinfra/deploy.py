from pyinfra.operations import server, dnf, git, systemd, apt
from pyinfra import host
from pyinfra.facts.server import Which, LinuxDistribution, Home, User

home_dir = host.get_fact(Home)
current_user = host.get_fact(User)
linux_version = host.get_fact(LinuxDistribution)
print(linux_version)

if linux_version['name'] == "Ubuntu":
    apt.packages(
        name="Insall packages: git",
        packages=['git'],
        _sudo=True
    )
    if not host.get_fact(Which, 'docker'):
        server.shell(
            name="Add repository and install Docker Engine",
            commands=[
                # Add Docker's official GPG key
                "sudo apt-get update",
                "sudo apt-get install ca-certificates curl",
                "sudo install -m 0755 -d /etc/apt/keyrings",
                "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
                "sudo chmod a+r /etc/apt/keyrings/docker.asc",
                # Add the repository to Apt sources
                'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
                "sudo apt-get update",
                # Install Docker Engine
                "sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin",
                # Instal Docker Compose
                # "sudo apt-get -y install docker-compose-plugin"
            ]
        )
else:
    # In case of Amazon Linux 2023 and other RH
    dnf.packages(
        name="Insall Docker, git",
        packages=['docker', 'git'],
        _sudo=True
    )


server.user(
    name='Add current user to group "docker"',
    groups=['docker'],
    user=current_user,
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
    dest=f"{home_dir}/lab01"
)
