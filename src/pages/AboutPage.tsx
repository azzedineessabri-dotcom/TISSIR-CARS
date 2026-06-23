import PageBanner from "../components/PageBanner";
import About from "../components/About";
import CTA from "../components/CTA";

const values = [
  { icon: "🎓", title: "Expertise", desc: "Des ingénieurs certifiés sur les technologies leaders du marché." },
  { icon: "🤝", title: "Proximité", desc: "Un accompagnement humain et un interlocuteur dédié à votre projet." },
  { icon: "🔐", title: "Confidentialité", desc: "Le respect et la protection de vos données comme priorité absolue." },
  { icon: "🚀", title: "Innovation", desc: "Une veille permanente pour des solutions toujours à la pointe." },
];

const milestones = [
  { num: "01", title: "Écoute & Audit", desc: "Nous analysons votre existant et vos objectifs." },
  { num: "02", title: "Conception", desc: "Nous concevons une architecture sur mesure et sécurisée." },
  { num: "03", title: "Déploiement", desc: "Nous mettons en œuvre la solution avec rigueur." },
  { num: "04", title: "Accompagnement", desc: "Nous supervisons et maintenons votre infrastructure." },
];

export default function AboutPage() {
  return (
    <>
      <PageBanner
        crumb="À propos"
        title="Votre partenaire de confiance en ingénierie systèmes & réseaux"
        subtitle="Sannad Tech Solutions accompagne les entreprises et PME dans la conception d'infrastructures informatiques fiables, évolutives et hautement sécurisées."
      />

      <About />

      {/* Valeurs */}
      <section className="bg-slate-50 py-24">
        <div className="mx-auto max-w-7xl px-5 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
              Nos valeurs
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
              Ce qui guide chacune de nos missions
            </h2>
          </div>
          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((v) => (
              <div key={v.title} className="rounded-3xl border border-slate-200 bg-white p-7 shadow-sm">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-navy-50 text-2xl">
                  {v.icon}
                </div>
                <h3 className="mt-5 text-lg font-bold text-navy-900">{v.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-500">{v.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Méthode */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-5 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
              Notre méthode
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
              Une démarche structurée, du premier contact au support
            </h2>
          </div>
          <div className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {milestones.map((m) => (
              <div key={m.num} className="relative rounded-3xl bg-gradient-to-br from-navy-800 to-navy-900 p-7 text-white">
                <span className="text-4xl font-extrabold text-cyan-400/40">{m.num}</span>
                <h3 className="mt-3 text-lg font-bold">{m.title}</h3>
                <p className="mt-2 text-sm text-slate-300">{m.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CTA />
    </>
  );
}
