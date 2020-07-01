# MULTISIGS - PART ONE - GENERATING A MULTISIG ADDRESS & REDEEM SCRIPT
# wobine code for world bitcoin network blackboard 101
# Educational Purposes only
# Python 2.7.6 and relies on bitcoind & bitcoinrpc & wobine's github connection file
# We had to change the bitcoinrpc 'connection.py' file to add multisig support
# https://github.com/wobine/blackboard101/blob/master/wbn_multisigs_pt1_create-address.py
# Modify:
#      ask private key from user. so we could use the code in real situation

from bitcoinrpc.authproxy import AuthServiceProxy

bitcoin = AuthServiceProxy("http://test:123456@127.0.0.1:8332") #creates an object called 'bitcoin' that allows for bitcoind calls

pubkey = dict()


print "Please input your pubKey, which is the oubput of command [validate address]"
pubkey[0] = str(raw_input("Please input the pubkey owned by Partner 1£º"))
pubkey[1] = str(raw_input("Please input the pubkey owned by Partner 2£º"))
pubkey[2] = str(raw_input("Please input the pubkey owned by Partner 3£º"))
n = int(raw_input("Please input the number which can sign the address£º"))
threeaddy = [pubkey[0],pubkey[1],pubkey[2]]
print "The multi-sig address is £º"
multisigaddy = bitcoin.addmultisigaddress(n,threeaddy)
multiaddyandredeem = (bitcoin.createmultisig(n,threeaddy))
print len(multisigaddy),"chars - ", multisigaddy
print
print "redeemScript -", len(multiaddyandredeem["redeemScript"]), "chars -",multiaddyandredeem["redeemScript"]
print
print "Now you can copy all this ouput text and save it so you'll be ready for spend it"




