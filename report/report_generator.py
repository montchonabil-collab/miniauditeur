from datetime import datetime

def generate_report(port_results=None, http_results=None, tls_results=None, output="rapport.md"):
    """
    Génère un rapport Markdown contenant :
    - scan de ports
    - analyse HTTP
    - analyse TLS
    """

    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append(f"# Rapport d'audit de sécurité")
    lines.append(f"**Généré le :** {now}\n")

    # SECTION PORTS
    if port_results:
        lines.append("## 🔍 Scan de ports")
        lines.append("| Port | Statut |")
        lines.append("|------|--------|")
        for port, status in port_results:
            lines.append(f"| {port} | {status} |")
        lines.append("")

    # SECTION HTTP
    if http_results:
        lines.append("## 🌐 Analyse des en-têtes HTTP")
        for res in http_results:
            lines.append(f"### URL : {res['url']}")
            if res["error"]:
                lines.append(f"**Erreur :** {res['error']}\n")
                continue

            lines.append("| En-tête | Présence |")
            lines.append("|---------|----------|")
            for header, status in res["headers"].items():
                lines.append(f"| {header} | {status} |")

            lines.append(f"\n**Score de sécurité :** {res['score']} / {len(res['headers'])}\n")

    # SECTION TLS
    if tls_results:
        lines.append("## 🔐 Analyse TLS / Certificat HTTPS")
        for res in tls_results:
            lines.append(f"### Domaine : {res['hostname']}")

            if res["error"]:
                lines.append(f"**Erreur :** {res['error']}\n")
                continue

            lines.append(f"- Certificat valide : **{res['valid']}**")
            lines.append(f"- Issuer : **{res['issuer']}**")
            lines.append(f"- Expiration : **{res['expires']}**")
            lines.append(f"- Jours restants : **{res['days_left']}**\n")

    # Écriture du fichier
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output
