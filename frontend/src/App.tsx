import { useEffect, useState } from "react";
import Footer from "./components/Footer";
import Navbar from "./components/Navbar";
import "./styles/style.css";

type Produksjon = {
  id: number;
  tittel: string;
  forfatter: string;
  premieredato: string;
  beskrivelse: string;
  banner: string | null;
  spilleperiode: string;
  produksjonstype: number;
  produksjonstype_display: string;
  lokaler: {
    id: number;
    navn: string;
  }[];
  tags: {
    id: number;
    navn: string;
  }[];
};

function App() {
  const [produksjoner, setProduksjoner] = useState<Produksjon[]>([]);
  const [sok, setSok] = useState("");
  const [forfatterSok, setForfatterSok] = useState("");
  const [fraAr, setFraAr] = useState("");
  const [tilAr, setTilAr] = useState("");
  const [fritekst, setFritekst] = useState("");

  const [visFilter, setVisFilter] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/api/produksjoner/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Kunne ikke hente produksjoner");
        }
        return response.json();
      })
      .then((data: Produksjon[]) => {
        setProduksjoner(data);
      })
      .catch((error: Error) => {
        setError(error.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const filtrerteProduksjoner = produksjoner.filter((produksjon) => {
    const ar = new Date(produksjon.premieredato).getFullYear();

    const matcherTittel = (produksjon.tittel ?? "")
      .toLowerCase()
      .includes(sok.trim().toLowerCase());

    const matcherForfatter = (produksjon.forfatter ?? "")
      .toLowerCase()
      .includes(forfatterSok.trim().toLowerCase());

    const matcherFraAr = !fraAr || ar >= Number(fraAr);
    const matcherTilAr = !tilAr || ar <= Number(tilAr);

    const matcherFritekst = (produksjon.beskrivelse ?? "")
      .toLowerCase()
      .includes(fritekst.trim().toLowerCase());

    return (
      matcherTittel &&
      matcherForfatter &&
      matcherFraAr &&
      matcherTilAr &&
      matcherFritekst
    );
  });

  return (
    <>
      <Navbar />
      <main className="production-wrapper">
        <div className="title-wrapper">
          <h2>Produksjoner</h2>
        </div>

        <div className="filter-and-result-container">
          <aside className="filter-column">
            <button
              type="button"
              className="filter-button"
              aria-expanded={visFilter}
              aria-controls="filter-container"
              onClick={() => setVisFilter(!visFilter)}
            >
              Filter {visFilter ? "▲" : "▼"}
            </button>

            <div
              id="filter-container"
              className={visFilter ? "filter-show" : "filter-hide"}
            >
              <div className="filter-category">
                <label htmlFor="produksjon-sok">Tittel</label>
                <input
                  id="produksjon-sok"
                  type="search"
                  placeholder="Søk etter tittel..."
                  value={sok}
                  onChange={(e) => setSok(e.target.value)}
                />
              </div>

              <div className="filter-category">
                <label htmlFor="forfatter-sok">Forfatter</label>
                <input
                  id="forfatter-sok"
                  type="search"
                  placeholder="Søk etter forfatter..."
                  value={forfatterSok}
                  onChange={(e) => setForfatterSok(e.target.value)}
                />
              </div>

              <div className="filter-category">
                <label>Spilleår</label>

                <div className="year-search-container">
                  <p>Se oppsetninger mellom</p>

                  <div className="year-inputs">
                    <input
                      type="number"
                      aria-label="Fra år"
                      placeholder="Fra år"
                      value={fraAr}
                      onChange={(e) => setFraAr(e.target.value)}
                    />

                    <span>og</span>

                    <input
                      type="number"
                      aria-label="Til år"
                      placeholder="Til år"
                      value={tilAr}
                      onChange={(e) => setTilAr(e.target.value)}
                    />
                  </div>
                </div>
              </div>

              <div className="filter-category">
                <label htmlFor="fritekst">Tekstsøk</label>
                <input
                  id="fritekst"
                  type="search"
                  placeholder="Søk i beskrivelse..."
                  value={fritekst}
                  onChange={(e) => setFritekst(e.target.value)}
                />
              </div>

              <button
                type="button"
                className="reset-filter-button"
                onClick={() => {
                  setSok("");
                  setForfatterSok("");
                  setFraAr("");
                  setTilAr("");
                  setFritekst("");
                }}
              >
                Nullstill filtre
              </button>
            </div>
          </aside>

          <section className="result-column" aria-label="Produksjoner">
            {loading && <p>Laster produksjoner...</p>}

            {error && <p role="alert">{error}</p>}

            {!loading && !error && (
              <>
                <p className="antall-resultater">
                  {filtrerteProduksjoner.length} produksjoner funnet
                </p>

                {filtrerteProduksjoner.length === 0 ? (
                  <p>Fant ingen produksjoner.</p>
                ) : (
                  <div className="card-wrapper">
                    {filtrerteProduksjoner.map((produksjon) => (
                      <a
                        className="card"
                        key={produksjon.id}
                        href={`http://127.0.0.1:8000/produksjon/${produksjon.id}/`}
                      >
                        {produksjon.banner && (
                          <img
                            src={produksjon.banner}
                            alt={`Banner for ${produksjon.tittel}`}
                            className="card-image"
                            loading="lazy"
                          />
                        )}
                        <div className="card-container">
                          <h3 className="card-title">{produksjon.tittel}</h3>

                          <div className="font-info text-strong">
                            {produksjon.premieredato
                              ? new Date(
                                  `${produksjon.premieredato}T00:00:00`,
                                ).toLocaleDateString("nb-NO")
                              : "Ukjent premieredato"}
                          </div>
                        </div>
                      </a>
                    ))}
                  </div>
                )}
              </>
            )}
          </section>
        </div>
      </main>
      <Footer />
    </>
  );
}

export default App;
