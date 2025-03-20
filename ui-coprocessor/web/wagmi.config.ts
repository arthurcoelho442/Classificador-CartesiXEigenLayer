import { defineConfig, loadEnv } from "@wagmi/cli";
import { foundry, react } from "@wagmi/cli/plugins";
import { classifierCallerAbi } from "./src/generated";

export default defineConfig(() => {
  if (process.env.NODE_ENV === "development") {
    const env = loadEnv({
      mode: process.env.NODE_ENV,
      envDir: process.cwd(),
    });
    return {
      // dev specific config
      out: "src/generated.ts",
      contracts: [
        {
          abi: classifierCallerAbi,
          name: "ClassifierCaller",
        },
      ],
      plugins: [
        react(),
        foundry({
          project: "../contracts",
        }),
      ],
    };
  } else {
    return {
      // production specific config
      out: "src/generated.ts",
      contracts: [
        {
          abi: classifierCallerAbi,
          name: "ClassifierCaller",
        },
      ],
      plugins: [],
    };
  }
});
