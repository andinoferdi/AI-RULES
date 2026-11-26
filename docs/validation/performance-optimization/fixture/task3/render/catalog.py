NAMES = ["welcome", "invoice", "receipt", "reminder", "password_reset", "digest",
         "invite", "trial_ending", "payment_failed", "export_ready", "comment", "goodbye"]

STRINGS = {
    "en": {"hello": "Hello", "thanks": "Thank you", "footer": "Sent by Lumen",
           "action": "Open Lumen", "amount": "Amount"},
    "id": {"hello": "Halo", "thanks": "Terima kasih", "footer": "Dikirim oleh Lumen",
           "action": "Buka Lumen", "amount": "Jumlah"},
    "nl": {"hello": "Hallo", "thanks": "Bedankt", "footer": "Verzonden door Lumen",
           "action": "Open Lumen", "amount": "Bedrag"},
}

BODY = ("{{t:hello}} {{name}},\n"
        "{{t:thanks}} for using Lumen. Item {{item}}: {{t:amount}} {{amount}}.\n"
        "[{{t:action}}](https://lumen.example/{{template}})\n"
        "-- {{t:footer}}\n")

# Each template is the shared body plus a template-specific block of 20 lines.
TEMPLATES = {
    name: BODY + "".join(f"<!-- {name} block line {n}: {{{{item}}}} -->\n" for n in range(20))
    for name in NAMES
}
