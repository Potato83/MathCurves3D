import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson

# t - array of numbers(radian), x,y,z - arrays of coordinates
# R - radius H - high n - division

def whoami():
    print('Вариант 8. Кривые в трехмерном пространстве')

def gen_t(t,R,H):
    x = R * np.cos(t)
    y = R * np.sin(t)
    z = H * t
    return (x,y,z)
    
def main():
    #define
    R, H = [int(x) for x in input().split()]
    n_values = [10, 20, 50, 100, 200, 500]
    errors = []
    
    #calc
    for n in n_values:   
        t = np.linspace(0 , 2 * np.pi, n)
        x,y,z = gen_t(t, R, H)
        dx_dt,dy_dt,dz_dt = np.gradient(x,t), np.gradient(y,t), np.gradient(z,t)
        integrand = np.sqrt((dx_dt)**2 + (dy_dt)**2 + (dz_dt)**2)
        L_simpson = simpson(integrand, x=t)
        L_exact = 2 * np.pi * np.sqrt(R**2 + H**2)
        errors.append(abs(L_exact - L_simpson))
        
    # график погрешноси
    plt.figure(figsize=(8, 5))
    plt.plot(n_values, errors, marker='o', color='red', linestyle='-', linewidth=2)
    plt.title("Анализ сходимости: Зависимость погрешности от $n$")
    plt.xlabel("Число разбиений (n)")
    plt.ylabel("Абсолютная погрешность")
    plt.grid(True)
    
    # график 3д
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection="3d") 
    ax.plot(x, y, z, label="Винтовая линия", color="blue", linewidth=2)
    ax.set_xlabel("Ось X")
    ax.set_ylabel("Ось Y")
    ax.set_zlabel("Ось Z (Высота H*t)") 
    ax.set_title(f"Разбиение n={n}\nВычисленная длина: {L_simpson:.4f}, Точная: {L_exact:.4f}") 
    ax.scatter(x, y, z, color="red", label="Точки разбиения", s=10) # s=10 делает точки поменьше
    ax.legend() 
    # Проекция на XY
    ax.plot(x, y, np.zeros_like(z), label='Проекция на XY (Окружность)', linestyle='--', color='gray')

    plt.show()
    
    print(L_simpson,L_exact)
    return True

main()

if __name__ == '__main__':
    whoami()