#!/usr/bin/env python3
"""
doForMe.py
Wrapper para lanzar nmap, testssl/sslscan, whatweb, wpscan, nikto, joomscan, dirsearch sobre una lista de objetivos.
Diseñado para ser más robusto y configurable que el bash original.
"""

import argparse
import subprocess
import shutil
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

DEFAULT_PROJECTS_DIR = Path.home() / "proyectos"

TOOLS = {
    "nmap": "nmap",
    "xsltproc": "xsltproc",
    "testssl": "testssl.sh",     # asumimos disponible en PATH o especificar ruta
    "sslscan": "sslscan",
    "dnsrecon": "dnsrecon",
    "whatweb": "whatweb",
    "wpscan": "wpscan",
    "nikto": "nikto",
    "joomscan": "joomscan",
    "dirsearch": "dirsearch.py", # si es un script, puede requerir ruta
    "aha": "aha"
}

def check_tools(required):
    missing = [t for t in required if shutil.which(TOOLS.get(t, t)) is None]
    if missing:
        print("Faltan herramientas necesarias:", ", ".join(missing))
        return False
    return True

def run_cmd_to_file(cmd_list, out_path, timeout=None):
    """Ejecuta comando (lista) y guarda stdout/stderr en out_path (Path). Devuelve True si rc==0."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fh:
        try:
            proc = subprocess.run(cmd_list, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout)
            return proc.returncode == 0
        except subprocess.TimeoutExpired:
            fh.write(b"\n[timeout]\n")
            return False
        except Exception as e:
            fh.write(f"\n[error] {e}\n".encode())
            return False

def run_nmap(project_dir, ip_file, timeout=3600):
    xml_out = project_dir / "salidaNmap.xml"
    html_out = project_dir / "salidaNmap.html"
    if xml_out.exists():
        print("Nmap ya estaba hecho:", xml_out)
        return xml_out, html_out
    cmd = ["nmap", "-iL", str(ip_file), "-sV", "-Pn", "-oX", str(xml_out)]
    print("Ejecutando:", " ".join(cmd))
    ok = run_cmd_to_file(cmd, project_dir / "nmap_full.log", timeout=timeout)
    if not ok:
        print("Nmap fallo, revisar", project_dir / "nmap_full.log")
    # intentar convertir a HTML si xsltproc existe
    if xml_out.exists() and shutil.which("xsltproc"):
        try:
            subprocess.run(["xsltproc", str(xml_out), "-o", str(html_out)], check=True, timeout=30)
        except Exception:
            pass
    return xml_out, html_out

def per_host_tasks(host, project_dir, tools_enabled):
    host_safe = host.replace(":", "_").replace("/", "_")
    results = {}
    # testssl -> testssl.sh produces html via aha; if not available you can save raw
    if "testssl" in tools_enabled and shutil.which("testssl.sh"):
        out_html = project_dir / f"salidaTestSSL-{host_safe}.html"
        if not out_html.exists():
            cmd = ["bash", "-c", f"testssl.sh {host} | aha"]
            run_cmd_to_file(cmd, out_html, timeout=120)
    if "sslscan" in tools_enabled and shutil.which("sslscan"):
        out_html = project_dir / f"salidaSSL-{host_safe}.html"
        if not out_html.exists():
            cmd = ["bash", "-c", f"sslscan {host}:443 | aha"]
            run_cmd_to_file(cmd, out_html, timeout=60)
    if "dnsrecon" in tools_enabled and shutil.which("dnsrecon"):
        out_html = project_dir / f"salidaDNSrecon-{host_safe}.html"
        if not out_html.exists():
            cmd = ["bash", "-c", f"dnsrecon -d {host} -D /usr/share/wordlists/dnsmap.txt -t std | aha"]
            run_cmd_to_file(cmd, out_html, timeout=120)
    if "whatweb" in tools_enabled and shutil.which("whatweb"):
        out_html = project_dir / f"salidaWhatWeb-{host_safe}.html"
        if not out_html.exists():
            cmd = ["whatweb", "-a", "3", host]
            run_cmd_to_file(cmd, out_html, timeout=30)
    if "wpscan" in tools_enabled and shutil.which("wpscan"):
        out_txt = project_dir / f"salidaWPscan-{host_safe}.txt"
        out_htm = project_dir / f"salidaWPscan-{host_safe}.htm"
        if not out_txt.exists():
            # actualizar wpscan antes de la primera ejecución global en caller
            cmd = ["wpscan", "--url", host]
            run_cmd_to_file(cmd, out_txt, timeout=120)
            # intentar convertir a html con aha si disponible
            if shutil.which("aha"):
                run_cmd_to_file(["bash", "-c", f"cat {out_txt} | aha"], out_htm, timeout=10)
    if "nikto" in tools_enabled and shutil.which("nikto"):
        out_html = project_dir / f"salidaNikto-{host_safe}.html"
        if not out_html.exists():
            cmd = ["nikto", "-host", host, "-port", "80,443", "-output", str(out_html)]
            run_cmd_to_file(cmd, out_html, timeout=120)
    if "joomscan" in tools_enabled and shutil.which("joomscan"):
        out_html = project_dir / f"salidaJoomScan-{host_safe}.html"
        if not out_html.exists():
            cmd = ["perl", "/usr/bin/joomscan", "-u", host, "-ec"]
            run_cmd_to_file(cmd, out_html, timeout=120)
    if "dirsearch" in tools_enabled and shutil.which("dirsearch.py"):
        out_base = project_dir / f"salidaDirSearch-{host_safe}"
        out_html = project_dir / f"salidaDirSearch-{host_safe}.htm"
        if not out_html.exists():
            cmd = ["python3", "/root/tools/dirsearch/dirsearch.py", "-u", host,
                   "-e", "php,asp,aspx,war,js,jsp,do", "-r",
                   "-w", "/usr/share/wfuzz/wordlist/general/big.txt", "--plain-text-report", str(out_base)]
            run_cmd_to_file(cmd, out_base.with_suffix(".log"), timeout=300)
            if shutil.which("aha") and out_base.exists():
                run_cmd_to_file(["bash", "-c", f"cat {out_base} | aha"], out_html, timeout=10)
    return results

def main():
    parser = argparse.ArgumentParser(description="Recon Runner (nmap + web tools) in Python")
    parser.add_argument("-p", "--project", required=True, help="Nombre del proyecto")
    parser.add_argument("-i", "--ip-file", required=True, help="Fichero con IPs/dominios, una por linea")
    parser.add_argument("--projects-dir", default=str(DEFAULT_PROJECTS_DIR), help="Directorio base para proyectos")
    parser.add_argument("--nmap", action="store_true", help="Ejecutar nmap")
    parser.add_argument("--wpscan", action="store_true", help="Ejecutar WPScan")
    parser.add_argument("--nikto", action="store_true", help="Ejecutar Nikto")
    parser.add_argument("--joomscan", action="store_true", help="Ejecutar JoomScan")
    parser.add_argument("--dirsearch", action="store_true", help="Ejecutar Dirsearch")
    parser.add_argument("--workers", type=int, default=8, help="Hilos concurrentes para hosts")
    parser.add_argument("--timeout", type=int, default=3600, help="Timeout para nmap (segundos)")
    parser.add_argument("--force-wpscan-update", action="store_true", help="Forzar update de wpscan antes de correr")
    args = parser.parse_args()

    project_dir = Path(args.projects_dir) / args.project
    project_dir.mkdir(parents=True, exist_ok=True)
    ip_file = Path(args.ip_file)
    if not ip_file.exists():
        print("Fichero de ips no encontrado:", ip_file)
        sys.exit(1)

    # Verificar herramientas requeridas según flags
    required_tools = []
    if args.nmap:
        required_tools += ["nmap", "xsltproc"]
    if args.wpscan:
        required_tools += ["wpscan", "aha"]
    if args.nikto:
        required_tools += ["nikto"]
    if args.joomscan:
        required_tools += ["joomscan"]
    if args.dirsearch:
        required_tools += ["dirsearch.py", "aha"]
    # Para testssl/sslscan/whatweb/dnsrecon (si usas nmap detect 443 abierto)
    required_tools += ["sslscan", "testssl", "whatweb", "dnsrecon"]

    # Eliminar duplicados
    required_tools = list(dict.fromkeys(required_tools))

    if not check_tools(required_tools):
        print("Instala las herramientas necesarias o ajusta PATH.")
        # No abortamos del todo; podrías cambiar a abortar -> sys.exit(1)
        # sys.exit(1)

    start = datetime.now()
    print(f"Start: {start.isoformat()}")

    # Si se pide wpscan update global
    if args.wpscan and args.force_wpscan_update and shutil.which("wpscan"):
        try:
            subprocess.run(["wpscan", "--update"], check=True, timeout=120)
        except Exception as e:
            print("Warning updating wpscan:", e)

    # Nmap (global)
    if args.nmap:
        xml_out, html_out = run_nmap(project_dir, ip_file, timeout=args.timeout)
        # Si quieres parsear xml para ver puertos 443 abiertos, aquí puedes hacerlo con xml.etree

    # Leer objetivos y lanzar tareas por host en paralelo
    tools_enabled = set()
    if args.wpscan: tools_enabled.add("wpscan")
    if args.nikto: tools_enabled.add("nikto")
    if args.joomscan: tools_enabled.add("joomscan")
    if args.dirsearch: tools_enabled.add("dirsearch")
    # añade testssl/whatweb/... si quieres ejecutar por defecto
    tools_enabled.update(["testssl", "sslscan", "dnsrecon", "whatweb"])

    hosts = []
    with ip_file.open("r", encoding="utf-8") as fh:
        for line in fh:
            t = line.strip()
            if t and not t.startswith("#"):
                hosts.append(t)

    if hosts:
        print(f"Lanzando tareas para {len(hosts)} hosts con {args.workers} workers...")
        with ThreadPoolExecutor(max_workers=args.workers) as exe:
            futures = {exe.submit(per_host_tasks, h, project_dir, tools_enabled): h for h in hosts}
            for fut in as_completed(futures):
                host = futures[fut]
                try:
                    fut.result()
                    print(f"[ok] {host}")
                except Exception as e:
                    print(f"[error] {host} -> {e}")

    end = datetime.now()
    print(f"Finish: {end.isoformat()} (elapsed {end - start})")

if __name__ == "__main__":
    main()
