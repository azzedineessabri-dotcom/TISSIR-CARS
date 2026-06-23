const services = [
  {
    icon: "🔒",
    title: "Cybersécurité",
    accent: "from-rose-500 to-red-500",
    items: [
      "Audit de sécurité",
      "Protection périmétrique (Firewalls)",
      "Détection des menaces (EDR / SIEM)",
      "Sécurisation des données",
    ],
  },
  {
    icon: "🌐",
    title: "Réseaux & Systèmes",
    accent: "from-cyan-500 to-sky-500",
    items: [
      "Architecture & commutation (VLAN, Stacking)",
      "Solutions Wi-Fi professionnelles",
      "Administration systèmes (Active Directory, Cloud)",
      "Supervision 24/7",
    ],
  },
  {
    icon: "🛠️",
    title: "Support & Maintenance",
    accent: "from-amber-500 to-orange-500",
    items: [
      "Support technique (Helpdesk)",
      "Maintenance préventive & curative",
      "Gestion de parc informatique",
      "Infogérance sur mesure",
    ],
  },
];

export default function Services() {
  return (
    <section id="services" className="relative bg-slate-50 py-24">
      <div className="mx-auto max-w-7xl px-5 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
            Nos domaines d'expertise
          </span>
          <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
            Des services complets pour toute votre infrastructure
          </h2>
          <p className="mt-4 text-lg text-slate-600">
            Trois piliers complémentaires pour bâtir, protéger et maintenir votre
            système d'information.
          </p>
        </div>

        <div className="mt-14 grid gap-7 md:grid-cols-3">
          {services.map((s) => (
            <div
              key={s.title}
              className="group relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-8 shadow-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl"
            >
              <div className={`absolute inset-x-0 top-0 h-1.5 bg-gradient-to-r ${s.accent}`} />
              <div
                className={`flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${s.accent} text-3xl shadow-lg`}
              >
                {s.icon}
              </div>
              <h3 className="mt-6 text-xl font-extrabold text-navy-900">{s.title}</h3>
              <ul className="mt-5 space-y-3">
                {s.items.map((it) => (
                  <li key={it} className="flex items-start gap-3 text-sm text-slate-600">
                    <svg viewBox="0 0 24 24" className="mt-0.5 h-4 w-4 shrink-0 text-cyan-500" fill="none" stroke="currentColor" strokeWidth={3} strokeLinecap="round" strokeLinejoin="round">
                      <path d="m5 12 4 4L19 7" />
                    </svg>
                    {it}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
