const reasons = [
  {
    icon: "🎓",
    title: "Expertise Certifiée",
    desc: "Une maîtrise approfondie des meilleures technologies du marché.",
  },
  {
    icon: "🎯",
    title: "Approche Sur Mesure",
    desc: "Des solutions adaptées à la taille et aux défis réels de votre entreprise.",
  },
  {
    icon: "⚡",
    title: "Réactivité Maximale",
    desc: "Un support technique disponible pour garantir la continuité de vos activités.",
  },
  {
    icon: "🛡️",
    title: "Sécurité Native",
    desc: "La protection de vos données intégrée au cœur de chaque projet conçu.",
  },
];

const techs = ["Cisco", "Aruba", "Sophos", "FortiGate", "Wazuh", "Active Directory"];

export default function WhyUs() {
  return (
    <section id="securite" className="relative overflow-hidden bg-navy-900 py-24">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-0 h-80 w-80 -translate-x-1/2 rounded-full bg-cyan-500/10 blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-7xl px-5 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <span className="text-sm font-bold uppercase tracking-widest text-cyan-400">
            Pourquoi choisir Sannad Tech Solutions ?
          </span>
          <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            La sécurité et la performance, par conception
          </h2>
        </div>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {reasons.map((r) => (
            <div
              key={r.title}
              className="rounded-3xl border border-white/10 bg-white/5 p-7 backdrop-blur transition-colors hover:border-cyan-400/40 hover:bg-white/[0.08]"
            >
              <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500/20 to-navy-600/30 text-2xl">
                {r.icon}
              </div>
              <h3 className="mt-5 text-lg font-bold text-white">{r.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-400">{r.desc}</p>
            </div>
          ))}
        </div>

        <div className="mt-16 rounded-3xl border border-white/10 bg-gradient-to-r from-white/[0.06] to-transparent p-8 text-center">
          <p className="text-sm font-semibold uppercase tracking-widest text-slate-400">
            Technologies & partenaires
          </p>
          <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
            {techs.map((t) => (
              <span
                key={t}
                className="rounded-xl border border-white/10 bg-navy-800/60 px-5 py-2.5 text-sm font-semibold text-cyan-300"
              >
                {t}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
