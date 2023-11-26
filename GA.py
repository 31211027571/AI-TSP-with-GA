import tkinter as tk
from tkinter import messagebox
import random
import math


# Tạo tọa độ các thành phố 
cities = {i: (random.randint(0, 1000), random.randint(0, 650)) for i in range(1000)}

# Function tính khoảng cách giữa 2 thành phố
def distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Function tính tổng khoảng cách của đường đi
def route_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance(route[i], route[i + 1])
    total_distance += distance(route[-1], route[0])  # Trở về thành phố bắt đầu
    return total_distance

# Tham số thuật toán GA
population_size = 100
mutation_rate = 0.015
generations = 500

# Function tạo các tuyến đường
def initial_population():
    initial_route = list(cities.keys())
    population = [random.sample(initial_route, len(initial_route)) for _ in range(population_size)]
    return population

# Function thực hiện lai ghép chéo giữa các tuyến đường
def crossover(parent1, parent2):
    start = random.randint(0, len(parent1) - 1)
    end = random.randint(0, len(parent1) - 1)
    if start > end:
        start, end = end, start
    child = [None] * len(parent1)
    for i in range(start, end):
        child[i] = parent1[i]
    j = 0
    for i in range(len(parent2)):
        if child[i] is None:
            while parent2[j] in child:
                j += 1
            child[i] = parent2[j]
    return child

# Function thực hiện Đột biến
def mutate(route):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

# Function phát triển dân số quần thể 
def evolve(population):
    graded = [(route_distance(route), route) for route in population]
    graded = sorted(graded, key=lambda x: x[0])
    parents = [route for _, route in graded[:int(0.2 * len(population))]]

    # Tạo thế hệ mới
    desired_length = len(population) - len(parents)
    children = []
    while len(children) < desired_length:
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = crossover(parent1, parent2)
        child = mutate(child)
        children.append(child)

    parents.extend(children)
    return parents

# Setup UI
root = tk.Tk()
root.title("TSP Genetic Algorithm")

canvas = tk.Canvas(root, width=1080, height=700)
canvas.pack()

# Vẽ city trên UI
for city, (x, y) in cities.items():
    canvas.create_oval(x, y, x + 5, y + 5, fill="red")
    canvas.create_text(x + 10, y, text=city)

best_distance_label = tk.Label(root, text="Best Distance: ")
best_distance_label.pack()

# Function Bắt đầu tối ưu hóa
def start_optimization():
    population = initial_population()
    best_distance = float('inf')  
    unchanged_gens = 0
    best_route_line = None  # Giữ tuyến đường tốt nhất
    for gen in range(generations):
        population = evolve(population)
        current_best_route = population[0]
        current_best_distance = route_distance(current_best_route)
        
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            unchanged_gens = 0
            # Xóa đường cũ
            if best_route_line:
                canvas.delete(best_route_line)
        else:
            unchanged_gens += 1
        best_distance_label.config(text=f"Best Distance: {best_distance:.2f}")
        root.update()
        # Vẽ đường tốt nhất trên UI
        route_coords = []
        for city in current_best_route:
            x, y = cities[city]
            route_coords.extend([x + 2, y + 2])
        if best_route_line:
            canvas.delete(best_route_line)  
        best_route_line = canvas.create_line(route_coords, fill="blue")
        root.update()
        if unchanged_gens >= 50:
            messagebox.showinfo("Optimization Halted", f"No improvement after 50 generations. Best Distance: {best_distance:.2f}")
            break
    if unchanged_gens < 50:
        messagebox.showinfo("Optimization Complete", f"Best Distance: {best_distance:.2f}")

# Start button Optimization
start_button = tk.Button(root, text="Start Optimization", command=start_optimization)
start_button.pack()

root.mainloop()
