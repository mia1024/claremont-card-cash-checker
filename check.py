STUDENT_ID = "YOUR_ID"
PASSWORD = "YOUR_PASSWORD"
DEBUG = False

import time, requests, sys, re


def log(s):
    if DEBUG:
        print(s, file=sys.stderr)


s = requests.Session()
s.headers["User-Agent"] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.7.5) Gecko/20060127 Netscape/8.1'

log("Fetching skey")
r = s.get("https://cards.services.claremont.edu/login.php")

skey = re.search(r"name='skey' value='([0-9a-f]+)'", r.text).group(1)
log(skey)

log("Logging in")
r = s.post("https://cards.services.claremont.edu/login.php", data={
    "loginphrase": STUDENT_ID,  # what kind of person would name this login phrase???
    "password": PASSWORD,
    "cid": "35",
    "save": "1",
    "skey": skey
})
if "Form contains errors" in r.text:
    # <div
    #   role="alert" class="jsa_form-error" id="form-error" tabindex="-1"
    #   aria-label="Form contains errors"
    # >
    print("Login failed")
    sys.exit(1)
log("success")

log("Waiting server")
s.get("https://cards.services.claremont.edu/login.php?cid=35&fullscreen=1")
while True:
    r = s.get("https://cards.services.claremont.edu/login-check.php?skey=" + skey)
    if "<message>0</message>" in r.text:
        time.sleep(0.2)
        log("waiting")
    else:
        break

log("fetching cash")
r = s.get("https://cards.services.claremont.edu/index.php?cid=35")
res = re.findall(r'<span class="sr-only">Current Balance (.+?)</span>', r.text)

print("Flex: " + res[0])
print("Claremont Cash: " + res[1])
print("Swipes: " + res[2])

s.get("https://cards.services.claremont.edu/logout.php?cid=35")
