"""Builds projects/<slug>.html from the content below.

Run from the portfolio folder:  python tools/build_projects.py
Edit the text here, run it again, and refresh the browser.
"""
import os, json, hashlib, base64
from PIL import Image

SITE = "https://tomasko.dev"
INLINE_JS = "document.documentElement.classList.add('js');window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)};"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "projects")

# ---------- small HTML helpers ----------

def cards(items):
    return '<div class="pg-grid">' + "".join(f"<div class='pg-card'><h3>{t}</h3><p>{p}</p></div>" for t, p in items) + "</div>"

def table(head, rows):
    h = "".join(f"<th>{c or '<span class=\"sr-only\">Detail</span>'}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="pg-table" tabindex="0"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'

def steps(items):
    return '<ol class="pg-steps">' + "".join(f"<li><div>{x}</div></li>" for x in items) + "</ol>"

def dims(src):
    with Image.open(os.path.join(ROOT, "assets", "projects", src)) as im:
        return im.size


def fig(src, cap, wide=False):
    cls = "pg-fig wide" if wide else "pg-fig"
    w, h = dims(src)
    return f'<figure class="{cls}"><img src="../assets/projects/{src}" width="{w}" height="{h}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'

def callout(title, text):
    return f'<div class="pg-callout"><b>{title}</b><p>{text}</p></div>'

def ul(items):
    return '<ul class="pg-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def code(text):
    return f'<pre class="pg-code" tabindex="0"><code>{text}</code></pre>'

# ---------- project content ----------

PROJECTS = []

# ===================== ALMIBOOST =====================
PROJECTS.append(dict(
    slug="almiboost", num="001", title="AlmiBoost",
    kicker="NFC review cards · web shop · sales",
    lead="NFC cards that turn one phone tap into a Google review. I built the whole thing around them: the online shop, a 3D card designer, payments, invoices and an admin panel, plus the hardware sourcing and the door-to-door sales behind it.",
    cover="almiboost-cover.webp",
    meta=[("Role", "Co-founder &amp; CTO"), ("Timeline", "Jun 2026 – present"), ("Status", "Live, taking orders"),
          ("Stack", "Next.js, React, TypeScript, Tailwind, Postgres, Vercel")],
    links=[("Visit almiboost.com", "https://www.almiboost.com/")],
    next=("almiboost-scout", "AlmiBoost Scout"),
    sections=[
        ("overview", "Overview", f"""
<p>AlmiBoost sells small NFC cards to local businesses. A customer holds a phone against the card and the Google review form for that business opens straight away. There is no app, no QR code and no searching for the profile. The cards are programmed for each customer's own Google profile before they ship.</p>
<p>The company is run by three students, and I am the CTO. That means I own the technical side end to end: the hardware supply chain, the website and shop, and a good part of the in-person selling. This page covers the website and shop in detail, because that is the largest piece of software I have shipped.</p>
"""),
        ("problem", "The problem", """
<p>Google reviews decide whether a customer picks one shop or the one down the street. Most owners know this, but asking for a review is awkward and the customer usually postpones it. By the time they find the profile, tap through to the form and start writing, many have given up.</p>
<p>A QR code removes some friction but still needs the camera, a scan, and often a second tap. An NFC card removes the rest: the form is open the moment the phone touches the card. The product is simple, so the work was in making it easy to buy, easy to customise, and easy for a three-person team to fulfil without errors.</p>
"""),
        ("product", "The product line", f"""
<p>The shop sells seven stock products and a fully custom card.</p>
{table(["Product", "Details"], [
    ["Standard Google review card", "85 × 54 mm, the size of a payment card. Fits next to the till. From €14.99."],
    ["Round card", "A 100 mm round sticker-style card, the most visible option on a counter. €19.99."],
    ["Square Google card", "A square format for a counter or window."],
    ["Menu card", "Opens a restaurant's menu on tap."],
    ["Instagram, TikTok, Facebook cards", "Open the business's social profile on tap."],
    ["Custom card", "Own logo, print and size, designed in the browser (see the configurator below)."],
])}
<p>Volume discounts apply across the whole basket: 3 pieces 10%, 5 pieces 15%, 10 pieces 20%, 20 pieces 25%. Each review-card chip is programmed for the customer's Google profile, which we look up ourselves from the business name and address, so the customer does not have to hunt for a link.</p>
{fig("almiboost-product.webp", "A product page with a draggable 3D card, live stock status and the volume-discount selector.")}
"""),
        ("built", "What I built", cards([
            ("Storefront and product pages", "Product grid, stock badges and a 3D card viewer you can drag to rotate and double-click to flip. The 3D card uses the real millimetre dimensions of each product, so the preview matches what arrives."),
            ("Custom card configurator", "Pick one of the preset sizes (from 45 × 25 mm up to 100 mm round) or enter your own size, upload artwork, crop it in a modal, and check it for print readiness. A live price with the volume discount updates as you go."),
            ("Checkout without registration", "Cart, delivery and payment in one flow. One order can cover several businesses, each with its own address and cards, which is how a small chain or a landlord actually buys."),
            ("Online payments", "Card, Apple Pay, Google Pay and bank buttons through the GoPay gateway. Bank transfer and cash on personal pickup are also supported, and the form only offers combinations that make sense."),
            ("Delivery options", "Packeta pickup point (free above a set order value), courier, personal pickup in Bratislava, or us installing the card in person. A Packeta point picker is built into the checkout."),
            ("Invoices", "A PDF tax document is generated for each order with pdf-lib and an embedded font, so Slovak characters render correctly. All the arithmetic is done in whole cents to avoid rounding errors."),
            ("Admin panel", "A protected area to see orders, change status, trigger payment and e-mail actions, upload invoices, see stats cards and switch products in or out of stock."),
            ("Content and SEO", "Twelve blog posts and guide pages about getting Google reviews, NFC versus QR codes, and local SEO, with a sitemap, dynamic share images and rich structured data on every page."),
        ])),
        ("architecture", "How an order flows through the system", f"""
<p>The site is a Next.js application deployed on Vercel. Pages render on the server; mutations go through route handlers. Postgres holds orders, Vercel Blob holds uploaded designs and invoices, GoPay handles money, and a scheduled job nags unpaid orders.</p>
{steps([
    "The customer fills the basket or the configurator. Nothing the browser sends about price is trusted.",
    "The order route validates the input with Zod, then recalculates the price on the server from the shared price tables: product price, volume discount, delivery price and, for custom cards, the setup fee.",
    "The order is stored in Postgres with a short human-readable number (like #0012) from a database sequence. Custom orders also store the design file URL and a JSON spec.",
    "For card payments the server creates a GoPay payment and redirects the customer to the secure gateway.",
    "GoPay calls a notification endpoint. The server then asks GoPay for the real payment state instead of reading anything from the return URL, because a return URL can be edited by the customer.",
    "Confirmation e-mail goes out through Nodemailer. In the admin panel the order shows as paid.",
    "When the parcel ships, the invoice PDF is generated and attached; for custom orders a proof is sent first and its approval time is recorded.",
    "A daily Vercel cron job at 08:00 finds unpaid orders and sends payment reminders.",
])}
"""),
        ("configurator", "The custom card designer", f"""
<p>This was the most interesting part to build, because it has to be pleasant for a shop owner and strict enough for a printer.</p>
{ul([
    "<b>Sizes and limits.</b> Eight presets plus a free-size mode with minimum and maximum edges and a maximum area. All cards are PVC at payment-card thickness (0.76 mm). A size flag lets us switch off a format the supplier cannot deliver by editing one line, so the picker never offers something we cannot ship.",
    "<b>Artwork upload and crop.</b> The customer uploads an image and crops it in a modal. A print-readiness check calculates the effective DPI from the pixel size and the physical size, and warns when the image is too small to print sharply.",
    "<b>3D preview.</b> The card is rendered with the uploaded art on the correct shape (rectangle with rounded corners, or circle) so the owner can rotate it before paying. Front images are prepared at 1024 px because smaller textures produced jagged edges when the browser scaled them down.",
    "<b>Proof and consent.</b> A proof is sent before production and both the sent and approved times are stored. That record matters legally: made-to-order goods are excluded from the right to withdraw only if they were made to the customer's approved specification.",
    "<b>Pricing.</b> Price per piece by size, volume discount on the total, and a one-time design setup fee that is waived from five pieces. The same pricing module is used by the form and the API so the two can never disagree.",
])}
{fig("almiboost-custom.webp", "The custom-card page: pick a size, upload artwork and spin the card in 3D.")}
"""),
        ("data", "Data model", f"""
<p>One Postgres table holds orders, grown by small additive migrations so that old orders never broke:</p>
{ul([
    "Customer and business fields, an <code>items</code> JSON array (product, quantity, unit price), totals, discount and delivery.",
    "Custom-order columns: design URL, a pending-design flag, a JSON spec with sizes and artwork metadata, a setup fee, and the proof timestamps.",
    "A <code>businesses</code> JSON column for orders that cover more than one business. The first business is also copied into the classic columns, so existing lists and search keep working.",
    "Invoice URL and file name, payment method and payment status, and a unique human-friendly order number.",
    "A separate <code>product_stock</code> table that the admin panel edits, so availability is a switch rather than a code change.",
])}
"""),
        ("security", "Security and correctness decisions", ul([
            "<b>The server is the source of truth for money.</b> Delivery price, discounts and totals are recomputed on the server. A tampered request cannot buy at a different price.",
            "<b>Payment state comes from the gateway.</b> The return URL only tells the page to refresh; the paid status is read from GoPay's API.",
            "<b>Admin is protected before anything renders.</b> A proxy layer verifies a signed session cookie for every admin page, the admin API routes and the Server Actions, so an action cannot be called directly without loading the page.",
            "<b>Secrets stay in environment variables.</b> Gateway credentials and mail settings are never in the code or sent to the browser.",
            "<b>One source of truth for company data.</b> The company identity used in the footer, terms and privacy policy comes from a single module, so the pages cannot drift apart. Slovak distance-selling law requires this information to be complete and correct.",
            "<b>Honest marketing rules.</b> The copy never promises a number of reviews or star ratings. Promising either breaks Google's policy and the EU Omnibus directive, which matters for a business that sells review-collection hardware.",
        ])),
        ("seo", "Search and structured data", f"""
<p>Because most customers find us by searching for review cards, the site is built to be understood by search engines. Each page type carries the right structured data: a local business with its social profiles on every page, products with offers (including return policy and shipping details), articles with named authors, FAQ pages with the real questions, how-to guides and breadcrumbs. Blog posts and product pages generate their own share images. I checked all pages in a crawl against the sitemap, and the one thing I deliberately do not add yet is star-rating markup, because there is no real customer review data to back it up.</p>
"""),
        ("hardware", "Hardware and supply chain", """
<p>The cards use NTAG213 and NTAG215 NFC chips. I source them directly from a manufacturer in Shenzhen and pay by international wire transfer. Each card is programmed with the customer's Google review link, tested with a phone, and shipped; delivery inside Slovakia takes about 3–5 working days. A replacement guarantee covers the first twelve months.</p>
<p>Before AlmiBoost I had already built a servo-driven cabinet lock around a PN532 NFC module, so the hardware side was familiar. The hard part was not the chip but the logistics: sample orders, quality checks, and keeping stock honest on the website, which is why the stock panel exists.</p>
"""),
        ("sales", "Selling it", """
<p>The first customers came from door-to-door visits in Bratislava. I deliberately skipped cold calling in favour of showing the card in person. A pitch leads with the prospect's own review count compared to a competitor nearby, not with a product demo. Every visit is logged in a field tool I built for the purpose, <a href="almiboost-scout.html">AlmiBoost Scout</a>. At the time of writing, the live About page reports 15 businesses served and 26 cards sold since August 2026.</p>
"""),
        ("learned", "What I learned", ul([
            "A small shop is mostly edge cases: partial stock, multi-business orders, VAT maths, proofs for custom goods. Designing the data model for them early saved a lot of rework.",
            "Never trust the client with money, and never trust a redirect to prove a payment.",
            "Doing sales myself made me a better developer. Watching a shop owner try to leave a review shaped almost every decision in the checkout and the product pages.",
            "Hardware sourcing is a project of its own: lead times, samples and quality checks need as much planning as software.",
        ])),
        ("next", "What is next", ul([
            "Collect real customer reviews and add star-rating markup once there is genuine data behind it.",
            "Improve the follow-up funnel, since many pitched businesses are never contacted a second time.",
            "Extend the platform into new NFC products for small businesses.",
        ])),
    ],
))

# ===================== SCOUT =====================
PROJECTS.append(dict(
    slug="almiboost-scout", num="002", title="AlmiBoost Scout",
    kicker="Field sales tool · map · realtime",
    lead="A mobile web app I built to run door-to-door sales in Bratislava. It shows every nearby business on a map, tracks each pitch and sale, and syncs live between my phone and my laptop. It runs without Google's APIs and without a server of my own.",
    cover="scout-app.webp",
    meta=[("Role", "Designer and developer"), ("Timeline", "Aug 2026 – present"), ("Status", "In daily use, private"),
          ("Stack", "Vanilla JS, Leaflet, OpenStreetMap, Supabase")],
    links=[],
    next=("pier-ai", "Pier AI"),
    sections=[
        ("overview", "Overview", f"""
<p>Door-to-door selling lives and dies on two questions: where should I go next, and what happened the last time I went there? Scout answers both. It is one HTML file you open on a phone, with a bundle of 8,493 Bratislava businesses built in, a map you can use outside, and a shared record of every pitch.</p>
<p>It is a private tool, so there is no public link. The screenshot below is the real app showing about eight thousand businesses on the map.</p>
"""),
        ("problem", "Why I built it", ul([
            "I needed to find streets full of the right kind of business: hair salons, cafés, bars, bakeries and small shops.",
            "I needed to remember what I said, who was closed, who asked me to come back, and who bought.",
            "I wanted the phone in my pocket and the laptop at home to show the same data, instantly.",
            "I wanted to know what the whole effort cost and earned, including expenses.",
        ])),
        ("features", "What it does", cards([
            ("Search by type and area", "Chips for coffee, restaurants, hair salons, nail studios, beauty salons, bars, bakeries, barbershops, small supermarkets, flower shops, tattoo studios and clothing shops, combined with an area or street search and a Bratislava-only switch."),
            ("Find by name", "A separate field for looking up one named business without the category filter getting in the way."),
            ("Filters and sort", "Narrow results and sort them. The header always shows how many businesses match."),
            ("List, map and dashboard", "Three views over the same data. The map colours markers by pitch state and has a \"sales only\" filter."),
            ("Pitch tracking", "Open any business and record the outcome, notes and follow-up. Every change is saved and synced."),
            ("GPS and radius", "A live location dot and a radius around you so you can see what is within walking distance."),
            ("Calendar and expenses", "A calendar of pitches, an expense list and a net-revenue figure on the dashboard."),
            ("Review growth", "For every sale, how many reviews the business had then and now, which is the metric that proves the card works."),
        ])),
        ("data", "The data: from Google to open data", f"""
<p>The first version called Google Places for every search, Google Geocoding for every area lookup and the Google Maps JavaScript API for the map, with Firebase for storage. That meant a billing account, quotas and a recurring cost. I rebuilt it so that none of those are needed.</p>
{table(["Before", "After"], [
    ["Google Places search, a call per search", "A bundled file of 8,493 businesses that ships with the app"],
    ["Google Geocoding for areas", "A bundled file of 2,448 street centrelines"],
    ["Google Maps JavaScript map", "Leaflet drawn over OpenStreetMap tiles"],
    ["Firebase for the shared dashboard", "Supabase (Postgres and Realtime)"],
])}
<p>I verified the result: loading the app, running a search and opening the map produces zero requests to Places, Maps, Geocoding or Firebase. The only Google-owned request left is a free font CDN.</p>
<p>The business file is built by a script that pulls a fresh OpenStreetMap extract through Overpass and a current Overture Maps release, removes duplicates by name and proximity, maps categories onto the chips, filters out the big chains, and writes a new file. The app picks it up with no code change, so refreshing it every few months is a single command.</p>
"""),
        ("streets", "A better street search", """
<p>Google capped each search at 20 results per category, so a search for a long street returned a random slice. The new version finds the road itself in the street file and returns everything standing along it.</p>
<p>That distinction matters more than it sounds. Matching the typed name against business address fields looks equivalent and is not. Gagarinova is a three-kilometre arterial lined with shops, yet only one of them lists \"Gagarinova\" as its address, because the rest are addressed to the side streets they front onto. Searching addresses found 1 business there; searching the road found 85. Obchodná returns 258 businesses instantly, with no paging.</p>
<p>The search corridor is 80 metres on each side of the centreline and widens automatically when a street comes back sparse, because an arterial's shops sit further from the road than an old-town street's.</p>
"""),
        ("architecture", "Architecture", f"""
<p>Scout is deliberately a single static file with no server. Any static host works.</p>
{ul([
    "<b>Front end.</b> Plain JavaScript, no framework and no build step. About a hundred small functions: search, rendering, map markers, modals, the calendar, the dashboard.",
    "<b>Map.</b> Leaflet with OpenStreetMap tiles, markers redrawn from the current result list, a distance calculation for the radius filter.",
    "<b>Storage.</b> Two Supabase tables, <code>pitches</code> and <code>expenses</code>. Each row keeps the whole entry in a JSON column, so the app's data shape carries over untouched and adding a field later needs no migration. A trigger keeps the update time honest.",
    "<b>Realtime.</b> Both tables are in the Realtime publication, which is what makes a pitch marked on the phone appear on the laptop.",
    "<b>Works without a backend.</b> Until the Supabase keys are filled in, the app keeps everything on one device, so it can be tried before it is set up.",
    "<b>Password gate.</b> A front-end prompt on opening.",
])}
"""),
        ("ratings", "Ratings by hand", """
<p>I checked carefully: there is no free source of Google ratings anywhere. So each business has an \"Add rating\" button. You tap \"Open in Maps\", read the two numbers and type them in. Once a number exists, everything that depended on it still works: the high-potential badge, the filters and the review growth since a sale. On the dashboard, \"Update review counts\" walks through every sale one at a time, so refreshing growth is a single job rather than hunting for each shop.</p>
<p>Copying a review link now copies a normal Google Maps search link for the business. It lands on the shop's Maps page, where \"Write a review\" is one tap away. The old direct link needed a Google Place ID, and keeping those would have meant going back to Google.</p>
"""),
        ("migration", "Moving the old data", """
<p>The old app identified businesses by Google Place ID, and the new one has its own ids. A small migration page takes an export from the old site and re-links every pitch by name and location. Anything it cannot match is kept anyway with its full history, so the dashboard totals stay correct and nothing is lost; it just will not line up with a search result.</p>
"""),
        ("limits", "Honest limits", ul([
            "<b>Coverage is about 80%, not 100%.</b> Checked against 28 businesses I had actually pitched, 22 were in the free data. The misses were small or recently opened places that OpenStreetMap and Overture have not recorded. For those I search by name or add them later; a place I already pitched keeps its record regardless.",
            "<b>Ratings are manual,</b> as described above.",
            "<b>The database key is public.</b> It is embedded in the page, so the password prompt only deters casual access and does not protect the database. That is acceptable while the tool is private. If it were ever shared, the fix is Supabase Auth with real policies, and the schema file says exactly what to change.",
            "<b>Map tiles come from OpenStreetMap's own servers</b> under their usage policy, which suits one person scouting a city. Growth would mean switching one tile-URL line to a paid or self-hosted provider.",
        ])),
        ("learned", "What I learned", ul([
            "Open data goes a long way once you merge two sources and deduplicate carefully.",
            "Constraints can improve a product: dropping Google forced a street search that is better than the paid one.",
            "Be honest about security. Writing down exactly what the public key exposes made it easy to decide when it would need to change.",
            "A tool you use every day tells you what to fix. Most features here exist because a visit went wrong without them.",
        ])),
    ],
))

# ===================== PIER AI =====================
PROJECTS.append(dict(
    slug="pier-ai", num="003", title="Pier AI",
    kicker="Voice assistant · local AI · Slovak",
    lead="A voice assistant for my school with a face: an animated mountaineer portrait of the patron, Pier Giorgio Frassati. You talk to it in Slovak with no button, and it answers out loud and in a speech bubble. It runs on local models, and no recordings or transcripts are stored.",
    cover="pier-ai.webp",
    meta=[("Role", "Designer, developer, model trainer"), ("Timeline", "Oct 2026 (state as of 19 Oct)"), ("Status", "Running on Windows; Raspberry Pi bundle prepared, not yet run on a real Pi"),
          ("Stack", "Python, sherpa-onnx, Ollama, Gemma 4 (LoRA), Piper, OmniVoice, SVG and JS")],
    links=[],
    next=("song-finder", "Song finder"),
    sections=[
        ("overview", "Overview", '''
<p>Pier AI is the voice of CSOŠE, the Frassati church technical secondary school in Bratislava. Students talk to it in Slovak. It knows facts about the school, tells the time and the bell schedule, reads out the timetable, gives the weather, answers questions from the curriculum and tells jokes. It deliberately refuses to answer what it has no verified answer for.</p>
<p>The mascot is the school's patron, Pier Giorgio Frassati, drawn as the mountaineer he was. The sky behind him follows the real Bratislava sun, so the scene changes through the day. On Windows the app is a double-click icon; it opens a window, <code>F</code> or a double-click makes it full screen, and it shuts itself down when the window closes.</p>
''' + table(["At a glance", ""], [
    ["Language model", "pier-e2b, a fine-tuned and pruned Gemma 4 E2B, Q4_K_M, 1.55 GB (Apache-2.0)"],
    ["Prompt", "about 1,000 tokens, plus the 2 closest verified answers"],
    ["Verified answers", "414 hand-written question and answer pairs"],
    ["Quality", "98 of 105 on a test the model never saw; 2.2% unknown words"],
    ["Speed on a simulated Pi", "9 s to read the prompt at start; 1.5 to 3.1 s from the end of a question to the first text"],
    ["Raspberry Pi estimate (not measured)", "about 30 s to start, 5 to 10 s per answer, about 4 GB of 8 GB memory"],
    ["Ports", "8765 for the screen (state over SSE), 8008 for the voice service"],
    ["Code", "about 730 lines in the main program, plus prompt, retrieval, spell-fix and timetable modules"],
])),
        ("goal", "The goal and the constraint", '''
<p>The decision I made early was that everything must run on a Raspberry Pi 5 (8 GB) with no PC, so a school could put it on a wall without a gaming machine or a cloud bill. That one constraint shaped every other choice: a small model, CPU speech recognition, and no dependence on paid services.</p>
<p>Today the full version runs on my home PC (RTX 3060) with a male voice. A Raspberry Pi package is prepared, but I have not yet run it on a real Pi, and I say so on purpose. What I have verified is the syntax of the scripts, a simulation of the Pi on a PC without a GPU, and a remote voice.</p>
'''),
        ("pipeline", "What happens when you ask a question", steps([
    "<b>Listen.</b> The microphone is always on. No button is needed; the app detects speech. The detection threshold (<code>SPEECH_RMS</code>) is tuned for a headset on the PC.",
    "<b>Transcribe.</b> Parakeet-sk (int8, via sherpa-onnx) turns Slovak speech into text on the CPU. Audio is never written to disk.",
    "<b>Fix names.</b> <code>fix_names</code> corrects speech-model mistakes such as \"farsati\" to Frassati.",
    "<b>Route.</b> In <code>turn()</code> the question goes through these checks, in this order: <code>clock_answer</code> (time and date), <code>unknown_word_answer</code> (\"what does the word X mean\" when X is not Slovak), <code>unclear_answer</code> (one word that is not a greeting), <code>strict_answer</code> (strict mode), and <code>timetable.answer</code> (timetable and bells, computed by Python).",
    "<b>Retrieve.</b> Otherwise the two closest verified answers from <code>data/znalosti.jsonl</code> are found by text similarity (minimum 0.40) and added to the prompt.",
    "<b>Generate.</b> The local language model answers in a sentence or two at temperature 0.3, streaming sentence by sentence (<code>stream_llm</code>).",
    "<b>Clean up.</b> <code>spellfix.fix</code> restores missing diacritics and common small-model mistakes, only when the correction is unambiguous.",
    "<b>Speak.</b> Each sentence goes to the voice service with <code>POST /speak</code>, which returns a WAV that <code>sounddevice</code> plays.",
    "<b>Show.</b> The screen is a web page at <code>http://localhost:8765</code>; the app streams state changes to it over server-sent events, and the face moves its mouth, eyes and head to match.",
])),
        ("routing", "Routing and strict mode", '''
<p>Strict mode (<code>PIER_STRICT=1</code>, on by default) is the most important safety decision. The model may answer freely only on topics that were verified: the school, the patron, the weather, jokes, greetings, facts about Pier himself, the rules and places in the building. This is a regular expression, <code>ALLOWED_TOPICS</code>. Anything else gets a fixed answer saying there is no verified answer.</p>
''' + ul([
    "<b>Why.</b> A small model outside its collection makes things up. Examples from testing: it turned \"neštyri\" into \"the sign for the number three\", and a garbled word into confused text.",
    "<b>The bypass.</b> A question that matches a verified answer with similarity of at least 0.40 is answered even if its topic is not on the list, so adding a verified answer is the way to widen what Pier can do.",
    "<b>An ordering trap.</b> Strict mode runs before the timetable. So the words students use for timetable and bell questions (hours, breaks, bells, timetable) must be on the allowed list, or those questions get refused before the timetable logic sees them.",
    "<b>When it is wrong.</b> Strict mode also refuses simple general questions outside the collection (\"how many days are in a week?\"). The remedy is to add verified answers, not to loosen the model.",
    "<b>Switching it off.</b> <code>PIER_STRICT=0</code>, for experiments only.",
])),
        ("components", "Components", table(["Part", "What it does"], [
    ["Speech recognition", "Parakeet-sk int8 through sherpa-onnx, CPU only. About 0.7 GB; about 0.2 s per sentence on the PC, estimated 0.5 to 1 s on a Pi"],
    ["Language model", "pier-e2b: a fine-tuned and pruned Gemma 4 E2B in Q4_K_M, 1.55 GB, served by Ollama (version 0.40.6 on the PC)"],
    ["Verified answers", "414 hand-written question and answer pairs, retrieved by similarity (<code>knowledge.py</code>)"],
    ["Voice", "OmniVoice (male, needs an NVIDIA GPU) or Piper \"lili\" (female, runs on CPU, about 60 MB)"],
    ["Spell fix", "Rule-based correction (<code>spellfix.py</code>) with the Hunspell sk_SK dictionary"],
    ["Time, bells, timetable, weather", "Computed in Python from the clock, the school's EduPage data and Open-Meteo, never guessed by the model"],
    ["Window", "A full-screen web page with an SVG character, sky and clock (<code>web/</code>)"],
    ["School facts", "Plain text files, <code>data/skola.txt</code> and <code>data/patron.txt</code>, that a teacher could edit"],
])),
        ("voice", "Two voices, one interface", '''
<p>Both voice services expose the same small API (<code>/health</code> and <code>/speak</code>, port 8008), so the main program does not care which one is running.</p>
''' + table(["", "Piper \"lili\"", "OmniVoice"], [
    ["Voice", "Female", "Male"],
    ["Runs on", "CPU", "NVIDIA GPU with CUDA"],
    ["Licence", "MIT", "Weights are CC-BY-NC (non-commercial)"],
    ["Sample rate", "22,050 Hz", "24,000 Hz"],
    ["Used on", "The Raspberry Pi", "The Windows PC"],
    ["Script", "<code>tts/piper_server.py</code>", "<code>tts/omni_server.py</code>"],
]) + '''
<p>On Windows the app starts OmniVoice by itself. If <code>PIER_TTS_URL</code> is set, no local voice is started and the remote one is used instead, which is how a Pi can borrow the PC's male voice over the private network. The sample rate is also a quick way to tell the two apart: I once benchmarked OmniVoice by mistake, thinking it was Piper, because port 8008 was already taken.</p>
'''),
        ("model", "Making a small model speak good Slovak", '''
<p>An off-the-shelf small model speaks poor Slovak and invents facts. I trained my own.</p>
''' + ul([
    "<b>Pruning.</b> The original Gemma 4 E2B has 5.1 billion parameters, of which about 2.75 billion are word tables for every language and 0.45 billion are audio and vision. I removed the audio and vision towers and cut the vocabulary from 262,144 to about 60,000 tokens. The model shrank to 2.5 billion parameters, the quantised file is 1.56 GB instead of 4.6 GB, and picking a word is about 15% less work.",
    "<b>Fine-tuning.</b> LoRA training on the pruned model with about 1,500 samples: Slovak answer style, length, refusals (\"I don't know, ask at the office\"), the persona, weather, rules and general curriculum answers. It trains only on the answer. It took about 80 minutes on the RTX 3060 at about 650 words per second.",
    "<b>Facts are not in the weights.</b> The model learned to read school facts from the prompt, including examples where the line is missing and the correct answer is \"I don't know\". When a fact changes, someone edits a text file and no retraining is needed. On changed data it scored 5 out of 5.",
    "<b>Retrieval of verified answers.</b> A 2-billion-parameter model cannot absorb a curriculum from a few hundred answers. So at question time the closest verified answers go into the prompt and the model rephrases them. On 20 brand-new topics it had never seen, it answered 19 correctly.",
    "<b>Own prompt template.</b> The Modelfile has a custom template identical to the one used in training. It must not be overwritten, and its <code>FROM</code> line contains a Windows path that the Pi installer rewrites.",
    "<b>No \"thinking\".</b> For Gemma 4 models Ollama writes the answer into a <code>thinking</code> field by default, so the app sends <code>reasoning_effort: none</code> and the evaluation script needs <code>--think-off</code>.",
]) + '''
<div class="pg-callout"><b>A lesson about teacher models</b><p>I first used a 12B Slovak model (OpenEuroLLM-Slovak) as a teacher to write general answers, and it invented facts (asked what the word \"var\" means, it answered \"a Slavic calendar\"). So every general answer is now written by hand in the <code>answers_*.py</code> files, and the teacher is only used to paraphrase questions.</p></div>
<div class="pg-callout"><b>A lesson about GPU memory</b><p>When batch lengths differ, GPU memory fragments, and on a 12 GB card Windows starts spilling it into normal memory, which is about 3 times slower. Rounding each batch length up to a multiple of 128 in <code>train_lora.py</code> fixed it.</p></div>
'''),
        ("results", "Measured results", '''
<p>All figures come from tests the model never saw in training. Each model got the same prompt and the same questions at temperature 0. The test grew over time (57, 62, 85 and finally 105 questions), so rows measured on different sizes are not directly comparable.</p>
''' + table(["Model", "Correct", "Unknown words", "Response"], [
    ["gemma3:4b with examples (3.4 GB)", "72 / 85", "3.9%", "1.7 s"],
    ["Original Gemma 4 E2B with examples (4.6 GB)", "62 / 85", "5.0%", "1.5 s"],
    ["Original Gemma 4 E2B without examples", "61 / 85", "4.3%", "1.5 s"],
    ["pier-e2b, round 1 (fine-tuned, pruned, 1.6 GB)", "76 / 85", "5.3%", "1.3 s"],
    ["pier-e2b, round 2 (plus 287 verified answers)", "79 / 85", "2.6%", "1.3 s"],
    ["gemma3:4b with examples and verified answers", "78 / 85", "3.4%", "2.1 s"],
    ["pier-e2b round 3 (continued from round 2, not used)", "77 / 85", "3.0%", "1.3 s"],
    ["pier-e2b round 2 plus 414 answers (105-question test)", "98 / 105", "2.5%", "1.3 s"],
    ["<b>pier-e2b deployed (414 answers plus spell fix)</b>", "<b>98 / 105</b>", "<b>2.2%</b>", "<b>1.3 s</b>"],
]) + '''
<p>Inside the 105-question test, the deployed model scores: facts 18 of 20, traps 10 of 10, changed data 5 of 5, general questions 15 of 18, taught topics 23 of 23, new topics without training 19 of 20, rules 3 of 3, weather 3 of 3, persona 2 of 3. The column that matters for a fair comparison is the 62 questions that are new to every model, where gemma3:4b with examples scores 57 (55 once it gets the same verified answers) and pier-e2b scores 56.</p>
<p>With the same help, gemma3:4b and pier-e2b score about the same (78 and 79 out of 85). But pier-e2b is half the size and needs half the prompt, which is what lets it fit on a Raspberry Pi. gemma3:4b is slightly better on general questions outside the list (17 against 15 out of 18).</p>
'''),
        ("experiments", "Experiments and what they decided", table(["Experiment", "Result", "Decision"], [
    ["Quantisation Q4_K_M, Q5_K_M, Q6_K", "All 79 of 85. Q5 is 12% and Q6 25% bigger; speed on 4 CPU threads is 25, 23 and 20 words per second", "Stay on Q4_K_M"],
    ["Temperature 0, 0.1, 0.3", "98 to 99 of 105, the same within noise", "Stay on 0.3"],
    ["Round 3 of training with unrelated records in the prompt", "77 against 79", "Not used"],
    ["Verified answers 287 to 414", "No retraining needed; 19 of 20 new topics correct; the old test did not get worse", "Keep adding answers, not retraining"],
    ["Spell-fix with dictionary suggestions", "Broke names (\"Merkur\" to \"Merku\", \"Pier\" to \"Pieta\")", "Discarded; rules-only version kept"],
    ["Select only relevant school facts per question", "Would cut 2 to 3 s on a Pi but needs a short new fine-tune", "Not done yet"],
])),
        ("performance", "Speed and memory", f"""
{table(["Measure", "Value", "Status"], [
    ["Prompt read at start (PC, CPU, 4 threads, Piper)", "9 s", "Measured"],
    ["End of question to first text (same setup)", "1.5 to 3.1 s", "Measured"],
    ["Generation speed (PC, 4 threads, Q4_K_M)", "25 words per second", "Measured"],
    ["Raspberry Pi 5 versus that setup", "2.5 to 3.5 times slower", "Estimate"],
    ["Pi start", "about 30 s", "Estimate"],
    ["Pi answer", "5 to 10 s", "Estimate"],
    ["Pi generation speed", "7 to 9 words per second", "Estimate"],
    ["Speech recognition per sentence", "about 0.2 s on the PC; 0.5 to 1 s on a Pi", "Measured; estimate"],
])}
<p>Memory budget on the Pi: the model 1.6 GB, its context about 0.5 GB, Parakeet 0.7 GB, the voice about 0.3 GB and the system about 1 GB, so around 4 GB of the 8 GB. The first start after power-on is slower because the model reads the roughly 1,000-token prompt once, then Ollama remembers it.</p>
"""),
        ("face", "The face", '''
<p>The first version used a real photo with a WebGL effect. I replaced it with an illustrated SVG character because the patron is famous as a mountaineer ("Verso l'alto", towards the top) and a cartoon climber fits a school app better than an uncanny photo. The photo version is kept in a backup folder.</p>
''' + ul([
    "A round medallion with a halo, a pipe and an ice axe, drawn entirely in SVG (<code>web/avatar.js</code>, about 290 lines).",
    "Head, eyes and mouth are driven by the app's state and the voice level while it speaks (<code>web/app.js</code>). The hand lifts the pipe away while it thinks and speaks.",
    "The sky and the sun position follow the real time in Bratislava. A <code>?time=HH:MM</code> parameter previews any hour.",
    "The screen shows a clock card at the top left, a status pill at the top and the speech bubble near the mouth.",
    "Only public-domain artwork is used. Paintings with a watermark were rejected.",
]) + '''
<div class="pg-fig-row">
''' + fig("pier-day.webp", "Midday sky, using the time preview.") + fig("pier-dusk.webp", "Dusk, using the time preview.") + '''
</div>
'''),
        ("deterministic", "Things the model never guesses", '''
<p>Clocks and timetables are facts, so Python computes them and the model is never asked. The time and date come from the machine clock; bell times and the class timetable come from the school's EduPage data (a 370-line module, <code>timetable.py</code>); weather comes from Open-Meteo for Bratislava, with no key. When speech recognition garbles a class name, the app does not guess a time; it answers with a fixed request to repeat it.</p>
<p>The spell-fix pass is deliberately cautious. It only restores missing diacritics, i versus y, and the Czech <code>o</code> that small models write instead of <code>a</code>, and only when exactly one candidate fits. That cut unknown words from 2.5% to 2.2% without damaging any names.</p>
'''),
        ("layout", "Project layout", table(["Path", "What it is"], [
    ["<code>pier_ai.py</code>", "The whole program: routing, microphone, language model, voice and HTTP server"],
    ["<code>school_prompt.py</code>, <code>knowledge.py</code>, <code>slovak_text.py</code>, <code>spellfix.py</code>, <code>timetable.py</code>", "The prompt, verified-answer retrieval, Slovak text preparation for the voice, spell-fix, and the timetable"],
    ["<code>data/skola.txt</code>, <code>data/patron.txt</code>", "Facts about the school and the patron, as plain editable text"],
    ["<code>data/znalosti.jsonl</code>, <code>data/slovnik/</code>", "414 verified answers, and the Hunspell sk_SK dictionary"],
    ["<code>web/</code>", "The screen: <code>app.js</code>, <code>avatar.js</code>, <code>style.css</code>"],
    ["<code>tts/</code>", "The two voice services (<code>piper_server.py</code>, <code>omni_server.py</code>)"],
    ["<code>pi/</code>", "<code>install.sh</code>, the <code>pier-ai.sh</code> kiosk launcher, <code>autostart.sh</code>, <code>stiahni-hlas.sh</code>, and <code>pripravit-balik.ps1</code> that builds the bundle on Windows"],
    ["<code>train/</code>", "Training and tests, only on my home PC: <code>build_knowledge.py</code>, <code>answers_1..5.py</code>, <code>test_set.py</code>, <code>evaluate.py</code>, <code>VYSLEDKY.md</code>"],
    ["<code>PierAI.cs</code>, <code>Pier AI.exe</code>", "The Windows launcher that opens the Edge window"],
])),
        ("config", "Configuration", '''
<p>Behaviour is controlled by environment variables. On the Pi they live in <code>~/.config/pier-ai.env</code>.</p>
''' + table(["Variable", "Meaning"], [
    ["<code>PIER_MODEL</code>", "Which Ollama model to use, for example <code>gemma3:4b</code>"],
    ["<code>PIER_FEWSHOT</code>", "<code>0</code> for the fine-tuned model; <code>1</code> adds worked examples to the prompt for other models"],
    ["<code>PIER_KB</code>", "<code>0</code> turns the verified answers off"],
    ["<code>PIER_STRICT</code>", "Strict mode; on by default, <code>0</code> turns it off"],
    ["<code>PIER_TTS_URL</code>", "Use a remote voice service instead of starting a local one"],
    ["<code>PIER_VOICE_CHECK</code>", "Checks each sentence with the recogniser; switched off on the Pi (<code>0</code>)"],
    ["<code>PIER_MIC</code>, <code>PIER_SPEAKER</code>", "Microphone and speaker, by number or part of the name (list them with <code>python -m sounddevice</code>)"],
])),
        ("maintain", "Keeping it up to date", '''
<p>The school does not need me or a graphics card to improve it.</p>
''' + ul([
    "<b>New facts about the school</b> go into <code>data/skola.txt</code>, which is read from the prompt. The model learned to read facts even when they change, so a new line works immediately.",
    "<b>New verified answers</b> are one line each in <code>data/znalosti.jsonl</code> in the form below. Write 1 to 2 sentences in standard Slovak with no invented facts. They work immediately without retraining.",
]) + code('{"question": "...", "answer": "..."}') + '''
<p>One trap: at home I keep the same answers in <code>train/answers_*.py</code> and a build script generates <code>znalosti.jsonl</code> from them, <b>overwriting</b> it. Additions made directly in the school file therefore have to be copied into the answer files, or the next build erases them.</p>
'''),
        ("privacy", "Privacy and licensing decisions", ul([
    "No transcript and no audio is ever written to disk. The launcher discards output and the voice services print nothing. Logging recognised questions would need the school's agreement first.",
    "The assistant refuses to reveal its own rules.",
    "The portrait is public-domain only.",
    "Licences are tracked honestly: Piper \"lili\" is MIT, Gemma 4 is Apache-2.0, and the OmniVoice weights are CC-BY-NC, so the male voice needs an assessment from the school's data-protection officer before it is used there.",
])),
        ("pi", "The Raspberry Pi plan", '''
<p>The target is a Raspberry Pi 5 with 8 GB, active cooling and the original 27 W supply, a microSD card of at least 32 GB (NVMe is better), a USB microphone or headset, a speaker and a monitor, running Raspberry Pi OS 64-bit (Bookworm or newer). The installer downloads packages, Ollama and the voice, so it needs internet; weather and timetable use it permanently.</p>
''' + steps([
    "On Windows, a script builds a 2.2 GB bundle with the program, the language model, the recogniser and the voice service.",
    "Copy it to the Pi by USB stick or <code>scp</code>, then run the installer. It sets up the Python environment, Ollama, the voice, the <code>pier-e2b</code> model and a menu icon.",
    "The launcher starts Piper by itself and opens the screen in full-screen Chromium. Closing the window with Alt+F4 also stops the program.",
    "For a wall display, the autostart script plus automatic login starts it at power-on. I can administer the Pi from a school PC over SSH with keys.",
]) + '''
<h3 class="pg-h3">Risks to check first, because it has never run on real hardware</h3>
''' + ul([
    "Whether <code>sherpa-onnx</code> and <code>piper-tts</code> have ARM packages for the Pi's Python version.",
    "Whether Ollama on ARM is new enough to recognise the Gemma 4 architecture (the PC runs 0.40.6).",
    "The real speed, temperature (<code>vcgencmd get_throttled</code>) and memory (<code>free -h</code>, about 4 GB expected).",
    "The microphone: the speech threshold is tuned to a PC headset, and devices must be selected with the variables above.",
]) + '''
<h3 class="pg-h3">If it turns out too slow</h3>
''' + ul([
    "Shorten the prompt and the answers.",
    "Lower <code>num_ctx</code> in the Modelfile.",
    "Put only the relevant school facts into the prompt, which needs a short new fine-tune on the PC.",
    "A male voice on the Pi is not available yet, because there is no good Slovak male voice that runs without a GPU.",
]) + '''
'''),
        ("issues", "Known issues", ul([
    "Speech recognition errors can turn into a refusal or into \"I did not understand the whole question\". I saw this with synthetic questions and it is not always repeatable.",
    "Strict mode also refuses simple general questions outside the verified set.",
    "Piper's female voice has softer word starts that the recogniser sometimes mishears (\"Veľká\" heard as \"dvetka\"), which is why the sentence check is off on the Pi.",
    "A single word that is not a greeting gets \"say the whole question\", and an unknown word in \"what does X mean\" gets \"I do not know it\".",
    "Holidays and school breaks are not in the timetable logic. Weather is fixed to Bratislava.",
    "Training and the large models exist only on my home PC; at school only the app and the data can be changed.",
])),
        ("pitfalls", "Engineering pitfalls", ul([
    "<b>A full disk emptied a file.</b> While testing quantisations the disk filled up and a file was silently truncated. Temporary GGUF and Ollama copies are deleted immediately after each experiment.",
    "<b>A regular expression that never matched.</b> One with doubled slashes never matched, and an alternation joined with <code>||</code> was always true. Every new regex is tested on positive and negative examples.",
    "<b>Port 8008</b> is taken by OmniVoice while the app runs, so Piper has to be tried on another port, for example 8009.",
    "<b>Windows only.</b> <code>creationflags</code> for <code>subprocess.Popen</code> exists only on Windows (fixed).",
    "<b>Line endings.</b> Shell scripts must have LF endings, which the bundle script enforces. Editing files through scripts also needs care with CRLF and with <code>\\U</code> in Windows paths inside Python strings.",
])),
        ("roadmap", "Roadmap, in priority order", steps([
    "Run it on the Pi, measure the speed and fix whatever breaks.",
    "Shorten the prompt or answers if it is slow.",
    "Add about 200 more verified answers, based on what students actually ask.",
    "Relax strict mode where it refuses without need, using real questions, without writing recognised questions to disk unless the school agrees.",
    "Get the OmniVoice licence assessed, with the school's data-protection officer, if the male voice is to be used at school.",
    "Optionally: a short new fine-tune that selects only the relevant facts for the prompt, and a good male voice for the Pi.",
])),
        ("glossary", "Glossary", table(["Term", "Meaning"], [
    ["LLM", "Large language model: the program that writes the answers"],
    ["STT / TTS", "Speech to text and text to speech"],
    ["Parakeet-sk, sherpa-onnx", "The Slovak speech recogniser and the runtime that runs it on a CPU"],
    ["int8", "Numbers stored in 8 bits: smaller and faster, slightly less precise"],
    ["Gemma 4 E2B", "The base model from Google (Apache-2.0)"],
    ["Pruning", "Cutting parts of a model away: here the audio and vision parts and most of the vocabulary"],
    ["LoRA", "A cheap way to fine-tune a model by training small extra matrices"],
    ["Quantisation, Q4_K_M, GGUF", "Storing the weights in about 4 bits each in the GGUF file format used by llama.cpp and Ollama"],
    ["Ollama", "A program that runs local models behind a simple API"],
    ["Retrieval", "Finding the closest verified answers and giving them to the model"],
    ["Strict mode", "Refusing questions outside the verified topics instead of improvising"],
    ["SSE", "Server-sent events: how the program streams state to the screen"],
    ["Hunspell", "An open-source spelling dictionary, here Slovak (sk_SK)"],
    ["EduPage", "The school's timetable system the bell and timetable data come from"],
])),
        ("learned", "What I learned", ul([
    "A small model plus retrieval plus strict rules beats a bigger model with no guard rails for a school helper.",
    "Put facts where they can be edited (text files and a retrieval collection), and put style where it must be learned (the weights).",
    "Rules beat a clever model where the answer is checkable: clocks, timetables, weather and spelling.",
    "Test every regular expression on both positive and negative examples.",
    "Disk space and GPU memory are real resources when quantising and training models.",
    "Be honest about what has and has not been tested. The handover notes list the untested Raspberry Pi risks first.",
])),
    ],
))

# ===================== SONG FINDER =====================
PROJECTS.append(dict(
    slug="song-finder", num="004", title="Song finder",
    kicker="Arduino Mega · LCD · signal processing",
    lead="A small device that listens to music for five seconds, finds out what song it is over the internet, and shows the title on an LCD. The bottom row of the display is a live 16-band spectrum analyser. Built with my classmate Boris Kalmár.",
    cover="song-home.webp",
    meta=[("Role", "Built with Boris Kalmár"), ("Timeline", "Oct 2026"), ("Status", "Working prototype"),
          ("Stack", "Arduino Mega, C++, Python, AudD API")],
    links=[("Project website", "https://arduino-rozpoznanie-pesniciek.vercel.app"), ("Source code", "https://github.com/tomaskooooo/arduino-rozpoznanie-pesniciek")],
    next=("almiboost", "AlmiBoost"),
    sections=[
        ("overview", "Overview", f"""
<p>The device has an Arduino Mega, a sound sensor, a 16×2 LCD and a button. You hold a speaker close to the sensor and press the button. The Mega records five seconds of audio and streams it to a PC over USB, the PC sends it to the AudD music-recognition service, and the answer goes back to the display. While all of that happens, the bottom row of the LCD acts as an equaliser that bounces to the music.</p>
<pre class="pg-code lcd" tabindex="0"><code>┌────────────────┐
│One Kiss (Extend│  ← title and artist, long text scrolls
│▇█▆▅▆▄▃▄▂▃▂▂▁▁  │  ← spectrum, 16 columns = 16 frequency bands
└────────────────┘</code></pre>
<p>It is a school project at CSOŠE Frassatiho III. It replaces a larger earlier idea, a 16-step sequencer with an LED matrix and a joystick, which I rebuilt from zero one part at a time and left untouched in an archive folder.</p>
"""),
        ("split", "Dividing the work between two devices", f"""
<p>An Arduino Mega has no internet. So the job is split:</p>
{table(["Device", "Does"], [
    ["Arduino Mega", "Reads the button, samples the sound sensor, draws on the LCD, computes the spectrum"],
    ["PC (Python)", "Receives the recording, cleans it, sends it to AudD, sends the result back to the LCD"],
])}
{steps([
    "Press the button (pin 2). The Mega shows \"Listening...\".",
    "For five seconds the Mega reads the sensor at 8,000 samples per second, 8 bits each: 40,000 bytes. It sends the header <code>AUDIO 40000</code> and then the raw samples over USB.",
    "The PC removes the DC offset, boosts the signal to full volume and saves it as <code>last_capture.wav</code>.",
    "The PC sends the WAV to AudD over HTTPS. The LCD shows \"Searching...\".",
    "AudD answers with a title and an artist. The PC sends them to the Mega, which shows them on the top row.",
    "The whole time, the bottom row shows the spectrum from the same sensor.",
])}
"""),
        ("hardware", "Hardware", f"""
{table(["Qty", "Part", "Note"], [
    ["1", "Arduino Mega 2560", "Connected by USB to the PC"],
    ["1", "LCD 16×2 (HD44780)", "Parallel connection, no I2C module, 4-bit mode"],
    ["1", "Sound sensor KS0035 (analogue)", "Pins G, V, S, with a trimmer to adjust gain"],
    ["1", "Push button", "Wired diagonally to avoid the paired pins"],
    ["1", "10 kΩ potentiometer", "LCD contrast"],
    ["1", "220 Ω resistor", "Backlight"],
])}
<h3 class="pg-h3">Pin map</h3>
{table(["Mega pin", "Use"], [
    ["2", "Button (internal pull-up, no resistor)"],
    ["9", "LCD backlight (PWM, brightness control)"],
    ["22 / 23", "LCD RS / E"],
    ["24, 25, 26, 27", "LCD D4 to D7"],
    ["A4", "Sound sensor signal"],
    ["0, 1", "USB serial, not used for anything else"],
])}
<p>The backlight draws about 8 mA, which a Mega pin can drive without a transistor, so putting the 220 Ω resistor on pin 9 lets the code dim the display. Contrast comes from the voltage on pin V0. A potentiometer is best; without one, a 4.7 kΩ and a 1 kΩ resistor make a divider that gives about 0.9 V.</p>
"""),
        ("analyser", "The spectrum analyser", f"""
<p>The bottom row shows how much energy is in each of 16 frequency bands, bass on the left and treble on the right. About twenty times a second:</p>
{steps([
    "The Mega takes 128 sensor samples at 8 kHz (16 ms) and subtracts the average.",
    "For each of 16 bands it runs a <b>Goertzel filter</b>, a simplified FFT that computes just one frequency. That is why it fits on a small, slow chip. It is all integer maths with no library, and the bands are spaced logarithmically from 110 Hz to 3,500 Hz.",
    "It converts each result to an amplitude.",
    "<b>Automatic gain:</b> the loudest band of the last second defines a full bar, so the bars dance the same way no matter how loud the speaker is.",
    "<b>Noise gate:</b> a band weaker than a set amplitude is not shown, so the display does not flicker in silence.",
    "<b>Sensitivity:</b> bar height is 8 × (amplitude ÷ reference) to the power γ. Level 9 is γ = 0.5 (bars stay tall even for weak bands), level 1 is about γ = 2 (only strong peaks show), and level 6 is roughly linear. The <code>+</code> and <code>-</code> keys on the PC change it live.",
    "A bar rises instantly and falls one step per frame, so it looks smooth.",
])}
<p>Each bar is one LCD character with eight possible heights. An HD44780 has room for exactly eight custom characters, and all eight are used by the bars, which is also why accented letters cannot be shown.</p>
<p>The display also gets fully re-initialised every ten seconds. The HD44780 chip can lose sync after electrical noise or a loose wire and stay blocked until it is reinitialised, and this makes the device recover on its own, with at most a brief blink.</p>
"""),
        ("protocol", "The serial protocol", f"""
<p>The Mega and the PC talk over USB at 250,000 baud with a small text protocol.</p>
{table(["PC to Mega", "Meaning"], [
    ["<code>L&lt;text&gt;</code>", "Show text on the top row (up to 120 characters)"],
    ["<code>B&lt;0–255&gt;</code>", "Backlight brightness"],
    ["<code>S&lt;1–9&gt;</code>", "Analyser sensitivity"],
    ["<code>D1</code> / <code>D0</code>", "Debug output on or off"],
    ["<code>g</code>", "Start recording (same as the button)"],
])}
{table(["Mega to PC", "Meaning"], [
    ["<code>BOOT</code>", "The Mega just started"],
    ["<code>AUDIO 40000</code> + bytes", "A recording: header, then the raw samples"],
    ["<code>V a0 … a15 ref ms</code>", "A debug line with the 16 amplitudes, the reference and the frame time"],
])}
<p>Most of the effort was in the rules that prevent subtle bugs:</p>
{ul([
    "The PC sends an empty line before every command. It ends any half-finished line in the Mega's memory that would otherwise swallow the next command.",
    "The Mega drops an unfinished line after 500 ms of silence.",
    "The PC sends long messages in 24-byte pieces with a 50 ms pause, because the Mega's receive buffer is only 64 bytes and is not read while the LCD redraws.",
    "The PC opens the port with DTR low, so connecting does not reset the Mega.",
    "The port settings are never changed while a recording is arriving, because on Windows that could drop a byte.",
])}
"""),
        ("recognition", "Recognition and its quirks", f"""
{ul([
    "Audio is 8 kHz, 8 bits (the top 8 bits of the 10-bit ADC), mono, five seconds. That is telephone quality, but enough for AudD in a quiet room with the speaker a few centimetres away.",
    "The PC makes a 16-bit WAV and posts it to the AudD API. The reply has a title and an artist. The last recording is always saved so that when recognition fails you can play it and hear what the sensor actually captured.",
    "<b>Diacritics.</b> The LCD font has no é, š, ť or á, and the custom characters are used by the bars, so the PC strips accents before sending (\"Život ide ďalej\" becomes \"Zivot ide dalej\"). Scripts like Japanese or Cyrillic show as question marks.",
    "<b>Sensor quirk.</b> The KS0035 rests at zero and only swings upwards, so 50 to 90 percent of samples read near zero. That looked like clipping, but it is normal for this sensor.",
])}
"""),
        ("problems", "Problems I hit and how I solved them", table(["Symptom", "Cause", "Fix"], [
    ["Backlight on but no text, top row full of squares", "The LCD never initialised", "Check E, RS and RW wiring; replace jumper wires; press reset"],
    ["A cluster of random characters", "D4 to D7 wires in the wrong order or loose", "Flash the included test sketch that tries all 24 wire orders; readable text shows the right one"],
    ["Brightness cannot be changed", "The resistor was on 5 V, not pin 9", "Move it to pin 9"],
    ["Upload fails, port busy", "Another program holds the COM port", "Close the recogniser and the serial monitor first"],
    ["Commands from the PC sometimes lost", "A half-finished line in the Mega's buffer", "Leading newline and a timeout"],
    ["\"got 39999 of 40000 bytes\"", "A byte lost during transfer", "The script now tolerates up to 2% missing samples"],
    ["One bar always lit at reduced brightness", "Possibly PWM backlight noise (about 490 Hz) coupling into the sensor", "Run at 100% brightness or move the sensor away from the backlight wires (suspected, not proven)"],
])),
        ("limits", "Limits and ideas", f"""
<h3 class="pg-h3">Limits</h3>
{ul([
    "It needs a PC with internet. The Mega cannot recognise songs on its own.",
    "The sensor is basic, so the sound is distorted and recognition is not always successful.",
    "Audio is only 8 kHz and 8 bits.",
    "The LCD shows only ASCII.",
    "The sensitivity keys work on Windows only. During the five-second recording the Mega does not draw the analyser or scroll text.",
    "The AudD key used so far is a free trial.",
])}
<h3 class="pg-h3">Ideas</h3>
{ul([
    "A better microphone such as a MAX4466 or MAX9814, which rests in the middle of its range and swings both ways. Wiring is identical and the code does not change.",
    "An ESP32 with Wi-Fi that sends the recording to AudD by itself, so no PC is needed.",
    "Show the rhythm on the 8×8 LED matrix from the earlier project, or beep on success.",
    "Real accented letters by reducing the bars from eight heights to four.",
])}
"""),
        ("learned", "What I learned", ul([
            "Efficient signal processing on a tiny chip: why a Goertzel filter beats an FFT when you only need a few frequencies.",
            "Designing a reliable serial protocol: framing, timeouts, buffer sizes and resets.",
            "Hardware debugging as a method: change one thing, test it, and write the symptom and cause table so the next person does not repeat it.",
            "Writing documentation as I go. The project has a full Slovak manual covering wiring, installation, settings, protocol and troubleshooting.",
        ])),
    ],
))

# ---------- page template ----------

def jsonld(p):
    url = f"{SITE}/projects/{p['slug']}.html"
    graph = [
        {"@type": "CreativeWork", "@id": url + "#work", "name": p["title"], "description": p["lead"], "url": url,
         "image": f"{SITE}/assets/projects/{p['cover']}", "inLanguage": "en",
         "creator": {"@type": "Person", "@id": SITE + "/#me", "name": "Tomáš Dobos", "url": SITE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Projects", "item": SITE + "/#projects"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def write_headers():
    digest = "sha256-" + base64.b64encode(hashlib.sha256(INLINE_JS.encode("utf-8")).digest()).decode()
    csp = ("default-src 'self'; script-src 'self' '" + digest + "'; style-src 'self' 'unsafe-inline'; "
           "font-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; "
           "form-action 'self'; object-src 'none'")
    cfg = {"headers": [
        {"source": "/(.*)", "headers": [
            {"key": "Content-Security-Policy", "value": csp},
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "X-Frame-Options", "value": "DENY"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=()"},
            {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains"},
            {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"}]},
        {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800, stale-while-revalidate=86400"}]},
        {"source": "/(style\.css|script\.js)", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400, stale-while-revalidate=604800"}]},
    ]}
    with open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    print("wrote vercel.json", digest)


def page(p, idx):
    toc = "".join(f'<a href="#{sid}">{label}</a>' for sid, label, _ in p["sections"])
    body = "".join(f'<section class="pg-sec" id="{sid}"><h2>{label}</h2>{html}</section>' for sid, label, html in p["sections"])
    meta = "".join(f"<div><small>{k}</small><b>{v}</b></div>" for k, v in p["meta"])
    links = "".join(f'<a class="btn-or{" ghost" if i else ""}" href="{u}" target="_blank" rel="noopener">{t} <i>↗</i></a>' for i, (t, u) in enumerate(p["links"]))
    nslug, ntitle = p["next"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title']} | Tomáš Dobos</title>
<meta name="description" content="{p['lead'][:155]}">
<meta name="author" content="Tomáš Dobos">
<meta property="og:title" content="{p['title']} | Tomáš Dobos">
<meta property="og:description" content="{p['lead'][:155]}">
<meta property="og:type" content="article">
<link rel="canonical" href="{SITE}/projects/{p['slug']}.html">
<meta property="og:url" content="{SITE}/projects/{p['slug']}.html">
<meta property="og:site_name" content="Tomáš Dobos">
<meta property="og:image" content="{SITE}/assets/projects/{p['cover']}">
<meta property="og:image:alt" content="{p['title']} screenshot">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{p['title']} | Tomáš Dobos">
<meta name="twitter:description" content="{p['lead'][:155]}">
<meta name="twitter:image" content="{SITE}/assets/projects/{p['cover']}">
<script type="application/ld+json">{jsonld(p)}</script>
<meta name="theme-color" content="#e5541f">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23e5541f'/%3E%3Ctext x='16' y='22' font-family='Arial' font-weight='800' font-size='15' text-anchor='middle' fill='%23fff5ec'%3ETD%3C/text%3E%3C/svg%3E">
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/inter-tight-latin.woff2" crossorigin>
<link rel="stylesheet" href="../style.css">
<script>{INLINE_JS}</script>
</head>
<body class="pg">

<header class="nav show" id="nav">
  <div class="wrap nav-in">
    <a class="nav-brand" href="../index.html">Tomáš<sup>®</sup></a>
    <nav class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../index.html#about">About</a>
      <a href="../index.html#projects">Projects</a>
      <a href="../index.html#experience">Experience</a>
      <a href="../index.html#contact">Contact</a>
    </nav>
    <a class="pg-back" href="../index.html#projects">← All projects</a>
  </div>
</header>

<main>
  <section class="pg-hero">
    <div class="wrap">
      <p class="chip"><i></i>Project {p['num']} · {p['kicker']}</p>
      <h1>{p['title']}</h1>
      <p class="pg-lead">{p['lead']}</p>
      <div class="pg-meta">{meta}</div>
      <div class="btns pg-links">{links}</div>
    </div>
    <div class="wrap"><figure class="pg-cover"><img src="../assets/projects/{p['cover']}" width="{dims(p['cover'])[0]}" height="{dims(p['cover'])[1]}" alt="{p['title']} screenshot" fetchpriority="high"></figure></div>
  </section>

  <div class="wrap pg-layout">
    <aside class="pg-toc" aria-label="On this page"><small>On this page</small>{toc}</aside>
    <article class="pg-body">{body}</article>
  </div>

  <section class="pg-next">
    <div class="wrap">
      <small>Next project</small>
      <a href="{nslug}.html">{ntitle} <i>→</i></a>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="foot-bar"><span>© 2026 Tomáš Dobos</span><a href="../index.html#contact">Get in touch</a></div>
</footer>

<script src="../script.js"></script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for i, p in enumerate(PROJECTS):
        path = os.path.join(OUT, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page(p, i))
        print("wrote", os.path.relpath(path, ROOT))
    write_headers()


if __name__ == "__main__":
    main()
