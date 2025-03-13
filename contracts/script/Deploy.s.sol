// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Script} from "../lib/forge-std/src/Script.sol";
import {ClassifierCaller} from "../src/ClassifierCaller.sol";

contract DeployCounterCaller is Script {
    function run() external returns (ClassifierCaller) {
        // These values should be replaced with your actual values
        address coprocessorAddress = vm.envAddress("COPROCESSOR_ADDRESS");
        bytes32 machineHash = vm.envBytes32("MACHINE_HASH");

        vm.startBroadcast();
        ClassifierCaller counter = new ClassifierCaller(
            coprocessorAddress,
            machineHash
        );
        vm.stopBroadcast();

        return counter;
    }
}