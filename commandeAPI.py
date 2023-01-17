import sys, getopt
import xml.etree.ElementTree as ET
import subprocess as sp
import os

oo = os.system("color")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

co = bcolors
def parserDemande():
    global co
    argv = sys.argv
    
    hashes = ['sha256']
    contacts = ['SMITH John', 'Joe TOTO']
    types = ['ssl','dev','wssl']

    if "-h" in argv or len(argv)<2 :
        
        
        str = """python test.py -h

    Mandatory arguments:

        -CSR CSR => path to CSR
        -H HASH => --list-hash to print the list of available hashes
        -C LASTNAME Firstname => --list-contact to print the list of known contacts
        -R S000000_000111 => REF
        -T TYPE => --list-type to print the list of type of certificate

    Optional arguments:

        --list-hash
        --list-contact
        --list-type
        -h => print this help menu

    Example:

    python API.py -CSR C:\\Users\\Public\\csr.csr -H sha256 -C "SMITH John" -T ssl -R S211007_123456
        """
        print(str)
        
    elif "--list-hash" in argv:
        str="List of hashes: sha256"
        print(str)

    elif "--list-contact" in argv:
        str="The contact list is:\n"+"\n".join(contacts)
        
        print(str)

    elif "--list-type" in argv:
        
        str="""ssl: Thawte SSL Standard
dev: Thawte Développeur
wssl: Thawte SSL Wildcard"""
        print(str)
        
        
    elif "-CSR" not in argv:
        print("-CSR missing")
    elif "-H" not in argv:
        print("-H missing")
    elif "-C" not in argv:
        print("-C missing")
    elif "-R" not in argv:
        print("-R missing")
    elif "-T" not in argv:
        print("-T missing")
    elif argv[ argv.index("-H")+1] not in hashes:
        print("Hashing function not valid")
    elif argv[ argv.index("-C")+1] not in contacts:
        print("Unknown contact")
    elif argv[ argv.index("-T")+1] not in types:
        print("Unknown type")
    elif len(argv[ argv.index("-R")+1])!=14:
        print("Wrong ref length (must be equals to 14)")
    elif len(argv)!=11:
        print("Unknown arguments")
        str = """python test.py -h

    Mandatory arguments:

        -CSR CSR => path to CSR
        -H HASH => --list-hash to print the list of available hashes
        -C LASTNAME Firstname => --list-contact to print the list of known contacts
        -R S000000_000111 => REF
        -T TYPE => --list-type to print the list of type of certificate

    Optional arguments:

        --list-hash
        --list-contact
        --list-type
        -h => print this help menu

    Example:

    python API.py -CSR C:\\Users\\Public\\csr.csr -H sha256 -C "SMITH John" -T ssl -R S210906_000123
        """
        print(str)
    else:
        try:
            #Vérifie si le fichier existe
            CSR = argv[argv.index('-CSR')+1]
            open(CSR,"r").read()
        except:
            print("The file doesn't exist")
            return 0
        Hash = argv[argv.index('-H')+1]
        Contact = argv[argv.index('-C')+1]
        Type = argv[argv.index('-T')+1]
        Ref = argv[argv.index('-R')+1]
        bool = creationDemande(CSR,Hash,Contact,Type,Ref)
        return bool

def creationDemande(CSRc,H,C,T,R):
    global co
    admins = open("listeContacts.txt","r").read()
    contactsAdmin = [e.split('\n') for e in admins.split('\n\n')] 
    filename = "XMLAPI.xml"
    xmlTree = ET.parse(filename)
    rootElement= xmlTree.getroot()

    for elm in rootElement.findall(".//member[name='produit']//string"): #Check product params
        codeElm = elm
        
    choixCert = ["Thawte SSL Standard", "Thawte SSL Wildcard", "Thawte Développeur"]

    code = T
    codeElm.text=code

    CSRs = []
    for elm in rootElement.findall(".//member[name='requete']//string"):
        CSRs.append(elm)

    
    chemin=CSRc
    CSR = open(chemin,"r").read()
    output = sp.getoutput('certutil '+chemin)

    
    CSRs[1].text=CSR


    
    for elm in rootElement.findall(".//member[name='divers']//string"):
        elm.text=R
    
    #Check if the CSR contains SANs 
    member = rootElement.findall(".//member[name='requete']//member[name='hashage']")
    lignes = output.split('\n')
    
    SANs = [e.split("DNS=")[1] for e in lignes if "DNS=" in e]
    
    CN = [e.split("CN=")[1] for e in lignes if "CN=" in e]
    CN=CN[0]
    print(co.WARNING+"[*]:"+co.ENDC+" CN={0}".format(CN))
    
    nbr=0
    DCV = "dcv@company.com"
    
    adminUser = [c for c in contactsAdmin if "nomAdm:"+C.split(" ")[0] in c][0]
    adminUser=adminUser[1:]
    for i,e in enumerate(rootElement.findall(".//member[name='contactAdm']//string")): 
        e.text = adminUser[i].split(":")[1]
    
    
    if SANs:
        if CN not in SANs:
            member = rootElement.findall(".//member[name='requete']//struct")
            MEMBER = ET.SubElement(member[0],"member")
            NAME= ET.SubElement(MEMBER,"name")
            NAME.text="domainePrincipal"
            VALUE=ET.SubElement(MEMBER,"value")
            STRING=ET.SubElement(VALUE,"string")
            STRING.text=CN
            nbr+=1
        else:
            member = rootElement.findall(".//member[name='requete']//struct")
            MEMBER = ET.SubElement(member[0],"member")
            NAME= ET.SubElement(MEMBER,"name")
            NAME.text="domainePrincipal"
            VALUE=ET.SubElement(MEMBER,"value")
            STRING=ET.SubElement(VALUE,"string")
            STRING.text=CN
            nbr+=1
            SANs.remove(CN)
        
        member = rootElement.findall(".//member[name='requete']//struct")
        MEMBER = ET.SubElement(member[0],"member")
        NAME= ET.SubElement(MEMBER,"name")
        NAME.text="domaines"
        VALUE=ET.SubElement(MEMBER,"value")
        STRING=ET.SubElement(VALUE,"string")
        STRING.text="\n".join(SANs)
        nbr+=len(SANs)
        
        MEMBERDCV = ET.SubElement(member[0],"member")
        NAMEDCV= ET.SubElement(MEMBERDCV,"name")
        NAMEDCV.text="adresseDVC"
        VALUEDCV=ET.SubElement(MEMBERDCV,"value")
        STRINGDCV=ET.SubElement(VALUEDCV,"string")
        STRINGDCV.text="\n".join([DCV for k in range(nbr)])
    print(co.WARNING+"[*]:"+co.ENDC+" SANs="+",".join(SANs))
    print(co.WARNING+"[*]:"+co.ENDC+" Hashage=SHA256")
    print(co.WARNING+"[*]:"+co.ENDC+" Organisation=GRTGAZ")
    print(co.WARNING+"[*]:"+co.ENDC+" Contact admin={0}".format(C))
    print(co.WARNING+"[*]:"+co.ENDC+" Produit={0}".format(T))
    print(co.WARNING+"[*]:"+co.ENDC+" Référence TBS={0}".format(R))

    TOUTOK = input("Valider commande ? [y/n]")
    if TOUTOK.lower() == "y":
        print(f"{co.OKGREEN}[*]: Commande validée{co.ENDC}")
        print("[*]: Commande en cours...")
        xmlTree.write("XMLAPI2.xml")
    else:
        print(f"{co.FAIL}[*]: Commande annulée{co.ENDC}")
    return TOUTOK.lower() == "y"
    
