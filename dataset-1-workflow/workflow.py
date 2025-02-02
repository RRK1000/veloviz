import asyncio
import requests
import zipfile
import csv
from io import BytesIO
from datetime import timedelta
from pathlib import Path

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import (
    SandboxedWorkflowRunner,
    SandboxRestrictions,
)

from pymongo import MongoClient


@activity.defn
async def fetch() -> bool:
    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    url = base_url + "/api/3/action/package_show"
    params = {"id": "bike-share-toronto-ridership-data"}
    package = requests.get(url, params=params).json()
    latest_resource = package["result"]["resources"][-1]
    if not latest_resource["datastore_active"]:
        url = base_url + "/api/3/action/resource_show?id=" + latest_resource["id"]
        resource_metadata = requests.get(url).json()

    url = resource_metadata["result"]["url"]
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for failed requests

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("./dataset-1-workflow")

        print(f"ZIP file downloaded and extracted to: {"./dataset-1-workflow"}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False


@activity.defn
async def load() -> str:
    # Todo: dynamically identify latest csv
    csv_file = "dataset-1-workflow/Bike share ridership 2024-09.csv"
    mongo_config = {
        "host": "localhost",
        "port": 27017,
        "username": "mongoadmin",
        "password": "mongoadmin",
        "authSource": "admin",
    }
    db_name = "fireball"
    collection_name = "bike-share-ridership"

    try:
        client = MongoClient(
            mongo_config["host"],
            mongo_config["port"],
            username=mongo_config.get("username"),
            password=mongo_config.get("password"),
            authSource=mongo_config.get("authSource"),
        )
        db = client[db_name]
        db[collection_name].drop()

        # Connect to the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Open the CSV file and read data
        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            # Prepare the data to insert (convert each row to a dictionary)
            documents = []
            for row in csv_reader:
                documents.append(dict(row))
        result = collection.insert_many(documents)
        
        for p in Path("./dataset-1-workflow").glob("*.csv"):
            p.unlink()

        
        return f"Successfully inserted {len(result.inserted_ids)} records into the '{collection_name}' collection."
        
    except Exception as e:
        return f"An error occurred while loading the collection: {e}"
    


@workflow.defn
class Dataset1Workflow:
    """Fetches and loads the https://open.toronto.ca/dataset/bike-share-toronto-ridership-data dataset to MongoDB

    Returns:
        _type_: _description_
    """

    @workflow.run
    async def run(self) -> str:
        result = await workflow.execute_local_activity(
            fetch,
            start_to_close_timeout=timedelta(seconds=10),
        )
        print(f"fetch: {result}")
        return await workflow.execute_local_activity(
            load,
            start_to_close_timeout=timedelta(seconds=10),
        )


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="dataset-1-activity-task-queue",
        workflows=[Dataset1Workflow],
        activities=[fetch, load],
        workflow_runner=SandboxedWorkflowRunner(
            restrictions=SandboxRestrictions.default.with_passthrough_modules(
                "requests"
            )
        ),
    ):
        result = await client.execute_workflow(
            Dataset1Workflow.run,
            id="dataset-1-activity-workflow-id",
            task_queue="dataset-1-activity-task-queue",
            # cron_schedule="0 0 1 * *"
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
