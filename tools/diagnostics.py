def analyze_diagnostics(report):

    report.notes = []

    html = (
        getattr(report, "rendered_html", "")
        or getattr(report, "html", "")
    ).lower()

    scripts = " ".join(
        getattr(report, "scripts", [])
    ).lower()

    # Render Type
    if report.json_ld:
        report.render = "ssr"

    elif "__next" in html or "__nuxt" in html:
        report.render = "csr"

    else:
        report.render = "unknown"

    # Framework
    if "__next" in html:
        report.framework = "nextjs"

    elif "__nuxt" in html:
        report.framework = "nuxt"

    elif "react" in scripts:
        report.framework = "react"

    elif "vue" in scripts:
        report.framework = "vue"

    elif "angular" in scripts:
        report.framework = "angular"

    # Anti Bot
    report.anti_bot = []

    keywords = {
        "akamai": "akamai",
        "cloudflare": "cloudflare",
        "perimeterx": "perimeterx",
        "datadome": "datadome",
        "captcha": "captcha",
        "recaptcha": "recaptcha",
        "hcaptcha": "hcaptcha",
    }

    for key, value in keywords.items():

        if key in html or key in scripts:
            report.anti_bot.append(value)

    # Önerilen strateji
    if report.anti_bot:
        report.recommended_strategy = "playwright"

    elif report.render == "csr":
        report.recommended_strategy = "playwright"

    else:
        report.recommended_strategy = "requests"

    # Güven puanı
    score = 0

    if report.json_ld:
        score += 30

    if report.meta:
        score += 20

    if report.product_candidate:
        score += 20

    if report.api_endpoints:
        score += 10

    if report.scripts:
        score += 10

    if report.framework:
        score += 10

    report.confidence = min(score, 100)

    # Notlar
    if report.render == "csr":
        report.notes.append(
            "Client Side Rendering detected."
        )

    if report.anti_bot:
        report.notes.append(
            "Anti-bot protection detected."
        )

    if report.api_endpoints:
        report.notes.append(
            f"{len(report.api_endpoints)} API endpoint(s) detected."
        )

    return report