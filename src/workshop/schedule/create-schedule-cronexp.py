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

#   Define schedule with with cron expression pattern
#   "pipeline_job" is defined in connect-azml-workspace.py file
schedule_name = "simple_sdk_create_schedule_cron"

schedule_start_time = datetime.utcnow()
cron_trigger = CronTrigger(
    expression="15 10 * * *",
    start_time=schedule_start_time,  # start time
    time_zone="Eastern Standard Time",  # time zone of expression
)

job_schedule = JobSchedule(
    name=schedule_name, trigger=cron_trigger, create_job=pipeline_job
)


#create a schedule
job_schedule = ml_client.schedules.begin_create_or_update(
    schedule=job_schedule
).result()
print(job_schedule)