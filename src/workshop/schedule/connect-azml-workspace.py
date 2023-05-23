#In this section we will connect to the workspace in which the job will be run.
# Import required libraries
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient, Input, load_component
from azure.ai.ml.constants import TimeZone
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import (
    JobSchedule,
    CronTrigger,
    RecurrenceTrigger,
    RecurrencePattern,
)
from datetime import datetime

#configure credentials
#We are using DefaultAzureCredential to get access to workspace.
try:
    credential = DefaultAzureCredential()
    # Check if given credential can get token successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
    credential = InteractiveBrowserCredential()

#Configure workspace details and get a handle to the workspace
#To connect to a workspace, we need identifier parameters - a subscription, resource group and workspace name. 
#We will use these details in the MLClient from azure.ai.ml to get a handle to the required Azure Machine Learning workspace.
try:
    ml_client = MLClient.from_config(credential=credential)
except Exception as ex:
    # enter details of your AML workspace
    subscription_id = ""
    resource_group = ""
    workspace = ""

    # get a handle to the workspace
    ml_client = MLClient(credential, subscription_id, resource_group, workspace)
print(ml_client)

#CHANGE PARENT DIRECTORY PATH AND MODEL PATHS
#
#Create a pipeline job with settings
parent_dir = "../jobs/pipelines/1a_pipeline_with_components_from_yaml"
train_model = load_component(source=parent_dir + "/train_model.yml")
score_data = load_component(source=parent_dir + "/score_data.yml")
eval_model = load_component(source=parent_dir + "/eval_model.yml")

# Construct pipeline
@pipeline()
def pipeline_with_components_from_yaml(
    training_input,
    test_input,
    training_max_epochs=20,
    training_learning_rate=1.8,
    learning_rate_schedule="time-based",
):
    """E2E dummy train-score-eval pipeline with components defined via yaml."""
    # Call component obj as function: apply given inputs & parameters to create a node in pipeline
    train_with_sample_data = train_model(
        training_data=training_input,
        max_epochs=training_max_epochs,
        learning_rate=training_learning_rate,
        learning_rate_schedule=learning_rate_schedule,
    )

    score_with_sample_data = score_data(
        model_input=train_with_sample_data.outputs.model_output, test_data=test_input
    )
    score_with_sample_data.outputs.score_output.mode = "upload"

    eval_with_sample_data = eval_model(
        scoring_result=score_with_sample_data.outputs.score_output
    )

    # Return: pipeline outputs
    return {
        "trained_model": train_with_sample_data.outputs.model_output,
        "scored_data": score_with_sample_data.outputs.score_output,
        "evaluation_report": eval_with_sample_data.outputs.eval_output,
    }

# set run time settings
pipeline_job = pipeline_with_components_from_yaml(
    training_input=Input(type="uri_folder", path=parent_dir + "/data/"),
    test_input=Input(type="uri_folder", path=parent_dir + "/data/"),
    training_max_epochs=20,
    training_learning_rate=1.8,
    learning_rate_schedule="time-based",
)

# set pipeline level compute
pipeline_job.settings.default_compute = "cpu-cluster"