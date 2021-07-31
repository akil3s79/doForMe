#!/bin/bash
clear
echo -e ""
echo -e ""
echo -e "\e[0;31m *************************************************** \e[0m"
echo -e "\e[0;31m No olvides actualizar WPScan antes de empezar \e[0m"
echo -e '\e[0;31m *************************************************** \e[0m' 
echo ""         
echo ""
read -p $'\e[0;31m Introduce el nombre del proyecto: \e[0m' proyecto
read -p $'\e[0;31m ¿Tienes fichero con las IPs o dominios? (s/n): \e[0m' confirma
read -p $'\e[0;31m ¿Quieres tirar WPScan? (s/n): \e[0m' valida
read -p $'\e[0;31m ¿Quieres tirar nikto? (s/n): \e[0m' nik
read -p $'\e[0;31m ¿Quieres tirar joomscan? (s/n): \e[0m' joomla
read -p $'\e[0;31m ¿Quieres tirar dirsearch? (s/n): \e[0m' dirsearch

DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M"`

echo ""
echo ""
echo -e "\e[0;31m Start time $DIA $HORA \e[0m"

if [ ! -d "/root/proyectos/$proyecto" ] ; then
    mkdir /root/proyectos/$proyecto
else
    echo -e "\e[0;31m El directorio ya existía \e[0m"
fi

if [ $confirma == "s" ]; then
    if [ ! -f "/root/proyectos/$proyecto/salidaNmap.xml" ] ;then
                #nmap --host-timeout 40s -iL /root/proyectos/ips.txt -sV -Pn -oX /root/proyectos/$proyecto/salidaNmap.xml
                nmap -iL /root/proyectos/ips.txt -sV -Pn -oX /root/proyectos/$proyecto/salidaNmap.xml
	              xsltproc /root/proyectos/$proyecto/salidaNmap.xml -o /root/proyectos/$proyecto/salidaNmap.html
        aux1=$(cat /root/proyectos/$proyecto/salidaNmap.xml | grep 443 | grep "state=\"open\"" | cut -d"\"" -f4 | uniq)
        aux2=$(cat /root/proyectos/$proyecto/salidaNmap.xml | grep 443 | grep "state=\"open\"" | cut -d"\"" -f6 | uniq)
        if [ $aux1="443" ] && [ $aux2="open" ];then
                for i in $(cat /root/proyectos/ips.txt); do
                    if [ ! -f "/root/proyectos/$proyecto/salidaTestSSL-$i.txt" ] ;then
                        bash /opt/testssl.sh/testssl.sh $i | aha > /root/proyectos/$proyecto/salidaTestSSL-$i.html ; sslscan $i:443 |aha > /root/proyectos/$proyecto/salidaSSL-$i.html ; dnsrecon -d $i -D /usr/share/wordlists/dnsmap.txt -t std |aha > /root/proyectos/$proyecto/salidaDNSrecon-$i.html ; whatweb -a 3 $i |aha > /root/proyectos/$proyecto/salidaWhatWeb-$i.html
                    else
                        echo ""
                        echo -e "\e[0;31m TestSSL ya estaba hecho \e[0m"
                        echo ""
                    fi
                           done
            fi

        echo ""
        echo -e "\e[0;31m Terminado \e[0m"
        echo ""
    else
    echo ""
    echo -e "\e[0;31m Nmap ya estaba hecho \e[0m"
    echo ""

    fi

if [ $valida == "s" ]; then
        for u in $(cat /root/proyectos/ips.txt); do
        if [ ! -f "/root/proyectos/$proyecto/salidaWPscan-$u.txt" ]; then
            ruby /usr/bin/wpscan --update ; ruby /usr/bin/wpscan --url $u > /root/proyectos/$proyecto/salidaWPscan-$u.txt
            cat /root/proyectos/$proyecto/salidaWPscan-$u.txt |aha > /root/proyectos/$proyecto/salidaWPscan-$u.htm
        else
        echo " "
        echo -e "\e[0;31m WPScan ya estaba hecho \e[0m"
        echo " "
        fi
    done
fi
if [ $nik == "s" ]; then
        for v in $(cat /root/proyectos/ips.txt); do
        if [ ! -f "/root/proyectos/$proyecto/salidaNikto-$v.html" ]; then
                nikto -host $v -port 80,443 -output /root/proyectos/$proyecto/salidaNikto-$v.html
        else
        echo " "
        echo -e "\e[0;31m Nikto ya estaba hecho \e[0m"
        echo " "
        fi
    done
fi
# Lo de joomla
if [ $joomla == "s" ]; then
        for w in $(cat /root/proyectos/ips.txt); do
        if [ ! -f "/root/proyectos/$proyecto/salidaJoomScan-$w.html" ]; then
                perl /usr/bin/joomscan -u $w -ec 
        else
        echo " "
        echo -e "\e[0;31m JoomScan ya estaba hecho \e[0m"
        echo " "
        fi
    done
fi
# La parte dirsearch
if [ $dirsearch == "s" ]; then
        for x in $(cat /root/proyectos/ips.txt); do
        if [ ! -f "/root/proyectos/$proyecto/salidaDirSearch-$x.htm" ]; then
              python3 /root/tools/dirsearch/dirsearch.py -u $x -e php,asp,aspx,war,js,jsp,do -r -w /usr/share/wfuzz/wordlist/general/big.txt --plain-text-report=/root/proyectos/$proyecto/salidaDirSearch-$x
                cat /root/proyectos/$proyecto/salidaDirSearch-$x |aha > /root/proyectos/$proyecto/salidaDirSearch-$x.htm
        else
        echo " "
        echo -e "\e[0;31m DirSearch ya estaba hecho \e[0m"
        echo " "
        fi
    done
fi
fi

echo ""
echo ""
echo -e "\e[0;31m Job finished \e[0m"

DIA2=`date +"%d/%m/%Y"`
HORA2=`date +"%H:%M"`

echo ""
echo ""
echo -e "\e[0;31m Finish time $DIA2 $HORA2 \e[0m"
