import type { Metadata } from "next";
import { Fraunces, Inter } from "next/font/google";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--w2w-display",
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--w2w-body",
});

export const metadata: Metadata = {
  title: "Waste2Worth — Give waste a second life",
  description:
    "Waste2Worth prevents usable organic waste from becoming disposal waste by using AI to determine its highest-value reuse pathway and autonomously connect it with a suitable buyer.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${fraunces.variable} ${inter.variable} antialiased`}>{children}</body>
    </html>
  );
}