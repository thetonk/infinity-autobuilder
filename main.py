import os,sys,requests,json
from git import Repo
from android_utilities import App
from time import sleep

api_token = os.getenv("REDDIT_API_KEY", None)
your_reddit_username = os.getenv("REDDIT_USERNAME",None)
user_agent = os.getenv("USER_AGENT", f"android:personal-app:0.0.1 (by /u/{your_reddit_username})")
interval = os.getenv("UPDATES_CHECK_INTERVAL_SECONDS", 86400) #defaults to once a day
webhookURL = os.getenv("DISCORD_WEBHOOK", None)
webserverURL = os.getenv("WEBSERVER_URL", None)
redirect_uri = 'http://127.0.0.1'
json_file_path = "/data/status.json"
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

#clone repo if not present
if not os.path.isdir("client"):
  repo = Repo.clone_from("https://github.com/Docile-Alligator/Infinity-For-Reddit","client")
else:
  repo = Repo("client")

while True:
  compiledRelease = None
  if os.path.exists(json_file_path):
    with open(json_file_path, "r") as f:
      js = json.load(f)
      compiledRelease = js["version"]
  #discard local changes before pulling
  repo.git.reset("--hard")
  repo.remotes.origin.pull()
  os.chdir("client")
  githubRelease = next(reversed(repo.tags), None).name
  if compiledRelease != githubRelease:
    sendDiscordMessage("New Infinity release!", f"New Infinity release found on Github! \nVersion: {githubRelease}\nInitializing app build!", int("ffcc00",16))
    app = App(api_token, user_agent, redirect_uri)
    status = app.build()
    if status == 0:
      compiledRelease = githubRelease
      print("direct download is ready!")
      if webserverURL != None:
        sendDiscordMessage("Infinity app build", f"App building for version {githubRelease} was successful and apk is ready for download, click [here]({webserverURL})!", int("33cc33",16))
      else:
        sendDiscordMessage("Infinity app build", f"App building for version {githubRelease} was successful! You may now download the latest apk!", int("33cc33",16))
    else:
      print("build failed!")
      sendDiscordMessage("Infinity app build", f"App building for version {githubRelease} failed! Please refer to logs for more info", int("cc0000",16))
    with open(json_file_path, "w") as f:
      obj = {"version": f"{githubRelease}"}
      json.dump(obj,f)
  os.chdir(os.pardir)
  sleep(interval)
