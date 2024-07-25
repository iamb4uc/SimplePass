#!/usr/bin/env python
import argparse
import hashlib
import pyperclip
import utils.add
import utils.retrieve
import utils.generate
from utils.dbconfig import dbconfig
from random import choice
from getpass import getpass
from rich import print as printc


def parseArgs():
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument(
        "option",
        choices=["a", "add", "e", "extract", "g", "generate"],
        help="(a)dd / (e)xtract / (g)enerate",
    )
    parser.add_argument("-s", "--name", help="Site Name")
    parser.add_argument("-u", "--url", help="Site URL")
    parser.add_argument("-e", "--email", help="Email")
    parser.add_argument("-l", "--login", help="Username")
    parser.add_argument("--length", type=int, help="Length of the password to generate")
    parser.add_argument(
        "-c", "--copy", action="store_true", help="Copy password to clipboard"
    )
    return parser.parse_args()


def chkMP():
    mp = getpass("MASTER PASSWORD: ")
    mpHash = hashlib.sha256(mp.encode()).hexdigest()

    with dbconfig() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sp.secrets")
        res = cursor.fetchone()

    if mpHash != res[0]:
        printc("[red][!] WRONG! [/red]")
        return None

    return mp, res[1]


def main():
    args = parseArgs()
    if args.option in ["add", "a"]:
        missing = [arg for arg in ["name", "url", "login"] if not getattr(args, arg)]
        if missing:
            for arg in missing:
                printc(f"[red][!][/red] {arg.capitalize()} (-{arg[0]}) required")
            return

        args.email = args.email or ""
        res = chkMP()
        if res:
            utils.add.addEntry(*res, args.name, args.url, args.email, args.login)

    elif args.option in ["extract", "e"]:
        res = chkMP()
        if res:
            search = {
                k: v
                for k, v in vars(args).items()
                if k in ["name", "url", "email", "login"] and v
            }
            utils.retrieve.retrieveEntries(*res, search, decryptPassword=args.copy)

    elif args.option in ["generate", "g"]:
        if args.length is None:
            printc(
                "[red][+][/red] Specify length of the password to generate (--length)"
            )
            return
        password = utils.generate.generatePassword(args.length)
        pyperclip.copy(password)
        printc("[green][+][/green] Password generated and copied to clipboard")


if __name__ == "__main__":
    main()

