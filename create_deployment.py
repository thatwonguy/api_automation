from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        # source= the github or repo location where the source is located
        source="https://github.com/thatwonguy/automation.git",
        # entrypoint = the python script name and function name where the flow is expected to start
        entrypoint="main.py:automate",
    ).deploy(
        name="streamlit_automate",
        work_pool_name="my-managed-pool",
        # this runs everyday at 5pm
        cron="0 17 * * *",
    )