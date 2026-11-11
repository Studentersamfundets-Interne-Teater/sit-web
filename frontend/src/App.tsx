import { useEffect, useState } from "react";

type Produksjon = {
  id: number;
  tittel: string;
};

function App() {
  const [produksjoner, setProduksjoner] = useState<Produksjon[]>([]);
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

  return (
    <main>
      <h1>SIT Produksjoner</h1>

      {loading && <p>Laster produksjoner...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && (
        <ul>
          {produksjoner.map((produksjon) => (
            <li key={produksjon.id}>{produksjon.tittel}</li>
          ))}
        </ul>
      )}
    </main>
  );
}

export default App;
