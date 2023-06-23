htb = dict(l.strip().split(" = ") for l in open("./bin.txt"))

def peek(s: iter, n: int) -> iter:
	return "".join([next(s) for _ in range(n)])

VERSION = 0
def parsestr(sb: iter) -> None:
	global VERSION
	end = 0
	if type(sb) is str: # Must have an iterator through binary!
		sb = (b for B in map(lambda c: htb[c], sb) for b in B) # string in bits instead of hexa
	version = int(peek(sb,3),2) # Getting first three bits
	VERSION += version
	ID = int(peek(sb,3),2)
	end += 6 # Accounting for the reading of type and version
	packet = ""
	whilecount = 0 # Number of times the while loop went
	while ID == 4: # Only literals follow
		group = peek(sb,5)
		packet = packet+group[1:]
		whilecount += 1
		end += 5
		if group[0]=="0":
			return (version, ID, int(packet,2)), end # Number of bits processed
	I = peek(sb,1)
	LL = {"0":15, "1":11}[I] # Length of length representation
	L = int(peek(sb,LL),2) # If i=0 length in bits, else number of subpackets
	end += 1 + LL
	subpackets = []
	if I == "1":
		for _ in range(L):
			packet, e = parsestr(sb)
			end += e
			subpackets.append(packet)
	else:
		e0 = 0
		while e0 < L:
			packet, e = parsestr(sb)
			end += e
			e0 += e
			subpackets.append(packet)
	return (version, ID, subpackets), end
	
def prod(it)->float:
	if len(it) > 1:
		return it[0]*prod(it[1:])
	return it[0]
gt = lambda a: int(a[0]>a[1])
st = lambda a: int(a[0]<a[1])
et = lambda a: int(a[0]==a[1])
operations = [sum,prod,min,max, lambda *a: a,gt,st,et]
def operate(r):
	if r[1] == 4:
		return r[2]
	values = [operate(t) for t in r[2]]
	return operations[r[1]](values)

imp = "60556F980272DCE609BC01300042622C428BC200DC128C50FCC0159E9DB9AEA86003430BE5EFA8DB0AC401A4CA4E8A3400E6CFF7518F51A554100180956198529B6A700965634F96C0B99DCF4A13DF6D200DCE801A497FF5BE5FFD6B99DE2B11250034C00F5003900B1270024009D610031400E70020C0093002980652700298051310030C00F50028802B2200809C00F999EF39C79C8800849D398CE4027CCECBDA25A00D4040198D31920C8002170DA37C660009B26EFCA204FDF10E7A85E402304E0E60066A200F4638311C440198A11B635180233023A0094C6186630C44017E500345310FF0A65B0273982C929EEC0000264180390661FC403006E2EC1D86A600F43285504CC02A9D64931293779335983D300568035200042A29C55886200FC6A8B31CE647880323E0068E6E175E9B85D72525B743005646DA57C007CE6634C354CC698689BDBF1005F7231A0FE002F91067EF2E40167B17B503E666693FD9848803106252DFAD40E63D42020041648F24460400D8ECE007CBF26F92B0949B275C9402794338B329F88DC97D608028D9982BF802327D4A9FC10B803F33BD804E7B5DDAA4356014A646D1079E8467EF702A573FAF335EB74906CF5F2ACA00B43E8A460086002A3277BA74911C9531F613009A5CCE7D8248065000402B92D47F14B97C723B953C7B22392788A7CD62C1EC00D14CC23F1D94A3D100A1C200F42A8C51A00010A847176380002110EA31C713004A366006A0200C47483109C0010F8C10AE13C9CA9BDE59080325A0068A6B4CF333949EE635B495003273F76E000BCA47E2331A9DE5D698272F722200DDE801F098EDAC7131DB58E24F5C5D300627122456E58D4C01091C7A283E00ACD34CB20426500BA7F1EBDBBD209FAC75F579ACEB3E5D8FD2DD4E300565EBEDD32AD6008CCE3A492F98E15CC013C0086A5A12E7C46761DBB8CDDBD8BE656780"
result,_ = parsestr(imp)
#print(VERSION)
#print(result)
r = operate(result)
print(r)
	
	
