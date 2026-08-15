

old_curve_formula : list[float] = [
    0.0033, # x^4
    4,  # x^2
    50 # Constant
]

old_values : list[int] = []
for i in range(1, 31):
    value : int = int(old_curve_formula[0] * i ** 4 + old_curve_formula[1] * i**2 + old_curve_formula[2])
    old_values.append(value)

# weights : list[float] = []
# for i in range(1, 6):
#     weights.append(3.0)
# for i in range(1, 6):
#     weights.append(2.0)
# for i in range(1, 6):
#     weights.append(1.0)
# for i in range(1, 6):
#     weights.append(0.6)
# for i in range(1, 6):
#     weights.append(0.4)
# for i in range(1, 6):
#     weights.append(0.2)



# # New curve : y = 4.95 * 1.25 ^ x + 3.9 * x ^ 2 + 46.0
# # Error : 2062.6

# # A=5.92, B=1.24, C=3.95, D=40.0, Error=1105.6


# # New formula look : A*B^x + C*x^2 + D

# # A_range : list[float] = [0.0, 10.0, 0.1]
# # B_range : list[float] = [1.0, 2.0, 0.1]
# # C_range : list[float] = [0.1, 3.0, 0.1]
# # D_range : list[float] = [0.0, 100.0, 1.0]

# A_range : list[float] = [4.0, 5.0, 0.05] # Must be restricted to max < 10 !
# B_range : list[float] = [1.0, 2.0, 0.02]
# C_range : list[float] = [2.0, 3.5, 0.05] # Must be restricted to max < 4 !
# D_range : list[float] = [30.0, 70.0, 1.0]

# A_steps : int = int((A_range[1] - A_range[0]) / A_range[2])
# B_steps : int = int((B_range[1] - B_range[0]) / B_range[2])
# C_steps : int = int((C_range[1] - C_range[0]) / C_range[2])
# D_steps : int = int((D_range[1] - D_range[0]) / D_range[2])

# error : list[list[list[list[float]]]] = []



# for a in range(A_steps):
#     error.append([])
#     # Percentage print
#     print(f"Progress: {a}/{A_steps} ({int(a/A_steps*100)}%)")
#     for b in range(B_steps):
#         error[a].append([])
#         for c in range(C_steps):
#             error[a][b].append([])
#             for d in range(D_steps):
#                 error[a][b][c].append(0.0)
#                 A : float = A_range[0] + a * A_range[2]
#                 B : float = B_range[0] + b * B_range[2]
#                 C : float = C_range[0] + c * C_range[2]
#                 D : float = D_range[0] + d * D_range[2]
#                 for i in range(1, 31):
#                     value = int(A*B**i + C*i**2 + D)
#                     error[a][b][c][d] += abs(value - old_values[i-1])*weights[i-1]

# print("Finished calculating error for all parameter combinations.")

# best_a : float = 0.0
# best_b : float = 0.0
# best_c : float = 0.0
# best_d : float = 0.0
# best_error : float = float("inf")

# for a in range(A_steps):
#     for b in range(B_steps):
#         for c in range(C_steps):
#             for d in range(D_steps):
#                 if error[a][b][c][d] < best_error:
#                     best_error = error[a][b][c][d]
#                     best_a = A_range[0] + a * A_range[2]
#                     best_b = B_range[0] + b * B_range[2]
#                     best_c = C_range[0] + c * C_range[2]
#                     best_d = D_range[0] + d * D_range[2]

# Draw the old and new curve using matplotlib
old_points : list[int] = []
# new_points : list[int] = []
for i in range(1, 31):
    old_points.append(old_values[i-1])
    # new_points.append(int(best_a * best_b ** i + best_c * i ** 2 + best_d))

# print(f"Best parameters found: A={best_a}, B={best_b}, C={best_c}, D={best_d}, Error={best_error}")
# print(f"Formula : y = {best_a} * {best_b} ^ x + {best_c} * x ^ 2 + {best_d}")
# # Plot the old and new curve
import matplotlib.pyplot as plt
# plt.plot(range(1, 31), old_points, label="Old Curve")
# plt.plot(range(1, 31), new_points, label="New Curve")
# plt.xlabel("Wave Number")
# plt.ylabel("Budget")
# plt.title("Old vs New Budget Curve")
# plt.legend()
# plt.show()


# Second plot : Hand-made curves
plt.plot(range(1, 31), old_points, label="Old Curve")
# plt.plot(range(1, 31), new_points, label="New Curve")

points1 : list[int] = []
for i in range(1, 31):
    points1.append(int(4.9 * 1.24 ** i + 4.1 * i ** 2 + 40.0))
plt.plot(range(1, 31), points1, label="Curve 1")

points2 : list[int] = []
for i in range(1, 31):
    points2.append(int(5.3 * 1.25 ** i + 4.1 * i ** 2 + 60.0))
plt.plot(range(1, 31), points2, label="Curve 2")

points3 : list[int] = []
for i in range(1, 31):
    points3.append(int(5.7 * 1.26 ** i + 4.1 * i ** 2 + 80.0))
plt.plot(range(1, 31), points3, label="Curve 3")


plt.xlabel("Wave Number")
plt.ylabel("Budget")
plt.title("Old vs New vs Hand-made Budget Curve")
plt.legend()
plt.show()

