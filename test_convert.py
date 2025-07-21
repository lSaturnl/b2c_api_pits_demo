from weasyprint import HTML

# Конвертація et.htm → et.pdf (усі локальні ресурси підтягуються)
HTML('et.htm', base_url='.').write_pdf('et.pdf')
print("Готово! et.pdf створено.")