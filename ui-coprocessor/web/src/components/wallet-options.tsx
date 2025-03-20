"use client";
import * as React from "react";
import { Connector, useConnect } from "wagmi";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { ChevronsUpDown, Dot } from "lucide-react";
import {
  Command,
  CommandEmpty,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

type PopoverTriggerProps = React.ComponentPropsWithoutRef<
  typeof PopoverTrigger
>;

//interface WalletOptionsProps extends PopoverTriggerProps {}

export function WalletOptions({ className }: PopoverTriggerProps) {
  const { connectors, connect } = useConnect();

  const [open, setOpen] = React.useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <div>
          <Label htmlFor="theme" className="w-full block">
            Wallet
          </Label>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            aria-label="Select a team"
            className={cn("w-[200px] justify-between", className)}
          >
            Select wallet
            <ChevronsUpDown className="ml-auto opacity-50" />
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandList>
            <CommandEmpty>No wallet found.</CommandEmpty>
            {connectors.map((connector) => (
              <WalletOption
                key={connector.uid}
                connector={connector}
                onClick={() => {
                  connect({ connector });
                  setOpen(false);
                }}
              />
            ))}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}

function WalletOption({
  connector,
  onClick,
}: {
  connector: Connector;
  onClick: () => void;
}) {
  const [ready, setReady] = React.useState(false);

  React.useEffect(() => {
    (async () => {
      const provider = await connector.getProvider();
      setReady(!!provider);
    })();
  }, [connector]);

  return (
    <CommandItem
      key={connector.uid}
      onSelect={onClick}
      className="text-sm"
      disabled={!ready}
    >
      <Avatar className="mr-2 h-5 w-5">
        <AvatarImage
          src={`https://avatar.vercel.sh/${connector.uid}`}
          alt={connector.name}
          className="grayscale"
        />
        <AvatarFallback>SC</AvatarFallback>
      </Avatar>
      {connector.name}
      <Dot
        className={cn("ml-auto", ready ? "text-green-500" : "text-gray-500")}
      />
    </CommandItem>
  );
}
