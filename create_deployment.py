from prefect import flow
import streamlit as st

if __name__ == "__main__":
    flow.from_source(
        # source= the github or repo location where the source is located
        source="https://github.com/thatwonguy/automation.git",
        # entrpoint = the python script name and function name where the flow is expected to start
        entrypoint="main.py:automate",
    ).deploy(
        name="my-first-deployment",
        work_pool_name="my-managed-pool",
        # this runs everyday at 5pm
        cron="0 17 * * *",
    )