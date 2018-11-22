#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:04:14 2018

@author: johnnyhsieh
"""

from boa.interop.System.Runtime import Log, GetTrigger, CheckWitness, Notify
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.System.Blockchain import GetHeight, GetHeader
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.builtins import substr,range


def Main(operation, args):

    nargs = len(args)
    if nargs == 0:
        print("No domain name supplied")
        return 0
    
    if operation == 'Owner':
        
        if nargs == 0:
            print("No domain name supplied")
            return 0
        
        domain = args[0]
        return Query(domain)

    if operation == 'Register':
        if nargs < 2:
            print("required arguments: [domain] [owner]")
            return 0
        
        domain = args[0]
        owner = args[1]
        return Register(domain, owner)

    if operation == 'Transfer':
        if nargs < 2:
            print("required arguments: [domain] [to_address]")
            return 0
        
        domain = args[0]
        to = args[1]
        return Transfer(domain, to)

    if operation == 'Release':
        if nargs == 0:
            print("No domain name supplied")
            return 0
        
        domain = args[0]
        return Release(domain)
    
    if operation == 'SetAddress':
        if nargs < 2:
            print("required arguments: [domain] [address]")
            return 0
        
        domain = args[0]
        address = args[1]
        return SetAddress(domain,address)
    
    if operation == 'addIPFS':
        if nargs < 2:
            print("required arguments: [domain] [IPFS_Hash]")
            return 0
        
        domain = args[0]
        IPFS = args[1]
        return AddIPFS(domain,IPFS)
    
    if operation == 'SetSubdomain':
        if nargs < 2:
            print("required arguments: [domain] [subdomain]")
            return 0
        
        domain = args[0]
        subdomain = args[1]
        return SetSubdomain(domain,subdomain)
    
    if operation == 'GetAddress':
        if nargs == 0:
            print("No domain name supplied")
            return 0
        
        domain = args[0]
        return GetAddress(domain)
    
    if operation == 'GetIPFS':
        if nargs == 0:
            print("No domain name supplied")
            return 0
        
        domain = args[0]
        return GetIPFS(domain)
    
    if operation == 'CheckStringVaild':
        if nargs ==0:
            print("Need at last one character")
            return 0
        
        Str = args[0]
        return CheckStringVaild(Str)   
            

    return False









def Query(domain):
    context = GetContext()
    owner = Get(context, domain)

    Notify('query', domain)
    if owner != None:
        return owner

    return False

def Register(domain, owner):
    context = GetContext()
    occupy = Get(context, domain)
    
    if CheckStringVaild(domain):
        Notify("Domain has incorrect char inside")
        return False
    
    if occupy != None:
        return False
    Put(context, domain, owner)
    Notify('Register', domain, owner)

    return True

def Transfer(domain, to):
    if to == None:
        return False

    context = GetContext()
    owner = Get(context, domain)
    if owner == None:
        return False
    if owner == to:
        return True

    is_owner = CheckWitness(owner)

    if not is_owner:
        return False

    Put(context, domain, to)
    Notify('Transfer', domain)

    return True

def Release(domain):
    context = GetContext()
    owner = Get(context, domain)
    is_owner = CheckWitness(owner)
    if not is_owner:
        return False

    Delete(context, domain)
    Notify('Delete', domain)

    return True

def SetAddress(domain,address):
    context = GetContext()
    owner = Get(context, domain)
    is_owner = CheckWitness(owner)
    if not is_owner:
        Notify("Owner argument is not the same as the sender")
        return False
    if not len(address) != 34:
        Notify("Invalid new owner address. Must be exactly 34 characters")
        return False
    
    Put(context,"{domain_name}.neo", address)
    Notify('SetAddress', address)
    return True
    
    

def GetAddress(domain_name):
    
    if Query(domain_name) == False:
       return False
    context = GetContext()
    address = Get(context, "{domain}.neo")
    return address

def AddIPFS(domain,IPFS):
    context = GetContext()
    owner = Get(context, domain)
    if not owner:
        Notify("Domain is not yet registered")
        return False
    
    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False
    
    Put(context,"{domain_name}.ipfs",IPFS)
    Notify('SetIPFS', IPFS)
    return True

    
def SetSubdomain(domain,subdomain):
    context = GetContext()
    owner = Get(context, domain)
    
    if CheckStringVaild(subdomain):
        Notify("Domain has incorrect char inside")
        return False
        
    
    if not owner:
        Notify("Domain is not yet registered")
        return False
    
    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot set subdomain")
        return False
    
    domain_name = concat(subdomain,".")
    domain = concat(domain_name,domain)
    
    Put(context,domain, owner)
    
    msg2 = [domain,"is owned by ",owner]
    Notify(msg2)
    return True
    
def GetIPFS(domain):
    if Query(domain) == False:
       return False
    context = GetContext()
    address = Get(context, "{domain_name}.ipfs")
    return address


def CheckStringVaild(Str):
    allow = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11
            ,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23
            ,"x":24,"y":25,"z":26,"-":27,"1":28,"2":29,"3":30,"4":31,"5":32,"6":33,"7":34,"8":39
            ,"9":40,"0":41}
    
    for i in range(0,len(Str)):
        s = (Str[i:i+1])
        try:
            result = allow[s]
        except:
            return True
    
    return False

    
