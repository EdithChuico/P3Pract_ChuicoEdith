import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Cargar el dataset
df = pd.read_csv('./resultados-geocerca-fase2.csv')

distancias = [2, 9, 11, 20]
frr_rates = []
far_rates = []

# 3. Calcular tasas dinámicamente desde el CSV
for d in distancias:
    # Filtrar por distancia usando el nombre correcto de tu columna
    subset = df[df['Distancia_Real_m'] == d]
    total_intentos = len(subset)
    
    if total_intentos == 0:
        frr_rates.append(0)
        far_rates.append(0)
        continue
        
    # FRR: Tasa de Falso Rechazo (Dentro de la geocerca, pero rechazado)
    if d <= 10:
        # Busca 'Rechazado' o 'Rejected' dependiendo de cómo esté escrito en tu CSV
        falsos_rechazos = len(subset[subset['Validacion'].astype(str).str.contains('Rechazad|Reject', case=False, na=False)])
        frr_rates.append((falsos_rechazos / total_intentos) * 100)
        far_rates.append(0) # No hay FAR dentro de la geocerca
        
    # FAR: Tasa de Falsa Aceptación (Fuera de la geocerca, pero aceptado)
    else:
        # Busca 'Aceptado' o 'Accepted'
        falsas_aceptaciones = len(subset[subset['Validacion'].astype(str).str.contains('Aceptad|Accept', case=False, na=False)])
        far_rates.append((falsas_aceptaciones / total_intentos) * 100)
        frr_rates.append(0) # No hay FRR fuera de la geocerca

# 4. Generar la gráfica
plt.figure(figsize=(8, 5))

# Extraer solo los puntos válidos para cada línea
distancias_in = [d for d in distancias if d <= 10]
frr_valid = [frr_rates[i] for i in range(len(distancias)) if distancias[i] <= 10]

distancias_out = [d for d in distancias if d > 10]
far_valid = [far_rates[i] for i in range(len(distancias)) if distancias[i] > 10]

plt.plot(distancias_in, frr_valid, marker='o', color='red', linestyle='-', linewidth=2, label='False Rejection Rate (FRR)')
plt.plot(distancias_out, far_valid, marker='s', color='orange', linestyle='-', linewidth=2, label='False Acceptance Rate (FAR)')
plt.plot(distancias, [f + a for f, a in zip(frr_rates, far_rates)], color='gray', linestyle='--', alpha=0.5)

plt.axvline(x=10, color='blue', linestyle='--', linewidth=2, label='Geofence Boundary (10m)')
plt.title('Error Rates vs. Physical Distance to Geofence Center')
plt.xlabel('Ground-Truth Distance (meters)')
plt.ylabel('Error Rate (%)')
plt.xticks(np.arange(0, 25, 2))
plt.yticks(np.arange(0, 100, 10))
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('error_curve_dynamic.png', dpi=300)
print("Gráfico generado desde el CSV con éxito: error_curve_dynamic.png")