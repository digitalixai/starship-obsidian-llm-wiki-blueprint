# Plan de Implementación: Publicación del Blueprint de Memoria LLM-Wiki (LMC)

**Fecha de generación:** 2026-07-08

Este plan detalla los pasos para preparar, licenciar y publicar el repositorio [starship-llm-wiki-blueprint](file:///Users/jorgeblackhawk/X26/starship-llm-wiki-blueprint) en GitHub bajo la cuenta del usuario (`github.com/jappy1961`), utilizando la licencia **Elastic License 2.0 (ELv2)** para proteger la propiedad intelectual contra explotación comercial no autorizada.

---

## User Review Required

> [!IMPORTANT]
> **Nombre del Proyecto:** Proponemos mantener el nombre oficial como **"Starship: Persistent Multi-Node LLM-Wiki Memory Blueprint"** (LMC - Local Memory Compounding), ya que describe perfectamente la capacidad de memoria persistente y sincronización en múltiples nodos de red.
>
> **Esquema de Licencia:** Se utilizará la **Elastic License 2.0 (ELv2)**. Esto permite el libre uso personal, educativo y experimental, pero prohíbe que terceros comercialicen el software como un servicio SaaS de pago.

---

## Open Questions

> [!WARNING]
> **Creación del Repositorio:** Dado que no disponemos de la herramienta CLI `gh` configurada y con tokens activos en esta terminal, el usuario deberá crear manualmente un repositorio **Público** vacío llamado `starship-llm-wiki-blueprint` en su cuenta de GitHub (`github.com/jappy1961`). Una vez creado, ejecutaremos la sincronización mediante SSH.

---

## Proposed Changes

### [License & Release Configuration]

#### [NEW] [LICENSE](file:///Users/jorgeblackhawk/X26/starship-llm-wiki-blueprint/LICENSE)
Crearemos el archivo de licencia oficial con el texto íntegro de **Elastic License 2.0 (ELv2)**.

#### [MODIFY] [README.md](file:///Users/jorgeblackhawk/X26/starship-llm-wiki-blueprint/README.md)
Actualizaremos la sección de Licencia en el archivo [README.md](file:///Users/jorgeblackhawk/X26/starship-llm-wiki-blueprint/README.md) para indicar explícitamente que está sujeto a la Elastic License 2.0 en lugar de la licencia MIT por defecto.

---

## Verification Plan

### Manual Verification
1. **Verificar Scripts y Limpieza:** Comprobar que no haya variables de entorno o tokens locales expuestos en los archivos de la carpeta `scripts/`.
2. **Crear Repo en GitHub:** El usuario crea el repositorio público `starship-llm-wiki-blueprint` en GitHub.
3. **Vincular y Push:**
   ```bash
   git remote add origin git@github.com:jappy1961/starship-llm-wiki-blueprint.git
   git branch -M main
   git push -u origin main
   ```
4. **Verificación en la Web:** Acceder a la URL pública y validar la correcta renderización del README.md, diagramas de Mermaid y el archivo LICENSE.
