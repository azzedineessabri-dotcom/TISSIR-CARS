import { Link } from "react-router-dom";

export default function CTA() {
  return (
    <section className="bg-white py-20">
      <div className="mx-auto max-w-7xl px-5 lg:px-8">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-navy-800 to-navy-900 px-8 py-14 text-center shadow-2xl lg:px-16">
          <div
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage:
                "radial-gradient(circle at 15% 20%, #22d3ee 0, transparent 40%), radial-gradient(circle at 85% 80%, #3b82f6 0, transparent 40%)",
            }}
          />
          <div className="relative">
            <h2 className="mx-auto max-w-2xl text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              Prêt à sécuriser et optimiser votre infrastructure ?
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-lg text-slate-300">
              Échangeons sur vos besoins. Obtenez un audit et un devis personnalisé,
              sans engagement.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link
                to="/contact"
                className="rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-400 px-7 py-3.5 text-sm font-semibold text-navy-900 shadow-xl shadow-cyan-500/30 transition-transform hover:scale-105"
              >
                Demander un devis
              </Link>
              <Link
                to="/services"
                className="rounded-lg border border-white/20 bg-white/5 px-7 py-3.5 text-sm font-semibold text-white backdrop-blur transition-colors hover:bg-white/10"
              >
                Voir nos services
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
