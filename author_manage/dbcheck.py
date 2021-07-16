from django.core.mail import send_mail, mail_admins

from author_manage.models import User
# from vfwheron.models import TblMeta


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


def deleteMetaMapEntry(uid, mid):
    """

    @param uid:
    @type uid:
    @param mid:
    @type mid:
    @return:
    @rtype:
    """


def addMetaMapEntry(uid, mid):
    """

    @param uid:
    @type uid:
    @param mid:
    @type mid:
    @return:
    @rtype:
    """
    # check if entry already exists
    # if not add entry



def checkUser(check_uid):
    """

    @param check_uid:
    @type check_uid:
    @return:
    @rtype:
    """

    # wenn neuer benutzer angelegt wird
    # prüfe ob uid bereits in tabelle
    # wenn uid vorhanden lösche alle einträge damit
    # danach kaskade in alle anderen uids
    # uids nach gültigkeit prüfen

    # TODO check if user exists?
    # TODO check if user is admin
    # TODO check if given uid is valid/unassigned
    # MetaMap.objects.filter(uid = check_uid).delete()




def checkMeta(check_mid):
    """

    @param check_mid:
    @type check_mid:
    @return:
    @rtype:
    """

    # wenn meta gelöscht wird
    # scan nach allen einträgen der mid und lösche diese

    # TODO check if meta exists
    # TODO check if given mid is valid/unassigned

    # MetaMap.objects.filter(mid = check_mid).delete()
    midConsistency()
    uidConsistency()




def uidConsistency():
    """
    Checks MetaMap Table for unvalid users and deletes respective entries
    If a Meta Ressource gets uncovered by this, it will be assigned to the first admin in DB
    @return:
    @rtype:
    """

    # cycle durch user id alle einträge
    # get list of table

    # for entry in MetaMap.objects.all():
    #     if not User.objects.filter(id = entry.uid).exists():
    #         # delete all entries with uid
    #         delList = MetaMap.objects.filter(uid = entry.uid).values_list('mid')
    #         MetaMap.objects.filter(uid = entry.uid).delete()
    #
    #         # get all mids that are no longer present in MetaMap
    #         diffList = list(set(delList) - set(MetaMap.objects.all().values_list('mid')))
    #         for deleted in diffList:
    #             # new table entry, owner is first admin
    #             admin = User.objects.get(is_superuser = True).first()
    #             MetaMap.objects.create(mid = deleted, uid = admin.id)
    #             # TODO notify admin
    #             send_mail('[v-for-water] A Ressource has been temp mapped', 'The Meta Ressource with id ' + deleted +
    #                       ' has been temporarily mapped to you because it is no longer present in MetaMap. Please take action and reassign it to another user or consider deletion.',
    #                       'system@v-for-water.de', admin.email,
    #                       fail_silently = False)
    #             # mail_admins(subject, message, fail_silently=False)


def midConsistency():
    """
    Cycles through the MetaMap table and checks for invalid meta ids. If a meta ID does not exists in TlbMeta, entry in MetaMap will be deleted.
    @return:
    @rtype:
    """

    # cycle durch alle meta id einträge
    # check ob mid valider eintrag ist
    #
    # for entry in MetaMap.objects.all():
    #     if not TblMeta.objects.filter(id = entry.mid).exists():
    #         MetaMap.objects.filter(mid = entry.mid).delete()
