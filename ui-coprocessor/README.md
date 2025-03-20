# Hackathon

## Built With

- [Cartesi](https://cartesi.io/)
- [Coprocessor](https://docs.mugen.builders/cartesi-co-processor-tutorial/introduction)
- [Foundry](https://github.com/foundry-rs/foundry)
- [Next.js](https://nextjs.org/)

## Getting Started

1. Clone the repo

   ```bash
   git clone https://github.com/srjheam/cartesi-x-eigenlayer-hackaton-feb-2025.git
   ```

2. Head to the repo directory

   ```bash
   cd cartesi-x-eigenlayer-hackaton-feb-2025/
   ```

### Coprocessor

1. Head to the coprocessor directory

   ```bash
   cd contracts/
   ```

2. Install packages

   ```bash
   forge install
   ```

3. Compile contracts

   ```bash
   forge build
   ```

   3.1. Run Wagmi CLI

   ```bash
   (cd ../frontend && pnpm wagmi generate)
   ```

4. Run tests

   ```bash
   # TODO
   ```

5. Start node

   ```bash
   # TODO
   ```

6. Deploy contracts

   ```bash
   # TODO
   ```

### Web

1. Head to the web directory

   ```bash
   cd web/
   ```

2. Install packages

   ```bash
   pnpm i
   ```

3. Set up your environment

   Copy .env.example file to .env (which will be ignored by Git):

   ```bash
   cp .env.example .env
   ```

4. Start development server and you're done

   ```bash
   pnpm dev
   ```

## License

Licensed under the [MIT License](./LICENSE).
