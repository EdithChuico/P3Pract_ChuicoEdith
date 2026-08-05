import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 1. Cargar los datos
df = pd.read_csv('./resultados-geocerca-fase2.csv')

print("="*50)
print(" ANÁLISIS DE TASAS DE ERROR (FAR Y FRR)")
print("="*50)

# 2. Calcular FAR (False Acceptance Rate)
total_fuera = len(df[df['Posicion_Esperada'] == 'Fuera'])
falsas_aceptaciones = len(df[(df['Posicion_Esperada'] == 'Fuera') & (df['Validacion'] == 'Aceptada')])
far = (falsas_aceptaciones / total_fuera) * 100 if total_fuera > 0 else 0

# 3. Calcular FRR (False Rejection Rate)
total_dentro = len(df[df['Posicion_Esperada'] == 'Dentro'])
falsos_rechazos = len(df[(df['Posicion_Esperada'] == 'Dentro') & (df['Validacion'] == 'Rechazada')])
frr = (falsos_rechazos / total_dentro) * 100 if total_dentro > 0 else 0

print(f"Total de pruebas 'Fuera': {total_fuera}")
print(f"Falsas Aceptaciones (Spoofing/Caché fallido): {falsas_aceptaciones}")
print(f"FAR (Tasa de Falsa Aceptación): {far:.2f}%\n")

print(f"Total de pruebas 'Dentro': {total_dentro}")
print(f"Falsos Rechazos (Anomalías de Red/VPN): {falsos_rechazos}")
print(f"FRR (Tasa de Falso Rechazo): {frr:.2f}%\n")

print("="*50)
print(" ANÁLISIS ESTADÍSTICO: ANOVA FACTORIAL")
print("="*50)

# 4. ANOVA para evaluar el impacto en el Tiempo de Red (RTT)
df_anova = df.copy()
df_anova.rename(columns={'Conexion': 'Conexion_Net'}, inplace=True)
df_anova['Conexion_Net'] = df_anova['Conexion_Net'].str.replace(' ', '_')

print("Variable Dependiente: Tiempo_RTT_ms")
print("Variables Independientes: Conexion_Net (Wi-Fi vs Datos), VPN (Sí vs No)\n")

# Modelo: RTT en función de la conexión, la VPN y la interacción entre ambas
modelo_rtt = ols('Tiempo_RTT_ms ~ C(Conexion_Net) + C(VPN) + C(Conexion_Net):C(VPN)', data=df_anova).fit()
anova_tabla_rtt = sm.stats.anova_lm(modelo_rtt, typ=2)
print(anova_tabla_rtt)
print("\n")

# 5. ANOVA para evaluar el impacto en el Tiempo de Geolocalización
df_anova['Dispositivo_OS'] = df_anova['Dispositivo'].apply(lambda x: 'Android' if 'Android' in x else 'Windows')
df_anova['Uso_Cache'] = df_anova['Tipo_Lectura'].apply(lambda x: 'Cached' if 'Cached' in x else 'Fresh')

print("Variable Dependiente: Tiempo_Geo_ms")
print("Variables Independientes: Dispositivo_OS (Android vs Windows), Uso_Cache (Fresh vs Cached)\n")

modelo_geo = ols('Tiempo_Geo_ms ~ C(Dispositivo_OS) + C(Uso_Cache) + C(Dispositivo_OS):C(Uso_Cache)', data=df_anova).fit()
anova_tabla_geo = sm.stats.anova_lm(modelo_geo, typ=2)
print(anova_tabla_geo)