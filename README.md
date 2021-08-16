# doForMe
**Este script en bash te ayuda a automatizar las tareas básicas de la parte de pentesting web.**

Para que funcione, lo mejor es que lo utilices en tu distribución preferida de seguridad (Kali, Parrot, BackBox...) aunque lo puedes utilizar en Debian, Ubuntu, Centos, etc. (instalando las herramientas necesarias). Además, necesitas instalar Aha (https://github.com/theZiz/aha) y xsltproc (si no está en Kali o Parrot: apt-get install xsltproc), dirsearch (si no está instalado: https://github.com/maurosoria/dirsearch).

Debes tener una carpeta llamada proyectos (en tu home, o si usas root en su directorio) y dentro, un fichero llamado ips.txt en el que meteras las IP o dominios que tienes que auditar (ej: 142.250.178.163 o google.es , sin las 3w ni el http o https).

El propio script se encarga de preguntar qué herramientas quieres lanzar y mira si tienes los directorios creados. También guarda los resultados de dichas herramientas con el nombre de cada una en su directorio correspondiente.

Herramientas utilizadas:
* Nmap
* Nikto
* WPScan
* JoomScan
* Dirsearch

To do:
Revisar el script
Implementar/mejorar herramientas
Posible migración a python



Gracias a Rodri por enseñarme el camino de bash :)


-------------------------------------------------------------------------

Puedes invitarme a un café si quieres!
<a href="https://www.buymeacoffee.com/akil3s1979" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="27" width="104"></a>

You can buy me a coffe if you want!
<a href="https://www.buymeacoffee.com/akil3s1979" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="27" width="104"></a>
