# Reddit Infinity autobuilder

Build from source [Infinity client app](https://github.com/Docile-Alligator/Infinity-For-Reddit) automatically when there is a new release available, using your own reddit API key!

## Setup
Please follow the steps below;
### Install docker and get your Reddit API Key
First, you will need to create your own application and get its api key from your own account on reddit from [here](https://old.reddit.com/prefs/apps/). It is recommended to set the `redirect uri` to `http://127.0.0.1` .
### Clone repository and build docker image
Afterwards, clone this repository and build the docker image. You may build the image using the following command, root may be required;
```sh
$ git clone <this repo url> && cd reddit-infinity-autobuilder
$ docker build -t infinity-autobuilder .
```
### Set container environment variables accordingly and run
An [example docker compose file](docker-compose.yml) is provided for this purpose. Container may be configured using the following environment variables;

- `REDDIT_API_KEY`: Your reddit API key
- `USER_AGENT`: User agent to use for communication with reddit (Optional)
- `REDDIT_USERNAME`: Your username in Reddit. It will be used for user agent generation in case you did not provide the previous `USER_AGENT` variable.
- `DISCORD_WEBHOOK`: Webhook URL for receiving notifications when a new version is released and compiled.
- `UPDATES_CHECK_INTERVAL_SECONDS`: Interval for checking for new version.

Finally, you may create the container with the following command;
```sh
$ docker compose up -d
```
