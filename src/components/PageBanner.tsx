import { Link } from "react-router-dom";

export default function PageBanner({
  title,
  subtitle,
  crumb,
}: {
  title: string;
  subtitle: string;
  crumb: string;
}) {
  return (
    <section className="relative overflow-hidden bg-navy-900 pt-36 pb-16 lg:pt-44 lg:pb-20">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -left-24 top-0 h-80 w-80 rounded-full bg-navy-600/40 blur-3xl" />
        <div className="absolute -right-24 bottom-0 h-80 w-80 rounded-full bg-cyan-500/20 blur-3xl" />
        <div
          className="absolute inset-0 opacity-[0.06]"
          style={{
            backgroundImage:
              "linear-gradient(to right, #fff 1px, transparent 1px), linear-gradient(to bottom, #fff 1px, transparent 1px)",
            backgroundSize: "54px 54px",
          }}
        />
      </div>

      <div className="relative mx-auto max-w-7xl px-5 lg:px-8">
        <nav className="flex items-center gap-2 text-sm text-slate-400">
          <Link to="/" className="transition-colors hover:text-cyan-400">Accueil</Link>
          <span>/</span>
          <span className="text-cyan-400">{crumb}</span>
        </nav>
        <h1 className="mt-4 max-w-3xl text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
          {title}
        </h1>
        <p className="mt-5 max-w-2xl text-lg leading-relaxed text-slate-300">{subtitle}</p>
      </div>
    </section>
  );
}
