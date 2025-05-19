x = input("Masukan nilai x : ")
y = input("Masukan nilai y : ")

x_bool = bool(x)
y_bool = bool(y)

and_result = x_bool and y_bool
or_result = x_bool or y_bool
not_x_result = not y_bool
xor_result = (x_bool and not y_bool) or (not x_bool and y_bool)

print(f"\n Nilai Boolean Dari ")
print(f"x AND y : {and_result}")
print(f"x OR y : {or_result} ")
print(f"x NOT y : {not_x_result} ")
print(f"x XOR y : {xor_result} ")