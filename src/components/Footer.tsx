import { Link } from "react-router-dom";

const links = [
  { to: "/", label: "Accueil" },
  { to: "/a-propos", label: "À propos" },
  { to: "/services", label: "Nos Services" },
  { to: "/securite-reseaux", label: "Sécurité & Réseaux" },
  { to: "/contact", label: "Contact" },
];

export default function Footer() {
  return (
    <footer className="bg-navy-900 border-t border-white/10">
      <div className="mx-auto max-w-7xl px-5 py-14 lg:px-8">
        <div className="grid gap-10 md:grid-cols-3">
          <div>
            <Link to="/" className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400 to-navy-600">
                <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2 19 5v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V5Z" />
                  <path d="m9 12 2 2 4-4" />
                </svg>
              </span>
              <span className="flex flex-col leading-none">
                <span className="text-base font-extrabold text-white">Sannad Tech</span>
                <span className="text-[11px] font-medium uppercase tracking-[0.25em] text-cyan-400">Solutions</span>
              </span>
            </Link>
            <p className="mt-5 max-w-xs text-sm leading-relaxed text-slate-400">
              Ingénierie systèmes, réseaux et cybersécurité. Des infrastructures fiables,
              évolutives et sécurisées pour votre entreprise.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-white">Navigation</h4>
            <ul className="mt-5 space-y-3">
              {links.map((l) => (
                <li key={l.to}>
                  <Link to={l.to} className="text-sm text-slate-400 transition-colors hover:text-cyan-400">
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold uppercase tracking-wider text-white">Contact</h4>
            <ul className="mt-5 space-y-3 text-sm text-slate-400">
              <li>📍 Casablanca, Maroc</li>
              <li>📞 +212 5 XX XX XX XX</li>
              <li>✉️ contact@sannadtechsolutions.com</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-8 sm:flex-row">
          <p className="text-sm text-slate-500">
            © 2026 Sannad Tech Solutions. Tous droits réservés.
          </p>
          <Link to="/" className="text-sm text-slate-500 transition-colors hover:text-cyan-400">
            Mentions Légales
          </Link>
        </div>
      </div>
    </footer>
  );
}
