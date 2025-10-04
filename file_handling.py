try:
    data = open("files/data.txt", "r")
    # print("Read all in the File ->",data.read())
    # print("Read Line only       ->" , data.readline())

    for line in data:
        print("from for" , line)

    data.close()
#     After using files -> close reading

except FileNotFoundError as e:
    print("file not found")


data_write = open("files/data_write.txt", "w")

data_write.write("My name is methmin\n")
data_write.write("My age is 18")

data_write.close()

data_write1 = open("files/data_write.txt", "a")
data_write1.write("adcscascdasc")


data_write1.close()




#  Auto close no need to close


with open("files/data.txt", "r") as  data_file:
    for line in data_file:
        print(line)
