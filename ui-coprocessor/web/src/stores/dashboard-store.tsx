import { create, StateCreator } from "zustand";
import { persist, PersistOptions } from "zustand/middleware";

type PowerKind = "active" | "reactive" | "apparent";

interface DashboardStore {
  powerKind: PowerKind;
  date: Date;
  setDate: (date: Date) => void;
  setPowerKind: (powerKind: PowerKind) => void;
}

type DashboardPersist = (
  config: StateCreator<DashboardStore>,
  options: PersistOptions<DashboardStore>
) => StateCreator<DashboardStore>;

const useDashboardStore = create<DashboardStore>()(
  (persist as DashboardPersist)(
    (set) => {
      const initialStore: DashboardStore = {
        powerKind: "active",
        date: new Date(),
        setDate: (date) => set({ date }),
        setPowerKind: (powerKind) => set({ powerKind }),
      };

      return initialStore;
    },
    {
      name: "dashboard-store",
    }
  )
);

export default useDashboardStore;
