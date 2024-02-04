// SPDX-License-Identifier: MIT 
pragma solidity >=0.7.0 <0.9.0;
contract UserMedicalData {
    struct MedicalData {
        string username;
        string password;
        string email;
    }

    mapping(address => MedicalData) public users;

    function addMedical(string memory _username, string memory _password, string memory _email) public {
        users[msg.sender] = MedicalData(_username, _password, _email);
    }
}