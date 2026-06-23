import PageBanner from "../components/PageBanner";
import Contact from "../components/Contact";

export default function ContactPage() {
  return (
    <>
      <PageBanner
        crumb="Contact"
        title="Discutons de votre projet"
        subtitle="Une question, un audit ou un devis ? Notre équipe vous répond rapidement pour étudier vos besoins et vous proposer la meilleure solution."
      />
      <Contact />
    </>
  );
}
