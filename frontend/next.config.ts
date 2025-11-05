import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  compress: true,
  reactStrictMode: false,
  async headers() {
    return [
      {
        source: "/api/:path*",
        headers: [
          { key: "Cache-Control", value: "public, max-age=60" },
          { key: "X-Nextjs-Cache", value: "short" },
        ],
      },
    ];
  },
};

export default nextConfig;
