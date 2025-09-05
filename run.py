import subprocess

subprocess.run(["uvicorn", "app.api.main:app", "--reload"])
