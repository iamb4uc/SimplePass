import utils.encryptpass
import base64
from utils.dbconfig      import dbconfig
from getpass             import getpass as gp
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash         import SHA512
from Crypto.Random       import get_random_bytes
from rich                import print as printc
from rich.console        import Console

def computeMK(mp, ds):
    return PBKDF2(mp.encode(), ds.encode(), 32, count=1000000, hmac_hash_module=SHA512)


def checkEntry(sitename, siteurl, email, username):
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM sp.entries WHERE sitename = %s AND siteurl = %s AND email = %s AND username = %s", (sitename, siteurl, email, username))
    exists = cursor.fetchone() is not None
    db.close()
    return exists


def addEntry(mp, ds, sitename, siteurl, email, username):
    if checkEntry(sitename, siteurl, email, username):
        printc("[yellow][-][/yellow] Entry with these details already exists")
        return

    password = gp("Password: ")
    mk = computeMK(mp,ds)
    encrypted = utils.encryptpass.encrypt(key=mk, src=password, keyType="bytes")

    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("INSERT INTO sp.entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)", (sitename,siteurl,email,username,encrypted))
    db.commit()
    db.close()
    printc("[green][+][/green] Added entry ")
