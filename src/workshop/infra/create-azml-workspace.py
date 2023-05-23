# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace, Environment, BuildContext
from azure.identity import DefaultAzureCredential


# Enter details of your subscription
# IMP: Create a configuration files with your subscription details!
subscription_id = ""
resource_group = ""
workspace = ""

#Get handle to ML workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)

ws_basic = Workspace(
    name=workspace,
    location="eastus",
    display_name="",
    description="This example shows how to create a basic workspace",
    hbi_workspace=False,
    tags=dict(purpose="demo"),
)

ws_basic = ml_client.workspaces.begin_create(ws_basic).result()
print(ws_basic)