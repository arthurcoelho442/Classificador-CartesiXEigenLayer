"use client";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import useDeviceStore from "@/stores/device-store";
import { useEffect, useState } from "react";
import { Device } from "@/types/device";
import { useAccount, usePublicClient } from "wagmi";
import { getContract, Address } from "viem";
import { classifierCallerAbi } from "@/generated";


const DeviceNav = () => {
  const { isConnected, address } = useAccount();
  const client = usePublicClient();

  const { device, setDevice } = useDeviceStore();

  const [devices, setDevices] = useState([] as Device[]);
  
  useEffect(() => {
    // const fetchDevices = async () => {
    //   const contract = getContract({
    //    client,
    //    address: process.env
    //      .NEXT_PUBLIC_CLASSIFIER_CALLER_CONTRACT_ADDRESS as `0x${string}`,
    //    abi: classifierCallerAbi,
    //   });
      
    //   const address:Address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

    //   const devices = await contract.read.getDevices([address]);
    //   // const devices = await contract.read.getDevices("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266");

      
    //   return devices.map((device) => ({
    //    id: Number(device.id),
    //    name: device.name,
    //   }));

    //   // return [
    //   //   { id: 10, name: "Ventilador" },
    //   //   { id: 13, name: "MaquinadeCortarCabelo" },
    //   //   { id: 15, name: "Notebook" },
    //   // ];
    // };

    const fetchDevices = async () => {
      try {
        // Log para ver o endereço sendo passado
        console.log("Fetching devices for address:", "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266");
    
        // Obtenha o contrato com a ABI e endereço
        const contract = getContract({
          client,
          address: process.env.NEXT_PUBLIC_CLASSIFIER_CALLER_CONTRACT_ADDRESS?.toLowerCase() as `0x${string}`, // Certifique-se de que a variável de ambiente está configurada corretamente
          abi: classifierCallerAbi,
        });
    
        const address:Address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266" // Endereço do usuário ou caller
        
        // Log antes de chamar a função do contrato
        console.log("Calling getDevices with address:", address);
    
        // Aqui passamos o endereço como argumento para a função `getDevices`
        const devices = await contract.read.getDevices([address]);
        console.log(devices)
    
        // Log para ver os dispositivos retornados
        console.log("Devices fetched:", devices);
    
        // Mapeando os dispositivos para uma forma mais legível
        return devices.map((device) => ({
          id: Number(device.id),  // Certifique-se de que 'device.id' seja um valor que pode ser convertido para número
          name: device.name,      // Nome do dispositivo
        }));
      } catch (error) {
        // Log do erro
        console.error("Erro ao buscar dispositivos:", error);
        throw error;
      }
    };
    

    if (!isConnected) return;

    fetchDevices()
      .then(setDevices)
      .catch((error) => {
        console.error("Failed to fetch devices", error);
      });
  }, [address, client, device, isConnected]);

  return (
    <Select
      disabled={!isConnected}
      onValueChange={(id) =>
        setDevice(devices.find((d) => d.id.toString() === id)!)
      }
    >
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder={device ? device.name : "Select device"} />
      </SelectTrigger>
      <SelectContent>
        {devices.map((device) => (
          <SelectItem key={device.id} value={device.id.toString()}>
            {device.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};

export default DeviceNav;
