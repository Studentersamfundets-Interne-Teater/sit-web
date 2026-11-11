function Footer() {
  return (
    <footer className="footer">
      <div className="footer-flex-wrapper">
        <div className="footer-section">
          <p>
            <a href="http://127.0.0.1:8000/kontakt/" className="text-strong">
              Kontakt oss
            </a>
          </p>

          <p>
            Studentersamfundet
            <br />
            Elgeseter gate 1
            <br />
            7030 Trondheim
          </p>

          <p>
            <a href="mailto:sit@samfundet.no">sit@samfundet.no</a>
          </p>
        </div>

        <div className="footer-section">
          <p>
            <a href="http://127.0.0.1:8000/info/" className="text-strong">
              Om SIT
            </a>
          </p>

          <a
            href="https://www.samfundet.no/informasjon"
            target="_blank"
            rel="noreferrer noopener"
          >
            Om Studentersamfundet i Trondhjem
          </a>
        </div>

        <div className="footer-some footer-section">
          <a
            href="https://www.facebook.com/studentersamfundetsinterneteater"
            target="_blank"
            rel="noreferrer noopener"
            className="some-links"
          >
            <i className="fa fa-facebook" /> Facebook
          </a>

          <a
            href="https://www.instagram.com/samfundetsinterneteater"
            target="_blank"
            rel="noreferrer noopener"
            className="some-links"
          >
            <i className="fa fa-instagram" /> Instagram
          </a>

          <a
            href="https://www.snapchat.com/add/SITeater"
            target="_blank"
            rel="noreferrer noopener"
            className="some-links"
          >
            <i className="fa fa-snapchat" /> Snapchat
          </a>

          <a
            href="https://forms.gle/LE4BEM3dZiBwo5wv8"
            target="_blank"
            rel="noreferrer noopener"
            className="feedback-button"
          >
            Gi oss tilbakemelding!
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
