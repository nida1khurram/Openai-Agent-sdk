my_list = [1,2,3,4,5]
print(my_list)
# seprate entity mean unpack
# list 1 *
print(*my_list)

# dict 2 **
def func(**kwargs):
    print(kwargs)
func(
    name="Nida",
    age= 38
)