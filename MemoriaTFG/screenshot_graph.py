from playwright.sync_api import sync_playwright
import os

HTML = os.path.abspath("code_review_graph/graph.html")
OUT  = os.path.abspath("imagenes/code_review_graph.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(
        viewport={"width": 2560, "height": 1440},
        device_scale_factor=2,          # 5120 x 2880 px de salida
    )
    page = ctx.new_page()
    page.goto(f"file://{HTML}")

    # Esperar a que D3 cargue y la simulación empiece
    page.wait_for_function("typeof simulation !== 'undefined'", timeout=15000)

    # Esperar a que la simulación se estabilice (alpha < 0.001)
    page.wait_for_function(
        "() => simulation.alpha() < 0.001",
        timeout=60000,
        polling=500,
    )

    # fitGraph ya se habrá llamado en "end"; dar tiempo a la transición (600ms) + extra
    page.wait_for_timeout(1200)

    # Ocultar controles y barras de UI para imagen limpia
    page.evaluate("""() => {
        const hide = ['#controls', '#stats-bar', '#search-results', '#tooltip'];
        hide.forEach(sel => {
            const el = document.querySelector(sel);
            if (el) el.style.display = 'none';
        });
    }""")

    page.screenshot(path=OUT, full_page=False)
    browser.close()

print(f"Guardado en: {OUT}")
