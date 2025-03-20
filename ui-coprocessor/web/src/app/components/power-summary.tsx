"use client";

import { DeviceRead } from "@/types/device-read";

interface PowerSummaryProps {
  deviceReads: DeviceRead[];
}

export function PowerSummary({ deviceReads }: PowerSummaryProps) {
  const minAmps = Math.min(...deviceReads.map((read) => read.amps));
  const maxAmps = Math.max(...deviceReads.map((read) => read.amps));
  const avgAmps =
    deviceReads.reduce((sum, read) => sum + read.amps, 0) / deviceReads.length;

  return (
    <div className="space-y-4">
      {deviceReads.length > 0 ? (
      <div className="grid grid-cols-1 gap-4">
        <div className="space-y-2">
          <div className="text-sm text-muted-foreground">Maximum</div>
          <div className="text-2xl font-bold">{maxAmps.toFixed(2)} A</div>
        </div>
        <div className="space-y-2">
          <div className="text-sm text-muted-foreground">Average</div>
          <div className="text-2xl font-bold">{avgAmps.toFixed(2)} A</div>
        </div>
        <div className="space-y-2">
          <div className="text-sm text-muted-foreground">Minimum</div>
          <div className="text-2xl font-bold">{minAmps.toFixed(2)} A</div>
        </div>
      </div>)
      : (
        <div className="text-muted-foreground">No data available</div>
      )}
    </div>
  );
}
