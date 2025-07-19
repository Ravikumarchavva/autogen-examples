from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool

import asyncio

async def main():
    code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
    await code_executor.start()
    code_execution_tool = PythonCodeExecutionTool(executor=code_executor)
    cancellation_token = CancellationToken()

    code = """
    import time
    def sleep_for_a_while():
        time.sleep(5)
        return "Slept for 5 seconds"
    sleep_for_a_while() 
    """
    result = await code_execution_tool.run_json({ "code": code }, cancellation_token=cancellation_token)
    print(code_execution_tool.return_value_as_string(result))
    await code_executor.stop()

if __name__ == "__main__":
    asyncio.run(main())