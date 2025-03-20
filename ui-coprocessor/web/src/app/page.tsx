"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DatePickerWithPresets } from "@/app/components/date-picker-with-presets";
import { PowerKindPicker } from "@/app/components/power-kind-picker";
import { DeviceRead } from "@/types/device-read";
import { useEffect, useState } from "react";
import useDeviceStore from "@/stores/device-store";
import useDashboardStore from "@/stores/dashboard-store";
import { PowerSummary } from "@/app/components/power-summary";
import { PowerOverview } from "@/app/components/power-overview";
import dynamic from "next/dynamic";
import { useAccount, usePublicClient } from "wagmi";
import { classifierCallerAbi } from "@/generated";
import { getContract } from "viem";
import { hardhat } from "wagmi/chains";


const UserNav = dynamic(() => import("../components/user-nav"), {
  ssr: false,
  loading: () => <div>Loading UserNav...</div>,
});

const DeviceNav = dynamic(() => import("../components/device-nav"), {
  ssr: false,
  loading: () => <div>Loading DeviceNav...</div>,
});

export default function DashboardPage() {
  const { isConnected, address } = useAccount();

  const { device } = useDeviceStore();
  const { date } = useDashboardStore();
  const [deviceReads, setDeviceReads] = useState([] as DeviceRead[]);

  const client = usePublicClient();

  useEffect(() => {
    const fetchReads = async () => {
      const contract = getContract({
       client,
       address: process.env
         .NEXT_PUBLIC_COPROCESSOR_CALLER_ADDRESS?.toLowerCase() as `0x${string}`,
       abi: classifierCallerAbi,
      });
      console.log(contract);
      const reads = await contract.read.getDeviceCurrentData(
       [address!, BigInt(device!.id)],
       {}
      );
      console.log(reads)

      
      return reads.map((read) => ({
       timestamp: Number(read.timestamp),
       amps: Number(read.current) / 100,
      }));

      // const ampDelta = (device!.id - 1) * 3;

      // return [
      //   { timestamp: Date.now() - 3600000 * 24, amps: ampDelta + 4.2 },
      //   { timestamp: Date.now() - 3600000 * 23, amps: ampDelta + 3.8 },
      //   { timestamp: Date.now() - 3600000 * 22, amps: ampDelta + 5.1 },
      //   { timestamp: Date.now() - 3600000 * 21, amps: ampDelta + 6.3 },
      //   { timestamp: Date.now() - 3600000 * 20, amps: ampDelta + 7.2 },
      //   { timestamp: Date.now() - 3600000 * 19, amps: ampDelta + 8.5 },
      //   { timestamp: Date.now() - 3600000 * 18, amps: ampDelta + 9.1 },
      //   { timestamp: Date.now() - 3600000 * 17, amps: ampDelta + 8.7 },
      //   { timestamp: Date.now() - 3600000 * 16, amps: ampDelta + 7.9 },
      //   { timestamp: Date.now() - 3600000 * 15, amps: ampDelta + 6.8 },
      //   { timestamp: Date.now() - 3600000 * 14, amps: ampDelta + 5.5 },
      //   { timestamp: Date.now() - 3600000 * 13, amps: ampDelta + 4.9 },
      //   { timestamp: Date.now() - 3600000 * 12, amps: ampDelta + 4.2 },
      //   { timestamp: Date.now() - 3600000 * 11, amps: ampDelta + 3.6 },
      //   { timestamp: Date.now() - 3600000 * 10, amps: ampDelta + 3.1 },
      //   { timestamp: Date.now() - 3600000 * 9, amps: ampDelta + 2.8 },
      //   { timestamp: Date.now() - 3600000 * 8, amps: ampDelta + 2.5 },
      //   { timestamp: Date.now() - 3600000 * 7, amps: ampDelta + 2.9 },
      //   { timestamp: Date.now() - 3600000 * 6, amps: ampDelta + 3.4 },
      //   { timestamp: Date.now() - 3600000 * 5, amps: ampDelta + 4.1 },
      //   { timestamp: Date.now() - 3600000 * 4, amps: ampDelta + 4.8 },
      //   { timestamp: Date.now() - 3600000 * 3, amps: ampDelta + 5.3 },
      //   { timestamp: Date.now() - 3600000 * 2, amps: ampDelta + 5.7 },
      //   { timestamp: Date.now() - 3600000, amps: ampDelta + 5.9 },
      // ];
    };

    if (!isConnected || !device) return;

    try {
      const endTimestamp = new Date(date);
      endTimestamp.setHours(23, 59, 59, 999);

      fetchReads().then(setDeviceReads);
    } catch (error) {
      console.error("Error fetching device reads:", error);
      // Handle error state
      setDeviceReads([]);
    }
  }, [isConnected, device, date, client, address]);

  return (
    <>
      <div className="hidden flex-col md:flex">
        <div className="border-b">
          <div className="flex h-16 items-center px-4">
            <div className="ml-auto flex items-center space-x-4">
              <DeviceNav />
              <UserNav />
            </div>
          </div>
        </div>
        <div className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
            <div className="flex items-center space-x-2">
              <DatePickerWithPresets />
              <PowerKindPicker />
            </div>
          </div>
          <div className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
              <Card className="col-span-5">
                <CardHeader>
                  <CardTitle>Power Overview</CardTitle>
                </CardHeader>
                <CardContent className="pl-2">
                  <PowerOverview deviceReads={deviceReads} />
                </CardContent>
              </Card>
              <Card className="col-span-2">
                <CardContent className="flex items-center h-full">
                  <PowerSummary deviceReads={deviceReads} />
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
