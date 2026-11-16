import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

def get_fonts():
    try:
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 50)
        h2_font = ImageFont.truetype(FONT_BOLD_PATH, 38)
        body_font = ImageFont.truetype(FONT_REG_PATH, 23)
        tag_font = ImageFont.truetype(FONT_BOLD_PATH, 18)
        badge_font = ImageFont.truetype(FONT_BOLD_PATH, 16)
        logo_font = ImageFont.truetype(FONT_BOLD_PATH, 26)
        sublogo_font = ImageFont.truetype(FONT_REG_PATH, 15)
    except Exception as e:
        print("Font fallback:", e)
        f = ImageFont.load_default()
        return f, f, f, f, f, f, f
    return title_font, h2_font, body_font, tag_font, badge_font, logo_font, sublogo_font

def create_banner(output_path, category_tag, title, subtitle, badge_text="Verifizierter Guide", theme="red"):
    W, H = 1200, 630
    title_font, h2_font, body_font, tag_font, badge_font, logo_font, sublogo_font = get_fonts()

    # Themes
    if theme == "amber":
        accent = (245, 158, 11)      # #F59E0B
        glow_primary = (245, 158, 11)
    elif theme == "blue":
        accent = (37, 99, 235)       # #2563EB
        glow_primary = (37, 99, 235)
    elif theme == "emerald":
        accent = (16, 185, 129)      # #10B981
        glow_primary = (16, 185, 129)
    else: # red
        accent = (220, 38, 38)       # #DC2626
        glow_primary = (220, 38, 38)

    base = Image.new("RGB", (W, H), (11, 12, 16))

    # Glow layer
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([(-120, -120), (450, 450)], fill=(glow_primary[0], glow_primary[1], glow_primary[2], 120))
    glow_draw.ellipse([(W - 400, H - 380), (W + 150, H + 150)], fill=(245, 158, 11, 90))
    glow_draw.ellipse([(W - 480, -100), (W + 100, 380)], fill=(37, 99, 235, 70))
    glow_draw.ellipse([(-80, H - 320), (320, H + 120)], fill=(16, 185, 129, 60))

    glow = glow.filter(ImageFilter.GaussianBlur(85))
    base.paste(glow, (0, 0), glow)

    # Grid lines
    grid_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_img)
    spacing = 48
    for x in range(0, W, spacing):
        grid_draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H, spacing):
        grid_draw.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

    base.paste(grid_img, (0, 0), grid_img)

    # Main Card Layer
    card_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card_img)

    card_x0, card_y0 = 60, 50
    card_x1, card_y1 = W - 60, H - 50
    card_radius = 24

    draw.rounded_rectangle(
        [(card_x0, card_y0), (card_x1, card_y1)],
        radius=card_radius,
        fill=(18, 20, 29, 235),
        outline=(255, 255, 255, 30),
        width=1
    )

    # Top accent line
    draw.rounded_rectangle(
        [(card_x0 + 40, card_y0), (card_x0 + 260, card_y0 + 3)],
        radius=2,
        fill=(accent[0], accent[1], accent[2], 255)
    )

    # Header Row
    header_x = card_x0 + 50
    header_y = card_y0 + 40

    icon_w = 42
    draw.rounded_rectangle(
        [(header_x, header_y), (header_x + icon_w, header_y + icon_w)],
        radius=10,
        fill=(accent[0], accent[1], accent[2], 240)
    )
    draw.polygon(
        [(header_x + 16, header_y + 11), (header_x + 16, header_y + 31), (header_x + 31, header_y + 21)],
        fill=(255, 255, 255, 255)
    )

    draw.text((header_x + 56, header_y + 5), "IPTV DEUTSCHLAND", font=logo_font, fill=(255, 255, 255, 255))
    draw.text((header_x + 56, header_y + 32), "PREMIUM 4K STREAMING", font=sublogo_font, fill=(156, 163, 175, 255))

    # Top Right Badge
    b_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    text_w = b_bbox[2] - b_bbox[0]
    badge_w = text_w + 50
    badge_h = 36
    badge_x = card_x1 - 50 - badge_w
    badge_y = header_y + 3

    draw.rounded_rectangle(
        [(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)],
        radius=18,
        fill=(accent[0], accent[1], accent[2], 30),
        outline=(accent[0], accent[1], accent[2], 120),
        width=1
    )
    draw.ellipse([(badge_x + 14, badge_y + 14), (badge_x + 22, badge_y + 22)], fill=(16, 185, 129, 255))
    draw.text((badge_x + 32, badge_y + 8), badge_text, font=badge_font, fill=(243, 244, 246, 255))

    # Category Tag
    tag_y = header_y + 72
    t_bbox = draw.textbbox((0, 0), category_tag.upper(), font=tag_font)
    t_w = t_bbox[2] - t_bbox[0]
    draw.rounded_rectangle(
        [(header_x, tag_y), (header_x + t_w + 24, tag_y + 30)],
        radius=8,
        fill=(255, 255, 255, 15),
        outline=(255, 255, 255, 30),
        width=1
    )
    draw.text((header_x + 12, tag_y + 5), category_tag.upper(), font=tag_font, fill=(245, 158, 11, 255))

    # Title Wrapping
    content_y = tag_y + 48
    content_max_w = card_x1 - card_x0 - 100

    words = title.split()
    lines = []
    current_line = []
    for w in words:
        test_line = " ".join(current_line + [w])
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if (bbox[2] - bbox[0]) < content_max_w:
            current_line.append(w)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))

    if len(lines) > 2:
        title_use_font = h2_font
        lines = []
        current_line = []
        for w in words:
            test_line = " ".join(current_line + [w])
            bbox = draw.textbbox((0, 0), test_line, font=title_use_font)
            if (bbox[2] - bbox[0]) < content_max_w:
                current_line.append(w)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [w]
        if current_line:
            lines.append(" ".join(current_line))
    else:
        title_use_font = title_font

    line_y = content_y
    for l in lines[:2]:
        draw.text((header_x, line_y), l, font=title_use_font, fill=(255, 255, 255, 255))
        bbox = draw.textbbox((0, 0), l, font=title_use_font)
        line_y += (bbox[3] - bbox[1]) + 14

    # Subtitle
    sub_y = line_y + 12
    draw.text((header_x, sub_y), subtitle, font=body_font, fill=(209, 213, 219, 255))

    # Bottom Features
    bottom_y = card_y1 - 65
    features = [
        ("4K ULTRA HD / 60 FPS", (220, 38, 38)),
        ("ANTI-FREEZE 9.8™", (245, 158, 11)),
        ("99.9% UPTIME CDN", (16, 185, 129)),
        ("WHATSAPP SUPPORT", (37, 99, 235))
    ]

    curr_pill_x = header_x
    for feat_text, col in features:
        f_bbox = draw.textbbox((0, 0), feat_text, font=badge_font)
        f_w = f_bbox[2] - f_bbox[0]
        pill_w = f_w + 36
        draw.rounded_rectangle(
            [(curr_pill_x, bottom_y), (curr_pill_x + pill_w, bottom_y + 36)],
            radius=18,
            fill=(col[0], col[1], col[2], 25),
            outline=(col[0], col[1], col[2], 90),
            width=1
        )
        draw.ellipse([(curr_pill_x + 12, bottom_y + 14), (curr_pill_x + 20, bottom_y + 22)], fill=(col[0], col[1], col[2], 255))
        draw.text((curr_pill_x + 26, bottom_y + 8), feat_text, font=badge_font, fill=(243, 244, 246, 255))
        curr_pill_x += pill_w + 14

    base.paste(card_img, (0, 0), card_img)

    final_img = base.convert("RGB")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path, "WEBP", quality=92, method=6)
    print(f"Generated: {output_path}")

ALL_IMAGES = [
    # 1. 10 Guides
    {
        "path": "public/images/guides/ist-iptv-legal-deutschland.webp",
        "tag": "Rechtlicher Ratgeber",
        "title": "Ist IPTV legal in Deutschland?",
        "subtitle": "Urheberrecht (UrhG) • EuGH Urteil • Grauzonen & Schutzmaßnahmen",
        "badge": "Verifizierter Guide",
        "theme": "red"
    },
    {
        "path": "public/images/guides/iptv-abmahnung-strafe.webp",
        "tag": "Recht & Abmahnung",
        "title": "IPTV Abmahnung & Strafen 2026",
        "subtitle": "Was droht bei Streaming? • Fakten, IP-Logs & wie Sie sich schützen",
        "badge": "Rechtsberatung Analyse",
        "theme": "amber"
    },
    {
        "path": "public/images/guides/bundesliga-streaming-guide.webp",
        "tag": "Sport Streaming 4K",
        "title": "Bundesliga Live Streamen",
        "subtitle": "Alle Spiele Freitag bis Sonntag in UHD 60FPS • Ohne teure Einzel-Abos",
        "badge": "4K UHD 60 FPS",
        "theme": "emerald"
    },
    {
        "path": "public/images/guides/iptv-kaufen-anleitung.webp",
        "tag": "Schritt-für-Schritt",
        "title": "IPTV Kaufen: Schritt-für-Schritt",
        "subtitle": "M3U Playlists • Xtream Codes • Express-Aktivierung in unter 2 Minuten",
        "badge": "Einrichtungs-Guide",
        "theme": "blue"
    },
    {
        "path": "public/images/guides/was-ist-iptv-guide.webp",
        "tag": "Grundlagen-Wissen",
        "title": "Was ist IPTV? Alles einfach erklärt",
        "subtitle": "Internet Protocol TV vs. Kabel & Satellit • M3U, EPG & Streaming",
        "badge": "Streaming Grundlagen",
        "theme": "red"
    },
    {
        "path": "public/images/guides/beste-iptv-app-vergleich.webp",
        "tag": "App & Player Test",
        "title": "Die besten IPTV Player Apps 2026",
        "subtitle": "TiviMate • IPTV Smarters • XCIPTV • Für Fire TV, Smart TV & Android",
        "badge": "Top Apps 2026",
        "theme": "amber"
    },
    {
        "path": "public/images/guides/formel-1-streaming-guide.webp",
        "tag": "Motorsport Live",
        "title": "Formel 1 Live Streamen in 4K",
        "subtitle": "Alle Rennwochenenden • Freies Training, Qualifying & Rennen werbefrei",
        "badge": "Motorsport 4K",
        "theme": "red"
    },
    {
        "path": "public/images/guides/iptv-paypal-kaeuferschutz.webp",
        "tag": "Sichere Bezahlung",
        "title": "IPTV Sicher mit PayPal Bezahlen",
        "subtitle": "Voller Käuferschutz • Keine Kreditkartendaten • Sofortige Freischaltung",
        "badge": "100% Käuferschutz",
        "theme": "emerald"
    },
    {
        "path": "public/images/guides/iptv-oesterreich-schweiz-dach.webp",
        "tag": "DACH Region",
        "title": "IPTV in Österreich & Schweiz",
        "subtitle": "ORF, SRF, Deutsche Sender & International • Ohne Geoblocking",
        "badge": "DACH Streaming",
        "theme": "blue"
    },
    {
        "path": "public/images/guides/champions-league-streaming-guide.webp",
        "tag": "Europäischer Fußball",
        "title": "Champions League Live Streamen",
        "subtitle": "Alle Einzelspiele, Konferenzen & Finals in echtem Ultra HD 60 FPS",
        "badge": "Live Fußball 4K",
        "theme": "emerald"
    },

    # 2. 13 Main Pages
    {
        "path": "public/images/pages/og-home.webp",
        "tag": "Premium Plattform",
        "title": "IPTV Deutschland — Testsieger 2026",
        "subtitle": "24.000+ Sender in 4K/8K • Bundesliga live • Anti-Freeze 9.8™ • Keine Bindung",
        "badge": "Testsieger 2026",
        "theme": "red"
    },
    {
        "path": "public/images/pages/iptv-kaufen.webp",
        "tag": "Tarife & Pakete",
        "title": "IPTV Kaufen Deutschland — Ab 8 €",
        "subtitle": "12 Monate für 55 € inkl. Bonusmonat • 2 Minuten Express Aktivierung",
        "badge": "Beliebteste Wahl",
        "theme": "red"
    },
    {
        "path": "public/images/pages/bester-iptv-anbieter.webp",
        "tag": "Vergleich & Test",
        "title": "Bester IPTV Anbieter Deutschland",
        "subtitle": "Stabilität, Senderangebot, Bildqualität und WhatsApp-Support im Test",
        "badge": "Note 1,1 Sehr Gut",
        "theme": "amber"
    },
    {
        "path": "public/images/pages/iptv-preise.webp",
        "tag": "Preisübersicht",
        "title": "IPTV Preise & Tarife 2026",
        "subtitle": "1, 3, 6 & 12 Monate • Keine versteckten Kosten • Rechnerisch ab 4,58 € / Mo",
        "badge": "Transparente Preise",
        "theme": "emerald"
    },
    {
        "path": "public/images/pages/iptv-erfahrungen.webp",
        "tag": "Verifizierte Bewertungen",
        "title": "IPTV Erfahrungen & Bewertungen",
        "subtitle": "4.9 von 5.0 Sternen bei über 1.840 verifizierten Kundenberichten",
        "badge": "4.9 / 5.0 Sterne",
        "theme": "amber"
    },
    {
        "path": "public/images/pages/iptv-senderliste.webp",
        "tag": "Programmübersicht",
        "title": "24.000+ Sender & EPG TV-Guide",
        "subtitle": "Komplette Senderliste für Deutschland, Österreich, Schweiz & International",
        "badge": "24.000+ Kanäle",
        "theme": "blue"
    },
    {
        "path": "public/images/pages/iptv-germany-hub.webp",
        "tag": "Germany Hub",
        "title": "IPTV Germany Streaming Guide",
        "subtitle": "German TV Channels, Bundesliga Live & Worldwide Networks in 4K UHD",
        "badge": "Germany Hub",
        "theme": "red"
    },
    {
        "path": "public/images/pages/landing-sport.webp",
        "tag": "Spitzensport Live",
        "title": "Live Sport IPTV Streaming in 4K",
        "subtitle": "Bundesliga, Motorsport, Tennis & US-Sport in flüssigen 60 FPS ohne Verzögerung",
        "badge": "Ultra HD 60 FPS",
        "theme": "emerald"
    },
    {
        "path": "public/images/pages/landing-devices.webp",
        "tag": "Hardware & Geräte",
        "title": "IPTV für Smart TV, Fire TV & iOS",
        "subtitle": "Samsung Tizen, LG webOS, Amazon Fire TV, Apple TV, Android & Windows",
        "badge": "Multi-Device",
        "theme": "blue"
    },
    {
        "path": "public/images/pages/iptv-referral.webp",
        "tag": "Partnerprogramm",
        "title": "Freunde Werben & Sparen",
        "subtitle": "Empfehlen Sie IPTV Deutschland und sichern Sie sich Gratismonate & Prämien",
        "badge": "Prämienprogramm",
        "theme": "amber"
    },
    {
        "path": "public/images/pages/iptv-kontakt.webp",
        "tag": "Kundenservice",
        "title": "24/7 WhatsApp Support & Kontakt",
        "subtitle": "Persönlicher Kundenservice in deutscher Sprache • 2 Minuten Antwortzeit",
        "badge": "24/7 WhatsApp",
        "theme": "emerald"
    },
    {
        "path": "public/images/pages/iptv-guides-hub.webp",
        "tag": "Wissenscenter",
        "title": "IPTV Ratgeber & Streaming Guides",
        "subtitle": "Umfassende Anleitungen, rechtliche Einordnung & Experten-Tipps",
        "badge": "Wissenscenter",
        "theme": "blue"
    },
    {
        "path": "public/images/pages/iptv-germany-en.webp",
        "tag": "English Edition",
        "title": "IPTV Germany — Premium 4K TV",
        "subtitle": "German & International Channels • Fast WhatsApp Setup • Anti-Freeze 9.8™",
        "badge": "English Edition",
        "theme": "red"
    },

    # 3. 15 Cities
    {
        "path": "public/images/locations/city-berlin.webp",
        "tag": "Standort Berlin",
        "title": "IPTV Kaufen in Berlin — 4K Streaming",
        "subtitle": "1. FC Union Berlin & Hertha BSC • Direkte DE-CIX Anbindung (11ms Ping)",
        "badge": "Highspeed Berlin",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-muenchen.webp",
        "tag": "Standort München",
        "title": "IPTV Kaufen in München — 4K Streaming",
        "subtitle": "FC Bayern München • M-net, Telekom Glasfaser & Vodafone (9ms Ping)",
        "badge": "Highspeed München",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-hamburg.webp",
        "tag": "Standort Hamburg",
        "title": "IPTV Kaufen in Hamburg — 4K Streaming",
        "subtitle": "Hamburger SV & FC St. Pauli • willy.tel & wilhelm.tel Highspeed (12ms)",
        "badge": "Highspeed Hamburg",
        "theme": "blue"
    },
    {
        "path": "public/images/locations/city-koeln.webp",
        "tag": "Standort Köln",
        "title": "IPTV Kaufen in Köln — 4K Streaming",
        "subtitle": "1. FC Köln & Fortuna Köln • NetCologne Glasfaseranbindung (10ms Ping)",
        "badge": "Highspeed Köln",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-frankfurt.webp",
        "tag": "Standort Frankfurt",
        "title": "IPTV Kaufen in Frankfurt — 4K Streaming",
        "subtitle": "Eintracht Frankfurt • Direktanbindung an weltgrößten Internetknoten DE-CIX (4ms)",
        "badge": "DE-CIX 4ms Ping",
        "theme": "emerald"
    },
    {
        "path": "public/images/locations/city-stuttgart.webp",
        "tag": "Standort Stuttgart",
        "title": "IPTV Kaufen in Stuttgart — 4K Streaming",
        "subtitle": "VfB Stuttgart & Kickers • Baden-Württemberg Highspeed Server (8ms Ping)",
        "badge": "Highspeed Stuttgart",
        "theme": "amber"
    },
    {
        "path": "public/images/locations/city-duesseldorf.webp",
        "tag": "Standort Düsseldorf",
        "title": "IPTV Kaufen in Düsseldorf — 4K",
        "subtitle": "Fortuna Düsseldorf • NRW Glasfaser Streaming mit Anti-Freeze 9.8™ (10ms)",
        "badge": "Highspeed NRW",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-leipzig.webp",
        "tag": "Standort Leipzig",
        "title": "IPTV Kaufen in Leipzig — 4K Streaming",
        "subtitle": "RB Leipzig & Chemie Leipzig • Sachsen Highspeed Server (13ms Ping)",
        "badge": "Highspeed Leipzig",
        "theme": "blue"
    },
    {
        "path": "public/images/locations/city-dortmund.webp",
        "tag": "Standort Dortmund",
        "title": "IPTV Kaufen in Dortmund — 4K",
        "subtitle": "Borussia Dortmund (BVB) • DOKOM21 & Telekom Glasfaser (11ms Ping)",
        "badge": "Highspeed BVB",
        "theme": "amber"
    },
    {
        "path": "public/images/locations/city-essen.webp",
        "tag": "Standort Essen",
        "title": "IPTV Kaufen in Essen — 4K Streaming",
        "subtitle": "Rot-Weiss Essen • Ruhrgebiet Highspeed IPTV mit 99.9% Uptime (11ms)",
        "badge": "Ruhrgebiet CDN",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-bremen.webp",
        "tag": "Standort Bremen",
        "title": "IPTV Kaufen in Bremen — 4K Streaming",
        "subtitle": "SV Werder Bremen • Norddeutschland Highspeed CDN (12ms Ping)",
        "badge": "Highspeed Bremen",
        "theme": "emerald"
    },
    {
        "path": "public/images/locations/city-dresden.webp",
        "tag": "Standort Dresden",
        "title": "IPTV Kaufen in Dresden — 4K Streaming",
        "subtitle": "SG Dynamo Dresden • Sachsen Highspeed Server mit Anti-Freeze 9.8™ (14ms)",
        "badge": "Highspeed Dresden",
        "theme": "amber"
    },
    {
        "path": "public/images/locations/city-hannover.webp",
        "tag": "Standort Hannover",
        "title": "IPTV Kaufen in Hannover — 4K",
        "subtitle": "Hannover 96 • Niedersachsen Highspeed CDN (10ms Ping)",
        "badge": "Highspeed Hannover",
        "theme": "emerald"
    },
    {
        "path": "public/images/locations/city-nuernberg.webp",
        "tag": "Standort Nürnberg",
        "title": "IPTV Kaufen in Nürnberg — 4K",
        "subtitle": "1. FC Nürnberg (Der Club) • Franken Highspeed Server (9ms Ping)",
        "badge": "Highspeed Franken",
        "theme": "red"
    },
    {
        "path": "public/images/locations/city-duisburg.webp",
        "tag": "Standort Duisburg",
        "title": "IPTV Kaufen in Duisburg — 4K",
        "subtitle": "MSV Duisburg • Niederrhein Highspeed Server mit 99.9% Uptime (11ms Ping)",
        "badge": "Highspeed Duisburg",
        "theme": "blue"
    },

    # 4. 4 Comparisons
    {
        "path": "public/images/compare/compare-pay-tv.webp",
        "tag": "Vergleichs-Analyse",
        "title": "IPTV vs. Traditionelles Pay-TV",
        "subtitle": "Bis zu 80% Ersparnis • Alle Spiele gebündelt • Ohne 24-Monats-Vertrag",
        "badge": "80% Ersparnis",
        "theme": "red"
    },
    {
        "path": "public/images/compare/compare-einzel-abos.webp",
        "tag": "Vergleichs-Analyse",
        "title": "IPTV vs. Fragmentierte Sport-Abos",
        "subtitle": "Keine 3 getrennten Monatsabos mehr nötig • Alle Ligen auf 1 Plattform",
        "badge": "Alles in Einem",
        "theme": "emerald"
    },
    {
        "path": "public/images/compare/compare-kabel-fernsehen.webp",
        "tag": "Vergleichs-Analyse",
        "title": "IPTV vs. Klassisches Kabel-TV",
        "subtitle": "Post-Nebenkostenprivileg • Keine Kabeldose & kein Receiverzwang nötig",
        "badge": "Ohne Kabelgebühr",
        "theme": "amber"
    },
    {
        "path": "public/images/compare/compare-basis-ott.webp",
        "tag": "Vergleichs-Analyse",
        "title": "IPTV vs. Standard Web-TV",
        "subtitle": "Volles Live-Sport Programm in 4K 60FPS statt kastrierter Basistarife",
        "badge": "Volles Programm",
        "theme": "blue"
    },

    # 5. Global Defaults
    {
        "path": "public/images/og-banner.webp",
        "tag": "Premium Plattform",
        "title": "IPTV Deutschland — Testsieger Streaming",
        "subtitle": "24.000+ Sender in 4K/8K • Bundesliga live • Anti-Freeze 9.8™ • Keine Bindung",
        "badge": "Testsieger 2026",
        "theme": "red"
    },
    {
        "path": "public/images/hero-bg.webp",
        "tag": "High-Speed CDN",
        "title": "IPTV Deutschland — Ultra HD 4K & 8K",
        "subtitle": "Ultraschnelle Server mit 99.9% Uptime und 2 Minuten Express Aktivierung",
        "badge": "Ultra HD 4K",
        "theme": "emerald"
    }
]

if __name__ == "__main__":
    print(f"Generating {len(ALL_IMAGES)} high-quality WebP banners...")
    for item in ALL_IMAGES:
        create_banner(
            output_path=item["path"],
            category_tag=item["tag"],
            title=item["title"],
            subtitle=item["subtitle"],
            badge_text=item["badge"],
            theme=item["theme"]
        )
    print("All banners generated successfully!")
