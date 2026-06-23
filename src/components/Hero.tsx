import { Link } from "react-router-dom";

const stats = [
  { value: "24/7", label: "Supervision" },
  { value: "100%", label: "Sécurité native" },
  { value: "+10", label: "Technologies maîtrisées" },
];

export default function Hero() {
  return (
    <section className="relative overflow-hidden bg-navy-900 pt-32 pb-20 lg:pt-44 lg:pb-28">
      {/* Background effects */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -left-32 top-10 h-96 w-96 rounded-full bg-navy-600/40 blur-3xl" />
        <div className="absolute -right-24 bottom-0 h-96 w-96 rounded-full bg-cyan-500/20 blur-3xl" />
        <div
          className="absolute inset-0 opacity-[0.07]"
          style={{
            backgroundImage:
              "linear-gradient(to right, #fff 1px, transparent 1px), linear-gradient(to bottom, #fff 1px, transparent 1px)",
            backgroundSize: "54px 54px",
          }}
        />
      </div>

      <div className="relative mx-auto grid max-w-7xl items-center gap-14 px-5 lg:grid-cols-2 lg:px-8">
        <div className="animate-fade-up">
          <span className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-cyan-300">
            <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400" />
            Ingénierie Systèmes & Réseaux
          </span>

          <h1 className="mt-6 text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">
            Propulsez et{" "}
            <span className="bg-gradient-to-r from-cyan-400 to-sky-300 bg-clip-text text-transparent">
              Sécurisez
            </span>{" "}
            votre Infrastructure Informatique.
          </h1>

          <p className="mt-6 max-w-xl text-lg leading-relaxed text-slate-300">
            Sannad Tech Solutions vous accompagne dans l'optimisation de vos réseaux,
            la cybersécurité et la maintenance de votre parc informatique avec des
            solutions sur mesure.
          </p>

          <div className="mt-9 flex flex-wrap gap-4">
            <Link
              to="/services"
              className="rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-400 px-7 py-3.5 text-sm font-semibold text-navy-900 shadow-xl shadow-cyan-500/30 transition-transform hover:scale-105"
            >
              Découvrir nos services
            </Link>
            <Link
              to="/contact"
              className="rounded-lg border border-white/20 bg-white/5 px-7 py-3.5 text-sm font-semibold text-white backdrop-blur transition-colors hover:bg-white/10"
            >
              Parler à un expert
            </Link>
          </div>

          <div className="mt-12 grid grid-cols-3 gap-6 border-t border-white/10 pt-8">
            {stats.map((s) => (
              <div key={s.label}>
                <div className="text-2xl font-extrabold text-cyan-400 lg:text-3xl">{s.value}</div>
                <div className="mt-1 text-xs font-medium text-slate-400">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Visual card */}
        <div className="relative hidden lg:block">
          <div className="animate-float-slow relative mx-auto max-w-md rounded-3xl border border-white/10 bg-gradient-to-br from-white/10 to-white/[0.02] p-6 backdrop-blur-xl shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-red-400/80" />
                <span className="h-3 w-3 rounded-full bg-yellow-400/80" />
                <span className="h-3 w-3 rounded-full bg-green-400/80" />
              </div>
              <span className="text-xs font-medium text-slate-400">monitoring.sannad</span>
            </div>

            <div className="mt-6 space-y-4">
              {[
                { icon: "🔒", title: "Firewall — FortiGate", status: "Actif", color: "text-green-400" },
                { icon: "🌐", title: "Cœur réseau — VLAN", status: "Stable", color: "text-cyan-400" },
                { icon: "🛡️", title: "EDR / SIEM — Wazuh", status: "0 menace", color: "text-green-400" },
                { icon: "📡", title: "Wi-Fi Pro — Aruba", status: "12 AP", color: "text-cyan-400" },
              ].map((row) => (
                <div
                  key={row.title}
                  className="flex items-center justify-between rounded-xl border border-white/10 bg-navy-800/60 px-4 py-3"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{row.icon}</span>
                    <span className="text-sm font-medium text-slate-200">{row.title}</span>
                  </div>
                  <span className={`text-xs font-semibold ${row.color}`}>{row.status}</span>
                </div>
              ))}
            </div>

            <div className="mt-6 rounded-xl bg-gradient-to-r from-cyan-500/20 to-transparent p-4">
              <div className="flex items-end justify-between gap-1.5">
                {[40, 65, 50, 80, 55, 90, 70, 95, 60].map((h, i) => (
                  <div
                    key={i}
                    className="w-full rounded-t bg-gradient-to-t from-cyan-500 to-cyan-300"
                    style={{ height: `${h}px` }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
