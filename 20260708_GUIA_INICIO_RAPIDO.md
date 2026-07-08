# Guía de Inicio Rápido: Configura la Memoria de tu IA (LMC) desde Cero

**Fecha de generación:** 2026-07-08

Esta guía está diseñada para personas **no técnicas** que quieren instalar y configurar el sistema de memoria persistente para su asistente de IA de forma fácil y paso a paso.

---

## 🛠️ Paso 1: Descargar e Instalar los Programas

Debes instalar tres programas gratuitos en las computadoras que quieras sincronizar:

1.  **Obsidian (El visualizador de notas):**
    *   **Qué es:** El programa donde verás y editarás la memoria de tu IA en carpetas organizadas.
    *   **Descarga:** Entra a [obsidian.md](https://obsidian.md/) y descárgalo para tu sistema operativo (Mac o Windows). Instálalo de forma normal.
2.  **Syncthing (El sincronizador privado):**
    *   **Qué es:** Sincroniza tus archivos entre tus computadoras directamente (P2P), sin subir nada a la nube de Google, Dropbox o Apple.
    *   **Descarga:** Entra a [syncthing.net](https://syncthing.net/) y descárgalo.
        *   *En Mac:* Se recomienda usar **Syncthing-macOS** (un instalador que corre en la barra de tareas).
        *   *En Windows:* Descarga **SyncTrayzor**.
3.  **Python y Git (Para las automatizaciones):**
    *   **Qué es:** Permiten que corran los scripts automáticos que envían tus chats a Obsidian.
    *   **Instalación:**
        *   *En Mac:* Abre la aplicación **Terminal** (búscala en tu Spotlight con `Cmd + Espacio`) y escribe: `git --version`. Si no está instalado, tu Mac te preguntará automáticamente si deseas instalar las herramientas de desarrollo de Xcode. Dile que **Sí**.
        *   *En Windows:* Descarga e instala Git desde [git-scm.com](https://git-scm.com/) y Python 3 desde la tienda oficial de Windows Microsoft Store.

---

## 📂 Paso 2: Crear las Carpetas en tu Computadora

Elige una computadora como tu "máquina principal". 

1.  Abre tu carpeta de **Documentos** y crea una carpeta llamada: **`MemoriaIA`**.
2.  Dentro de la carpeta `MemoriaIA`, crea las siguientes subcarpetas exactamente con estos nombres en minúsculas:
    *   `raw/` (aquí arrastrarás documentos PDF, imágenes o textos de referencia que quieras que la IA recuerde).
    *   `wiki/` (aquí es donde la IA escribirá sus notas).
3.  Dentro de la carpeta `wiki/`, crea estas subcarpetas:
    *   `concepts/`
    *   `entities/`
4.  Crea un archivo de texto vacío dentro de `wiki/` llamado **`index.md`** y otro llamado **`log.md`**.

*Tu estructura debe verse así:*
```text
Documentos/
└── MemoriaIA/
    ├── raw/
    ├── wiki/
    │   ├── index.md
    │   ├── log.md
    │   ├── concepts/
    │   └── entities/
    └── AGENTS.md
```

---

## 🛰️ Paso 3: Configurar la Sincronización (Syncthing)

Si solo usas una computadora, puedes saltarte este paso. Si tienes dos o más:

1.  Abre **Syncthing** en ambas computadoras.
2.  En la Computadora A, haz clic en **Acciones** (arriba a la derecha) -> **Mostrar ID**. Copia ese código largo.
3.  En la Computadora B, haz clic en **Añadir dispositivo** e introduce el ID de la Computadora A.
4.  En la pestaña de carpetas de Syncthing, añade la carpeta `MemoriaIA` (busca la ruta física: `/Users/tu-usuario/Documents/MemoriaIA` en Mac o `C:\Users\tu-usuario\Documents\MemoriaIA` en Windows).
5.  Marca la casilla para **Compartir** esa carpeta con la otra computadora.
6.  Acepta la sincronización en la otra computadora. ¡Listo! Los archivos que guardes en una se copiarán solos a la otra.

---

## 🚀 Paso 4: Activar y Usar tu Memoria

1.  **Abre Obsidian:** Abre Obsidian y selecciona la opción *"Open folder as vault"* (Abrir carpeta como bóveda). Selecciona tu carpeta **`MemoriaIA`**.
2.  **Copia las Instrucciones de la IA:** Copia el archivo [AGENTS.md](https://github.com/digitalixai/starship-obsidian-llm-wiki-blueprint/blob/main/AGENTS.md) de nuestro blueprint y pégalo en la raíz de tu carpeta `MemoriaIA`.
3.  **Dale las instrucciones a tu Chat de IA:** Cada vez que comiences un nuevo chat con tu asistente de IA, dile:
    > *"Por favor lee el archivo AGENTS.md en mi carpeta de memoria y actúa bajo las directivas del Protocolo de Bibliotecario."*
4.  **Sincronizar conversaciones al final del día:**
    Abre tu terminal, navega a tu carpeta y corre el script de sincronización para que tus conversaciones se guarden en tu Obsidian en la sección de diarios:
    ```bash
    python3 scripts/obsidian_sync_transcript.py
    ```

¡Eso es todo! Ahora tu asistente de IA irá acumulando su memoria directamente en tu computadora de forma 100% privada y segura.
