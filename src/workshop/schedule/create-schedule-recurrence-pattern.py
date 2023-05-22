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

#   Define schedule with with recurrence pattern
#   "pipeline_job" is defined in connect-azml-workspace.py file
schedule_name = "simple_sdk_create_schedule_recurrence"

schedule_start_time = datetime.utcnow()
recurrence_trigger = RecurrenceTrigger(
    frequency="day",
    interval=1,
    schedule=RecurrencePattern(hours=10, minutes=[0, 1]),
    start_time=schedule_start_time,
    time_zone=TimeZone.UTC,
)

job_schedule = JobSchedule(
    name=schedule_name, trigger=recurrence_trigger, create_job=pipeline_job
)

#create a schedule
job_schedule = ml_client.schedules.begin_create_or_update(
    schedule=job_schedule
).result()
print(job_schedule)