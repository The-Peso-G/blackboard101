# MULTISIGS - PART ONE - GENERATING A MULTISIG ADDRESS & REDEEM SCRIPT
# wobine code for world bitcoin network blackboard 101
# Educational Purposes only
# Python 2.7.6 and relies on bitcoind & bitcoinrpc & wobine's github connection file
# We had to change the bitcoinrpc 'connection.py' file to add multisig support
# https://github.com/wobine/blackboard101/blob/master/wbn_multisigs_pt1_create-address.py


from bitcoinrpc.authproxy import AuthServiceProxy

bitcoin = AuthServiceProxy("http://test:123456@127.0.0.1:8332") #creates an object called 'bitcoin' that allows for bitcoind calls

pubkey = dict()


print "请输入公钥，公钥可以由命令[validate address]的输出pubKey字段得到"
pubkey[0] = str(raw_input("请输入管理者1的公钥："))
pubkey[1] = str(raw_input("请输入管理者2的公钥："))
pubkey[2] = str(raw_input("请输入管理者3的公钥："))
n = int(raw_input("请输入几个私钥可以解锁："))
threeaddy = [pubkey[0],pubkey[1],pubkey[2]]
print "多重签名地址是："
multisigaddy = bitcoin.addmultisigaddress(n,threeaddy)
multiaddyandredeem = (bitcoin.createmultisig(n,threeaddy))
print len(multisigaddy),"chars - ", multisigaddy
print
print "redeemScript -", len(multiaddyandredeem["redeemScript"]), "chars -",multiaddyandredeem["redeemScript"]
print
print "现在可以把上面的输出都存起来，方便以后花费时构建输出单"




