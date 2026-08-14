import Link from "next/link";
import {
  ArrowRight,
  ArrowUpRight,
  Building2,
  FlaskConical,
  Leaf,
  Recycle,
  Sprout,
  Sparkles,
} from "lucide-react";
import { AuthGate } from "@/components/AuthGate";
import { cn } from "@/lib/cn";
import { Cube3D } from "@/components/anim/Cube3D";
import { ParticleField } from "@/components/anim/ParticleField";
import { Reveal } from "@/components/anim/Reveal";
import { TiltCard } from "@/components/anim/TiltCard";

const PATH = [
  {
    title: "You describe the waste in your own words",
    text: '"Around 2 tonnes of spoiled onions from Nashik." A photo works too. No technical classification needed.',
  },
  {
    title: "AI builds a structured profile",
    text: "Type, quantity, condition, moisture, location. Every claim is labelled - AI inference or rule - never silently mixed.",
  },
  {
    title: "The best reuse is chosen, not guessed",
    text: "Anaerobic digestion, composting, vermicompost or biochar - compared against real buyer demand, capacity and distance.",
  },
  {
    title: "Buyers are ranked by your net return",
    text: "Earnings minus transport and fee, distance, pickup, capacity. Each score carries an auditable factor breakdown.",
  },
  {
    title: "A human-approved agent closes the deal",
    text: "You approve contact. The agent writes the outreach, negotiates within your floor - never below it - and reports the transcript.",
  },
];

const ROUTES = ["Anaerobic digestion", "Composting", "Vermicomposting", "Biochar"];

const SUPPLIERS = [
  "Vegetable wholesale markets",
  "Farms and orchards",
  "Restaurants and hotels",
  "Supermarkets and food processors",
];

const BUYERS = [
  "Biogas and AD plants",
  "Composting companies",
  "Vermicompost producers",
  "Organic processors",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-parchment text-ink">
      <AuthGate />
      <Hero />
      <Gap />
      <Path />
      <WhereItGoes />
      <Impact />
      <Quote />
      <CTA />
      <SiteFooter />
    </main>
  );
}

function Hero() {
  return (
    <section className="relative overflow-hidden bg-forest-950 text-white">
      <ParticleField className="absolute inset-0 h-full w-full opacity-70" />
      <div className="relative">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-5 py-6">
          <span className="flex items-center gap-2.5">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
              <Recycle className="h-5 w-5" />
            </span>
            <span className="font-display text-lg font-medium tracking-tight">Waste2Worth</span>
          </span>
          <div className="flex items-center gap-6 text-sm">
            <Link href="/login" className="hidden text-white/70 transition-colors hover:text-white sm:block">
              Sign in
            </Link>
            <Link
              href="/register"
              className="btn-3d rounded-md bg-lime-400 px-4 py-2 text-sm font-medium text-forest-950 transition-colors hover:bg-lime-300"
            >
              Create account
            </Link>
          </div>
        </nav>

        <div className="mx-auto grid max-w-6xl gap-12 px-5 pb-14 pt-14 lg:grid-cols-[1.15fr_0.85fr] lg:pb-20 lg:pt-20">
          <div>
            <Reveal>
              <p className="eyebrow flex items-center gap-2 text-lime-400">
                <span className="h-px w-8 bg-lime-400/60" /> AI waste recovery - India
              </p>
            </Reveal>
            <Reveal delay={70}>
              <h1 className="font-display mt-5 text-5xl font-medium leading-[1.02] tracking-tight md:text-7xl">
                Give waste a <em className="font-normal italic text-lime-400">second life.</em>
              </h1>
            </Reveal>
            <Reveal delay={140}>
              <p className="mt-6 max-w-xl text-lg leading-8 text-white/75">
                Waste2Worth prevents usable organic waste from becoming disposal waste. AI determines
                its highest-value reuse pathway - then autonomously connects it with a suitable buyer.
              </p>
            </Reveal>
            <Reveal delay={210}>
              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link
                  href="/register?role=supplier"
                  className="btn-3d group flex items-center justify-center gap-2 rounded-md bg-lime-400 px-6 py-3 text-sm font-semibold text-forest-950 transition-colors hover:bg-lime-300"
                >
                  I have waste
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
                <Link
                  href="/register?role=buyer"
                  className="group flex items-center justify-center gap-2 rounded-md border border-white/25 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-white/10"
                >
                  I need waste
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                </Link>
              </div>
            </Reveal>
          </div>

          <Reveal delay={180} className="relative">
            <div className="anim-float absolute -right-4 -top-8 z-10 hidden md:block">
              <Cube3D size={88} />
            </div>
            <TiltCard intensity={8}>
              <div className="glass-card rounded-2xl border border-white/15 bg-forest-900/60 p-6 backdrop-blur">
                <div className="mb-5 flex items-center justify-between">
                  <p className="eyebrow text-lime-400">Live recommendation</p>
                  <span className="anim-pulse-ring rounded-full bg-lime-400/20 px-2.5 py-0.5 text-xs font-medium text-lime-400">
                    AI ranked
                  </span>
                </div>

                <div className="divide-y divide-white/10">
                  <Row label="Waste" value="700 kg tomato" />
                  <Row label="Condition" value="Spoiled" />
                  <Row label="Best route" value="Anaerobic digestion" />
                  <Row label="Top buyer" value="GreenBio Energy - 1.4 km" />
                  <Row label="Estimated net" value="INR 20,370" />
                  <Row label="Agent" value="Negotiating within limits" />
                </div>

                <div className="mt-5 rounded-lg border border-white/12 bg-forest-950/60 p-4">
                  <p className="eyebrow text-lime-400">Why this buyer</p>
                  <p className="mt-2 text-sm leading-6 text-white/85">
                    Accepts tomato waste, has open capacity, arranges pickup, and offers the highest
                    estimated net return after transport.
                  </p>
                </div>
              </div>
            </TiltCard>
          </Reveal>
        </div>

        <div className="hairline-wt">
          <div className="mx-auto grid max-w-6xl grid-cols-1 gap-y-1 px-5 py-8 sm:grid-cols-3">
            {[
              { value: "0.10 kg", label: "methane per kg of food waste - if landfilled" },
              { value: "28x", label: "stronger than CO2 (81x over 20 years)" },
              { value: "2,800 kg", label: "CO2e avoided for every tonne diverted" },
            ].map((s, i) => (
              <Reveal key={s.label} delay={i * 100}>
                <div className="flex items-baseline gap-3 sm:flex-col sm:gap-1">
                  <span className="font-display tabular text-3xl font-medium text-lime-400">{s.value}</span>
                  <span className="text-sm leading-5 text-white/60">{s.label}</span>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between py-3 text-sm">
      <span className="text-white/55">{label}</span>
      <span className="font-medium text-white">{value}</span>
    </div>
  );
}

function SectionHeading({
  index,
  eyebrow,
  title,
  aside,
}: {
  index: string;
  eyebrow: string;
  title: React.ReactNode;
  aside?: React.ReactNode;
}) {
  return (
    <div className="hairline-b mb-12 flex flex-col justify-between gap-6 pb-6 lg:flex-row lg:items-end">
      <div className="max-w-2xl">
        <p className="eyebrow text-forest-700">
          <span className="text-ink-muted">{index}</span> - {eyebrow}
        </p>
        <h2 className="font-display mt-3 text-4xl font-medium tracking-tight text-ink md:text-5xl">
          {title}
        </h2>
      </div>
      {aside && <div className="max-w-sm text-sm leading-6 text-ink-muted lg:text-right">{aside}</div>}
    </div>
  );
}

function Gap() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-24">
      <SectionHeading
        index="01"
        eyebrow="The gap"
        title={
          <>
            Organic waste is a <em className="font-normal italic">mispriced asset</em> - dumped instead of recovered.
          </>
        }
        aside="A marketplace finds A buyer. Waste2Worth finds the right destination - the route and buyer that give waste its best practical and economic value."
      />

      <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr]">
        <Reveal>
          <div className="space-y-5 text-lg leading-9 text-ink-muted">
            <p>
              Markets, farms and restaurants discard tonnes of reusable material every week. In an
              open dump, that material <strong className="font-semibold text-ink">ferments into methane</strong> - a
              greenhouse gas roughly <strong className="font-semibold text-ink">28x stronger than CO2</strong>.
            </p>
            <p>
              The waste is not the problem. The destination is. When organic waste reaches a biogas
              plant or a composter, it becomes a feedstock. When it reaches a dump, it becomes a
              liability - for the planet and for whoever paid to haul it.
            </p>
          </div>
        </Reveal>
        <Reveal delay={120}>
          <div className="rounded-xl border border-ink/10 bg-white p-6 shadow-soft">
            <p className="eyebrow text-forest-700">One tonne of spoiled onions</p>
            <div className="mt-4 space-y-3">
              <Outcome label="Dumped at a landfill" value="~280 kg CO2e released" bad />
              <Outcome label="Recovered via biogas" value="~280 kg CO2e avoided" good />
              <Outcome label="Supplier" value="earns for the material" good />
              <Outcome label="Buyer" value="gets reliable feedstock" good />
            </div>
            <p className="mt-4 text-xs leading-5 text-ink-muted">
              Methane yield 0.10 kg CH4/kg, GWP 28 (IPCC AR5). Methodology in the product docs.
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

function Outcome({ label, value, bad, good }: { label: string; value: string; bad?: boolean; good?: boolean }) {
  return (
    <div className="flex items-center justify-between gap-3 border-b border-ink/5 pb-3 text-sm">
      <span className="text-ink-muted">{label}</span>
      <span className={cn("text-right font-medium", bad ? "text-red-700" : good ? "text-forest-700" : "text-ink")}>
        {value}
      </span>
    </div>
  );
}

function Path() {
  return (
    <section className="bg-moss-50 py-24">
      <div className="mx-auto max-w-6xl px-5">
        <SectionHeading
          index="02"
          eyebrow="The path"
          title={
            <>
              From surplus to feedstock - <em className="font-normal italic">with a paper trail</em>.
            </>
          }
          aside="Five steps, one goal: keep the waste out of the dump and the value with you."
        />

        <div>
          {PATH.map((step, i) => (
            <Reveal key={step.title} delay={i * 60}>
              <div className="group grid gap-3 border-b border-ink/10 py-7 transition-colors hover:bg-moss-100/60 lg:grid-cols-[3rem_1fr_auto] lg:items-start lg:gap-8">
                <span className="font-display tabular text-2xl font-medium text-moss-200 transition-colors duration-300 group-hover:text-lime-400">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="font-display text-xl font-medium text-ink">{step.title}</h3>
                  <p className="mt-1.5 max-w-2xl leading-7 text-ink-muted">{step.text}</p>
                </div>
                <Sparkles className="hidden h-5 w-5 text-forest-700/40 transition-colors duration-300 group-hover:text-lime-400 lg:mt-1 lg:block" />
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function WhereItGoes() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-24">
      <SectionHeading
        index="03"
        eyebrow="Where it goes"
        title={
          <>
            Two sides of one <em className="font-normal italic">purposeful</em> marketplace.
          </>
        }
        aside="Waste2Worth is a marketplace - but every deal is also an environmental decision. That is by design, not by accident."
      />

      <div className="grid gap-8 lg:grid-cols-2">
        <Reveal>
          <div className="relative flex h-full flex-col overflow-hidden rounded-2xl bg-forest-900 p-8 text-white shadow-lift">
            <div className="flex items-center justify-between">
              <p className="eyebrow text-lime-400">I have waste</p>
              <Sprout className="h-5 w-5 text-lime-400/70" />
            </div>
            <p className="font-display mt-3 text-2xl font-medium">You are sitting on a resource.</p>
            <p className="mt-2 text-sm leading-6 text-white/65">
              List it in your own words. AI structures it, ranks buyers by your net return, and an
              approved agent negotiates. You approve every step.
            </p>
            <ul className="mt-6 flex-1 space-y-2.5">
              {SUPPLIERS.map((s) => (
                <li key={s} className="flex items-center gap-2.5 text-sm text-white/80">
                  <span className="h-1.5 w-1.5 rounded-full bg-lime-400" /> {s}
                </li>
              ))}
            </ul>
            <Link
              href="/register?role=supplier"
              className="group mt-8 inline-flex items-center gap-2 text-sm font-semibold text-lime-400 hover:text-lime-300"
            >
              List your waste <ArrowUpRight className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </Link>
          </div>
        </Reveal>

        <Reveal delay={120}>
          <div className="relative flex h-full flex-col overflow-hidden rounded-2xl border border-ink/10 bg-white p-8 shadow-soft">
            <div className="flex items-center justify-between">
              <p className="eyebrow text-forest-700">I need waste</p>
              <Building2 className="h-5 w-5 text-forest-700/50" />
            </div>
            <p className="font-display mt-3 text-2xl font-medium text-ink">Reliable feedstock, matched to your process.</p>
            <p className="mt-2 text-sm leading-6 text-ink-muted">
              Set your requirements - type, volume, pickup. AI scores suppliers by demand, distance
              and capacity, so your plant runs full.
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              {ROUTES.map((r) => (
                <span
                  key={r}
                  className="rounded-full border border-forest-900/15 bg-moss-50 px-3 py-1 text-xs font-medium text-forest-800 transition-colors hover:bg-moss-100"
                >
                  {r}
                </span>
              ))}
            </div>
            <ul className="mt-6 flex-1 space-y-2.5">
              {BUYERS.map((b) => (
                <li key={b} className="flex items-center gap-2.5 text-sm text-ink-muted">
                  <span className="h-1.5 w-1.5 rounded-full bg-forest-800" /> {b}
                </li>
              ))}
            </ul>
            <Link
              href="/register?role=buyer"
              className="group mt-8 inline-flex items-center gap-2 text-sm font-semibold text-forest-900 hover:text-forest-700"
            >
              Register as a buyer <ArrowUpRight className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

function Impact() {
  const stats = [
    { value: "0.10", unit: "kg", label: "methane per kg of wet food waste in an uncaptured dump" },
    { value: "28x", unit: "", label: "100-year warming power of methane vs CO2 (IPCC AR5)" },
    { value: "2,800", unit: "kg", label: "CO2e avoided per tonne recovered - about 14,000 car-kilometres" },
  ];
  return (
    <section className="bg-forest-950 py-24 text-white">
      <div className="mx-auto max-w-6xl px-5">
        <div className="hairline-wt mb-12 flex flex-col justify-between gap-6 pb-6 lg:flex-row lg:items-end">
          <div className="max-w-2xl">
            <p className="eyebrow text-lime-400">
              <span className="text-white/50">04</span> - The accounting
            </p>
            <h2 className="font-display mt-3 text-4xl font-medium tracking-tight md:text-5xl">
              Every listing carries a <em className="font-normal italic text-lime-400">measurable</em> environmental number.
            </h2>
          </div>
          <p className="max-w-sm text-sm leading-6 text-white/55 lg:text-right">
            Not a green badge - a figure. Computed per listing, aggregated per platform, and traceable
            to a published methodology.
          </p>
        </div>

        <div className="grid gap-8 sm:grid-cols-3">
          {stats.map((s, i) => (
            <Reveal key={s.label} delay={i * 100}>
              <div className="hairline-wt pt-6">
                <p className="font-display tabular text-5xl font-medium text-lime-400">
                  {s.value}
                  {s.unit && <span className="text-2xl text-white/50"> {s.unit}</span>}
                </p>
                <p className="mt-3 max-w-xs text-sm leading-6 text-white/60">{s.label}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function Quote() {
  return (
    <section className="mx-auto max-w-4xl px-5 py-28 text-center">
      <Reveal>
        <FlaskConical className="mx-auto h-7 w-7 text-lime-400" />
        <blockquote className="font-display mt-8 text-3xl font-medium leading-snug tracking-tight text-ink md:text-4xl">
          &ldquo;I used to <em className="font-normal italic">pay</em> to get rid of spoiled produce. Now the
          agent finds a buyer and negotiates a price.&rdquo;
        </blockquote>
        <p className="eyebrow mt-8 text-forest-700">Market stall holder - Nashik</p>
      </Reveal>
    </section>
  );
}

function CTA() {
  return (
    <section className="bg-forest-900">
      <div className="mx-auto flex max-w-6xl flex-col items-center px-5 py-24 text-center text-white">
        <Reveal>
          <p className="eyebrow text-lime-400">Start with your waste</p>
          <h2 className="font-display mt-4 max-w-2xl text-4xl font-medium tracking-tight md:text-5xl">
            Turn what you throw away into <em className="font-normal italic text-lime-400">what you earn.</em>
          </h2>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link
              href="/register?role=supplier"
              className="btn-3d rounded-md bg-lime-400 px-7 py-3 text-sm font-semibold text-forest-950 transition-colors hover:bg-lime-300"
            >
              List your first waste
            </Link>
            <Link href="/register" className="btn-3d rounded-md border border-white/25 px-7 py-3 text-sm font-semibold text-white transition-colors hover:bg-white/10">
              Create an account
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

function SiteFooter() {
  return (
    <footer className="bg-forest-950 text-white">
      <div className="mx-auto max-w-6xl px-5 py-14">
        <div className="flex flex-col items-start justify-between gap-10 md:flex-row">
          <div className="max-w-sm">
            <span className="flex items-center gap-2.5 font-display text-lg font-medium tracking-tight">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
                <Recycle className="h-5 w-5" />
              </span>
              Waste2Worth
            </span>
            <p className="mt-4 text-sm leading-6 text-white/60">
              Preventing usable organic waste from becoming disposal waste. AI finds the highest-value
              reuse pathway; an approved agent connects it with a suitable buyer.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-10 text-sm">
            <div>
              <p className="eyebrow text-lime-400">Get started</p>
              <div className="mt-4 space-y-2.5 text-white/70">
                <p><Link href="/register?role=supplier" className="transition-colors hover:text-white">I have waste</Link></p>
                <p><Link href="/register?role=buyer" className="transition-colors hover:text-white">I need waste</Link></p>
                <p><Link href="/login" className="transition-colors hover:text-white">Sign in</Link></p>
              </div>
            </div>
            <div>
              <p className="eyebrow text-lime-400">Why it matters</p>
              <div className="mt-4 space-y-2.5 text-white/70">
                <p>Methane is ~28x stronger than CO2</p>
                <p>Recovery beats landfill</p>
                <p>Suppliers earn from surplus</p>
              </div>
            </div>
          </div>
        </div>
        <div className="hairline-wt mt-12 flex flex-col gap-2 pt-5 text-xs text-white/45 sm:flex-row sm:justify-between">
          <p>Waste2Worth - give waste a second life.</p>
          <p className="flex items-center gap-1.5">
            <Leaf className="h-3 w-3 text-lime-400/70" /> Made for the AI 4 Earth hackathon.
          </p>
        </div>
      </div>
    </footer>
  );
}
