import { useState } from "react";
import sitLogo from "../assets/sit_logo_without_text.svg";
import profileIcon from "../assets/sit_profile_icon.svg";

const DJANGO_URL = "http://127.0.0.1:8000";

function Navbar() {
  const [menyApen, setMenyApen] = useState(false);

  return (
    <nav className="topnav" aria-label="Hovedmeny">
      <a href={DJANGO_URL + "/"}>
        <img src={sitLogo} height={60} id="logo" alt="SIT" />
      </a>

      <div id="menuLinks" className={menyApen ? "menu-open" : ""}>
        <a href={DJANGO_URL + "/info/"}>Om SIT</a>
        <a href={DJANGO_URL + "/kontakt/"}>Kontakt</a>
        <a href={DJANGO_URL + "/medlemmer/"}>Medlemmer</a>
        <a href="/">Produksjoner</a>
        <a href={DJANGO_URL + "/numre/"}>Numre</a>
        <a href={DJANGO_URL + "/opptak/"}>Søk SIT</a>
      </div>

      <div id="status">
        <a href={DJANGO_URL + "/konto/login/"} className="logo">
          <img src={profileIcon} alt="" />
          Logg inn
        </a>
      </div>

      <button
        type="button"
        className="hamburger-icon"
        aria-label={menyApen ? "Lukk meny" : "Åpne meny"}
        aria-expanded={menyApen}
        aria-controls="menuLinks"
        onClick={() => setMenyApen(!menyApen)}
      >
        <i className="material-icons">{menyApen ? "close" : "menu"}</i>
      </button>
    </nav>
  );
}

export default Navbar;
