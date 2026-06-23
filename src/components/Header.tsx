import { useEffect, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";

const links = [
  { to: "/", label: "Accueil" },
  { to: "/a-propos", label: "À propos" },
  { to: "/services", label: "Nos Services" },
  { to: "/securite-reseaux", label: "Sécurité & Réseaux" },
  { to: "/contact", label: "Contact" },
];

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-navy-900/90 backdrop-blur-lg shadow-lg shadow-navy-900/30"
          : "bg-navy-900/40 backdrop-blur-sm"
      }`}
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 lg:px-8">
        <Link to="/" className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400 to-navy-600 shadow-lg shadow-cyan-500/30">
            <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2 19 5v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V5Z" />
              <path d="m9 12 2 2 4-4" />
            </svg>
          </span>
          <span className="flex flex-col leading-none">
            <span className="text-base font-extrabold tracking-tight text-white">Sannad Tech</span>
            <span className="text-[11px] font-medium uppercase tracking-[0.25em] text-cyan-400">Solutions</span>
          </span>
        </Link>

        <div className="hidden items-center gap-8 lg:flex">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors hover:text-cyan-400 ${
                  isActive ? "text-cyan-400" : "text-slate-200"
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </div>

        <div className="hidden lg:block">
          <Link
            to="/contact"
            className="rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-400 px-5 py-2.5 text-sm font-semibold text-navy-900 shadow-lg shadow-cyan-500/30 transition-transform hover:scale-105"
          >
            Demander un devis
          </Link>
        </div>

        <button
          onClick={() => setOpen((o) => !o)}
          className="flex h-10 w-10 items-center justify-center rounded-lg text-white lg:hidden"
          aria-label="Menu"
        >
          <svg viewBox="0 0 24 24" className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round">
            {open ? <path d="M6 6 18 18M18 6 6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
      </nav>

      {open && (
        <div className="border-t border-white/10 bg-navy-900/95 px-5 py-4 lg:hidden">
          <div className="flex flex-col gap-1">
            {links.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                className={({ isActive }) =>
                  `rounded-lg px-3 py-3 text-sm font-medium hover:bg-white/5 hover:text-cyan-400 ${
                    isActive ? "text-cyan-400" : "text-slate-200"
                  }`
                }
              >
                {l.label}
              </NavLink>
            ))}
            <Link
              to="/contact"
              className="mt-2 rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-400 px-5 py-3 text-center text-sm font-semibold text-navy-900"
            >
              Demander un devis
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
