from scraper.investing_scraper import ejecutar_scraping_indices
from scraper.bme_scraper import BmeScraper
from log_utils import log_info, log_error

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

    log_info("=== FIN DEL PROCESO DE SCRAPING ===")

if __name__ == "__main__":
    main()

















