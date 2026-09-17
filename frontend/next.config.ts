import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    const rawApiUrl =
      process.env.API_URL ??
      process.env.NEXT_PUBLIC_API_URL ??
      "http://localhost:8000";
    const apiUrl = rawApiUrl.replace(/\/+$/, "");

    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
