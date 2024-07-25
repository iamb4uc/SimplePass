import utils.encryptpass
import pyperclip
import base64
from utils.dbconfig      import dbconfig
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash         import SHA512
from Crypto.Random       import get_random_bytes as grb
from rich                import print as printc
from rich.console        import Console
from rich.table          import Table

def computeMasterKey(mp,ds):
    return PBKDF2(mp.encode(), ds.encode(), 32, count=1000000, hmac_hash_module=SHA512)

def retrieveEntries(mp, ds, search, decryptPassword=False):
    db = dbconfig()
    cursor = db.cursor()

    query = ""
    if search:
        query = "SELECT * FROM sp.entries"
    else:
        query = "SELECT * FROM sp.entries WHERE "
        for i in search:
            query+=f"{i} = '{search[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    res = cursor.fetchall()
    db.close()

    if not res:
        printc("[yellow][-][/yellow] No results for the search")
        return

    if decryptPassword and len(res) == 1:
        mk = computeMasterKey(mp,ds)
        decrypted = utils.encryptpass.decrypt(key = mk, src = res[0][4], keyType = "bytes")
        printc("[green][+][/green] Password copied to clipboard")
        pyperclip.copy(decrypted.decode())
    elif decryptPassword and len(res)>1:
        printc("[yellow][-][/yellow] More than one result found for the search, therefore not extracting the password. Be more specific.")
    table = Table(title="Result")
    table.add_column("Site Name")
    table.add_column("URL",)
    table.add_column("Email")
    table.add_column("Username")
    table.add_column("Password")

    for row in res:
        table.add_row(row[0], row[1], row[2], row[3], "{hidden}" if not decryptPassword else row[4])
    Console().print(table)
