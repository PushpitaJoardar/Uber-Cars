error_message = 'r'
print(error_message)

if error_message:
    print("OK")
else:
    print("NO")

lst=[]
lst.append('d')
print(lst, len(lst))
if lst[0]:
    print("Okey-doke")

print('1' > 'a' and '1' < 'z')
print('a' >= 'a' and 'a'  <= 'z')
strr = '  a a    '
strr = strr.strip()

print(strr, 'OK')

print(not False)
lst1 = []
lst1.append(1)
print("Ok", not lst1)


print(lst)


lst = []
tup = (1, 3, 4)
lst.append(tup)
print(lst)
print(lst[0][2])

print("stRIng".lower())
sttr = "STrint"
str1 = sttr.lower()
print(str1 + strr)

lst = []
lst.append([1,3])
print(lst)
