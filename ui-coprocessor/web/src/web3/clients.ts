import {
  createPublicClient,
  createWalletClient,
  http,
  PrivateKeyAccount,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";

export const rpcUrl =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8545"
    : process.env.RPC_URL;

export const publicClient = createPublicClient({
  transport: http(rpcUrl),
});

export const account = (privateKey: `0x${string}`) =>
  privateKeyToAccount(privateKey);

export const walletClient = (account: PrivateKeyAccount) =>
  createWalletClient({
    account,
    transport: http(rpcUrl),
  });
