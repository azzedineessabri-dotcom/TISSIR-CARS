import PageBanner from "../components/PageBanner";
import WhyUs from "../components/WhyUs";
import CTA from "../components/CTA";

const security = [
  { icon: "🔍", title: "Audit & Pentest", desc: "Identification des vulnérabilités et évaluation de votre niveau de sécurité." },
  { icon: "🧱", title: "Pare-feu nouvelle génération", desc: "Protection périmétrique avancée avec FortiGate et Sophos." },
  { icon: "🚨", title: "EDR / SIEM", desc: "Détection et réponse aux menaces en temps réel avec Wazuh." },
  { icon: "🔐", title: "Sécurisation des données", desc: "Chiffrement, sauvegardes et plans de reprise d'activité (PRA)." },
];

const network = [
  { icon: "🔀", title: "Commutation & VLAN", desc: "Architecture réseau segmentée, performante et évolutive." },
  { icon: "📡", title: "Wi-Fi professionnel", desc: "Couverture optimale et sécurisée avec les bornes Aruba & Cisco." },
  { icon: "🗂️", title: "Active Directory & Cloud", desc: "Administration centralisée des utilisateurs et des ressources." },
  { icon: "📊", title: "Supervision 24/7", desc: "Monitoring continu pour anticiper et résoudre les incidents." },
];

function Grid({ title, items, accent }: { title: string; items: typeof security; accent: string }) {
  return (
    <div>
      <div className="flex items-center gap-3">
        <span className={`h-8 w-1.5 rounded-full ${accent}`} />
        <h2 className="text-2xl font-extrabold tracking-tight text-navy-900">{title}</h2>
      </div>
      <div className="mt-8 grid gap-6 sm:grid-cols-2">
        {items.map((it) => (
          <div key={it.title} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-start gap-4">
              <span className="text-3xl">{it.icon}</span>
              <div>
                <h3 className="font-bold text-navy-900">{it.title}</h3>
                <p className="mt-1.5 text-sm leading-relaxed text-slate-500">{it.desc}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function SecurityPage() {
  return (
    <>
      <PageBanner
        crumb="Sécurité & Réseaux"
        title="La sécurité et la performance réseau, par conception"
        subtitle="Nous construisons des infrastructures protégées de bout en bout, où chaque composant est pensé pour la résilience et la disponibilité."
      />

      <section className="bg-slate-50 py-24">
        <div className="mx-auto max-w-7xl space-y-16 px-5 lg:px-8">
          <Grid title="Cybersécurité" items={security} accent="bg-rose-500" />
          <Grid title="Réseaux & Systèmes" items={network} accent="bg-cyan-500" />
        </div>
      </section>

      <WhyUs />
      <CTA />
    </>
  );
}
