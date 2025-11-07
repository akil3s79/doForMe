# doForMe
**Este script en bash te ayuda a automatizar las tareas básicas de la parte de pentesting web.**

Actualización 2025
Código mejorado y migrado a python (por fin).

Gracias a Rodri por enseñarme el camino de bash :)

doForMe.py es un wrapper de reconocimiento desarrollado en Python que automatiza la ejecución ordenada y paralela de varias herramientas de reconocimiento web y de red sobre una lista de objetivos (IPs o dominios). Su objetivo es replicar y mejorar la funcionalidad del script Bash original, proporcionando una interfaz configurable, ejecución más robusta y paralela, y un manejo de errores/control de tiempos adecuado para uso en laboratorios de pentesting.

Resumiendo:

Crea la estructura de proyecto donde guardar salidas.
Opcionalmente ejecuta nmap de forma global sobre la lista de objetivos y genera salida XML/HTML.
Para cada host objetivo ejecuta (según flags) una serie de herramientas web y de análisis TLS: testssl.sh, sslscan, dnsrecon, whatweb, wpscan, nikto, joomscan, dirsearch, etc.
Ejecuta tareas por host en paralelo (ThreadPoolExecutor), registrando salidas en ficheros por host y evitando sobrescribir resultados ya existentes salvo que se indique.
Maneja timeouts, captura salidas y errores, y deja logs/parciales en caso de fallo.

Herramientas que utiliza
El script invoca (según configuración) las siguientes herramientas externas:
nmap (con salida XML)
xsltproc (para convertir XML a HTML)
testssl.sh
sslscan
dnsrecon
whatweb
wpscan
nikto
joomscan
dirsearch (python)
aha (ANSI to HTML) — para convertir salidas en HTML legible

Nota: doForMe.py no incluye estas herramientas, las ejecuta como dependencias instaladas en el sistema. Comprueba PATH o especifica rutas si las tienes en ubicaciones no estándar.

Características principales

Interfaz por línea de comandos vía argparse (nombre del proyecto, fichero de IPs, selección de herramientas, número de workers, timeouts, etc.).
Comprobación previa de la disponibilidad de herramientas necesarias (shutil.which).
Creación automática de la estructura de proyecto y ficheros de salida.
Ejecución paralela por host (controlable con --workers).
Timeout por herramienta para evitar procesos colgados.
Conversión de salidas a HTML (cuando aha/xsltproc están disponibles).
Evita re-ejecutar trabajos ya completados (comprueba existencia de ficheros de salida).
Manejo de excepciones y reporting básico por host.

Uso básico
python3 doForMe.py -p mi_proyecto -i ips.txt --nmap --wpscan --nikto --workers 8

Flags importantes:

-p, --project : nombre del proyecto (directorio de salida)
-i, --ip-file : fichero con IPs/domains (una por línea)
--nmap : ejecutar nmap global (genera XML)
--wpscan : ejecutar WPScan por host
--nikto : ejecutar Nikto por host
--joomscan : ejecutar JoomScan por host
--dirsearch : ejecutar Dirsearch por host
--workers : número de hilos para paralelizar (por defecto 8)
--timeout : timeout general para nmap (segundos)
--force-wpscan-update : forzar wpscan --update antes de las ejecuciones

Recomendaciones de uso:

Ejecutar en un entorno de laboratorio o con autorización explícita.
Ajustar --workers según recursos y objetivo (no saturar la red o el objetivo).
Mantener las herramientas actualizadas (nmap, wpscan, testssl, etc.).
Comprobar permisos y rutas cuando algunas herramientas sean scripts fuera del PATH.

-------------------------------------------------------------------------

Puedes invitarme a un café si quieres!
<a href="https://www.buymeacoffee.com/akil3s1979" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="27" width="104"></a>

You can buy me a coffe if you want!
<a href="https://www.buymeacoffee.com/akil3s1979" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="27" width="104"></a>
