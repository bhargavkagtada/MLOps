# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential


# Enter details of your subscription
subscription_id = "cae5edf4-d666-4dd5-a2fe-bf47d8b5fc06"
resource_group = "rg-msft-bk-mlops-demo"
workspace = "ws_mlw_mlopsv2"

ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)

ws_basic = Workspace(
    name=workspace,
    location="eastus",
    display_name="ws_mlw_mlopsv2",
    description="This example shows how to create a basic workspace",
    hbi_workspace=False,
    tags=dict(purpose="demo"),
)

ws_basic = ml_client.workspaces.begin_create(ws_basic).result()
print(ws_basic)