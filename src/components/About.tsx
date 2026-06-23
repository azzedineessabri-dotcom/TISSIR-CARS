const points = [
  { title: "Fiables", desc: "Des infrastructures stables et résilientes." },
  { title: "Évolutives", desc: "Qui grandissent avec votre entreprise." },
  { title: "Sécurisées", desc: "La protection des données au cœur du design." },
];

export default function About() {
  return (
    <section id="apropos" className="relative bg-white py-24">
      <div className="mx-auto grid max-w-7xl items-center gap-14 px-5 lg:grid-cols-2 lg:px-8">
        <div className="relative">
          <div className="absolute -left-4 -top-4 h-24 w-24 rounded-2xl bg-cyan-100" />
          <div className="absolute -bottom-4 -right-4 h-32 w-32 rounded-2xl bg-navy-100" />
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-navy-800 to-navy-900 p-10 shadow-2xl">
            <div
              className="absolute inset-0 opacity-10"
              style={{
                backgroundImage:
                  "radial-gradient(circle at 20% 20%, #22d3ee 0, transparent 40%), radial-gradient(circle at 80% 80%, #3b82f6 0, transparent 40%)",
              }}
            />
            <div className="relative">
              <span className="text-5xl">🤝</span>
              <p className="mt-6 text-xl font-semibold leading-snug text-white">
                « Concentrez-vous sur votre cœur de métier. Nous gérons la complexité
                technique en toute sérénité. »
              </p>
              <div className="mt-6 h-1 w-16 rounded bg-cyan-400" />
              <p className="mt-4 text-sm font-medium text-cyan-300">
                L'équipe Sannad Tech Solutions
              </p>
            </div>
          </div>
        </div>

        <div>
          <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
            Qui sommes-nous ?
          </span>
          <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
            Votre partenaire de confiance en ingénierie systèmes & réseaux
          </h2>
          <p className="mt-6 text-lg leading-relaxed text-slate-600">
            Sannad Tech Solutions conçoit des infrastructures informatiques fiables,
            évolutives et hautement sécurisées pour permettre à votre entreprise de se
            concentrer sur son cœur de métier en toute sérénité.
          </p>

          <div className="mt-8 grid gap-5 sm:grid-cols-3">
            {points.map((p) => (
              <div key={p.title} className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-navy-700 text-white">
                  <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
                    <path d="m5 12 4 4L19 7" />
                  </svg>
                </div>
                <h3 className="mt-4 font-bold text-navy-900">{p.title}</h3>
                <p className="mt-1 text-sm text-slate-500">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
