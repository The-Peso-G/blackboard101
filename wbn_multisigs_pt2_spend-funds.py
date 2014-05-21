# MULTISIGS - PART TWO - SPENDING FROM A 2-of-3 MULTISIG ADDRESS
# This simple wallet works with bitcoind and will only work with 2-of-3 multisigs
# wobine code for world bitcoin network blackboard 101
# Educational Purposes only
# Python 2.7.6 and relies on bitcoind & bitcoinrpc & wobine's github connection file
# We had to change the bitcoinrpc 'connection.py' file to add multisig support
# you'll need to download our 'connection.py' file from Github & stuff it in your bitcoinrpc folder

#import sys;
#sys.path.append("D:\github\python-bitcoinrpc\bitcoinrpc")

from bitcoinrpc.authproxy import AuthServiceProxy



bitcoin = AuthServiceProxy("http://test:123456@127.0.0.1:8332")#creates an object called 'bitcoin' that allows for bitcoind calls

SetTxFee = int(0.00005461*100000000) # Lets proper good etiquette & put something aside for our friends the miners

ChangeAddress = bitcoin.getnewaddress();

unspent = bitcoin.listunspent() # Query wallet.dat file for unspent funds to see if we have multisigs to spend from

print "你的钱包里这些地址有 ",len(unspent)," 个地址可以花费"
for i in range(0, len(unspent)):
    print
    print "第 ",i+1," 个地址有 ",unspent[i]["amount"]," 个比特币，相当于 ",int(unspent[i]["amount"]*100000000),"聪"
    print "它的传输ID ",i+1,"是"
    print unspent[i]["txid"]
    print "ScriptPubKey： ", unspent[i]["scriptPubKey"]
    print "地址 =====>>",unspent[i]["address"]

print
totalcoin = int(bitcoin.getbalance()*100000000)
print "钱包总额是：", totalcoin, "聪"
print

WhichTrans = int(raw_input('你想花费哪个地址上的币? '))-1
if WhichTrans > len(unspent): #Basic idiot check. Clearly a real wallet would do more checks.
    print "抱歉这个地址不存在，请确认您输入的序号" 
else:
    tempaddy = str(unspent[WhichTrans]["address"])
    print
    if int(tempaddy[0:1]) == 1:
        print "这是一个普通地址，请输入多重签名地址的序号"
    elif int(tempaddy[0:1]) == 3:
        print "地址是",tempaddy
        print "以3开头的地址意味着这是一个多重签名地址."
        print
        print "发送多重签名地址上的币，需要如下的一些参数: txid, scriptPubKey,  redeemScript"
        print "这些命令可以在listunspent命令里获得"
        print
        print "txid :",unspent[WhichTrans]["txid"]
        print "ScriptPubKey :", unspent[WhichTrans]["scriptPubKey"]
        print
        print "redeemScript :",unspent[WhichTrans]["redeemScript"]
        print
        
        print "在这个地址里有 ",int(unspent[WhichTrans]["amount"]*100000000)," 聪"

        HowMuch = int(raw_input('您想支出多少 '))
        if HowMuch > int(unspent[WhichTrans]["amount"]*100000000):
            print "抱歉账户里没有这么多钱" # check to see if there are enough funds.
        else:
            print
            
            SendAddress = str(raw_input('发送到哪个地址？ (例如33hxAeUqNnFs3gdayu7aAaijhTbbfnphq8) ')) 
            if SendAddress == "33hxAeUqNnFs3gdayu7aAaijhTbbfnphq8":
                print "太感谢了，你选择捐赠给johnson Diao"
            print
            Leftover = int(unspent[WhichTrans]["amount"]*100000000)-HowMuch-SetTxFee
            print "将要发送您的比特币到这个地址：",SendAddress,"账户里会留下来 ", Leftover," 聪","，这些币会发送到找零地址：",ChangeAddress
            print "会发送 ",SetTxFee," 聪的网络手续费给矿工"
            print
            print "将要创建发送单"
            
            
            rawtransact = bitcoin.createrawtransaction ([{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],
                    "scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],{SendAddress:HowMuch/100000000.00,ChangeAddress:Leftover/100000000.00})
            print "发送单为：", rawtransact
            print
            print
            print "现在我们要用私钥进行签名"
            multisigprivkeyone = str(raw_input("请输入第一个私钥："))
            print
            signedone = bitcoin.signrawtransaction (rawtransact,
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeyone])
            print "签名结果"
            print signedone
            print
            print "在实际应用时，您可以把上面的数据发给第二个密钥的持有者，由他完成第二步签名，上述信息不会泄露您的私钥，因为"
            print "私钥已经经过了加密"
            print
            multisigprivkeytwo = str(raw_input("请输入第二个私钥："))
            print
            doublesignedrawtransaction = bitcoin.signrawtransaction (signedone["hex"],
                    [{"txid":unspent[WhichTrans]["txid"],
                    "vout":unspent[WhichTrans]["vout"],"scriptPubKey":unspent[WhichTrans]["scriptPubKey"],
                    "redeemScript":unspent[WhichTrans]["redeemScript"]}],
                    [multisigprivkeytwo])
            print "第二步签名的结果是"
            print doublesignedrawtransaction
            print
            print "现在您已经准备好发送",HowMuch,"聪的比特币到",SendAddress
            print Leftover," 聪的比特币会发送到找零地址：",ChangeAddress
            print "网络手续费是 ",SetTxFee," 聪"
            print

            ReallyNow = (raw_input('如果现在点击回车，这笔钱将从多重地址发送出去，您确定吗？'))
            ReallyNow2 = (raw_input('真的？您真的打算发送这笔钱？ '))
            print
            print "哈哈，我们不会把钱发送出去的。我们可不希望您因为运行脚本受到任何损失"
            print "如果您真的想发送这笔钱的话，可以将下面这一坨东西复制到bitcoin-qt的命令窗口，然后回车，币就真的发出去了"
            print "sendrawtransaction "+"\""+str(doublesignedrawtransaction['hex'])+"\""

        
