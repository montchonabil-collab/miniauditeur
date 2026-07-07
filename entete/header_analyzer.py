import requests

# Liste des en-têtes de sécurité à vérifier
SECURITY_HEADERS = {
    "Strict-Transport-Security": "HSTS",
    "Content-Security-Policy": "CSP",
    "X-Frame-Options": "XFO",
    "X-Content-Type-Options": "XCTO",
    "Referrer-Policy": "RP",
    "Permissions-Policy": "PP"
}

def analyze_headers(url, timeout=3):
    """
    Analyse les en-têtes HTTP de sécurité d'une URL.
    Retourne un dictionnaire : {header: present/absent}
    + un score de sécurité.
    """

    result = {
        "url": url,
        "headers": {},
        "score": 0,
        "error": None
    }

    try:
        response = requests.get(url, timeout=timeout)
        headers = response.headers

        score = 0
        header_results = {}

        for header in SECURITY_HEADERS:
            if header in headers:
                header_results[header] = "present"
                score += 1
            else:
                header_results[header] = "absent"

        result["headers"] = header_results
        result["score"] = score

    except requests.exceptions.MissingSchema:
        result["error"] = "URL invalide (schéma manquant : http:// ou https://)"
    except requests.exceptions.ConnectionError:
        result["error"] = "Impossible de se connecter à la cible"
    except requests.exceptions.Timeout:
        result["error"] = "Timeout réseau"
    except Exception as e:
        result["error"] = f"Erreur inconnue : {e}"

    return result
