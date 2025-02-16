// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "../lib/coprocessor-base-contract/src/CoprocessorAdapter.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract ClassifierCaller is CoprocessorAdapter, AccessControl {
    struct DeviceReportView {
        uint256 current;    // in amper
        uint256 timestamp;  // unix timestamp
    }
    struct DeviceView {
        string name;
        uint256  id;
    }
    struct Device {
        string name;
        uint256  id;
        DeviceReportView[] data;
    }

    struct User {
        string name;
        Device[]  devices;
    }

    address public owner;
    address[] public userAddresses;
    mapping(address => User) public users;
    mapping(bytes32 => address) private requestSender;
    mapping(bytes32 => uint256) private requestTimestamp;

    event ResultReceived(bytes32 indexed inputPayloadHash, bytes output);

    modifier onlySuperAdmin() {
        require(hasRole(DEFAULT_ADMIN_ROLE, msg.sender), "Not super admin");
        _;
    }
    modifier userExists(address user) {
        require(bytes(users[user].name).length != 0, "User does not exist");
        _;
    }
    constructor(address _taskIssuerAddress, bytes32 _machineHash) CoprocessorAdapter(_taskIssuerAddress, _machineHash) {
        owner = msg.sender;

        userAddresses.push(owner);
        users[owner].name = 'owner';

        // Add devices using push
        users[owner].devices.push(Device('Fan', 10, new DeviceReportView[](0)));
        users[owner].devices.push(Device('Hair cutter', 13, new DeviceReportView[](0)));
        users[owner].devices.push(Device('Notebook Wanderley', 14, new DeviceReportView[](0)));
        users[owner].devices.push(Device('Notebook Leo', 15, new DeviceReportView[](0)));

        // ADMIN
        _grantRole(DEFAULT_ADMIN_ROLE, owner);
    }

    function runExecution(bytes calldata input) {
        callCoprocessor(input);
    }

    function handleNotice(bytes32 inputPayloadHash, bytes memory notice) internal override {
        require(notice.length >= 64, "Invalid notice length");

        (uint256 id, uint256 current) = abi.decode(notice, (uint256, uint256));

        address sender      = requestSender[inputPayloadHash];
        uint256 timestamp   = requestTimestamp[inputPayloadHash];
        require(sender != address(0), "Unknown request");

        delete requestSender[inputPayloadHash];
        delete requestTimestamp[inputPayloadHash];

        for (uint i = 0; i < users[sender].devices.length; i++) {
            if (users[sender].devices[i].id == id) {
                users[sender].devices[i].data.push(DeviceReportView(current, timestamp));
                break;
            }
        }
        emit ResultReceived(inputPayloadHash, notice);
    }

    // send
    function sendData(uint256[] memory currents, uint256 timestamp) external userExists(msg.sender) {
        // Verifica se o array de currents tem exatamente 100.000 elementos
        require(currents.length == 1666, "The batch must contain exactly 1666 current values.");

        bytes memory input = abi.encode(currents);
        bytes32 requestHash = keccak256(input);

        requestSender[requestHash]      = msg.sender;
        requestTimestamp[requestHash]   = timestamp;

        runExecution(input);
    }

    // get
    function getDevices (address user) public view userExists(user) returns (DeviceView[] memory) {
        uint256 devicesCount = users[user].devices.length;
        DeviceView[] memory deviceView = new DeviceView[](devicesCount);

        for (uint i = 0; i < devicesCount; i++) {
            Device memory device = users[user].devices[i];
            deviceView[i] = DeviceView(device.name, device.id);
        }
        return deviceView;
    }
    function getDeviceCurrentData(address user, uint256 id) public view userExists(user) returns (DeviceReportView[] memory) {
        for (uint i = 0; i < users[user].devices.length; i++) {
            if (users[user].devices[i].id == id){
                uint256 dataLength = users[user].devices[i].data.length;
                uint256 init = dataLength >= 60 ? dataLength - 60 : 0;
                DeviceReportView[] memory data = new DeviceReportView[](dataLength - init);

                for (uint j = 0; j < dataLength - init; j++) {
                    data[j] = users[user].devices[i].data[init + j];
                }

                return data;
            }
        }
        return new DeviceReportView[](0);
    }

    // add
    function addUser(address user, string memory  name) external onlySuperAdmin {
        require(bytes(users[user].name).length == 0, "User already exists");
        users[user].name = name;
        userAddresses.push(user);
    }
    function addDevice(address user, string memory name, uint256 id) external userExists(user) onlySuperAdmin {
        for (uint i = 0; i < users[user].devices.length; i++) {
            require(users[user].devices[i].id != id, "Device already exists");
        }
        users[user].devices.push(Device(name, id, new DeviceReportView[](0)));
    }
}