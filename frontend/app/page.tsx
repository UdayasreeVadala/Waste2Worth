import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Bot,
  Building2,
  FlaskConical,
  Leaf,
  Recycle,
  Route,
  Sparkles,
  Target,
  Users,
} from "lucide-react";
import { AuthGate } from "@/components/AuthGate";
import { cn } from "@/lib/cn";

const JOURNEY = [
  { icon: Recycle, title: "Waste", text: "You list what you have — tomatoes, peels, produce, food." },
  { icon: Sparkles, title: "AI Analysis", text: "Waste2Worth builds a structured profile of the material." },
  { icon: Route, title: "Best Use", text: "The AI compares economic routes, not just the nearest buyer." },
  { icon: Building2, title: "Buyer", text: "Suitable buyers are ranked by net return, distance and capacity." },
  { icon: Leaf, title: "Resource", text: "An AI agent closes the deal. The waste becomes a feedstock." },
];

const STEPS = [
  {
    step: "01",
    title: "List your waste",
    text: "Type, quantity, condition, location. No technical classifications needed.",
  },
  {
    step: "02",
    title: "AI finds the best destination",
    text: "The engine compares routes like composting, anaerobic digestion and vermicomposting against live buyer demand.",
  },
  {
    step: "03",
    title: "Compare real returns",
    text: "See buyer offers, estimated transport, platform fee and your estimated net earnings side by side.",
  },
  {
    step: "04",
    title: "Approve the AI agent",
    text: "After your permission, the agent contacts the buyer, negotiates within your limits and reports back.",
  },
  {
    step: "05",
    title: "Track the deal to completion",
    text: "Pickup, collection and completion are tracked in a transparent transaction timeline.",
  },
];

const METRICS = [
  { icon: Leaf, value: "Tonnage", label: "organic waste diverted from disposal", accent: "lime" },
  { icon: Users, value: "2 actor types", label: "suppliers with waste, buyers with capacity", accent: "moss" },
  { icon: Bot, value: "AI-first", label: "recommendation, ranking and agent negotiation", accent: "lime" },
  { icon: BarChart3, value: "Net returns", label: "estimated before any deal is closed", accent: "moss" },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-parchment text-ink">
      <AuthGate />
      <Hero />
      <Problem />
      <Journey />
      <HowItWorks />
      <UseCases />
      <Metrics />
      <CTA />
    </main>
  );
}

function Hero() {
  return (
    <section className="bg-forest-950 text-white">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
        <span className="flex items-center gap-2 font-semibold tracking-wide">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
            <Recycle className="h-5 w-5" />
          </span>
          Waste2Worth
        </span>
        <div className="flex items-center gap-4 text-sm">
          <Link href="/login" className="hidden text-white/75 hover:text-white sm:block">
            Sign in
          </Link>
          <Link
            href="/register"
            className="rounded-md bg-lime-400 px-4 py-2 text-sm font-medium text-forest-950 hover:bg-lime-300"
          >
            Create account
          </Link>
        </div>
      </nav>

      <div className="mx-auto grid max-w-6xl gap-10 px-5 pb-16 pt-14 lg:grid-cols-[1.1fr_0.9fr] lg:pb-24 lg:pt-20">
        <div>
          <p className="mb-4 flex items-center gap-2 text-sm font-medium uppercase tracking-[0.22em] text-lime-400">
            <Sparkles className="h-4 w-4" />
            AI-powered organic waste recovery
          </p>
          <h1 className="text-5xl font-semibold leading-[1.05] tracking-tight md:text-7xl">
            Give waste a second life.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-white/80">
            Waste2Worth uses AI to find the most valuable destination for organic waste and connects
            waste owners with the businesses that can turn it into biogas, compost and other
            resources.
          </p>

          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/register?role=supplier"
              className="group flex items-center justify-center gap-2 rounded-md bg-lime-400 px-6 py-3 text-sm font-semibold text-forest-950 transition-colors hover:bg-lime-300"
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
        </div>

        <div className="relative">
          <div className="rounded-2xl border border-white/15 bg-forest-900/60 p-6 shadow-2xl backdrop-blur">
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm font-medium text-white/80">Live recommendation</p>
              <span className="rounded-full bg-lime-400/20 px-2.5 py-0.5 text-xs font-medium text-lime-400">
                AI ranked
              </span>
            </div>

            <div className="space-y-3">
              <Row label="Waste" value="700 kg tomato waste" />
              <Row label="Condition" value="Spoiled" />
              <Row label="Best route" value="Anaerobic digestion" />
              <Row label="Top buyer" value="GreenBio Energy — 1.4 km" />
              <Row label="Estimated net" value="INR 20,370" />
              <Row label="Agent" value="Negotiating within limits" />
            </div>

            <div className="mt-5 rounded-lg border border-white/15 bg-forest-950/60 p-4">
              <p className="text-xs font-medium uppercase tracking-wider text-lime-400">Why this buyer</p>
              <p className="mt-2 text-sm leading-6 text-white/85">
                Accepts tomato waste, has open capacity, arranges pickup, and offers the highest
                estimated net return after transport.
              </p>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-3 gap-3 text-center">
            {[["Route", "Biogas"], ["Distance", "1.4 km"], ["Pickup", "Included"]].map(([key, value]) => (
              <div key={key} className="rounded-xl border border-white/15 bg-white/5 p-4">
                <p className="text-xs uppercase tracking-wider text-white/55">{key}</p>
                <p className="mt-1 text-sm font-semibold">{value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between rounded-lg border border-white/10 bg-forest-950/50 px-4 py-3 text-sm">
      <span className="text-white/60">{label}</span>
      <span className="font-medium text-white">{value}</span>
    </div>
  );
}

function Problem() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-20 lg:py-24">
      <div className="grid gap-10 lg:grid-cols-2">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-forest-800">The problem</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Organic waste is a mispriced asset.
          </h2>
          <p className="mt-5 max-w-lg leading-8 text-ink-muted">
            Markets, farms, restaurants and supermarkets discard tonnes of perfectly reusable material.
            A simple marketplace finds A buyer. Waste2Worth finds the <em>right</em> destination — the
            route and buyer that give the waste its best practical and economic value.
          </p>
        </div>
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-forest-800">The solution</p>
          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            Waste → AI analysis → best use → buyer → resource.
          </h2>
          <p className="mt-5 max-w-lg leading-8 text-ink-muted">
            The platform analyzes the material, compares processing routes and buyer demand, estimates
            your real net return, and then uses an AI agent — only after your approval — to contact,
            negotiate and track the deal until the waste is collected.
          </p>
        </div>
      </div>
    </section>
  );
}

function Journey() {
  return (
    <section className="bg-forest-950 py-20 text-white">
      <div className="mx-auto max-w-6xl px-5">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-lime-400">The journey</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          One path from surplus to feedstock.
        </h2>
        <div className="mt-10 grid gap-4 md:grid-cols-5">
          {JOURNEY.map((item, index) => (
            <div
              key={item.title}
              className="relative rounded-xl border border-white/12 bg-forest-900/70 p-5"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
                <item.icon className="h-5 w-5" />
              </div>
              <p className="mt-4 text-sm font-semibold uppercase tracking-wider text-lime-400">
                {String(index + 1).padStart(2, "0")}
              </p>
              <h3 className="mt-1 font-semibold">{item.title}</h3>
              <p className="mt-2 text-sm leading-6 text-white/70">{item.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function HowItWorks() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-20 lg:py-24">
      <p className="text-sm font-medium uppercase tracking-[0.2em] text-forest-800">How it works</p>
      <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
        From listing to a completed transaction.
      </h2>
      <div className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        {STEPS.map((step) => (
          <div key={step.step} className="rounded-xl border border-ink/10 bg-white p-5">
            <p className="text-3xl font-semibold text-moss-200">{step.step}</p>
            <h3 className="mt-3 font-semibold text-ink">{step.title}</h3>
            <p className="mt-2 text-sm leading-6 text-ink-muted">{step.text}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function UseCases() {
  const suppliers = [
    "Farmers and wholesale markets",
    "Restaurants and hotels",
    "Supermarkets and food processors",
    "Cafeterias and institutions",
  ];
  const buyers = [
    "Composting companies",
    "Biogas and anaerobic digestion plants",
    "Vermicompost producers",
    "Biochar and organic processors",
  ];
  return (
    <section className="bg-moss-50 py-20">
      <div className="mx-auto max-w-6xl px-5">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-forest-800">Who it connects</p>
        <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
          Two sides of one marketplace.
        </h2>
        <div className="mt-10 grid gap-4 lg:grid-cols-2">
          {[
            {
              icon: Target,
              title: "I have waste",
              items: suppliers,
              accent: true,
              cta: { label: "List your waste", href: "/register?role=supplier" },
            },
            {
              icon: Leaf,
              title: "I need waste",
              items: buyers,
              accent: false,
              cta: { label: "Register as a buyer", href: "/register?role=buyer" },
            },
          ].map((card) => (
            <div
              key={card.title}
              className={cn(
                "rounded-xl border p-8",
                card.accent ? "border-forest-900 bg-forest-900 text-white" : "border-ink/10 bg-white"
              )}
            >
              <card.icon className={cn("h-7 w-7", card.accent ? "text-lime-400" : "text-forest-800")} />
              <h3 className="mt-4 text-xl font-semibold">{card.title}</h3>
              <ul className="mt-5 space-y-2.5">
                {card.items.map((item) => (
                  <li key={item} className="flex items-start gap-2 text-sm">
                    <span className={cn("mt-1.5 h-1.5 w-1.5 rounded-full", card.accent ? "bg-lime-400" : "bg-forest-800")} />
                    <span className={cn(card.accent ? "text-white/85" : "text-ink-muted")}>{item}</span>
                  </li>
                ))}
              </ul>
              <Link
                href={card.cta.href}
                className={cn(
                  "group mt-7 inline-flex items-center gap-2 rounded-md px-5 py-2.5 text-sm font-semibold transition-colors",
                  card.accent
                    ? "bg-lime-400 text-forest-950 hover:bg-lime-300"
                    : "bg-forest-900 text-white hover:bg-forest-700"
                )}
              >
                {card.cta.label}
                <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Metrics() {
  return (
    <section className="border-y border-ink/10 bg-white">
      <div className="mx-auto grid max-w-6xl gap-px px-5 py-16 sm:grid-cols-2 lg:grid-cols-4">
        {METRICS.map((metric) => (
          <div key={metric.label} className="px-2">
            <metric.icon
              className={cn("h-6 w-6", metric.accent === "lime" ? "text-lime-400" : "text-forest-800")}
            />
            <p className="mt-4 text-2xl font-semibold">{metric.value}</p>
            <p className="mt-1 text-sm text-ink-muted">{metric.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function CTA() {
  return (
    <section className="mx-auto max-w-6xl px-5 py-20 text-center">
      <FlaskConical className="mx-auto h-8 w-8 text-forest-800" />
      <h2 className="mx-auto mt-4 max-w-2xl text-3xl font-semibold tracking-tight md:text-4xl">
        The platform does not simply find someone who wants the waste.
      </h2>
      <p className="mx-auto mt-5 max-w-2xl leading-8 text-ink-muted">
        It determines where that waste has the best practical and economic destination — then sends an
        AI agent to close the deal for you.
      </p>
      <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
        <Link
          href="/register?role=supplier"
          className="rounded-md bg-forest-900 px-6 py-3 text-sm font-semibold text-white hover:bg-forest-700"
        >
          Start with your waste
        </Link>
        <Link href="/register" className="rounded-md border border-ink/20 px-6 py-3 text-sm font-semibold hover:bg-moss-100">
          Create an account
        </Link>
      </div>
    </section>
  );
}