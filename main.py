import os,sys,requests,json
from git import Repo
from android_utilities import App
from time import sleep

api_token = os.getenv("REDDIT_API_KEY", None)
your_reddit_username = os.getenv("REDDIT_USERNAME",None)
user_agent = os.getenv("USER_AGENT", f"android:personal-app:0.0.1 (by /u/{your_reddit_username})")
interval = os.getenv("UPDATES_CHECK_INTERVAL_SECONDS", 86400) #defaults to once a day
webhookURL = os.getenv("DISCORD_WEBHOOK", None)
redirect_uri = 'http://127.0.0.1'
version = '[GitHub Repository]'

def sendDiscordMessage(title: str, message:str, color: int) -> None:
  JSONPayload = {"embeds":[{"author": {"name": "Infinity Reddit client updater"}, "title": title, "description": message, "color":color}]}
  if webhookURL:
    requests.post(webhookURL, json=JSONPayload)

if not api_token or not your_reddit_username:
  print("")
  print("\x1b[31m[IMPORTANT]")
  print("No settings have been set. Please input your token and username.\x1b[0m")
  sys.exit()
else:
  print("Following settings have been set:")
  print("- User-Agent:", user_agent)
  print("- API token:", api_token)
  print("- Source location:", version)

if not os.path.isdir("client"):
  repo = Repo.clone_from("https://github.com/Docile-Alligator/Infinity-For-Reddit","client")
else:
  repo = Repo("client")

if not os.path.exists("/data/status.json"):
  latest = None
else:
  #avoid recompiling same version on container restart
  with open("/data/status.json", "r") as f:
    js = json.load(f)
    latest = js["version"]

while True:
  #discard local changes before pulling
  repo.git.reset("--hard")
  repo.remotes.origin.pull()
  os.chdir("client")
  #get latest tag
  if latest != next(reversed(repo.tags), None):
    latest = next(reversed(repo.tags),None).name
    sendDiscordMessage("New Infinity release!", f"New Infinity release found on Github! \nVersion: {latest}\nInitializing app build!", int("ffcc00",16))
    app = App(api_token, user_agent, redirect_uri)
    status = app.build()
    if status == 0:
      print("direct download is ready!")
      sendDiscordMessage("Infinity app build", f"App building for version {latest} was successful and apk is ready for download, click [here](https://private-files.sbaltsas.xyz/infinity/Infinity.apk)!", int("33cc33",16))
    else:
      print("build failed!")
      sendDiscordMessage("Infinity app build", f"App building for version {latest} failed! Please refer to logs for more info", int("cc0000",16))
    with open("/data/status.json", "w") as f:
      obj = {"version": f"{latest}"}
      json.dump(obj,f)
  os.chdir(os.pardir)
  sleep(interval)
