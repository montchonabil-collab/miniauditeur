import ssl
import socket
from datetime import datetime

def analyze_tls(hostname, port=443):
    result = {
        "hostname": hostname,
        "valid": False,
        "issuer": None,
        "expires": None,
        "days_left": None,
        "error": None
    }

    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname
        )
        conn.settimeout(3)
        conn.connect((hostname, port))

        cert = conn.getpeercert()

        # Certificat valide
        result["valid"] = True

        # Issuer
        issuer = cert.get("issuer")
        if issuer:
            result["issuer"] = " ".join(x[0][1] for x in issuer)

        # Expiration
        expires = cert.get("notAfter")
        if expires:
            expires_dt = datetime.strptime(expires, "%b %d %H:%M:%S %Y %Z")
            result["expires"] = expires_dt.strftime("%Y-%m-%d")
            result["days_left"] = (expires_dt - datetime.utcnow()).days

    except Exception as e:
        result["error"] = str(e)

    return result
