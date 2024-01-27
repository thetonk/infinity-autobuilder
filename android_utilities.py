import re,os,subprocess
class App():
    def __init__(self,api_token: str, user_agent: str, redirect_url: str) -> None:
        self.api_token = api_token
        self.redirect_uri = redirect_url
        self.user_agent = user_agent

    def build(self) -> int:
        # Change API
        apiutils_file = "app/src/main/java/ml/docilealligator/infinityforreddit/utils/APIUtils.java"
        apiutils_code = open(apiutils_file, "r", encoding="utf-8-sig").read()
        apiutils_code = apiutils_code.replace("NOe2iKrPPzwscA", self.api_token)
        apiutils_code = apiutils_code.replace("infinity://localhost", self.redirect_uri)
        apiutils_code = re.sub(r'public static final String USER_AGENT = ".*?";', f'public static final String USER_AGENT = "{self.user_agent}";', apiutils_code)
        with open(apiutils_file, "w", encoding="utf-8") as f:
            f.write(apiutils_code)
        # Add Keystore
        if not os.path.exists("Infinity.jks"):
            print("fetching infinity key!")
            subprocess.run("wget https://github.com/TanukiAI/Infinity-keystore/raw/main/Infinity.jks", shell=True, check=True)
        build_gradle_file = "app/build.gradle"
        build_gradle_code = open(build_gradle_file, "r", encoding="utf-8-sig").read()
        build_gradle_code = build_gradle_code.replace(r"""    buildTypes {""", fr"""    signingConfigs {{
        release {{
            storeFile file("{os.getcwd()}/Infinity.jks")
            storePassword "Infinity"
            keyAlias "Infinity"
            keyPassword "Infinity"
        }}
    }}
    buildTypes {{""")
        build_gradle_code = build_gradle_code.replace(r"""    buildTypes {
        release {""", r"""    buildTypes {
        release {
            signingConfig signingConfigs.release""")
        with open(build_gradle_file, "w", encoding="utf-8") as f:
            f.write(build_gradle_code)
        process = subprocess.run("./gradlew assembleRelease",shell=True)
        subprocess.run("mv app/build/outputs/apk/release/app*.apk /output/Infinity.apk", shell=True)
        #stop gradle daemon for now, save memory and disk space
        subprocess.run("./gradlew --stop && rm -rf ~/.gradle/", shell=True)
        return process.returncode
