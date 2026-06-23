import { useState } from "react";

const contactInfo = [
  { icon: "📍", label: "Adresse", value: "Casablanca, Maroc" },
  { icon: "📞", label: "Téléphone", value: "+212 5 XX XX XX XX" },
  { icon: "✉️", label: "Email", value: "contact@sannadtechsolutions.com" },
];

export default function Contact() {
  const [sent, setSent] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => setSent(false), 5000);
  };

  return (
    <section id="contact" className="relative bg-white py-24">
      <div className="mx-auto max-w-7xl px-5 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2">
          {/* Left: info */}
          <div>
            <span className="text-sm font-bold uppercase tracking-widest text-cyan-600">
              Contact
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-navy-900 sm:text-4xl">
              Discutons de votre projet
            </h2>
            <p className="mt-5 max-w-md text-lg text-slate-600">
              Une question, un audit ou un devis ? Notre équipe vous répond rapidement
              pour étudier vos besoins.
            </p>

            <div className="mt-10 space-y-5">
              {contactInfo.map((c) => (
                <div key={c.label} className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-50 text-xl">
                    {c.icon}
                  </div>
                  <div>
                    <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      {c.label}
                    </div>
                    <div className="font-semibold text-navy-900">{c.value}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-10 rounded-2xl bg-navy-900 p-6 text-white">
              <div className="flex items-center gap-3">
                <span className="flex h-3 w-3">
                  <span className="absolute h-3 w-3 animate-ping rounded-full bg-cyan-400 opacity-75" />
                  <span className="h-3 w-3 rounded-full bg-cyan-400" />
                </span>
                <span className="text-sm font-semibold">Support disponible 24/7</span>
              </div>
              <p className="mt-2 text-sm text-slate-400">
                Nous garantissons la continuité de vos activités à tout moment.
              </p>
            </div>
          </div>

          {/* Right: form */}
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-8 shadow-sm">
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-5 sm:grid-cols-2">
                <Field label="Nom" name="nom" placeholder="Votre nom" />
                <Field label="Entreprise" name="entreprise" placeholder="Votre société" />
              </div>
              <div className="grid gap-5 sm:grid-cols-2">
                <Field label="Téléphone" name="tel" type="tel" placeholder="+212 ..." />
                <Field label="Email" name="email" type="email" placeholder="vous@email.com" required />
              </div>
              <div>
                <label className="mb-1.5 block text-sm font-semibold text-navy-900">
                  Message
                </label>
                <textarea
                  name="message"
                  rows={4}
                  required
                  placeholder="Décrivez votre besoin..."
                  className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-navy-900 outline-none transition-colors placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                />
              </div>

              <button
                type="submit"
                className="w-full rounded-xl bg-gradient-to-r from-navy-700 to-navy-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-navy-600/30 transition-transform hover:scale-[1.02]"
              >
                Envoyer ma demande
              </button>

              {sent && (
                <p className="rounded-xl bg-green-50 px-4 py-3 text-center text-sm font-medium text-green-700">
                  ✅ Merci ! Votre message a bien été envoyé. Nous vous recontactons rapidement.
                </p>
              )}
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}

function Field({
  label,
  name,
  type = "text",
  placeholder,
  required,
}: {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  required?: boolean;
}) {
  return (
    <div>
      <label className="mb-1.5 block text-sm font-semibold text-navy-900">{label}</label>
      <input
        type={type}
        name={name}
        required={required}
        placeholder={placeholder}
        className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-navy-900 outline-none transition-colors placeholder:text-slate-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
      />
    </div>
  );
}
