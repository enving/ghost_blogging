"""Apply the Digitalalchemisten publication design through Ghost's Admin API."""
import sys
import time
from pathlib import Path

import jwt
import requests
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
API = "https://digitalalchemisten.de/ghost/api/admin/"
LINKEDIN = "https://www.linkedin.com/in/tristan-h%C3%A4fele-812b8011b/"
DESCRIPTION = "Praxisversuche mit KI im Unternehmen. Tristan Wilms zeigt, wie er vorgeht und woran du selbst prüfen kannst, ob das Ergebnis taugt."


def main():
    cfg = dotenv_values(ROOT / "scripts/.env")
    key_id, secret = cfg["GHOST_ADMIN_API_KEY"].strip().split(":")
    now = int(time.time())
    token = jwt.encode({"iat": now, "exp": now + 240, "aud": "/admin/"},
                       bytes.fromhex(secret), algorithm="HS256", headers={"kid": key_id})
    session = requests.Session()
    session.headers.update({"Authorization": "Ghost " + token, "Accept-Version": "v6.0"})
    pending = []

    def call(method, route, **kwargs):
        res = session.request(method, API + route, timeout=35, allow_redirects=False, **kwargs)
        if not res.ok or res.is_redirect:
            print(f"{method} {route.partition('?')[0]}: HTTP {res.status_code}", flush=True)
            return None
        return res.json() if res.content else {}

    # Keep unrelated posts, memberships, menus and existing author URLs intact.
    user_data = call("GET", "users/?limit=all")
    matching = [u for u in (user_data or {}).get("users", [])
                if u["name"] in ("Tristan Häfele", "Tristan Wilms")]
    if len(matching) == 1:
        user = matching[0]
        if call("PUT", f"users/{user['id']}/", json={"users": [{"name": "Tristan Wilms", "website": LINKEDIN}]}) is None:
            pending.append("Author profile")
    else:
        pending.append("Author profile")

    pages = call("GET", "pages/slug/about/?formats=html")
    if pages:
        page = pages["pages"][0]
        if "is an independent publication launched" in (page.get("html") or ""):
            html = ('<p>Ich bin Tristan Wilms. Ich habe KI-Förderprojekte fachlich begleitet und später selbst '
                    'an der internen KI-Einführung gearbeitet.</p><p>Hier probiere ich aus, wie wir KI im Unternehmen '
                    'für konkrete Aufgaben nutzen können. Mich interessiert, was passiert, wenn das Wissen im Intranet, '
                    'in Dokumenten und in den Köpfen verschiedener Menschen steckt. Wie bekommt ein KI-Werkzeug den '
                    'Kontext, den es für die Arbeit braucht?</p><p>Meine Versuche und Erfahrungen teile ich hier. '
                    'Mit den Digitalalchemisten möchte ich eine Community aufbauen, in der wir solche Fragen gemeinsam '
                    'weiterverfolgen.</p><p><a href="' + LINKEDIN + '">Tristan Wilms auf LinkedIn</a></p>')
            if call("PUT", f"pages/{page['id']}/?source=html", json={"pages":[{
                "updated_at": page["updated_at"], "title": "Über mich", "html": html}]}) is None:
                pending.append("About page")
        elif page["title"] != "Über mich":
            pending.append("About page contains custom content")
    else:
        pending.append("About page")
    if call("PUT", "settings/", json={"settings":[{"key":"title","value":"Digitalalchemisten"},
            {"key":"description","value":DESCRIPTION},{"key":"accent_color","value":"#0040ce"}]}) is None:
        pending.append("Site settings")

    theme = ROOT / "appearance/digitalalchemisten-praxis.zip"
    with theme.open("rb") as f:
        result = call("POST", "themes/upload/", files={"file": (theme.name, f, "application/zip")})
    if result is None or call("PUT","themes/digitalalchemisten-praxis/activate/") is None:
        pending.append("Theme")
    print("Remaining: " + (", ".join(pending) or "none"))
    return int(bool(pending))


if __name__ == "__main__":
    sys.exit(main())
