# doForMe
Este script te ayuda a automatizar las tareas básicas de la parte de pentesting web.
Para que funcione, lo mejor es que lo utilices en tu distribución preferida de seguridad (Kali, Parrot, BackBox...) aunque lo puedes utilizar en Debian, Ubuntu, Centos, etc. (instalando las herramientas necesarias). Además, necesitas instalar Aha (https://github.com/theZiz/aha) y xsltproc (si no está en Kali o Parrot: apt-get install xsltproc)

Debes tener una carpeta llamada proyectos (en tu home, o si usas root en su directorio) y dentro, un fichero llamado ips.txt en el que meteras las IP o dominios que tienes que auditar (ej: 142.250.178.163 o google.es , sin las www. ni http).

El propio script se encarga de preguntar qué herramientas quieres lanzar y mira si tienes los directorios creados. También guarda los resultados de dichas herramientas con el nombre de cada una en su directorio correspondiente.

Este script fue creado en 2018 y aunque es funcional, está pendiente de revisión/actualización.
