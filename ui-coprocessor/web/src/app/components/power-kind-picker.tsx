"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import useDashboardStore from "@/stores/dashboard-store";

export const PowerKindPicker = () => {
  const { powerKind, setPowerKind } = useDashboardStore();

  return (
    <Select onValueChange={setPowerKind} value={powerKind}>
      <SelectTrigger>
        <SelectValue placeholder="Power" />
      </SelectTrigger>
      <SelectContent position="popper">
        <SelectItem value="active">Active Power</SelectItem>
        <SelectItem value="reactive">Reactive Power</SelectItem>
        <SelectItem value="apparent">Apparent Power</SelectItem>
      </SelectContent>
    </Select>
  );
};
