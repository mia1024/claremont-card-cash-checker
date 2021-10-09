from flask import Flask, request, jsonify, render_template, make_response
import time, requests, sys, re

app = Flask("CCCCCC")


class LoginFailed(Exception): pass


def check(username, password):
    s = requests.Session()
    s.headers["User-Agent"] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.7.5) Gecko/20060127 Netscape/8.1'
    r = s.get("https://cards.services.claremont.edu/login.php")
    skey = re.search(r"name='skey' value='([0-9a-f]+)'", r.text).group(1)
    r = s.post("https://cards.services.claremont.edu/login.php", data={
        "loginphrase": username,  # what kind of person would name this login phrase???
        "password": password,
        "cid": "35",
        "save": "1",
        "skey": skey
    })
    if "Form contains errors" in r.text:
        # <div
        #   role="alert" class="jsa_form-error" id="form-error" tabindex="-1"
        #   aria-label="Form contains errors"
        # >
        raise LoginFailed
    s.get("https://cards.services.claremont.edu/login.php?cid=35&fullscreen=1")
    time.sleep(0.1)
    while True:
        r = s.get("https://cards.services.claremont.edu/login-check.php?skey=" + skey)
        if "<message>0</message>" in r.text:
            time.sleep(0.2)
        else:
            break
    
    r = s.get("https://cards.services.claremont.edu/index.php?cid=35")
    res = re.findall(r'<span.*?>Current Balance (.+?)</span>', r.text, re.I)
    s.get("https://cards.services.claremont.edu/logout.php?cid=35")
    return res


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        j = request.get_json()
        try:
            res = check(j.get("username"), j.get("password"))
            return jsonify({
                "Flex": res[0],
                "Cash": res[1],
                "Swipe": res[2]
            })
        except LoginFailed:
            return "", 401
        except:
            return "", 400


@app.route("/manifest.json", methods=["GET"])
def manifest():
    return jsonify({
        "name": "Completely Convoluted Claremont Card Cash Checker",
        "short_name": "C6",
        "start_url": "/",
        "display": "standalone",
        "description": "Check your card balance more easily",
        "orientation": "portrait",
        "icons": [
            {
                "type": "image/png",
                "sizes": f"{w}x{w}",
                "src": f"https://raw.githubusercontent.com/mia1024/claremont-card-cash-checker/web/icons/{w}.png"
            } for w in (48, 72, 96, 144, 192, 512)
        ]
    })


@app.route("/sw.js", methods=["GET"])
def sw():
    # for PWA
    resp = make_response("""
    self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          return await fetch(event.request);
        } catch (error) {
          return new Response("No internet connection. ", {headers:{"Content-Type": "text/html"}})
        }
      })()
    );
  }})
    
    """)
    resp.headers["Content-Type"] = "text/javascript"
    return resp


if __name__ == "__main__":
    app.run(debug=True)
