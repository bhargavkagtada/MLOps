# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace, Environment, BuildContext
from azure.identity import DefaultAzureCredential


# Create environment from docker image with a conda YAML
env_docker_conda = Environment(
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
    conda_file="infra/pydata.yml",
    name="docker-image-plus-conda-example",
    description="Environment created from a Docker image plus Conda environment.",
)
ml_client.environments.create_or_update(env_docker_conda)