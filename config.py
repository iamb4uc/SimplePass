import os
import sys
import string as s
import random as rand
import hashlib as hl
from getpass import getpass as gp
from utils.dbconfig import dbconfig
from rich import print as printc
from rich.console import Console

console = Console()

def chkConf():
    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'sp'"
    cursor.execute(query)
    res = cursor.fetchall()
    db.close()
    if len(res)!=0:
        return True
    return False


def genDevSecret(length=10):
    return ''.join(rand.choices(s.ascii_uppercase + s.digits, k = length))


def make():
    if chkConf():
        printc("[red][!] Already Configured!!! [/red]")
        printc("[green][!] Already Configured!!! [/green]")
        printc("[red][!] Already Configured!!! [/red]")
        return

    printc("[green][+] Creating new config [/green]")

    db = dbconfig()
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE sp")
        printc("[green][+] Database created [/green]")
    except Exception as err:
        printc("[red][!] An error occurred while creating database.[/red]")
        console.print_exception(show_locals=True)
        db.close()
        sys.exit(0)

    printc("[green][+][/green] Database 'sp' created")

    # Create tables
    # res = cursor.execute("CREATE TABLE sp.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)")
    # printc("[green][+][/green] Table 'secrets' created ")
    #
    # query = "CREATE TABLE sp.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    # res = cursor.execute(query)
    # printc("[green][+][/green] Table 'entries' created ")
    cursor.execute("CREATE TABLE sp.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)")
    printc("[green][+][/green] Table 'secrets' created")

    cursor.execute("CREATE TABLE sp.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)")
    printc("[green][+][/green] Table 'entries' created")


    # Set Master Password **IMPORTANT**
    printc("[green][+] A [bold]MASTER PASSWORD[/bold] is the only password you will need to remember in-order to access all your other passwords. Choosing a strong [bold]MASTER PASSWORD[/bold] is essential because all your other passwords will be [bold]encrypted[/bold] with a key that is derived from your [bold]MASTER PASSWORD[/bold]. Therefore, please choose a strong one that has upper and lower case characters, numbers and also special characters. Remember your [bold]MASTER PASSWORD[/bold] because it won't be stored anywhere by this program, and you also cannot change it once chosen. [/green]\n")
    while True:
        mp = gp("Choose a MASTER PASSWORD: ")
        if mp == gp("Re-type: ") and mp:
            break
        printc("[yellow][-] Please try again.[/yellow]")

    # Hash mp
    mpHash = hl.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")


    # Generate a device secret
    ds = genDevSecret()
    printc("[green][+][/green] Device Secret generated")

    # Add them to db
    # query = "INSERT INTO sp.secrets (masterkey_hash, device_secret) values (%s, %s)"
    # val = (mpHash, ds)
    # cursor.execute(query, val)
    # db.commit()
    # printc("[green][+][/green] Added to the database")
    # printc("[green][+] Configuration done![/green]")
    # db.close()
    cursor.execute("INSERT INTO sp.secrets (masterkey_hash, device_secret) VALUES (%s, %s)", (mpHash, ds))
    db.commit()
    printc("[green][+][/green] Added to the database")

    db.close()
    printc("[green][+] Configuration done![/green]")


def delete():
    printc("[red][-] Deleting a config clears the device secret and all your entries from the database. This means you will loose access to all your passwords that you have added into the password manager until now. Only do this if you truly want to 'destroy' all your entries. This action cannot be undone. [/red]")
    if input("Are you sure you want to continue? (y/N): ").strip().lower() != "y":
        sys.exit(0)

    printc("[green][-][/green] Deleting config")


    if not chkConf():
        printc("[yellow][-][/yellow] No configuration exists to delete!")
        return

    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("DROP DATABASE sp")
    db.commit()
    db.close()
    printc("[green][+] Config deleted![/green]")

def remake():
    printc("[green][+][/green] Remaking config")
    delete()
    make()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python config.py <make/delete/remake>")
        sys.exit(0)

    opt = sys.argv[1].lower()

    if opt == "make":
        make()
    elif opt == "delete":
        delete()
    elif opt == "remake":
        remake()
    else:
        print("Usage: python config.py <make/delete/remake>")
