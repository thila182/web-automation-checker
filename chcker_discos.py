import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURACIÓN ---
URL_LISTA = "https://spammusic.netlify.app/disc-list"
NOMBRE_FALTANTES = "discos_faltantes.csv"
CAMPOS_CSV = ['Artista', 'Álbum', 'Género', 'Fecha', 'Spotify URL']

# --- CREDENCIALES ---
USER_LOGIN = "TU_USUARIO"
PASS_LOGIN = "TU_CONTRASEÑA"

VARIACIONES_SELF_TITLED = [
    "self titled", "self-titled", "selftitled", "self_titled",
    "(self-titled)", "[self-titled]", "s/t", "st", "homonimo"
]

def seleccionar_archivo_csv():
    archivos = [f for f in os.listdir('.') if f.endswith('.csv') and f != NOMBRE_FALTANTES]
    if not archivos:
        print("❌ No hay archivos .csv de datos aquí.")
        return None
    
    print("\n--- ARCHIVOS DISPONIBLES ---")
    for i, archivo in enumerate(archivos):
        print(f"{i + 1}. {archivo}")
    
    while True:
        try:
            val = input("\nElige número: ")
            return archivos[int(val) - 1]
        except: pass

def cargar_faltantes_en_memoria():
    datos = []
    if os.path.exists(NOMBRE_FALTANTES):
        try:
            with open(NOMBRE_FALTANTES, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    datos.append(row)
        except Exception as e:
            print(f"⚠️ Error leyendo faltantes: {e}")
    return datos

def buscar_indice_en_memoria(lista_datos, artista, album):
    art_norm = artista.lower().strip()
    alb_norm = album.lower().strip()
    
    for i, item in enumerate(lista_datos):
        if item['Artista'].lower().strip() == art_norm and \
           item['Álbum'].lower().strip() == alb_norm:
            return i
    return -1

def main():
    # 1. SETUP
    archivo_csv = seleccionar_archivo_csv()
    if not archivo_csv: return

    print("\n🎹 CONFIGURACIÓN DE GÉNERO")
    genero_global = input("Introduce el GÉNERO para aplicar a TODOS los discos procesados hoy: ").strip()
    if not genero_global:
        print("❌ El género es obligatorio.")
        return

    lista_faltantes = cargar_faltantes_en_memoria()
    
    indices_para_actualizar = [] 
    nuevos_para_anadir = []      
    total_leidos = 0

    print("🚀 Abriendo navegador...")
    driver = webdriver.Chrome()
    
    try:
        # Abrimos la web inicial (seguramente redirija al login)
        driver.get(URL_LISTA)

        # 2. AUTOLOGIN
        print("🔑 Autologin...")
        try:
            wait_login = WebDriverWait(driver, 5)
            input_user = wait_login.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='email']")))
            input_pass = driver.find_element(By.XPATH, "//input[@type='password']")
            
            input_user.clear()
            input_user.send_keys(USER_LOGIN)
            input_pass.clear()
            input_pass.send_keys(PASS_LOGIN)
            input_pass.send_keys(Keys.RETURN)
            print("✅ Login enviado.")
            
            # Pequeña pausa para dejar que el login procese
            time.sleep(2)
        except:
            print("⚠️ Haz login manual (o ya estabas logueado).")

        # --- REDIRECCIÓN FORZADA A LA LISTA ---
        print(f"🔄 Redirigiendo a: {URL_LISTA}")
        driver.get(URL_LISTA)
        # --------------------------------------

        # 3. ESPERAR BUSCADOR
        print("\n⏳ Esperando carga de la lista...")
        wait = WebDriverWait(driver, 60)
        search_input = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[placeholder='Buscar álbum o artista...']")
        ))
        print("✅ Listo para buscar.")

        # --- BUCLE DE PROCESAMIENTO ---
        with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) # Saltar header
            
            for row in reader:
                if len(row) < 2: continue
                
                artista = row[0].strip()
                album = row[1].strip()
                fecha = row[3] if len(row) > 3 else ""
                spotify = row[4] if len(row) > 4 else ""
                
                total_leidos += 1

                # --- 🛑 NUEVO FILTRO: SPLIT ---
                if "split" in album.lower():
                    print(f"[{total_leidos}] ⏭️  {album}: OMITIDO por ser un split de más de un grupo.")
                    continue
                # ------------------------------

                # A. ¿YA EXISTE EN LOCAL?
                idx = buscar_indice_en_memoria(lista_faltantes, artista, album)
                if idx != -1:
                    print(f"[{total_leidos}] 📂 YA EXISTE EN CSV LOCAL: {album} (Se actualizará género al final)")
                    indices_para_actualizar.append(idx)
                    continue 
                
                # B. BUSCAR EN WEB
                termino_busqueda = album
                es_self_titled = False
                
                if album.lower().strip() in VARIACIONES_SELF_TITLED:
                    termino_busqueda = artista
                    es_self_titled = True
                    print(f"[{total_leidos}] 🔄 Self-Titled detectado. Buscando: '{artista}'")
                
                search_input.clear()
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
                search_input.send_keys(termino_busqueda)
                
                # Reactividad
                time.sleep(0.1)
                search_input.send_keys(" ")
                time.sleep(0.1)
                search_input.send_keys(Keys.BACKSPACE)

                time.sleep(3) # Espera 3s

                cards = driver.find_elements(By.CLASS_NAME, "card")
                encontrado = False
                
                if len(cards) > 0:
                    for card in cards:
                        txt = card.text.lower()
                        if es_self_titled:
                            if artista.lower() in txt: encontrado = True; break
                        else:
                            if album.lower() in txt: encontrado = True; break
                
                if encontrado:
                    print(f"[{total_leidos}] ✅ ESTÁ EN WEB: {album}")
                else:
                    print(f"[{total_leidos}] ❌ FALTA: {album}")
                    nuevos_para_anadir.append({
                        'Artista': artista,
                        'Álbum': album,
                        'Género': genero_global,
                        'Fecha': fecha,
                        'Spotify URL': spotify
                    })

    except Exception as e:
        print(f"\n💥 Error durante la ejecución del navegador: {e}")

    finally:
        print("\n🏁 Cerrando navegador...")
        driver.quit()


    # --- LÓGICA DE GUARDADO ---
    if not nuevos_para_anadir and not indices_para_actualizar:
        print("\n✨ No hay nada nuevo que añadir ni actualizar.")
        return

    print("\n" + "="*40)
    print("📢 RESUMEN DE CAMBIOS PENDIENTES")
    print("="*40)
    print(f"🔹 Género objetivo:      '{genero_global}'")
    print(f"🔹 Nuevos a añadir:      {len(nuevos_para_anadir)}")
    print(f"🔹 Existentes a editar:  {len(indices_para_actualizar)}")
    print("="*40)

    confirmacion = input("¿Confirmas aplicar este género a TODOS estos discos y guardar? (s/n): ").lower().strip()

    if confirmacion in ['s', 'si', 'y']:
        # 1. Aplicar cambios a los existentes
        for idx in indices_para_actualizar:
            lista_faltantes[idx]['Género'] = genero_global
        
        # 2. Añadir los nuevos
        lista_faltantes.extend(nuevos_para_anadir)
        
        # 3. Guardar archivo
        try:
            with open(NOMBRE_FALTANTES, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CAMPOS_CSV)
                writer.writeheader()
                writer.writerows(lista_faltantes)
            print(f"\n💾 ¡GUARDADO! Archivo '{NOMBRE_FALTANTES}' actualizado correctamente.")
        except Exception as e:
            print(f"\n❌ Error guardando el archivo: {e}")
    else:
        print("\n⛔ Operación cancelada. No se han guardado cambios.")

    input("\nPresiona ENTER para salir.")

if __name__ == "__main__":
    main()