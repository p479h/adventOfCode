# Input target area: x=244..303, y=-91..-54
sq = [[244, -54],[303,-91]] # Top left and bottom right. s[0][0]<x<s[1][0] & s[0][1]<y<s[1][1]

vymax = (91-1)*(91-1+1)//2
v0 = ([i, j] for i in range(1,vymax+10) for j in range(-vymax-2,vymax+2))

su = 0
for v in v0:
	s = [0, 0]
	for _ in range(vymax*2):
		# Updating position
		for i in range(2):
			s[i] += v[i]
		
		# Checking if falls inside the square 
		if sq[0][0]<=s[0]<=sq[1][0] and sq[1][1]<=s[1]<=sq[0][1]:
			su += 1
			break
		if v[0] == 0 and s[0] < sq[0][0]:
			break
		if s[0] > sq[1][0]:
			break
		if s[1] < sq[1][1]:
			break

		if v[0] != 0: # Changing x velocity 
			v[0] -= v[0]//abs(v[0])
		v[1] -= 1 # Changing y velocity 
	
print(su)
