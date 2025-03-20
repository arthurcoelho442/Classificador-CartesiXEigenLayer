import { Device } from "@/types/device";
import { create, StateCreator } from "zustand";
import { persist, PersistOptions } from "zustand/middleware";

interface DeviceStore {
  device?: Device;
  setDevice: (device: Device) => void;
  resetDevice: () => void;
}

type DevicePersist = (
  config: StateCreator<DeviceStore>,
  options: PersistOptions<DeviceStore>
) => StateCreator<DeviceStore>;

const useDeviceStore = create<DeviceStore>()(
  (persist as DevicePersist)(
    (set) => {
      const initialStore: DeviceStore = {
        device: undefined,
        setDevice: (device) => set({ device }),
        resetDevice: () => set({ device: undefined }),
      };

      return initialStore;
    },
    {
      name: "device-store",
    }
  )
);

export default useDeviceStore;
