from vfwheron.models import TblMeta
from AuthorizationManagement.models import MetaMap, User



def metaMapCheck():
    """
    """
    
    # für gegebene uid
    # check table nach einträgen
    # wenn neuer user lösche alle einträge mit uid
    # prüfe zu uid zugeordnete mid auf gültigkeit
    # wenn genereller check prüfe jede uid auf gültigkeit
    
    # für gegebene mid
    # prüfe uid zu mid nach not null
    
    # generell mid
    # sortiere einträge nach mids
    # prüfe ob mids valide
    
    # generell uid
    # sortiere nach uids
    # prüfe nach gültigkeit der uid
    
    
    
    
    pass


def metaUserDel():
    """
    """
    
    # wenn benutzer gelöscht wird
    # scan tabelle nach uid und entferne einträge
        
    pass


def metaUserAdd():
    """
    """

    # wenn neuer benutzer angelegt wird
    # prüfe ob uid bereits in tabelle
    # wenn uid vorhanden lösche alle einträge damit
    # danach kaskade in alle anderen uids 
    # uids nach gültigkeit prüfen    
        
    pass

def metaDel():    
    """
    """
    
    # wenn meta gelöscht wird
    # scan nach allen einträgen der mid und lösche diese
       
    pass
    
def metaAdd():
    """
    """
    
    # wenn neuer meta eintrag
    # prüfe ob mid bereits in tabelle
    # lösche alle einträge mit mid
    # kaskade in alle anderen mids
    
    pass

def uidConsistency():
    """
    """
    
    # cycle durch user id alle einträge
    # get list of table

    metaList = MetaMap.objects().all()
    for entry in metaList:
       if not User.objects.filter(id=entry.uid).exists():    
           # delete all entries with uid
           MetaMap.objects.filter(uid=entry.uid).delete()
           # TODO: wie mit ressourcen verfahren, die nicht in MetaMap abgedeckt sind bzw rausfallen?
           # reload metaList
           metaList = MetaMap.objects().all()
    
    
    
    
    # if User.objects.filter(id=entry.uid).exists():
    #    continue
    # check ob uid ist valider benutzer
    # if not User.objects.filter(id=entry.uid).exists():
    #    
    
    
    pass    


def midConsistency():
    """
    """
    
    # cycle durch alle meta id einträge
    # check ob mid valider eintrag ist
    
    pass








