import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Waste2Worth — Give waste a second life",
  description:
    "AI-powered organic waste recovery. Waste2Worth analyzes waste, finds the best processing route, and connects suppliers with buyers through an AI agent.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}