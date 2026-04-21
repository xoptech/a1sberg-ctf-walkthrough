
"""

rx{1Atr_34_f_p_0}3_rhm113m05rfl3S

r  x  {  1  A  t  r  _  3  4  _  f  _  p  _  0  }  3  _  r  h  m  1  1  3  m  0  5  r  f  l  3  S
00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32

3  r  1  p  r  3  m  m  _  f  f  A  _  0  _  h  S  r  1  _  4  _  t  x  3  1  }  l  0  r  5  3  {
17 06 03 13 00 08 21 25 10 29 11 04 18 26 07 20 32 28 22 14 09 12 05 01 31 23 16 30 15 19 27 24 02
"""

string = "rx{1Atr_34_f_p_0}3_rhm113m05rfl3S"
nums = [17, 6, 3, 13, 0, 8, 21, 25, 10, 29, 11, 4, 18, 26, 7, 20, 32, 28, 22, 14, 9, 12, 5, 1, 31, 23, 16, 30, 15, 19, 27, 24, 2]
emptyarr = [""] * len(string)

i = 0
for s in string:
    emptyarr[nums[i]] = string[i]
    i += 1

for c in u:
    print(c, end="")








# i = 0
# for c in s:
#     print(c, end="  ")

# print("\n")

# for c in s:
#     print(f"{i:02}", end=" ")
#     i += 1
