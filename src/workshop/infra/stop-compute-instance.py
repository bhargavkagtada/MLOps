# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ComputeInstance, AmlCompute
from azure.identity import DefaultAzureCredential

# Enter details of your AML workspace
subscription_id = ""
resource_group = ""
workspace = ""

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)


# Stop compute
ci_basic_name = "ci-mlops-dev"
ml_client.compute.begin_stop(ci_basic_name).wait()