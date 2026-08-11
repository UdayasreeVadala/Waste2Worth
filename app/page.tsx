const rankedBuyers = [
  {
    name: "GreenBio Energy",
    type: "Biogas plant",
    distance: "1.4 km",
    net: "INR 20,370",
    pickup: "Pickup available",
    score: 96,
  },
  {
    name: "EcoCompost Nashik",
    type: "Composting company",
    distance: "8.6 km",
    net: "INR 18,920",
    pickup: "Supplier delivery",
    score: 84,
  },
  {
    name: "BioCycle Organics",
    type: "Organic processor",
    distance: "14.2 km",
    net: "INR 17,480",
    pickup: "Pickup available",
    score: 79,
  },
];

const agentEvents = [
  "Waste analyzed",
  "3 suitable buyers ranked",
  "Supplier approval required",
  "Buyer contact ready",
];

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f4f1e8] text-[#17211b]">
      <section className="grid min-h-screen grid-cols-1 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="flex flex-col justify-between border-b border-[#17211b]/15 bg-[#12362a] p-6 text-white lg:border-b-0 lg:border-r lg:p-10">
          <nav className="flex items-center justify-between text-sm">
            <span className="font-semibold tracking-wide">Waste2Worth</span>
            <span className="rounded-full border border-white/30 px-3 py-1 text-white/80">
              AI Recovery
            </span>
          </nav>

          <div className="my-14 max-w-xl">
            <p className="mb-4 text-sm uppercase tracking-[0.24em] text-[#b6d87a]">
              Give waste a second life
            </p>
            <h1 className="text-5xl font-semibold leading-tight md:text-7xl">
              Find the best destination for organic waste.
            </h1>
            <p className="mt-6 max-w-lg text-lg leading-8 text-white/80">
              Waste2Worth analyzes waste, compares buyer demand, estimates real
              returns, and prepares an agent-led transaction after supplier approval.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3 text-sm">
            <Metric label="Recovered" value="700 kg" />
            <Metric label="Best route" value="Biogas" />
            <Metric label="Net return" value="INR 20k" />
          </div>
        </div>

        <div className="p-4 md:p-8 lg:p-10">
          <div className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
            <section className="rounded-lg border border-[#17211b]/12 bg-white p-5 shadow-sm">
              <div className="mb-5 flex items-center justify-between">
                <h2 className="text-lg font-semibold">Supplier Waste</h2>
                <span className="rounded-full bg-[#e1f0c2] px-3 py-1 text-xs font-medium text-[#29410f]">
                  Live listing
                </span>
              </div>
              <div className="space-y-3">
                <InfoRow label="Waste type" value="Tomato waste" />
                <InfoRow label="Quantity" value="700 kg" />
                <InfoRow label="Condition" value="Spoiled" />
                <InfoRow label="Location" value="Nashik, India" />
              </div>
            </section>

            <section className="rounded-lg border border-[#17211b]/12 bg-white p-5 shadow-sm">
              <h2 className="text-lg font-semibold">AI Recommendation</h2>
              <div className="mt-5 rounded-md bg-[#eef5df] p-4">
                <p className="text-sm font-medium text-[#52681f]">Recommended route</p>
                <p className="mt-1 text-3xl font-semibold">Anaerobic digestion</p>
                <p className="mt-3 leading-7 text-[#526157]">
                  High-moisture tomato waste fits biogas production, and the strongest
                  buyer has capacity, short distance, and pickup availability.
                </p>
              </div>
            </section>
          </div>

          <section className="mt-4 rounded-lg border border-[#17211b]/12 bg-white p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold">Ranked Buyers</h2>
              <span className="text-sm text-[#68766e]">AI sorted by net return</span>
            </div>
            <div className="grid gap-3">
              {rankedBuyers.map((buyer, index) => (
                <div
                  className="grid gap-3 rounded-md border border-[#17211b]/10 p-4 md:grid-cols-[40px_1fr_120px_120px]"
                  key={buyer.name}
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#12362a] font-semibold text-white">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-semibold">{buyer.name}</p>
                    <p className="mt-1 text-sm text-[#68766e]">
                      {buyer.type} - {buyer.distance} - {buyer.pickup}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase text-[#68766e]">Estimated net</p>
                    <p className="font-semibold">{buyer.net}</p>
                  </div>
                  <div>
                    <p className="text-xs uppercase text-[#68766e]">Score</p>
                    <p className="font-semibold">{buyer.score}/100</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="mt-4 rounded-lg border border-[#17211b]/12 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold">Agent Activity</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-4">
              {agentEvents.map((event) => (
                <div className="rounded-md bg-[#f4f1e8] p-4 text-sm font-medium" key={event}>
                  {event}
                </div>
              ))}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-white/15 bg-white/10 p-4">
      <p className="text-xs uppercase text-white/60">{label}</p>
      <p className="mt-2 text-xl font-semibold">{value}</p>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b border-[#17211b]/10 pb-3 last:border-b-0">
      <span className="text-sm text-[#68766e]">{label}</span>
      <span className="font-medium">{value}</span>
    </div>
  );
}

