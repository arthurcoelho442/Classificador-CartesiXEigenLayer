import { http, cookieStorage, createConfig, createStorage } from "wagmi";
import { holesky, anvil, hardhat } from "wagmi/chains";
import {
  coinbaseWallet,
  injected,
  metaMask,
} from "wagmi/connectors";

export function getConfig() {
  return createConfig({
    chains: [hardhat],
    connectors: [
      injected(),
      coinbaseWallet(),
      //walletConnect({
      //  projectId:
      //    process.env.NEXT_PUBLIC_WC_PROJECT_ID ?? "default-project-id",
      //}),
      metaMask(),
    ],
    storage: createStorage({
      storage: cookieStorage,
    }),
    syncConnectedChain: true,
    ssr: true,
    transports: {
      [hardhat.id]: http(),
    },
  });
}

declare module "wagmi" {
  interface Register {
    config: ReturnType<typeof getConfig>;
  }
}
