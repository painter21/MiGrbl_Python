

test = "X57.157"
test2 = "X103.100"
print(test.translate({ord(i): None for i in ".XY;"})[-7:-3])
print(test2.translate({ord(i): None for i in ".XY;"})[-7:-3])