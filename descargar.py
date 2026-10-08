import os
from playwright.sync_api import sync_playwright

USUARIO = os.environ["UC3M_USER"]
CLAVE = os.environ["UC3M_PASS"]
URL_ICS = os.environ["UC3M_ICS_URL"]
CANAL = os.environ.get("NAVEGADOR")

HORARIO = "https://aplicaciones.uc3m.es/horarios-web/alumno/verHorario.page"

with sync_playwright() as p:
    if CANAL:
        navegador = p.chromium.launch(channel=CANAL)
    else:
        navegador = p.chromium.launch()
    page = navegador.new_page()

    page.goto(HORARIO)
    page.get_by_role("textbox", name="Usuario").fill(USUARIO)
    page.get_by_role("textbox", name="Contraseña").fill(CLAVE)
    page.get_by_role("button", name="Aceptar").click()
    page.wait_for_url("https://aplicaciones.uc3m.es/horarios-web/**", timeout=30000)

    respuesta = page.context.request.get(URL_ICS)
    texto = respuesta.text()

    if not texto.startswith("BEGIN:VCALENDAR"):
        raise SystemExit("No se descargó un .ics válido. Revisa el login o la URL.")

    with open("horario.ics", "w", encoding="utf-8") as f:
        f.write(texto)
    print("OK: horario.ics guardado,", texto.count("BEGIN:VEVENT"), "eventos")

    navegador.close()
