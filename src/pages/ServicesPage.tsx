import PageBanner from "../components/PageBanner";
import Services from "../components/Services";
import CTA from "../components/CTA";

const offers = [
  {
    icon: "🏢",
    title: "PME & TPE",
    desc: "Des solutions clé en main, économiques et fiables pour digitaliser et sécuriser votre activité.",
  },
  {
    icon: "🏭",
    title: "Entreprises & Industries",
    desc: "Des architectures réseau robustes, haute disponibilité et conformité aux normes de sécurité.",
  },
  {
    icon: "☁️",
    title: "Cloud & Hybride",
    desc: "Migration, administration et sécurisation de vos environnements cloud et hybrides.",
  },
];

export default function ServicesPage() {
  return (
    <>
      <PageBanner
        crumb="Nos Services"
        title="Des services complets pour toute votre infrastructure"
        subtitle="De la cybersécurité à la maintenance, en passant par les réseaux et les systèmes, nous couvrons l'ensemble de vos besoins informatiques."
      />

      <Services />

      {/* Pour qui */}
      <section className="bg-white py-24">
        <div className="mx-auto max-w-7xl px-5 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
              Des solutions adaptées
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
              À chaque structure, sa solution sur mesure
            </h2>
          </div>
          <div className="mt-14 grid gap-7 md:grid-cols-3">
            {offers.map((o) => (
              <div
                key={o.title}
                className="rounded-3xl border border-slate-200 bg-slate-50 p-8 transition-all hover:-translate-y-1 hover:shadow-xl"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-navy-700 text-3xl">
                  {o.icon}
                </div>
                <h3 className="mt-6 text-xl font-extrabold text-navy-900">{o.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-slate-600">{o.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CTA />
    </>
  );
}
