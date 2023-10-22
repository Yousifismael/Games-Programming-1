#homework1
#Exploration of text adventures
print("Welcome player to the jungle!")
river = "1"
mountain = "2"
print('Would you like to go towards the river or towards the mountains? ')
answer = input("Choose 1 or 2: ")
print(answer)
if answer == "1":
    print("Heading towards the river!")
elif answer == "2":
    print("Heading towards the mountain!")
else:
    print("That is not a destination.")


#problem
name = input("Choose a monster name: ")
add1 = "elle"
add2 = "ling"
prefix = "baby"
last_letter = "monster_name" [-1]
name_length = len(name)

if name_length >= 3:
    if last_letter == 'a' or last_letter == 'e' or last_letter == 'i' or last_letter == 'o' or last_letter == 'u':
        print(name + add2)
    else:
        print(name + add1)
else:
    print(prefix + " " + name)
