"use client";

import { DeviceRead } from "@/types/device-read";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { useTheme } from "next-themes";

interface PowerOverviewProps {
  deviceReads: DeviceRead[];
}

export function PowerOverview({ deviceReads }: PowerOverviewProps) {
  const { theme } = useTheme();

  const formatXAxis = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatTooltip = (value: number) => [`${value} A`];

  const isDark = theme === "dark";
  const gridColor = isDark ? "#374151" : "#E5E7EB"; // gray-700 : gray-200
  const lineColor = isDark ? "#818CF8" : "#4F46E5"; // indigo-400 : indigo-600
  const textColor = isDark ? "#E5E7EB" : "#111827"; // gray-200 : gray-900
  const boundaryColor = isDark ? "#9CA3AF" : "#4B5563"; // gray-400 : gray-600

  const average =
    deviceReads.reduce((sum, read) => sum + read.amps, 0) / deviceReads.length;
  const maximum = Math.max(...deviceReads.map((read) => read.amps));
  const minimum = Math.min(...deviceReads.map((read) => read.amps));

  return (
    <div className="h-[400px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={deviceReads}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={gridColor} />
          <XAxis
            dataKey="timestamp"
            tickFormatter={formatXAxis}
            interval="preserveStartEnd"
            stroke={gridColor}
            tick={{ fill: textColor }}
          />
          <YAxis
            label={{
              value: "Amperes (A)",
              angle: -90,
              position: "insideLeft",
              style: { fill: textColor },
            }}
            stroke={gridColor}
            tick={{ fill: textColor }}
          />
          <Tooltip
            labelFormatter={(timestamp) => new Date(timestamp).toLocaleString()}
            formatter={formatTooltip}
            contentStyle={{
              backgroundColor: isDark ? "#1F2937" : "#FFFFFF", // gray-800 : white
              border: `1px solid ${gridColor}`,
            }}
            labelStyle={{ color: isDark ? "#E5E7EB" : "#111827" }} // gray-200 : gray-900
          />
          <ReferenceLine
            y={maximum}
            stroke={boundaryColor}
            strokeDasharray="3 3"
          />
          <ReferenceLine
            y={minimum}
            stroke={boundaryColor}
            strokeDasharray="3 3"
          />
          <ReferenceLine y={average} stroke={lineColor} strokeDasharray="3 3" />
          <Line
            type="monotone"
            dataKey="amps"
            stroke={lineColor}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 8, fill: lineColor }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
