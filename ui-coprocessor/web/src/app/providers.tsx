"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode, useEffect, useState } from "react";
import { type State, WagmiProvider } from "wagmi";
import { ThemeProvider } from "next-themes";

import { getConfig } from "@/wagmi";

const queryClient = new QueryClient();
const config = getConfig();

export default function Providers(props: {
  children: ReactNode;
  initialState?: State;
}) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <WagmiProvider config={config} initialState={props.initialState}>
        <QueryClientProvider client={queryClient}>
          {props.children}
        </QueryClientProvider>
      </WagmiProvider>
    ); // Render children without ThemeProvider during SSR
  }

  return (
    <WagmiProvider config={config} initialState={props.initialState}>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {props.children}
        </ThemeProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
