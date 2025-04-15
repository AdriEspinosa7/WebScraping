from scraper.investing_scraper import ejecutar_scraping_indices
from scraper.bme_scraper import BmeScraper
from scraper.ibex_pdf_scraper import IbexPDFScraper
from log_utils import log_info, log_error

# Ejecutar verificación de requisitos antes de comenzar
import requirements_check

def main():
    log_info("=== INICIO DEL PROCESO DE SCRAPING ===")

    try:
        ejecutar_scraping_indices()
        log_info("✅ Scraping de índices completado.")
    except Exception as e:
        log_error(f"❌ Error durante el scraping de índices: {e}")

    try:
        scraper_bme = BmeScraper()
        scraper_bme.ejecutar()
        log_info("✅ Scraping de empresas BME completado.")
    except Exception as e:
        log_error(f"❌ Error durante el scraping de empresas BME: {e}")

    try:
        scraper_ibex = IbexPDFScraper()
        scraper_ibex.ejecutar()
        log_info("✅ Scraping de PDFs de IBEX 35 completado.")
    except Exception as e:
        log_error(f"❌ Error durante el scraping de PDFs IBEX 35: {e}")

    log_info("=== FIN DEL PROCESO DE SCRAPING ===")

if __name__ == "__main__":
    main()



















