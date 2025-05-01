from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint, minimize_scalar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 1b. Resolver utilizando una librería de optimización en Python.

# Definir la función objetivo (a minimizar el negativo de los rendimientos)
def objective_function(vars):
    x = vars[0]
    y = vars[1]
    return -(0.1 * x + 0.08 * y) # Negativo de la función de rendimientos

# Definir la restricción de igualdad: x + y = 1
# Los coeficientes de las variables son [1, 1] y los límites inferior y superior son 1.
linear_constraint = LinearConstraint([1, 1], 1, 1)

# Definir la restricción de desigualdad: 0.02*x^2 + 0.03*y^2 <= 0.05
# La restricción g(x,y) <= c se convierte en g(x,y) - c <= 0
# Aquí g(x,y) = 0.02*x^2 + 0.03*y^2 y c = 0.05
# El límite inferior es -inf y el límite superior es 0.05
def risk_constraint(vars):
    x = vars[0]
    y = vars[1]
    # OJO: Basado en la interpretación más común, asumo 0.02x^2
    # Si es estrictamente 0.0*2x^2, la función sería solo 0.03 * y**2
    return 0.02 * x**2 + 0.03 * y**2

def risk_constraint2(vars):
    y = vars[1]
    return 0.03 * y**2
# Definir los límites de la restricción no lineal.
# El valor calculado por risk_constraint debe estar entre -inf y 0.05
nonlinear_constraint = NonlinearConstraint(risk_constraint, -np.inf, 0.05)
nonlinear_constraint2 = NonlinearConstraint(risk_constraint2, -np.inf, 0.05)


# Definir los límites para x y y (no negativos, ya que representan inversiones)
# aunque la restricción x+y=1 y la restricción de riesgo ya implican esto en la práctica.
bounds = Bounds(0, np.inf)

# Elegir un punto de inicio (debe satisfacer idealmente las restricciones, pero no es estrictamente necesario para SLSQP)
initial_guess = [0.5, 0.5] # Un punto simple donde x + y = 1

# Llamar a la función minimize
# Usamos el método 'SLSQP' que maneja restricciones de igualdad y desigualdad.
solution = minimize(objective_function, initial_guess, method='SLSQP',
                    bounds=bounds, constraints=[linear_constraint, nonlinear_constraint])
solution2 = minimize(objective_function, initial_guess, method='SLSQP',
                    bounds=bounds, constraints=[linear_constraint, nonlinear_constraint2])

# Mostrar los resultados
print("=== Resultado del Problema 1b ===")
print("Estado de la optimización:", solution.message)
print("Éxito:", solution.success)
print("Valores óptimos de (x, y):", solution.x)
print("Valor mínimo de la función objetivo (-rendimientos):", solution.fun)
print("Valor máximo de rendimientos:", -solution.fun)
print("-" * 30)

print("=== Resultado del Problema 1b si 0.0∗2x∧2+0.03∗y∧2≤0.05. ===")
print("Estado de la optimización:", solution2.message)
print("Éxito:", solution2.success)
print("Valores óptimos de (x, y):", solution.x)
print("Valor mínimo de la función objetivo (-rendimientos):", solution2.fun)
print("Valor máximo de rendimientos:", -solution2.fun)
print("-" * 30)

def cost_function(vars):
    x = vars[0]
    y = vars[1]
    z = vars[2]
    return 5 * x**2 + 3 * y**2 + z**2

# Restricción de igualdad: x + y + z = 100
linear_constraint_prod = LinearConstraint([1, 1, 1], 100, 100)

# Límites para x, y, z (no negativos)
bounds_prod = Bounds(0, np.inf)

initial_guess_prod = [10, 10, 80] # Un punto factible
solution_prod = minimize(cost_function, initial_guess_prod, method='SLSQP',
                         bounds=bounds_prod, constraints=[linear_constraint_prod])
print("=== Resultado del Problema 2a ===")
print("Estado de la optimización:", solution_prod.message)
print("Éxito:", solution_prod.success)
print("Valores óptimos de (x, y, z):", solution_prod.x)
print("Valor mínimo de la función de costos:", solution_prod.fun)
print("-" * 30)

# Definir rangos para x e y para graficar el plano
x_range = np.linspace(0, 100, 20)
y_range = np.linspace(0, 100, 20)

X, Y = np.meshgrid(x_range, y_range)
Z = 100 - X - Y

# Filtrar puntos para asegurar z >= 0 (dentro de los límites del problema)
Z[Z < 0] = np.nan # Establecer a NaN para no graficar puntos con z negativo
# Reemplaza estos con los valores obtenidos de tu solución del Problema 2a
optimal_x = 13.04347809
optimal_y = 21.73913124
optimal_z = 65.21739067
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar el plano x + y + z = 100
ax.plot_surface(X, Y, Z, alpha=0.5, rstride=100, cstride=100, cmap='viridis')

# Marcar el punto óptimo
ax.scatter(optimal_x, optimal_y, optimal_z, color='red', s=100, label='Punto Óptimo')

# Configurar etiquetas y título
ax.set_xlabel('Cantidad Producto A (x)')
ax.set_ylabel('Cantidad Producto B (y)')
ax.set_zlabel('Cantidad Producto C (z)')
ax.set_title('Región Factible y Punto Óptimo para Minimización de Costos')
ax.legend()

# 2b. Graficar la solución en Python.

# Obtener los valores óptimos de la solución
optimal_x = solution_prod.x[0]
optimal_y = solution_prod.x[1]
optimal_z = solution_prod.x[2]

# Definir rangos para x e y para graficar el plano
# Asegúrate de que los rangos cubran la región donde se encuentra el punto óptimo
x_range = np.linspace(0, 100, 50) # Aumentar puntos para mejor superficie
y_range = np.linspace(0, 100, 50)

X, Y = np.meshgrid(x_range, y_range)
Z = 100 - X - Y

# Filtrar puntos para asegurar z >= 0 y que x, y estén en los rangos definidos
# Esto ayuda a graficar solo la porción del plano relevante para x,y,z >= 0
valid_indices = (Z >= 0) & (X >= 0) & (Y >= 0)
Z[~valid_indices] = np.nan


# Crear el gráfico 3D
fig = plt.figure(figsize=(12, 10)) # Ajustar tamaño de la figura
ax = fig.add_subplot(111, projection='3d')

# Graficar el plano x + y + z = 100
ax.plot_surface(X, Y, Z, alpha=0.7, rstride=10, cstride=10, cmap='viridis', edgecolor='none') # Ajustar rstride/cstride para densidad de malla

# Marcar el punto óptimo
ax.scatter(optimal_x, optimal_y, optimal_z, color='red', s=150, label='Punto Óptimo', edgecolors='black') # Aumentar tamaño del punto

# Configurar etiquetas y título
ax.set_xlabel('Cantidad Producto A (x)')
ax.set_ylabel('Cantidad Producto B (y)')
ax.set_zlabel('Cantidad Producto C (z)')
ax.set_title('Región Factible (x+y+z=100) y Punto Óptimo de Costo Mínimo')
ax.legend()

# Ajustar los límites de los ejes
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 100)

# Opcional: ajustar el punto de vista
ax.view_init(elev=20., azim=45) # Elevación y azimut

plt.show()

# 3b. Implementa el algoritmo de descenso del gradiente en Python para este problema.
# 3c. Realiza 15 iteraciones y gráfica la evolución del valor de la función f(x,y,z)

# Definir la función a minimizar
def f(x, y, z):
    return x**2 + y**2 + z**2 - 2*x*y + 3*z

# Definir el gradiente de la función
# Calculado en el paso 3a: (2x - 2y, 2y - 2x, 2z + 3)
def gradient_f(x, y, z):
    df_dx = 2 * x - 2 * y
    df_dy = 2 * y - 2 * x
    df_dz = 2 * z + 3
    return np.array([df_dx, df_dy, df_dz]) # Devolvemos el gradiente como un array de numpy

# Parámetros del algoritmo de descenso del gradiente
starting_point = np.array([1.0, 1.0, 1.0]) # Punto de inicio (x0, y0, z0)
learning_rate = 0.1 # Paso de aprendizaje alfa
num_iterations = 15 # Número de iteraciones

# Inicializar el punto actual y la lista para almacenar los valores de la función
current_point = starting_point
function_values = []
iteration_numbers = []

print("=== Ejecutando Descenso del Gradiente para el Problema 3 ===")
print(f"Punto de inicio: {current_point}")
print(f"Tasa de aprendizaje (alfa): {learning_rate}")
print(f"Número de iteraciones: {num_iterations}\n")

# Bucle del descenso del gradiente
for i in range(num_iterations):
    # Calcular el gradiente en el punto actual
    grad = gradient_f(current_point[0], current_point[1], current_point[2])

    # Actualizar el punto utilizando la fórmula del descenso del gradiente
    # point_new = point_current - learning_rate * gradient
    current_point = current_point - learning_rate * grad

    # Calcular el valor de la función en el nuevo punto
    current_function_value = f(current_point[0], current_point[1], current_point[2])

    # Almacenar el valor de la función y el número de iteración
    function_values.append(current_function_value)
    iteration_numbers.append(i + 1) # Guardamos el número de iteración (empezando en 1)

    # Opcional: imprimir el progreso
    print(f"Iteración {i+1}: Punto = {current_point}, Valor de la función = {current_function_value}")

print("\n=== Descenso del Gradiente Finalizado ===")
print(f"Punto aproximado del mínimo después de {num_iterations} iteraciones: {current_point}")
print(f"Valor aproximado mínimo de la función: {function_values[-1]}") # Último valor calculado

# Graficar la evolución del valor de la función
plt.figure(figsize=(10, 6))
plt.plot(iteration_numbers, function_values, marker='o', linestyle='-')
plt.title('Evolución del Valor de la Función f(x,y,z) durante el Descenso del Gradiente')
plt.xlabel('Número de Iteración')
plt.ylabel('Valor de la Función f(x,y,z)')
plt.grid(True)
plt.show()

# 4. Minimiza la función con restricciones.

# Definir la función a minimizar
def f(x):
    return x**2 + 4*x + 5

# Definir los límites (intervalo factible)
# La minimización se realizará dentro de este intervalo [2, 5]
bounds = (2, 5)

# Llamar a la función minimize_scalar con el método 'bounded'
# Este método es específico para optimización en un intervalo dado.
result = minimize_scalar(f, bounds=bounds, method='bounded')

# Mostrar los resultados
print("=== Resultado del Problema 4 ===")
print("Estado de la optimización:", result.message)
print("Éxito:", result.success)
print("Valor óptimo de x:", result.x)
print("Valor mínimo de la función:", result.fun)
print("-" * 30)