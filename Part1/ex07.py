#dictionary containing nams and ages
age = {"Hans" : 24, "Prag" : 23, "Bunyod" : 18}

#to do
print(age)
print(age.get("Hans"))

#age update
age.update({'Prag' : 30})
print(age.get("Prag"))

#remove Bunyod
del age["Bunyod"]
print(age)
