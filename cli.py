import argparse
from scanner.port_scanner import scan_range
from entete.header_analyzer import analyze_headers
from bonus.tls_analyzer import analyze_tls
from report.report_generator import generate_report

def main():
    parser = argparse.ArgumentParser(description="Mini auditeur de sécurité")

    parser.add_argument("--target", help="Cible à scanner")
    parser.add_argument("--ports", help="Plage de ports ex: 1-1024")
    parser.add_argument("--urls", nargs="*", help="Liste d'URL à analyser")
    parser.add_argument("--tls", nargs="*", help="Analyse TLS des domaines")
    parser.add_argument("--report", action="store_true", help="Générer un rapport Markdown")

    args = parser.parse_args()

    port_results = None
    http_results = []
    tls_results = []

    # MODULE 1 : Scan de ports
    if args.target and args.ports:
        start, end = map(int, args.ports.split("-"))
        port_results = scan_range(args.target, start, end)
        for port, status in port_results:
            print(f"{port}: {status}")

    # MODULE 2 : Analyse HTTP
    if args.urls:
        for url in args.urls:
            res = analyze_headers(url)
            http_results.append(res)
            print(f"\nURL : {res['url']}")
            if res["error"]:
                print(f"Erreur : {res['error']}")
                continue
            for header, status in res["headers"].items():
                print(f"  {header}: {status}")
            print(f"Score : {res['score']} / {len(res['headers'])}")

    # BONUS TLS
    if args.tls:
        for domain in args.tls:
            res = analyze_tls(domain)
            tls_results.append(res)
            print(f"\nDomaine : {domain}")
            if res["error"]:
                print(f"Erreur : {res['error']}")
                continue
            print(f"Certificat valide : {res['valid']}")
            print(f"Issuer : {res['issuer']}")
            print(f"Expiration : {res['expires']}")
            print(f"Jours restants : {res['days_left']}")

    # MODULE 3 : Rapport
    if args.report:
        output = generate_report(
            port_results=port_results,
            http_results=http_results,
            tls_results=tls_results
        )
        print(f"\n📄 Rapport généré : {output}")

        # Affichage du rapport dans le terminal
        print("\n===== CONTENU DU RAPPORT =====\n")
        with open(output, "r", encoding="utf-8") as f:
            print(f.read())

if __name__ == "__main__":
    main()
