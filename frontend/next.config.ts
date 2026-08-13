import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [{ protocol: "http", hostname: "localhost" }],
  },
  allowedDevOrigins: ["192.168.0.101"],
};

export default nextConfig;